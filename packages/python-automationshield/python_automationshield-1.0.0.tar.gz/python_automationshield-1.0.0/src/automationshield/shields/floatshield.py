from .baseshield import BaseShield


class FloatShield(BaseShield):
    """Class for Floatshield device. Inherits from BaseShield.

    The Floatshield features a ball in a vertical tube. A fan (the actuator) is installed at the bottom, which can blow the ball up in the tube. \
        The position of the ball in the tube is measured by a distance sensor at the top of the tube, using infrared laser.

    Interface:
        * Actuator input should be provided in percent by default.
        * Potentiometer is provided in percent by default.
        * Sensor values are provided in millimeters from the bottom of the tube.
    """
    script = "floatshield"
    shield_id = "FL"

    actuator_bits = 12

    def calibrate_sensor_reading(self, sensor: int) -> int:
        """Calibrate sensor reading. 0 is taken as the ball being at the bottome of the tube.

        :param sensor: Raw sensor value.
        :type sensor: int
        :return: Calibrate sensor value.
        :rtype: int
        """
        return - super().calibrate_sensor_reading(sensor)
