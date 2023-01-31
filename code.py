import time

import analogio
import board
import busio
import digitalio
import displayio
from adafruit_ble import BLERadio
from adafruit_ble_adafruit.adafruit_service import AdafruitServerAdvertisement

import air_quality
from adafruit_bme280 import basic as adafruit_bme280
from adafruit_st7735r import ST7735R
from pimoroni_circuitpython_ltr559 import Pimoroni_LTR559
from pimoroni_mics6814 import Pimoroni_MICS6814
from environmental_sensing_service import EnvironmentalSensingService

PIN_NH3 = analogio.AnalogIn(board.A0)
PIN_RED = analogio.AnalogIn(board.A1)
PIN_OX = analogio.AnalogIn(board.A2)
PIN_ENABLE = digitalio.DigitalInOut(board.A4)

gas = Pimoroni_MICS6814(PIN_OX, PIN_RED, PIN_NH3, PIN_ENABLE)

spi = board.SPI()
spi.try_lock()
spi.configure(baudrate=100000000)
spi.unlock()
tft_dc = board.D5
tft_cs = board.D6
displayio.release_displays()
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.D9)
display = ST7735R(display_bus, width=160, height=80, colstart=24, rowstart=1, rotation=270, invert=True)
i2c = board.I2C()

bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
bme280.sea_level_pressure = 1013.25
ltr559 = Pimoroni_LTR559(i2c)

air_uart = busio.UART(board.TX, board.RX, baudrate=9600)
air = air_quality.AirQualitySensor(air_uart)

env_sense_svc = EnvironmentalSensingService()
env_sense_svc.measurement_period = 1000
env_sense_svc_last_update = 0

ble = BLERadio()
ble.name = "nRFeather-Enviro+"

# CircuitPython: 0x8088
adv = AdafruitServerAdvertisement()
adv.pid = 0x8088

while True:
    # Advertise when not connected.
    print("Advertising")
    ble.start_advertising(adv)
    while not ble.connected:
        pass
    print("Connected")
    ble.stop_advertising()

    while ble.connected:
        now_msecs = time.monotonic_ns() // 1000000  # pylint: disable=no-member
        if now_msecs - env_sense_svc_last_update >= env_sense_svc.measurement_period:
            env_sense_svc.temperature = bme280.temperature
            env_sense_svc.humidity = bme280.humidity
            env_sense_svc.pressure = bme280.pressure
            env_sense_svc.gas = (gas.read_all().oxidising, gas.read_all().reducing, gas.read_all().nh3)
            env_sense_svc.lux = ltr559.get_lux()
            env_sense_svc.proximity = ltr559.get_proximity()
            if air.read():
                env_sense_svc.particulate_matter = (
                    air._pm10_standard, air._pm25_standard, air._pm100_standard, air._pm10_env,
                    air._pm25_env, air._pm100_env, air._particles_03um, air._particles_05um,
                    air._particles_10um, air._particles_25um, air._particles_50um,
                    air._particles_100um
                )
            env_sense_svc_last_update = now_msecs
    print("Disconnected")
