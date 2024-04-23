import time

from math import log

from .baseshield import BaseShield


class MagnetoShield(BaseShield):
    """Class for Magnetshield device. Inherits from BaseShield.

    The Magnetshield device is a control experiment using magnetic levitation. The actuator is an electormagnet over which the voltage can be controlled. \
        The electromagnet attracts a permanent magnet placed below the electormagnet. The position of the permanent magnet is estimated using a Hall effect sensor.

    Interface:
        * Actuator input should be provided in percent by default.
        * Potentiometer is provided in percent by default.
        * Sensor values are provided in Gauss by default. This class provides an additional method :py:meth:`MagnetoShield.magnet_position`, which calculates the distance of the permanent magnet from the electromagnet.

    :param emagnet_height: Height of the electromagnet above ground in mm.
    :type emagnet_height: int
    :param magnet_low: Top of the magnet from ground - distance from Hall element in mm when the magnet is at the bottom of the tube.
    :type magnet _low: int
    :param magnet_high: Top of the magnet from ground - distance from Hall element in mm when the magent is at the top of the tube.
    :type magnet_high: int
    :param default_p1: Default value for calculating the magnet position. See :py:meth:`MagnetoShield.magnet_position`.
    :type default_p1: float
    :param default_p2: Default value for calculating the magnet position. See :py:meth:`MagnetoShield.magnet_position`.
    :type default_p2: float
    :param p1: Calibrated constant to calculate magnet position. See :py:meth:`MagnetoShield.magnet_position`.
    :type p1: float
    :param p2: Calibrated constant to calculate magnet position. See :py:meth:`MagnetoShield.magnet_position`.
    :type p2: float

    This class does not use the :py:attr:`BaseShield.zero_reference` attribute.
    """
    script = "magnetoshield"
    shield_id = "MG"

    actuator_bits = 12
    sensor_bits = 10

    emagnet_height = 20  # height of electromagnet above ground (mm)
    magnet_low = 3  # top of magnet from ground - distance from hall element (mm)
    magnet_high = 8  # top of magnet from ground - distance from hall element (mm)

    default_p1 = 3.233100
    default_p2 = 0.220571

    def __init__(self, baudrate: int | None = 115200, port: str | None = None) -> None:
        super().__init__(baudrate, port)

        self._p1 = None
        self._p2 = None

    def convert_sensor_reading(self, sensor: int) -> float:
        """Converts the n-bit sensor reading of the Hall effect sensor to Gauss. \
            The constants in this method are for release 4 of the MagnetoShield. Conversion is done using

        .. math::
            B = \\left(2.5 - s \\cdot \\frac{3.3}{2^{10} - 1}\\right) \\cdot 800

        The sensor value :math:`s` is scaled with the ratio of the ADC reference voltage (:math:`3.3` (:math:`V`)) over the AD converter resolution (:math:`10` bits, i.e. :math:`1023`). \
            The :math:`2.5` (:math:`V`) bias for zero magnetic flux is subtracted and the result is scaled with the sensitivity of the Hall effect sensor (:math:`1.25 \\frac{mV}{G} = 800 \\frac{G}{V}`)

        :param sensor: Raw sensor value.
        :type sensor: int
        :return: Sensor value in Gauss.
        :rtype: int
        """
        return (2.5 - sensor*(3.3/(2**self.potentiometer_bits - 1)))*800

    def calibrate_sensor_reading(self, sensor: int) -> int:
        """Return sensor value as is. No calibration is performed.

        :param sensor: Raw sensor value.
        :type sensor: int
        :return: Raw sensor value.
        :rtype: int
        """
        return sensor

    @property
    def p1(self) -> float:
        """Return ``p1`` constant calculated during calibration. If not available, return ``MagnetoShield.default_p1``.

        :return: ``p1`` constant.
        :rtype: float
        """
        if self._p1:
            return self._p1

        return self.default_p1

    @p1.setter
    def p1(self, value: float):
        self._p1 = value

    @property
    def p2(self) -> float:
        """Return ``p2`` constant calculated during calibration. If not available, return ``MagnetoShield.default_p2``.

        :return: ``p2`` constant.
        :rtype: float
        """
        if self._p2:
            return self._p2

        return self.default_p2

    @p2.setter
    def p2(self, value: float):
        self._p2 = value

    def calibrate(self):
        """Perform sensor calibration for conversion from Gauss to magnet distance from electromagnet. \
            The sensor values are read in the lowest and highest position, :math:`s_{low}` and :math:`s_{high}` respectively. \
            The constants :math:`p_1` and :math:`p2` are calculated as follows:

        .. math::
            p_2 &= \\frac{ \\log{ \\left( height_{e-magnet} - magnet_{low} \\right) } - \\log{ \\left( height_{e-magnet} - magnet_{high} \\right) } } { \\log{ s_{low} } - \\log{ s_{high} } }

            p_1 &= \\frac{ height_{e-magnet} - magnet_{high} } { \\left( s_{high} \\right)^{p_2} }

        :math:`height_{e-magnet}` corresponds to ``MagnetShield.emagnet_height``, which is the height of the electromagnet above ground. \
            :math:`magnet_{low}` and :math:`magnet_{high}` correspond to ``MagnetShield.magnet_low`` and ``MagnetShield.magnet_high``, which are the distances from the top of the magnet to the sensor \\
            in the lowest and highest position, respectively.

        """
        self.write(self.RUN, 0)
        time.sleep(.5)
        self.read()
        low = 0
        for _ in range(100):
            self.write(self.RUN, 100)
            _, val = self.read()
            if val > low:
                low = val

        self.write(self.RUN, 100)
        time.sleep(.5)
        self.read()
        high = 1e3
        for _ in range(100):
            self.write(self.RUN, 100)
            _, val = self.read()
            if val < high:
                high = val

        self.write(self.STOP, 0)
        time.sleep(.5)

        self.p2 = log((self.emagnet_height - self.magnet_low) / (self.emagnet_height - self.magnet_high)) / log(low/high)
        self.p1 = (self.emagnet_height - self.magnet_high) / (high ** self.p2)

    def magnet_position(self, sensor: float) -> float:
        """Calculate magnet distance from electromagnet using

        .. math::
            y = p1 \cdot B^{p_2}

        where :math:`B` is the magnetic flux density in Gauss. :math:`p1` and :math:`p2` are constants which are calculated in ``MagnetoShield.calibrate``.

        The distance can vary between approximately :math:`12 mm` and :math:`17 mm`.

        :param sensor: Sensor value in Gauss.
        :type sensor: float
        :return: Magnet distance from electromagnet.
        :rtype: float
        """
        return self.p1 * sensor ** self.p2
