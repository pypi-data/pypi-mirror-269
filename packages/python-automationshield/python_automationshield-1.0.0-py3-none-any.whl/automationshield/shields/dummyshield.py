import numpy as np
import time

from .baseshield import BaseShield


class DummyShield(BaseShield):
    def read(self) -> tuple[float]:
        ti = time.perf_counter()

        pot = 100 + 50*np.sin(ti)
        sensor = 100 + 125*np.cos(ti)

        return pot, sensor

    def write(self, flag: int, actuator: float):
        return self.saturate_bits(actuator, self.actuator_bits)

    def open(self):
        return self

    def close(self, *args):
        pass

