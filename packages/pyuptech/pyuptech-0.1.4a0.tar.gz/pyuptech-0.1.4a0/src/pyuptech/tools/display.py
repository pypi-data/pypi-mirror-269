import time
from typing import Literal, Dict

from ..modules.emulation import SensorEmulator
from ..modules.screen import Screen, Color, FontSize
from ..modules.sensors import OnBoardSensors

sensors: OnBoardSensors | SensorEmulator | None = None
screen: Screen | None = None


def set_emulation_mode(mode: Literal["on", "off"]):
    """
    Sets the emulation mode of the sensors.

    Args:
        mode (Literal["on", "off"]): The emulation mode to set. Must be either "on" or "off".

    Returns:
        None

    This function sets the emulation mode of the sensors. If the mode is "on", it creates a new instance of the SensorEmulator class and assigns it to the global variable "sensors". If the mode is "off", it creates a new instance of the OnBoardSensors class and assigns it to the global variable "sensors".

    Raises:
        None
    """
    global sensors, screen
    match mode:
        case "on":
            #  仿真器不需要启动adc-io等硬件设备
            sensors = SensorEmulator()
            screen = None  # 仿真模式下，假设屏幕是脱机的
        case "off":
            sensors = (
                OnBoardSensors().adc_io_open().set_all_io_mode(0).set_all_io_level(1)
            )
            screen = (
                Screen()
                .open()
                .fill_screen(Color.BLACK)
                .refresh()
                .set_led_color(0, Color.BROWN)
                .set_led_color(1, Color.GRED)
            )


def mpu_display_on_lcd(mode: Literal["atti", "acc", "gyro"]):
    """
    Display the specified mode on the screen.

    Parameters:
        mode (Literal["atti", "acc", "gyro"]): The mode to display.

    Returns:
        None
    """
    match mode:
        case "atti":
            attitude = sensors.atti_all()
            screen.put_string(0, 30, f"Pitch:{attitude[0]:.2f}  ")
            screen.put_string(0, 48, f"Roll :{attitude[1]:.2f}  ")
            screen.put_string(0, 66, f"Yaw  :{attitude[2]:.2f}  ")
        case "gyro":
            gyro = sensors.gyro_all()
            screen.put_string(0, 30, f"Gyro x {gyro[0]:.2}")
            screen.put_string(0, 48, f"Gyro y {gyro[1]:.2}")
            screen.put_string(0, 66, f"Gyro z {gyro[2]:.2}")
        case "acc":
            accel = sensors.acc_all()
            screen.put_string(0, 30, f"x_acc :{accel[0]:.2}")
            screen.put_string(0, 44, f"y_acc :{accel[1]:.2}")
            screen.put_string(0, 54, f"z_acc :{accel[2]:.2}")
    screen.refresh()


def mpu_display_on_console():
    """
    Display the MPU data in a formatted table in the terminal.

    This function combines the ACC, GYRO, and ATTI data into a structured list and creates a table using the
    `terminaltables` library. The table is then printed to the console.

    """
    from terminaltables import DoubleTable

    # Combine data into one structured list
    combined_data = [
        ["ACC", "Value", "GYRO", "Value", "ATTI", "Value"],
    ]
    acc_names = ["X_ACC", "Y_ACC", "Z_ACC"]

    gyro_names = ["X_GYRO", "Y_GYRO", "Z_GYRO"]

    atti_names = ["Pitch", "Roll", "Yaw"]
    for i in range(len(acc_names)):
        combined_data.append(
            [
                acc_names[i],
                f"{sensors.acc_all()[i]:.2}",
                gyro_names[i],
                f"{sensors.gyro_all()[i]:.2}",
                atti_names[i],
                f"{sensors.atti_all()[i]:.2}",
            ]
        )

    # Create and print the table
    table = DoubleTable(combined_data)
    table.inner_row_border = True  # Add inner row borders for clarity
    print(table.table)


def adc_io_display_on_console(
    adc_labels: Dict[int, str] = None, io_labels: Dict[int, str] = None
):
    """
    Displays ADC and IO channel values on the console using the terminaltables library.

    Args:
        adc_labels (Dict[int, str], optional): A dictionary mapping ADC channel indices to custom labels. Defaults to None.
        io_labels (Dict[int, str], optional): A dictionary mapping IO channel indices to custom labels. Defaults to None.

    Returns:
        None

    Raises:
        None


    """
    from terminaltables import DoubleTable

    adc_labels = adc_labels or {}
    io_labels = io_labels or {}
    adc = sensors.adc_all_channels()
    io = sensors.io_all_channels()
    rows = [
        ["Names"] + ([adc_labels.get(i, f"ADC{i}") for i in range(10)]),
        ["ADC"] + [f"{x}" for x in adc],
        ["Names"] + ([io_labels.get(i, f"IO{i}") for i in range(8)]),
        ["IO"] + [int(bit) for bit in f"{io.value:08b}"],
    ]
    table = DoubleTable(rows)
    table.inner_row_border = True
    print(table.table)


def adc_io_display_on_lcd(
    interval: float = 0.01,
    adc_labels: Dict[int, str] = None,
    io_labels: Dict[int, str] = None,
):
    """
    Reads sensor values from ADC and IO channels and displays them on the screen.

    Args:
        interval (float, optional): The time interval between sensor readings in seconds. Defaults to 0.01.
        adc_labels (Dict[int, str], optional): A dictionary mapping ADC channel indices to custom labels. Defaults to None.
        io_labels (Dict[int, str], optional): A dictionary mapping IO channel indices to custom labels. Defaults to None.

    Returns:
        None

    Raises:
        KeyboardInterrupt: If the user interrupts the program by pressing Ctrl+C.
    """

    screen.set_font_size(FontSize.FONT_6X8)
    adc_labels = adc_labels or {}
    io_labels = io_labels or {}
    adc = sensors.adc_all_channels()
    # 打印 ADC 通道值表格
    for i in range(9):
        label = adc_labels.get(i, f"[{i}]")
        value = adc[i]
        screen.put_string(0, i * 8, f"{label}:{value}")

    io = [int(bit) for bit in f"{sensors.io_all_channels().value:08b}"]
    # 打印 IO 通道值表格
    for i in range(8):
        label = io_labels.get(i, f"[{i}]")
        value = io[i]
        screen.put_string(90, i * 8, f"{label}:{value}")
    screen.fill_screen(Color.BLACK).refresh()
    time.sleep(interval)
