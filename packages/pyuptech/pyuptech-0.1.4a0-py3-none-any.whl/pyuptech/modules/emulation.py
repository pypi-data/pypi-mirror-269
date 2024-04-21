import ctypes
from random import randint
from typing import Self, Literal, Any

from .sensors import OnBoardSensors


class SensorEmulator(OnBoardSensors):
    mpu_rand_range = (0, 2**32 - 1)
    adc_rand_range = (0, 2**16 - 1)
    io_rand_range = (0, 2**8 - 1)

    def adc_io_open(self) -> Self:
        return self

    def adc_io_close(self) -> Self:
        return self

    def set_io_level(self, index: int, level: Literal[0, 1]) -> Self:
        return self

    def set_io_mode(self, index: int, mode: Literal[0, 1]) -> Self:
        return self

    def set_all_io_mode(self, mode: Literal[0, 1]) -> Self:
        return self

    def set_all_io_level(self, level: Literal[0, 1]) -> Self:
        return self

    @staticmethod
    def io_all_channels() -> ctypes.c_uint8:
        return ctypes.c_uint8(randint(*SensorEmulator.io_rand_range))

    def adc_all_channels(self) -> ctypes.Array:

        for i in range(10):
            self._adc_all[i] = randint(*self.adc_rand_range)

        return self._adc_all

    def MPU6500_Open(self) -> Self:
        return self

    def acc_all(self) -> ctypes.Array:
        for i in range(3):
            self._accel_all[i] = randint(*self.mpu_rand_range)
        return self._accel_all

    def gyro_all(self) -> ctypes.Array:
        for i in range(3):
            self._gyro_all[i] = randint(*self.mpu_rand_range)
        return self._gyro_all

    def atti_all(self) -> ctypes.Array:
        for i in range(3):
            self._atti_all[i] = randint(*self.mpu_rand_range)
        return self._atti_all

    @staticmethod
    def get_io_level(index: Literal[0, 1, 2, 3, 4, 5, 6, 7]) -> int:
        return randint(0, 1)

    @staticmethod
    def get_all_io_mode() -> bytes:
        return ctypes.c_char(randint(*SensorEmulator.io_rand_range)).value

    @staticmethod
    def get_handle(attr_name: str) -> Any:
        raise NotImplementedError("Emulation is not supported")
