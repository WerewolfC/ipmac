"""Types module containing data classes and constants"""

from dataclasses import dataclass, astuple

IF_TYPE = {
    0: "Wired",
    1: "Wireless"
}

COLDATA = [
    {"text": "Device", "stretch": True},
    {"text": "IP address", "stretch": True},
    {"text": "MAC address", "stretch": True},
    {"text": "IF type", "stretch": True},
]

GUI_STYLE_NAME = "sandstone"


@dataclass
class DeviceData:
    device_id: int = 0
    device_name: str = ""
    device_desc: str = ""

    def __iter__(self):
        yield from astuple(self)


@dataclass
class InterfaceData:
    if_id: int = 0
    device_name: str = ""
    ip: str = ""
    mac: str = ""
    if_type: int = 0

    def __iter__(self):
        yield from astuple(self)


default_device_data = DeviceData()
default_if_data = InterfaceData()
all_device_list = DeviceData(0, "All", "All available devices")
