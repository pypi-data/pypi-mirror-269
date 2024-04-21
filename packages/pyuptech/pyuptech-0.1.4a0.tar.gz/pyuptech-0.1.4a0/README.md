# pyuptech

> 一个API包装库，通过调用TechStar的二进制so库完成的功能
---

# 安装

使用`pdm`安装

```shell
pdm add pyuptech
```

## OnBoardSensors

**简介**

`OnBoardSensors`是一个Python类，封装了对嵌入式硬件板载传感器和输入/输出接口的操作，如ADC、GPIO以及MPU6500六轴传感器。该类通过ctypes库调用预编译的C库函数实现底层硬件交互。

### 类方法概览

- **初始化**: 初始化所有IO通道模式为输入，并设置初始电平为高，同时初始化ADC插件。

- **ADC操作**:
    - `adc_min_sample_interval_ms`: 获取和设置ADC采样间隔（以毫秒为单位，内部存储为纳秒）。
    - `adc_all_channels`: 获取ADC的所有通道数据，确保采样间隔满足最小限制。

- **GPIO操作**:
    - `set_io_level`, `set_all_io_level`: 设置单个或全部GPIO引脚电平。
    - `set_io_mode`, `set_all_io_mode`: 设置单个或全部GPIO引脚的工作模式（输出或输入）。
    - `get_io_level`: 获取指定GPIO引脚电平。
    - `get_all_io_mode`: 获取所有GPIO引脚工作模式。
    - `io_all_channels`: 获取所有GPIO引脚的输入电平。

- **MPU6500六轴传感器操作**:
    - `MPU6500_Open`: 初始化MPU6500传感器。
    - `acc_all`, `gyro_all`, `atti_all`: 分别获取MPU6500的加速度、角速度和姿态数据。

### **已完成的功能**

- 初始化和关闭ADC及GPIO接口。
- 控制GPIO引脚的电平和工作模式。
- 限制ADC采样频率，防止过采样。
- 获取ADC和GPIO的数据。
- 初始化和读取MPU6500六轴传感器数据。

### QUICKSTART

```python
from pyuptech import OnBoardSensors
from ctypes import c_uint8, Array

# 创建OnBoardSensors对象，设置模拟量传感器最小采样间隔为5ms
sensor_controller = OnBoardSensors(adc_min_sample_interval_ms=5)

# 初始化ADC,设置所有GPIO引脚为输入，设置初始电平为高
sensor_controller.adc_io_open().set_all_io_mode(0).set_all_io_level(1)

# 设置ADC最小采样间隔为10ms，防止请求堵塞STM32从机
sensor_controller.adc_min_sample_interval_ms = 10

# 获取所有GPIO引脚当前电平
gpio_levels: c_uint8 = sensor_controller.io_all_channels()
print(gpio_levels.value)

# 初始化并读取MPU6500加速度数据
sensor_controller.MPU6500_Open()
acceleration_data: Array = sensor_controller.acc_all()

# 设置第3号GPIO引脚为输出并设置电平为低
sensor_controller.set_io_mode(2, 1)
sensor_controller.set_io_level(2, 0)
```

---

# Screen

本模块定义了一个名为 `Screen`
的类，用于操作和管理LCD屏幕。该类提供了一系列方法，允许用户设置字体大小、颜色、显示方向以及在屏幕上绘制字符串、填充颜色区域等多种操作。每个方法都返回 `Self`
实例，支持链式调用。

### **已完成功能**

- **初始化与打开屏幕**：`Screen` 类在实例化时可以自动打开屏幕并设置初始显示方向为水平（通过参数 `direction=2`
  ），同时清空屏幕背景色为黑色。

- **显示方向设置**：通过 `open()` 方法可设定屏幕显示方向，支持垂直（`direction=1`）或水平（`direction=2`）两种模式。

- **刷新屏幕**：`refresh()` 方法用于将缓存中的数据显示到实际LCD上。

- **字体大小设置**：通过 `set_font_size()` 方法可以选择不同预设字体大小，具体由枚举类型 `FontSize` 提供。

- **前景色与背景色设置**：分别使用 `set_fore_color()` 和 `set_back_color()`
  方法设置文本前景色和屏幕背景色，颜色值由枚举类型 `Color` 提供。

- **LED颜色设置**：针对特定索引位置的LED灯，可以通过 `set_led_color()` 方法设置其颜色。

- **填充屏幕**：`fill_screen()` 方法用于用指定的颜色填充整个屏幕。

- **输出字符串**：`put_string()` 方法可以在屏幕指定坐标位置显示字符串。

- **填充矩形框**：`fill_frame()` 方法用于填充指定矩形范围内的颜色。

- **填充圆角矩形框**：`fill_round_frame()` 方法用于填充带指定圆角半径的圆角矩形框。

- **填充圆形**：`fill_circle()` 方法用于填充指定圆心和半径的圆形。

- **绘制网格**：`draw_mesh()` 方法在指定矩形区域内绘制网格图案。

- **绘制矩形边框**：`draw_frame()` 方法用来绘制一个空心矩形框。

### **QUICKSTART**

```python
from pyuptech import Screen, FontSize, Color

# 创建 Screen 实例并初始化屏幕,设置屏幕显示方向为水平
screen = Screen(screen_dir=2)

# 设置字体大小为 8x12
screen.set_font_size(FontSize.FONT_8X12)

# 设置前景色为白色，背景色为深蓝色
screen.set_fore_color(Color.WHITE)
screen.set_back_color(Color.DARKBLUE)

# 填充屏幕背景色
screen.fill_screen(Color.DARKBLUE)

# 在屏幕左上角显示字符串
screen.put_string(0, 0, "Hello, World!")

# 刷新屏幕以确保所有更改生效
screen.refresh()
```

也可以使用链式调用

```python
from pyuptech import Screen, FontSize, Color

# 创建 Screen 实例并初始化屏幕,设置屏幕显示方向为水平
screen = Screen(screen_dir=2)

(screen
 .fill_screen(Color.BLACK)
 .set_font_size(FontSize.FONT_12X20)
 .put_string(0, 0, "Hello World")
 .refresh())

```

---

## 性能

通过调用 `set_log_level` 函数来静默控制台输出，在高强度压力场景下能够提升程序性能。

```python
from pyuptech import set_log_level

"""
日志等级 DEBUG - 用于详细调试阶段的日志信息，其默认值通常为10。
日志等级 INFO - 提供程序运行的基本状态信息，其值设定为20。
日志等级 WARN - 警告信息，表明可能存在问题但仍不影响程序继续运行，其值为30。
日志等级 ERROR - 错误信息，表示存在阻碍程序正常执行的问题，其值为40。
日志等级 CRITICAL - 致命错误信息，代表严重的系统故障情况，其值为50。
"""

set_log_level(50)  # 将日志等级设为50，此时logger只会记录优先级高于CRITICAL级别的消息

from logging import CRITICAL

set_log_level(CRITICAL)  # 上述代码与上面设置效果一致，即只记录CRITICAL及其以上级别的日志信息
```

---

## 调试

通过 `tools.display` 可以将传感器数据打印到终端或者主板板载LCD屏幕上

```python
from pyuptech import (
    set_emulation_mode,
    mpu_display_on_lcd,
    mpu_display_on_console,
    adc_io_display_on_lcd,
    adc_io_display_on_console)

# 关闭模拟模式，不关闭将无法进行正常的实机运行
set_emulation_mode("off")

mpu_display_on_console()  # 将MPU6500数据打印到终端

mpu_display_on_lcd(mode="acc")  # 将MPU6500加速度数据打印到LCD

# 定义ADC标签索引字典，可以空缺部分键值
adc_labels = {
    6: 'EDGE_FL',
    7: "EDGE_RL",
    2: 'EDGE_FR',
    1: 'EDGE_RR',
    8: 'L1',
    0: 'R1',
    3: 'FB', 5: 'RB',
    4: 'GRAY'
}
# 定义IO标签索引字典,可以空缺部分键值
io_labels = {
    3: "gray l",
    2: "gray r",

    7: 'ftl',
    6: 'ftr',
    5: 'rtr'
}

adc_io_display_on_lcd(adc_labels=adc_labels, io_labels=io_labels)  # 将ADC和GPIO数据打印到LCD 

adc_io_display_on_console(adc_labels=adc_labels, io_labels=io_labels)  # 将ADC和GPIO数据打印到终端 


```

## 使用传感器仿真器

通过 `modules.emulation.SensorEmulator` 可以使用传感器仿真器

```python

# 传感器仿真器导入
from pyuptech import SensorEmulator

# SensorEmulator 通过继承 OnBoardSensors 类并重写与硬件的交互方法完成的一个仿真器，所以它具有的方法是和OnBoardSensors 基本一致
# Note: 所有返回的数据都是随机生成的，只是用于演示
sensor_emulator = SensorEmulator(adc_min_sample_interval_ms=10)

print(sensor_emulator.adc_io_open())

print(list(sensor_emulator.MPU6500_Open().acc_all()))


```

配合 `modules.display` 使用

```python
from pyuptech import (
    set_emulation_mode,
    mpu_display_on_console,
    adc_io_display_on_console)

# 启动模拟模式，以便打印可以正常使用随机生成的数据进行工作
set_emulation_mode("on")

mpu_display_on_console()  # 将MPU6500数据打印到终端

adc_io_display_on_console()  # 将ADC和GPIO数据打印到终端

```

