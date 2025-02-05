"""Data model to process SQLite data"""
import ipmac.sqlOperations as db
from ipmac.types import all_device_list, DeviceData, InterfaceData, IF_TYPE, \
    DeviceNameNotFoundError, IfIdNotFoundError
from pprint import pprint


def return_name(e):
    return e.device_name


class SqlData:
    """Class to interract to SQLite db"""

    def __init__(self):
        self.device_list = None  # list of DeviceData obj
        self.active_device = None
        self.selected_if_list = None

    def update_data(self):
        # """Get all elements from device and if tables """
        # self.active_device = None
        # self.selected_if_list = None
        self.device_list = [all_device_list]  # list of DeviceData obj
        device_tbl_rows = db.get_all_devices()
        if_tbl_rows = db.get_all_interfaces()

        device_data_list = []
        for row in device_tbl_rows:
            if_list = [InterfaceData(ifx[0], ifx[1], ifx[2], ifx[3], ifx[4])
                        for ifx in if_tbl_rows if ifx[1] == row[0]]
            new_device = DeviceData(row[0], row[1], row[2], if_list)
            device_data_list.append((new_device))
        self.device_list.extend(device_data_list)
        pprint("++++++++++++Update ALL DATA +++++++++++++")
        pprint(f"Device_list : {self.device_list}")
        pprint(f"Active_device : {self.active_device}")
        pprint(f"Selected_if_list : {self.selected_if_list}")

    def get_if_data(self, device_obj):
        """Returns if data formated to be displayed, based on suplied device"""
        # create a list of (dev_name, ip, mac, type) extracted from InterfaceData obj list
        formated_if_list = []
        for ifx in device_obj.if_list:
            formated_if_list.append((device_obj.device_name,
                                     ifx.ip,
                                     ifx.mac,
                                     IF_TYPE[ifx.if_type]))
        return formated_if_list

    def get_all_if_data(self):
        """Returns all IF data formated"""
        # for all devices group interfaces in a list
        if_list = []
        for device in self.device_list[1::]:
            if_list.extend(self.get_if_data(device))
        # return [self.get_if_data(device) for device in self.device_list[1::]]
        return if_list

    def get_devices(self):
        """Returns a list of (dev_id, device_name)"""
        device_list_tuple = []
        for device in self.device_list:
            device_list_tuple.append((device.device_id, device.device_name))
        return device_list_tuple

    def update_active_device(self, active_id):
        """Update active device based on info from presenter"""
        self.active_device = [dev for dev in self.device_list if dev.device_id == active_id][0]

    def get_device_id(self, device_name=""):
        """"Search for device_id bases on device name in self.device_list

        Returns device id
        """

        for device in self.device_list:
            if device.device_name == device_name:
                return device.device_id
        raise DeviceNameNotFoundError(f"Device name {device_name} not found ")

    def get_if_id(self, if_obj):
        """Searches for an if_id based on the if_object provided

        Search is done in self.device_list
        Return: if_id
        """
        for device in [dev for dev in self.device_list if dev.device_id == if_obj.device_id]:
            for existing_if in device.if_list:
                # print(f"{existing_if}")
                # print(f"type {type(existing_if)}, and values {existing_if}")
                if if_obj.device_id == existing_if.device_id \
                    and if_obj.ip == existing_if.ip \
                    and if_obj.mac == existing_if.mac \
                    and if_obj.if_type == existing_if.if_type :
                    return existing_if.if_id
            else:
                raise IfIdNotFoundError(f"interface id {if_obj.device_id} not found")

    def update_selected_if_list(self, if_data):
        """ Updates the selected interface based on if_id

        Based on if_data, the if_id is retrieved from self.device_list,
        and using device_id, ip, mac, type
        if_data = list of InterfaceData() objects
        """
        self.selected_if_list = []
        # for every selected interface, add corresponding if_id
        # then search that obj in entire device_list and when found
        # add interface obj into # self.selected_if_list
        for interface in if_data:
            interface.if_id = self.get_if_id(interface)

            for device in [dev for dev in self.device_list if dev.device_id == interface.device_id]:
                # Correct device was found, proceed to check interface
                if interface in device.if_list:
                    self.selected_if_list.append(interface)

    def get_active_device(self):
        """Get active device object"""
        return self.active_device

    def add_device_data(self, *args):
        """Writes device data to device table"""
        formated_data = tuple(args[0])[1:-1]
        db.add_to_device_table(formated_data)

    def delete_device_data(self, device_obj):
        """Delete device data from device table"""
        db.delete_from_device_table(device_obj.device_id)

    def delete_if_data(self, if_obj_list):
        """Deletes interfaces from interface table"""
        for if_id in [interface.if_id for interface in if_obj_list]:
            db.delete_from_if_table(if_id)

    def update_device_data(self, *args):
        """Update device data to device table"""
        formated_data = (args[0].device_name,
                         args[0].device_desc,
                         args[0].device_id)
        db.update_device_table(formated_data)

    def is_device_present(self, device_name):
        """Search for specified device name in a list of Device obj"""
        device_name_list = [return_name(dev_obj) for dev_obj in self.device_list]
        return device_name in device_name_list

    def add_if_data(self, *args):
        """Writes if data to interface table"""
        db.add_to_if_table(tuple(args[0])[1::])

    def get_selected_if_list(self):
        """Get selected if object"""
        return self.selected_if_list

# from this down to be refactored

    def search_in_db(self):
        """Search in SQLite db"""
        pass
