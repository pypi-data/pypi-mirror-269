import ctypes
from time import perf_counter_ns
from typing import Self, Literal, Any, Callable

from .loader import TECHSTAR_LIB
from .logger import _logger

E6 = 1000000

"""
Only For IO, mode and level
OUTPUT = 1
INPUT = 0
HIGH = 1
LOW = 0
"""
# this will create a function that returns a C array, but it can't be recognized correctly by the pycharm
ADCArrayType: Callable = ctypes.c_uint16 * 10  # type: ignore
# on 32bit machine, this will create a C array of 3 floats with bit-width of 4 bytes
MPUArrayType: Callable = ctypes.c_float * 3  # type: ignore


class OnBoardSensors:
    """
    provides sealed methods accessing to the IOs and builtin sensors

    Owns 10 ADC channels and 3 MPU channels  and 8 IO channels

    ADC: 9 for normal use, 1 for power voltage measurement(the last element in the seq)
    IO: all the 8 are for normal use
    MPU: all the 3 are for normal use
    """

    def __init__(self, adc_min_sample_interval_ms: int = 5):
        """
        Initializes an instance of the OnBoardSensors class.
        init the ADC, IO and MPU data slots
        init sample freq limiter

        *Will NOT init the IO, ADC and MPU , you need to do it manually


        Parameters:
            adc_min_sample_interval_ms (int): The minimum sample interval in milliseconds for the ADC channels. Defaults to 5.

        Examples:
            >>> on_board = OnBoardSensors().adc_io_open().set_all_io_mode(0).set_all_io_level(1).MPU6500_Open()
        """

        self._adc_all: ctypes.Array = ADCArrayType()
        self._accel_all: ctypes.Array = MPUArrayType()
        self._gyro_all: ctypes.Array = MPUArrayType()
        self._atti_all: ctypes.Array = MPUArrayType()

        self.__adc_last_sample_timestamp: int = perf_counter_ns()

        self.__adc_min_sample_interval_ns: int = adc_min_sample_interval_ms * E6

    @property
    def last_sample_timestamp_ms(self) -> int:
        return int(self.__adc_last_sample_timestamp / E6)

    @property
    def adc_min_sample_interval_ms(self) -> int:
        """
        get the minimum interval between two consecutive samples, this is to prevent
        over-sampling, the value is in milliseconds。

        NOTE:
            the value is in milliseconds, but the unit is nanoseconds.
            a greater value means a lower rt performance
        """
        return int(self.__adc_min_sample_interval_ns / E6)

    @adc_min_sample_interval_ms.setter
    def adc_min_sample_interval_ms(self, value: int):
        self.__adc_min_sample_interval_ns = value * E6

    def adc_io_open(self) -> Self:
        """
        open the adc-io plug
        """
        _logger.info("Initializing ADC-IO")
        if open_times := TECHSTAR_LIB.adc_io_open() == -1:
            _logger.error("Failed to open ADC-IO")
        else:
            _logger.debug(f"ADC-IO open {open_times} times")
        return self

    def adc_io_close(self) -> Self:
        """
        close the adc-io plug
        """
        _logger.info("Closing ADC-IO")
        if TECHSTAR_LIB.adc_io_close() == -1:
            _logger.error("Failed to close ADC-IO")
        return self

    def adc_all_channels(self) -> ctypes.Array:
        """
        Get all the ADC channels. Length = 10

        Returns:
            ctypes.Array: An array containing the values of all the ADC channels.
        """

        can_update_time = (
            self.__adc_last_sample_timestamp + self.__adc_min_sample_interval_ns
        )
        if can_update_time > (current := perf_counter_ns()):

            return self._adc_all
        self.__adc_last_sample_timestamp = current
        if TECHSTAR_LIB.ADC_GetAll(self._adc_all):
            _logger.error("Failed to get all ADC channels")
        return self._adc_all

    def set_io_level(self, index: int, level: Literal[0, 1]) -> Self:
        """
        Set the level of the specified IO index.

        Args:
            index (int): The index of the IO.
            level (Literal[0, 1]): The level to set.

        Returns:
            Self: The instance of the class.

        Raises:
            None

        Description:
            This function sets the level of the specified IO index using the `adc_io_Set` method from the `OnBoardSensors` class.
            If the `adc_io_Set` method returns a truthy value, an error message is logged.
            The function returns the instance of the class.
        """
        if TECHSTAR_LIB.adc_io_Set(index, level):
            _logger.error(f"Failed to set IO level, index: {index}, level: {level}")
        return self

    def set_all_io_level(self, level: Literal[0, 1]) -> Self:
        """
        Sets the level of all IOs to the specified level.

        Args:
            level (Literal[0, 1]): The level to set for all IOs.

        Returns:
            Self: The instance of the class.

        Raises:
            None

        Description:
            This function sets the level of all IOs to the specified level using the `adc_io_SetAll` method from the `OnBoardSensors` class.
            If the `adc_io_SetAll` method returns a truthy value, an error message is logged.
            The function returns the instance of the class.
        """
        if TECHSTAR_LIB.adc_io_SetAll(level):
            _logger.error("Failed to set all IO level")
        return self

    @staticmethod
    def get_all_io_mode() -> bytes:
        """
        Get all IO modes. length = 8,store as bit0,bit1,bit2,bit3,bit4,bit5,bit6,bit7

        Returns:
            bytes: A buffer containing all IO modes.
        """
        buffer = ctypes.c_char()
        if TECHSTAR_LIB.adc_io_ModeGetAll(buffer):
            _logger.error("Failed to get all IO mode")
        return buffer.value

    @staticmethod
    def get_io_level(index: Literal[0, 1, 2, 3, 4, 5, 6, 7]) -> int:
        """
        Get the level of the specified IO index.

        Args:
            index (Literal[0, 1, 2, 3, 4, 5, 6, 7]): The index of the IO.

        Returns:
            int: The level of the specified IO index, which is calculated based on the result of adc_io_InputGetAll().

        """
        return (TECHSTAR_LIB.adc_io_InputGetAll() >> index) & 1

    def set_all_io_mode(self, mode: Literal[0, 1]) -> Self:
        """
        Sets the mode of all IOs to the specified mode.

        Args:
            mode (Literal[0, 1]): The mode to set for all IOs. Must be either 0 or 1.

        Returns:
            Self: The instance of the class.

        Raises:
            None

        Description:
            This function sets the mode of all IOs to the specified mode using the `adc_io_ModeSetAll` method from the `TECHSTAR_LIB` library.
            If the `adc_io_ModeSetAll` method returns a truthy value, an error message is logged.
            The function returns the instance of the class.
        """
        if TECHSTAR_LIB.adc_io_ModeSetAll(mode):
            _logger.error(f"Failed to set all IO mode to {mode}")
        return self

    def set_io_mode(
        self, index: Literal[0, 1, 2, 3, 4, 5, 6, 7], mode: Literal[0, 1]
    ) -> Self:
        """
        Sets the mode of the specified IO index to the specified mode.

        Args:
            index (Literal[0, 1]): The index of the IO. Must be either 0 or 1.
            mode (Literal[0, 1]): The mode to set for the IO. Must be either 0 or 1.

        Returns:
            Self: The instance of the class.

        Raises:
            None

        Description:
            This function sets the mode of the specified IO index to the specified mode using the `adc_io_ModeSet` method from the `TECHSTAR_LIB` library.
            If the `adc_io_ModeSet` method returns a truthy value, an error message is logged.
            The function returns the instance of the class.
        """
        if TECHSTAR_LIB.adc_io_ModeSet(index, mode):
            _logger.error(f"Failed to set IO mode, index: {index}, mode: {mode}")
        return self

    @staticmethod
    def io_all_channels() -> ctypes.c_uint8:
        """
        get all io plug input levels

        uint8, each bit represents a channel, 1 for high, 0 for low
        """
        return TECHSTAR_LIB.adc_io_InputGetAll()

    def MPU6500_Open(self) -> Self:
        """
        initialize the 6-axis enhancer MPU6500
        default settings:
            acceleration: -+8G
            gyro: -+2000 degree/s
            sampling rate: 1kHz
        """
        _logger.info("Initializing MPU6500...")
        if TECHSTAR_LIB.mpu6500_dmp_init():
            _logger.warning("Failed to initialize MPU6500")
        return self

    def acc_all(self) -> ctypes.Array:
        """
        Retrieves the acceleration data from the MPU6500 sensor.

        Returns:
            ctypes.Array: An array containing the acceleration data.
        Notes:
            length = 3
            [0] ==> axis X
            [1] ==> axis Y
            [2] ==> axis Z
        """
        TECHSTAR_LIB.mpu6500_Get_Accel(
            self._accel_all
        )  # this function return a C pointer to the self._accel_all
        return self._accel_all

    def gyro_all(self) -> ctypes.Array:
        """
        Retrieves the gyroscope data from the MPU6500 sensor.

        Returns:
            ctypes.Array: An array containing the gyroscope data.

        Notes:
            length = 3
            [0] ==> axis X
            [1] ==> axis Y
            [2] ==> axis Z
        """

        TECHSTAR_LIB.mpu6500_Get_Gyro(
            self._gyro_all
        )  # this function return a C pointer to the self._gyro_all

        return self._gyro_all

    def atti_all(self) -> ctypes.Array:
        """
        Retrieves the attitude data from the MPU6500 sensor.

        Returns:
            ctypes.Array: An array containing the attitude data.

        Notes:
            length = 3
            [0] ==> Pitch|axis X
            [1] ==> Roll |axis Y
            [2] ==> Yaw  |axis Z
        """
        TECHSTAR_LIB.mpu6500_Get_Attitude(
            self._atti_all
        )  # this function return a C pointer to the self._atti_all

        return self._atti_all

    @staticmethod
    def get_handle(attr_name: str) -> Any:
        """
        Returns the attribute value of the TECHSTAR_LIB object corresponding to the given attribute name.
        Reserved to the user to harness other attributes of the TECHSTAR_LIB object.
        Args:
            attr_name (str): The name of the attribute to retrieve.

        Returns:
            Any: The value of the attribute.

        Raises:
            AttributeError: If the attribute does not exist in the TECHSTAR_LIB object.
        """
        return getattr(TECHSTAR_LIB, attr_name)
