"""Data model to process SQLite data"""
import ipmac.sqlOperations as db
from ipmac.types import all_device_list, DeviceData, InterfaceData, IF_TYPE, \
    DeviceNameNotFoundError, IfIdNotFoundError

def return_name(e):
    return e.device_name


class SqlData:
    """Class to interract to SQLite db"""

    def __init__(self):
        self.device_list = None  # list of DeviceData obj
        self.active_device = None
        self.selected_if_list = None
        self.querry_results = None  # list of tuples (dev_name, [if_obj]) matching results

    def get_devices(self):
        """Returns a list of (dev_id, device_name)"""
        device_list_tuple = []
        for device in self.device_list:
            device_list_tuple.append((device.device_id, device.device_name))
        return device_list_tuple

    def get_device_id(self, device_name=""):
        """"Search for device_id bases on device name in self.device_list
        Returns device id
        """
        for device in self.device_list:
            if device.device_name == device_name:
                return device.device_id
        raise DeviceNameNotFoundError(f"Device name {device_name} not found ")

    def get_active_device(self):
        """Get active device object"""
        return self.active_device

    @staticmethod
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

    def get_if_data(self, device_obj):
        """Returns if data formated to be displayed, based on suplied device"""
        # returns a list of (dev_name, ip, mac, type) extracted from InterfaceData obj list
        return self.format_dev_if_list(device_obj.device_name, device_obj.if_list)

    def get_all_if_data(self):
        """Returns all IF data formated"""
        # for all devices group interfaces in a list
        if_list = []
        for device in self.device_list[1::]:
            if_list.extend(self.get_if_data(device))
        return if_list

    def get_if_id(self, if_obj):
        """Searches for an if_id based on the if_object provided
        Search is done in self.device_list
        Return: if_id
        """
        for device in [dev for dev in self.device_list if dev.device_id == if_obj.device_id]:
            for existing_if in device.if_list:
                if if_obj.device_id == existing_if.device_id \
                    and if_obj.ip == existing_if.ip \
                    and if_obj.mac == existing_if.mac \
                    and if_obj.if_type == existing_if.if_type :
                    return existing_if.if_id
        raise IfIdNotFoundError(f"interface id {if_obj.device_id} not found")

    def get_selected_if_list(self):
        """Get selected if object"""
        return self.selected_if_list

    def get_selected_ip_list(self):
        """Returns list of selected IPs """
        return [iface.ip for iface in self.selected_if_list]

    def get_selected_mac_list(self):
        """Returns list of selected MACs """
        return [iface.mac for iface in self.selected_if_list]

    def add_device_data(self, *args):
        """Writes device data to device table"""
        formated_data = tuple(args[0])[1:-1]
        db.add_to_device_table(formated_data)

    def add_if_data(self, *args):
        """Writes if data to interface table"""
        db.add_to_if_table(tuple(args[0])[1::])

    def delete_device_data(self, device_obj):
        """Delete device data from device table"""
        db.delete_from_device_table(device_obj.device_id)

    def delete_if_data(self, if_obj_list):
        """Deletes interfaces from interface table"""
        if if_obj_list:
            for if_id in [interface.if_id for interface in if_obj_list]:
                db.delete_from_if_table(if_id)

    def update_data(self):
        """Get all elements from device and if tables """
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

    def update_active_device(self, active_id):
        """Update active device based on info from presenter"""

        self.active_device = [dev for dev in self.device_list if dev.device_id == active_id][0]

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

    def export_to_csv(self):
        """Export DB to csv file"""
        print("Export")

    def import_from_csv(self):
        """Import from csv file"""
        print("Import")

    @staticmethod
    def is_match(searched_str, data_str):
        """Returns True if the data_string mathches search_string"""
        return searched_str.lower() in data_str.lower()

    def search(self, search_str):
        """Search in self.device_list and saves a list of tuples (dev_name, interface_list)
        that match the searched string and returns number of found items
        """
        self.querry_results = []
        found_count = 0
        for device in self.device_list[1:]:
            # If device name or device description matches string, add all interfaces
            if self.is_match(search_str, device.device_name) \
                or self.is_match(search_str, device.device_desc):
                self.querry_results.append((device.device_name, device.if_list))
                found_count += len(device.if_list)
                continue
            else:
                # if device data does not match, search in device if list
                if_list = []
                for device_if in device.if_list:
                    if self.is_match(search_str, device_if.ip) \
                        or self.is_match(search_str, device_if.mac) \
                        or self.is_match(search_str, IF_TYPE[device_if.if_type]):
                        if_list.append(device_if)
                        found_count += 1
                # if search_str found in interfaces add dev_name and if_list to results
                if if_list :
                    self.querry_results.append((device.device_name, if_list))
        return found_count

    def get_formated_results(self):
        """Returns full list of formated interface data to be displayed on GUI"""
        full_formated_list = []
        for dev_name, if_list in self.querry_results:
            full_formated_list.extend(self.format_dev_if_list(dev_name, if_list))

        return full_formated_list
