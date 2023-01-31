# nrfeather-enviro+
Adafruit Feather nRF52840 Express with Pimoroni Enviro+ FeatherWing

## CIRCUITPY
Adafruit CircuitPython 7.3.3 on 2022-08-29; Adafruit Feather nRF52840 Express with nRF52840
Board ID:feather_nrf52840_express

## PyCharm
* https://learn.adafruit.com/welcome-to-circuitpython/pycharm-and-circuitpython
* https://ordina-jworks.github.io/iot/2021/03/25/Getting-started-with-the-pi-pico.html
* https://github.com/adafruit/Adafruit_Learning_System_Guides/tree/main/Getting_Started_With_BLE_and_CP
* https://github.com/todbot/circuitpython-tricks

## Enviro+ FeatherWing
* https://shop.pimoroni.com/products/enviro-plus-featherwing
* https://github.com/pimoroni/EnviroPlus-FeatherWing
* https://github.com/pimoroni/EnviroPlus-FeatherWing/blob/master/REFERENCE.md
* https://github.com/pimoroni/EnviroPlus-FeatherWing/issues/31
* https://www.instructables.com/Using-the-Pimoroni-Enviro-FeatherWing-With-the-Ada/
* https://www.instructables.com/Plotting-Carbon-Dioxide-Levels-With-the-Pimoroni-E/
* https://www.instructables.com/Publishing-Particulate-Matter-Sensor-Data-to-Adafr/
* https://circuitpython.org/board/feather_nrf52840_express/
* https://adafruit-circuit-python.s3.amazonaws.com/index.html?prefix=bin/mpy-cross/
* https://circuitpython.org/libraries
* https://learn.adafruit.com/adafruit-bme280-humidity-barometric-pressure-temperature-sensor-breakout/overview
* https://learn.adafruit.com/introducing-the-adafruit-nrf52840-feather/overview
* https://github.com/Oakwright/m4feather
* https://learn.adafruit.com/circuitpython-multi-temperature-ble-monitoring/overview
* https://learn.adafruit.com/diy-air-quality-monitor/circuitpython-setup
* https://learn.adafruit.com/pmsa003i/python-circuitpython
* https://github.com/robmarkcole/HASS-circuitpython-air-quality-sensor-node
* https://github.com/robmarkcole/Useful-python/blob/master/Pyserial/pyserial.ipynb
* https://learn.adafruit.com/remote-iot-environmental-sensor/code
* https://blog.adafruit.com/2019/10/03/a-circuitpython-ble-client-and-server-tutorial-circuitpython-feather-bluetooth/
* https://www.rototron.info/circuitpython-ble-client-server-tutorial/

## Dependencies
* https://github.com/pimoroni/EnviroPlus-FeatherWing
* https://github.com/pimoroni/Pimoroni_CircuitPython_LTR559

## Tools
* https://github.com/adafruit/circup
* https://docs.circuitpython.org/projects/circup/en/latest/index.html
* https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup
* https://github.com/Neradoc/discotool
* https://github.com/scientifichackers/ampy

## Not related
* https://github.com/kung-foo/infinitree.git
* https://github.com/mraleson/piku

## Bluetooth Assigned Numbers
### Service:
* Environmental Sensing service 0x181A

### Characteristics:
* Humidity 0x2A6F
* Illuminance (lux)   0x2731
* Particulate Matter - PM1 Concentration      0x2BD5
* Particulate Matter - PM2.5 Concentration    0x2BD6
* Particulate Matter - PM10 Concentration     0x2BD7
* Pressure (pascal) 0x2724
* Temperature 0x2A6E

### Appearance:
* 0x015 0x0540 to 0x057F Sensor

### Appearance Sub-category: 0x015 
* 0x00 0x0540 Generic Sensor
* 0x01 0x0541 Motion Sensor
* 0x02 0x0542 Air quality Sensor 
* 0x03 0x0543 Temperature Sensor
* 0x04 0x0544 Humidity Sensor
* 0x0B 0x054B Ambient Light Sensor
* 0x11 0x0551 Proximity Sensor
* 0x12 0x0552 Multi-Sensor

### Units:
* Celsius temperature (degree Celsius)    0x272F
* Concentration (count per cubic metre)   0x27B5
 
 




