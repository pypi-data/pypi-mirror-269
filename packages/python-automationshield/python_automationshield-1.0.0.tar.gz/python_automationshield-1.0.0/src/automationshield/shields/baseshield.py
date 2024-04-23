import serial
import serial.tools.list_ports
import time

from typing import Optional

from .. import arduino
from ..exception import AutomationShieldException


class BaseShield:
    """Base class for shield devices. Handles communication with Arduino, sensor calibration and unit conversions. The class can also install the proper firmware on an Arduino.

    Interface:
        * Actuator input should be provided in percent by default.
        * Potentiometer is provided in percent by default.
        * Sensor values are converted to relevant physical units in the child classes.

    :param TEST: Flag to write to Arduino. This flag is used to check if the correct firmware is installed. The response from the Arduino should be the C++ software version and the id of the shield.
    :type TEST: int
    :param RUN: Falg to write to Arduino. This flag is used for normal running of the shield device. The actuator value is applied and the Arduino responds with the potentiometer and sensor values.
    :type RUN: int
    :param STOP: Flag to write to Arduino. This flag is used to stop the actuator. The Arduino will stop the actuator to ensure the shield is safely stopped.
    :type STOP: int
    :param TIMEOUT: Time to wait after opening the serial connection before writing to the Arduino.
    :type TIMEOUT: int
    :param script: name of the script directory in which the ``.ino`` file for the specific shield is located.
    :type script: str
    :param shield_id: ID assigned to shield. This is used to check whether the correct firmware is installed on the Arduino.
    :type shield_id: str
    :param actuator_bits: Number of bits used for actuator.
    :type actuator_bits: int
    :param potentiometer_bits: Number of bits used for potentiometer.
    :type potentiometer_bits: int
    :param sensor_bits: Number of bits used for sensor.
    :type sensor_bits: int
    :param port: Port of the Arduino.
    :type port: str
    :param conn: Serial connection to the Arduino.
    :type conn: serial.Serial
    :param zero_reference: Zero reference of the sensor for calibration.
    :type zero_reference: float
    """
    TEST = 0
    RUN = 1
    STOP = 2

    # Wait time after opening connection
    TIMEOUT = 3

    script = ""
    shield_id = ""

    actuator_bits = 8
    potentiometer_bits = 10  # resolution of system ad converter
    sensor_bits = 12

    def __init__(self, port:Optional[str]=None) -> None:
        """Constructor method. Create a serial connection object (without opening the connection). Will try to find the Arduino device is no port is provided.

        :param port: Port on which the Arduino is connected, defaults to None.
        :type port: str
        """
        if port is None:
            port = self.find_arduino()
        self.port = port

        self.conn = serial.Serial(baudrate=115200)
        self.conn.port = self.port
        self.conn.timeout = 1

        self.zero_reference = 0

    def find_arduino(self) -> str:
        """Get the name of the port that is connected to Arduino. Raises exception if no port was found.

        :raises automationshield.AutomationShieldException: Raised if no Arduino was found.
        :return: COM port of the Arduino.
        :rtype: str
        """
        ports = serial.tools.list_ports.comports()
        for p in ports:
            if p.manufacturer is not None and "Arduino" in p.manufacturer:
                return p.device

        raise AutomationShieldException("No Arduino Found")

    def check_firmware(self) -> int:
        """Check that the correct firmware is installed on the Arduino. When the arduino reads the :py:attr:`BaseShield.TEST` flag, it should respond with the code version and two bytes which, when converted to ASCII, should match the shield id.

        :raises automationshield.AutomationShieldException: If the arduino didn't respond correctly.
        :return: version number of Arduino firmware.
        :rtype: int
        """

        # set the upper limit of the range to the lower of the potentiometer bits divided by 2 and the sensor bits divided by 4, to guarantee the response fits in the bits.
        self.write(self.TEST, 0)
        bts = self.conn.read(size=3)
        id = f"{chr(bts[1])}{chr(bts[2])}"

        if id == self.shield_id:
            return bts[0]

        else:
            raise AutomationShieldException("Incorrect firmware installed on Arduino")

    def install_firmware(self, device:str) -> None:
        """Compile firmware for the current shield and upload to the Arduino.

        :param device: FQBN of Arduino. FQBNs for common devices are provided in :py:mod:`automationshield.arduino`, e.g. :py:const:`automationshield.arduino.LEONARDO`: ``arduino:avr:leonardo``.
        :type device: str
        """
        arduino.compile_script(device, self.script)
        arduino.upload_script(device, self.script, self.port)

    def convert_potentiometer_reading(self, raw: int) -> float:
        """Convert n-bit potentiometer reading to percentage value.

        :param raw: n-bit potentiometer value.
        :type raw: int
        :return: Potentiometer value as percentage [0, 100].
        :rtype: float
        """
        return raw / (2**self.potentiometer_bits - 1) * 100

    def convert_actuator_input(self, percent: float) -> int:
        """Convert actuator input from percentage to n-bit value.

        :param percent: Actuator percentage.
        :type percent: float
        :return: n-bit number of actuator value.
        :rtype: int
        """
        return percent / 100 * (2**self.actuator_bits - 1)


    def convert_sensor_reading(self, sensor: int) -> int:
        """Convert sensor reading to physical units. Should be implemented on subclasses.

        :param sensor: Raw sensor value
        :type sensor: int
        :return: Sensor value converted to physical units
        :rtype: int
        """
        return sensor

    def calibrate_sensor_reading(self, sensor: int) -> int:
        """Calibrate the sensor reading with the zero reference. Should be implemented on subclass. The default implementation is

        .. math::
            sensor_{calibrated} = sensor_{raw} - ref

        :param sensor: Raw sensor value.
        :type sensor: int
        :return: Calibrated sensor value.
        :rtype: int
        """
        return sensor - self.zero_reference

    def read(self, raw: bool=False) -> tuple[float]:
        """Read data from Arduino. If ``raw == False``, the potentiometer value is rescaled to percentages; and the sensor is calibrated with the zero reference and converted to relevant units. This is the default. \
            If ``raw == True``, none of that happens and the potentiometer and sensor are returned as n-bit values. No calibration is performed either.

        :param raw: If True, returns raw n-bit readings from potentiometer and sensor. Defaults to False, in which case the potentiometer is converted to percent and the sensor to approppriate units.
        :type raw: bool
        :raises automationshield.AutomationShieldException: Raised if no data was received. This can happen if there was no :py:meth:`BaseShield.write` command invoked preceding a call to :py:meth:`BaseShield.read`.
        :return: Converted and calibrated potentiometer and sensor readings, in that order.
        :rtype: tuple[float]
        """
        try:
            data = self.conn.read(size=3)

            pot = data[0] // 16 * 256 + data[1]
            sensor = data[0] % 16 * 256 + data[2]

            if raw:
                return pot, sensor

            else:
                return self.convert_potentiometer_reading(pot), self.convert_sensor_reading(self.calibrate_sensor_reading(sensor))

        except IndexError:
            raise AutomationShieldException("No data received from Arduino")

    @staticmethod
    def saturate_bits(value: float, bits: int) -> int:
        """Saturate value between :math:`0` and :math:`2^{bits - 1}` inclusive.

        :param value: Raw value.
        :type value: float
        :param bits: Number of bits.
        :type bits: int
        :return: Saturated value.
        :rtype: int
        """
        return int(min(max(value, 0), 2**bits - 1))

    @staticmethod
    def saturate_percent(value: float) -> float:
        """Saturate value between :math:`0` and :math:`100` inclusive.

        :param value: Raw value in percent.
        :type value: float
        :return: Saturated value in percent.
        :rtype: float
        """
        return min(max(value, 0), 100)

    def write(self, flag: int, actuator: float, raw: bool=False) -> int:
        """Write run/stop flag and actuator value to Arduino. Convert and saturate the actuator value before sending.

        the flag must be one of :py:attr:`BaseShield.TEST`, :py:attr:`BaseShield.RUN` or :py:attr:`BaseShield.STOP`.

        * :py:attr:`BaseShield.TEST` returns the version number of the Arduino code and a shield id, which should match :py:attr:`BaseShield.shield_id`. The actuator input is irrelevant for this command.
        * :py:attr:`BaseShield.RUN` means normal running mode. Set the actuator value.
        * :py:attr:`BaseShield.STOP` tells the arduino to stop the actuator. The supplied actuator value is ignored by the Arduino.

        :param flag: :py:attr:`BaseShield.TEST`, :py:attr:`BaseShield.RUN` or :py:attr:`BaseShield.STOP`.
        :type flag: int
        :param actuator: actuator value.
        :type actuator: float
        :param raw: If False, expects actuator as percentage [0, 100]. Value is converted before being sent. If True, expects actuator in range of [0, 2^actuator_bits - 1]. Defaults to False.
        :type raw: bool, optional
        :return: Saturated n-bit motor value.
        :rtype: int
        """

        if not raw:
            saturated_actuator = self.saturate_percent(actuator)
            actuator = self.convert_actuator_input(saturated_actuator)
            output = self.saturate_bits(actuator, self.actuator_bits)

        else:
            saturated_actuator = self.saturate_bits(actuator, self.actuator_bits)
            output = saturated_actuator

        if self.actuator_bits > 8:
            bts = [flag, output//256, output%256]
        else:
            bts = [flag, output]

        self.conn.write(bytes(bts))

        return saturated_actuator

    def calibrate(self):
        """Read out a zero reference. System should be at rest when calling this method. The zero reference is assigned to :py:attr:`BaseShield.zero_reference`."""
        self.write(self.RUN, 0)
        _, self.zero_reference = self.read(raw=True)

    def stop(self):
        """Send :py:attr:`BaseShield.STOP` signal to Arduino."""
        self.write(self.STOP, 0)

    def open(self):
        """Reset buffers and open connection to Arduino if it is not open already. Wait for :py:attr:`BaseShield.TIMEOUT` seconds to make sure connection is established."""
        if not self.conn.is_open:
            self.conn.open()

        self.conn.reset_input_buffer()
        self.conn.reset_output_buffer()

        time.sleep(self.TIMEOUT)

    def close(self, *args):
        """Close connection to Arduino."""
        self.conn.close()

    def __enter__(self):
        """Implements the ``with`` context manager. This method calls

        * :py:meth:`BaseShield.open`,
        * :py:meth:`BaseShield.check_firmware`,
        * :py:meth:`BaseShield.calibrate`.

        :return: Shield instance.
        :rtype: BaseShield
        """
        self.open()
        self.check_firmware()
        self.calibrate()
        return self

    def __exit__(self, *args):
        """Closes the context manager. This method calls

        * :py:meth:`BaseShield.stop`,
        * :py:meth:`BaseShield.close`.
        """
        self.stop()
        self.close(*args)
