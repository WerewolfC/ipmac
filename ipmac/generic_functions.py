"""Module containing Generic functions"""
import re
from ipmac.types import IF_TYPE


def return_name(e):
    return e.device_name

def format_dev_if_list(dev_name, if_list):
    """Returns a formated if list in order to be displayed on GUI"""
    formated_if_list = []
    # create a list of (dev_name, ip, mac, type) extracted from InterfaceData obj list
    for ifx in if_list:
        formated_if_list.append((dev_name,
                                    ifx.ip,
                                    ifx.mac,
                                    IF_TYPE[ifx.if_type]))
    return formated_if_list


def is_match(searched_str, data_str):
    """Returns True if the data_string mathches search_string"""
    return searched_str.lower() in data_str.lower()


def check_device_name(dev_name):
    """Validate device name
    Rules:
        -not empty
        -alphanumeric [0..9][aA..ZA]
    """
    valid_pattern = r"^[a-zA-Z0-9]+$"
    return bool(re.match(valid_pattern, dev_name))


def check_ip_address(ip_name):
    """Validate IP address
    Rules:
        - max len 15
        - digits only
        - 3 dots
    """
    valid_pattern = r"^(\d{1,3}[.]){3}(\d{1,3})$"
    return bool(re.match(valid_pattern, ip_name))


def check_mac_address(mac_name):
    """Validate MAC address
    Rules:
        - max len 17
        - HEXA only
        - 5 column char
    """
    valid_pattern = r"^([0-9A-F]{2}[:]){5}([0-9A-F]{2})$"
    return bool(re.match(valid_pattern, mac_name.upper()))
