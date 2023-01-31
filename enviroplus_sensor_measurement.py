import os
import struct
import time
import adafruit_ble
from adafruit_ble.advertising import Advertisement, LazyObjectField
from adafruit_ble.advertising.standard import ManufacturerData, ManufacturerDataField
from adafruit_ble.advertising.adafruit import (
    MANUFACTURING_DATA_ADT,
    ADAFRUIT_COMPANY_ID,
)

try:
    from typing import Optional
    from _bleio import ScanEntry
except ImportError:
    pass

_ble = adafruit_ble.BLERadio()  # pylint: disable=invalid-name
_sequence_number = 0  # pylint: disable=invalid-name


def broadcast(
        measurement: "EnviroSensorMeasurement",
        *,
        broadcast_time: float = 0.1,
        extended: bool = False
) -> None:
    """Broadcasts the given measurement for the given broadcast time. If extended is False and the
    measurement would be too long, it will be split into multiple measurements for transmission,
    each with the given broadcast time.
    """
    global _sequence_number  # pylint: disable=global-statement,invalid-name
    for submeasurement in measurement.split(252 if extended else 31):
        submeasurement.sequence_number = _sequence_number
        _ble.start_advertising(submeasurement, scan_response=None)
        time.sleep(broadcast_time)
        _ble.stop_advertising()
        _sequence_number = (_sequence_number + 1) % 256


# This line causes issues with Sphinx, so we won't run it in the CI
if not hasattr(os, "environ") or (
        "GITHUB_ACTION" not in os.environ and "READTHEDOCS" not in os.environ
):
    if _ble._adapter.address:  # pylint: disable=protected-access
        device_address = "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(  # pylint: disable=invalid-name
            *reversed(
                list(
                    _ble._adapter.address.address_bytes  # pylint: disable=protected-access
                )
            )
        )
    else:
        device_address = "000000000000"  # pylint: disable=invalid-name
        """Device address as a string."""


class EnviroSensorMeasurement(Advertisement):
    """A collection of sensor measurements."""

    # This prefix matches all
    match_prefixes = (
        # Matches the sequence number field header (length+ID)
        struct.pack("<BHBH", MANUFACTURING_DATA_ADT, ADAFRUIT_COMPANY_ID, 0x03, 0x0003),
    )

    manufacturer_data = LazyObjectField(
        ManufacturerData,
        "manufacturer_data",
        advertising_data_type=MANUFACTURING_DATA_ADT,
        company_id=ADAFRUIT_COMPANY_ID,
        key_encoding="<H",
    )

    sequence_number = ManufacturerDataField(0x0003, "<B")
    """Sequence number of the measurement. Used to detect missed packets."""

    temperature = ManufacturerDataField(0x0A00, "<f")
    """Temperature as a float in degrees centigrade."""

    humidity = ManufacturerDataField(0x0A01, "<f")
    """Humidity as a float percentage."""

    pressure = ManufacturerDataField(0x0A02, "<f")
    """Pressure as a float percentage."""

    gas = ManufacturerDataField(0x0A03, "<fff", ('oxidising', 'reducing', 'nh3'))
    """Gas as (oxidising, reducing, nh3) tuple of floats in Ohms."""

    lux = ManufacturerDataField(0x0A04, "<f")
    """Brightness as a float in SI lux."""

    proximity = ManufacturerDataField(0x0A05, "<i")
    """Proximity as int in cm"""

    particulate_matter = ManufacturerDataField(0x0A06, "<HHHHHHHHHHHH", (
        'pm10-std', 'pm25-std', 'pm100-std', 'pm10-env', 'pm25-env', 'pm100-env', '03um', '05um', '10um', '25um',
        '50um', '100um'))
    """PM1.0 ug/m3 (ultrafine particles)                            
    PM2.5 ug/m3 (combustion particles, organic compounds, metals)
    PM10 ug/m3  (dust, pollen, mould spores)                
    PM1.0 ug/m3 (atmos env)                                     
    PM2.5 ug/m3 (atmos env)                                      
    PM10 ug/m3 (atmos env)                                      
    >0.3um in 0.1L air                                           
    >0.5um in 0.1L air                                            
    >1.0um in 0.1L air                                            
    >2.5um in 0.1L air                                            
    >5.0um in 0.1L air                                            
    >10um in 0.1L air"""

    def __init__(
            self, *, entry: Optional[ScanEntry] = None, sequence_number: int = 0
    ) -> None:
        super().__init__(entry=entry)
        if entry:
            return
        self.sequence_number = sequence_number

    def __str__(self) -> str:
        parts = []
        for attr in dir(self.__class__):
            attribute_instance = getattr(self.__class__, attr)
            if issubclass(attribute_instance.__class__, ManufacturerDataField):
                value = getattr(self, attr)
                if value is not None:
                    parts.append("{}={}".format(attr, str(value)))
        return "<{} {} >".format(self.__class__.__name__, " ".join(parts))

    def split(self, max_packet_size: int = 31) -> "EnviroSensorMeasurement":
        """Split the measurement into multiple measurements with the given max_packet_size. Yields
        each submeasurement."""
        current_size = 8  # baseline for mfg data and sequence number
        if current_size + len(self.manufacturer_data) < max_packet_size:
            yield self
            return

        original_data = self.manufacturer_data.data
        submeasurement = None
        for key in original_data:
            value = original_data[key]
            entry_size = 2 + len(value)
            if not submeasurement or current_size + entry_size > max_packet_size:
                if submeasurement:
                    yield submeasurement
                submeasurement = self.__class__()
                current_size = 8
            submeasurement.manufacturer_data.data[key] = value
            current_size += entry_size

        if submeasurement:
            yield submeasurement

        return
