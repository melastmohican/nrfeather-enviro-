from adafruit_ble.attributes import Attribute
from adafruit_ble.characteristics import StructCharacteristic, Characteristic
from adafruit_ble.characteristics.float import FloatCharacteristic
from adafruit_ble.uuid import StandardUUID
from adafruit_ble_adafruit.adafruit_service import AdafruitService


class EnvironmentalSensingService(AdafruitService):
    """Environmental Sensing service (0x181A)."""

    uuid = StandardUUID(0x181A)
    temperature = FloatCharacteristic(uuid=StandardUUID(0x2A6E),
                                      properties=(Characteristic.READ | Characteristic.NOTIFY),
                                      write_perm=Attribute.NO_ACCESS)
    """Temperature (0x2A6E)."""
    humidity = FloatCharacteristic(uuid=StandardUUID(0x2A6F), properties=(Characteristic.READ | Characteristic.NOTIFY),
                                   write_perm=Attribute.NO_ACCESS)
    """Relative humidity over a range of 0 to 100%  (0x2A6F)"""
    pressure = FloatCharacteristic(uuid=StandardUUID(0x2724), properties=(Characteristic.READ | Characteristic.NOTIFY),
                                   write_perm=Attribute.NO_ACCESS, )
    """Barometric pressure in hectoPascals (hPa) (0x2724)"""
    gas = StructCharacteristic("<fff", uuid=AdafruitService.adafruit_service_uuid(0x666),
                               properties=(Characteristic.READ | Characteristic.NOTIFY),
                               write_perm=Attribute.NO_ACCESS)
    """Gas resistance for oxidising, reducing and NH3"""
    lux = FloatCharacteristic(uuid=StandardUUID(0x2731), properties=(Characteristic.READ | Characteristic.NOTIFY),
                              write_perm=Attribute.NO_ACCESS)
    """Illuminance (lux) (0x2731)"""
    proximity = FloatCharacteristic(uuid=AdafruitService.adafruit_service_uuid(0x777),
                                    properties=(Characteristic.READ | Characteristic.NOTIFY),
                                    write_perm=Attribute.NO_ACCESS)
    """B~5cm proximity detection range"""
    particulate_matter = StructCharacteristic(">HHHHHHHHHHHH", uuid=AdafruitService.adafruit_service_uuid(0x888),
                                              properties=(Characteristic.READ | Characteristic.NOTIFY),
                                              write_perm=Attribute.NO_ACCESS)
    """Dictionary with available particulate/quality data"""
    measurement_period = AdafruitService.measurement_period_charac()
    """Initially 1000ms."""
