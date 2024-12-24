"""Types module containing data classes and constants"""

from dataclasses import dataclass

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

GUI_STYLE_NAME = "yeti"


@dataclass
class DeviceData:
    device_name: str = ""
    device_desc: str = ""


@dataclass
class InterfaceData:
    device_name: str = ""
    ip: str = ""
    mac: str = ""
    if_type: int = 0


default_device_data = DeviceData()
default_if_data = InterfaceData()

stub_device_data = DeviceData("Wolverine", "Some really long description")
stub_if_data = InterfaceData(
    "Wolverine",
    "192.168.0.1",
    "aa:bb:cc:dd:ee:ff",
    0
)
