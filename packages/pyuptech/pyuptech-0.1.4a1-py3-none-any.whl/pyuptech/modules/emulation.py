import ctypes
from random import randint
from typing import Self, Literal, Any

from .sensors import OnBoardSensors, MPUDataPack, ADCDataPack


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
    def io_all_channels() -> int:
        return ctypes.c_uint8(randint(*SensorEmulator.io_rand_range)).value

    def adc_all_channels(self) -> ADCDataPack:

        for i in range(10):
            self._adc_all[i] = randint(*self.adc_rand_range)

        return tuple(self._adc_all)  # type: ignore

    def MPU6500_Open(self) -> Self:
        return self

    def acc_all(self) -> MPUDataPack:
        for i in range(3):
            self._accel_all[i] = randint(*self.mpu_rand_range)
        return tuple(self._accel_all)  # type: ignore

    def gyro_all(self) -> MPUDataPack:
        for i in range(3):
            self._gyro_all[i] = randint(*self.mpu_rand_range)
        return tuple(self._gyro_all)  # type: ignore

    def atti_all(self) -> MPUDataPack:
        for i in range(3):
            self._atti_all[i] = randint(*self.mpu_rand_range)
        return tuple(self._atti_all)  # type: ignore

    @staticmethod
    def get_io_level(index: Literal[0, 1, 2, 3, 4, 5, 6, 7]) -> int:
        return randint(0, 1)

    @staticmethod
    def get_all_io_mode() -> int:
        return ctypes.c_char(randint(*SensorEmulator.io_rand_range)).value[0]

    @staticmethod
    def get_handle(attr_name: str) -> Any:
        raise NotImplementedError("Emulation is not supported")
