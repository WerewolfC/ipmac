"""Data model to process SQLite data"""
import ipmac.sqlOperations as db
from ipmac.types import all_device_list, DeviceData, InterfaceData, IF_TYPE
from pprint import pprint


def return_name(e):
    return e.device_name


class SqlData:
    """Class to interract to SQLite db"""

    def __init__(self):
        self.device_list = None  # list of DeviceData obj
        # self.create_device_struct()
        self.active_device = None

    def update_data(self):
        """Get all elements from device and if tables """
        self.device_list = [all_device_list]  # list of DeviceData obj
        device_tbl_rows = db.get_all_devices()
        if_tbl_rows = db.get_all_interfaces()

        pprint(f'received from db ->> {device_tbl_rows} -->>{if_tbl_rows}')
        device_data_list = []
        for row in device_tbl_rows:
            if_list = [InterfaceData(ifx[0], ifx[1], ifx[2], ifx[3], ifx[4])
                        for ifx in if_tbl_rows if ifx[1] == row[0]]
            print(f"if_list {if_list}")
            new_device = DeviceData(row[0], row[1], row[2], if_list)
            device_data_list.append((new_device))
        self.device_list.extend(device_data_list)
        pprint(f"full data \n {self.device_list}")

    def get_if_data(self, device_obj):
        """Returns if data formated to be displayed, based on suplied device"""
        # create a list of (dev_name, ip, mac, type) extracted from InterfaceData obj list
        formated_if_list = []
        for ifx in device_obj.if_list:
            pprint(f"ifx {ifx}")
            formated_if_list.append((device_obj.device_name,
                                     ifx.ip,
                                     ifx.mac,
                                     IF_TYPE[ifx.if_type]))

        pprint(f"formated if list {formated_if_list}")
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

    def get_active_device(self):
        """Get active device object"""
        return self.active_device

    def add_device_data(self, *args):
        """Writes device data to device table"""
        formated_data = tuple(args[0])[1::]
        db.add_to_device_table(formated_data)

    def delete_device_data(self, device_obj):
        """Writes device data to device table"""
        db.delete_from_device_table(device_obj.device_id)

    def update_device_data(self, *args):
        """Update device data to device table"""
        pprint(f"update formated data {args}")
        id, name, desc = args[0]
        formated_data = (name, desc, id)
        pprint(f"update formated data {id} {name} {desc}")
        db.update_device_table(formated_data)

    def is_device_present(self, device_name):
        """Search for specified device name in a list of Device obj"""
        device_name_list = [return_name(dev_obj) for dev_obj in self.device_list]
        pprint(f"searched dev name list {device_name_list}")
        return device_name in device_name_list


# from this down to be refactored
    def get_if_struct(self, cursor):
        """Get all elements from interface table """
        table_rows = cursor.execute(queries.QUERY_SELECT_ALL_IF).fetchall()
        return table_rows

    
    def add_if_data(self, cursor, *args):
        """Writes if data to interface table"""
        cursor.execute(queries.QUERY_ADD_IF, *args)

    
    def remove_if_data(self, if_id):
        """Writes if data to if table"""
        pass

    
    def update_if_data(self, new_if_data):
        """Update if data to interface table"""
        pass

    
    def search_in_db(self):
        """Search in SQLite db"""
        pass
