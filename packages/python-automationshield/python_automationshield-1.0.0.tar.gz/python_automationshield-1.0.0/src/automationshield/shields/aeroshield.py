import numpy as np

from .baseshield import BaseShield


class AeroShield(BaseShield):
    """Class for Aeroshield device. Inherits from BaseShield.

    The Aeroshield is a pendulum control experiment. The actuator is propellor at the end of the pendulum. The position of the pendulum is measured by an angle sensor.

    Interface:
        * Actuator input should be provided in percent by default.
        * Potentiometer is provided in percent by default.
        * Sensor values are converted to degrees by default.
    """
    script = "aeroshield"
    shield_id = "AE"

    def convert_sensor_reading(self, raw: int) -> float:
        """Convert raw angle to degrees.

        .. math::
            \\alpha_{deg} = \\alpha_{raw} \\cdot \\frac{360}{2^{12}}

        :param raw: 12-bit value of angle sensor.
        :type raw: int
        :return: Angle value scaled to degrees.
        :rtype: float
        """
        return raw * 360 / 4096

    @staticmethod
    def raw_angle_to_rad(raw: int) -> float:
        """Convert raw angle to radians.

        .. math::
            \\alpha_{rad} = \\alpha_{raw} \\cdot \\frac{2 \\pi}{2^{12}}

        :param raw: 12-bit value of angle sensor.
        :type raw: int
        :return: Angle value scaled to radians.
        :rtype: float
        """
        return raw * np.pi / 2048

    def calibrate_sensor_reading(self, raw_angle: int) -> int:
        """Calibrate angle with ``BaseShield.zero_reference``. Subtracts zero offset from current angle reading.

        :param raw_angle: Raw 12-bit angle value.
        :type raw_angle: int
        :return: Calibrated angle.
        :rtype: int
        """

        angle = raw_angle - self.zero_reference
        # make sure angle is positive in testing range
        if angle < -1024:
            angle += 4096

        return angle
