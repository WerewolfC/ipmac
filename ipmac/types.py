"""Types module containing data classes and constants"""

from dataclasses import dataclass, astuple, field

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
class InterfaceData:
    if_id: int = 0
    device_id: int = 0
    ip: str = ""
    mac: str = ""
    if_type: int = 0

    def __iter__(self):
        yield from astuple(self)


@dataclass
class DeviceData:
    device_id: int = 0
    device_name: str = ""
    device_desc: str = ""
    if_list: list[InterfaceData] = field(default_factory=list)

    def __iter__(self):
        yield from astuple(self)


default_device_data = DeviceData()
default_if_data = InterfaceData()
all_device_list = DeviceData(0, "All", "All available devices")
