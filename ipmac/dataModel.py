"""Data model to process SQLite data"""
import ipmac.sqlOperations as db
from ipmac.types import all_device_list, DeviceData, InterfaceData


def return_name(e):
    return e.device_name


class SqlData:
    """Class to interract to SQLite db"""

    def __init__(self):
        self.device_list = None  # list of DeviceData obj
        # self.create_device_struct()
        self.active_device = None

    def create_device_struct(self):
        """Get all elements from device table """
        self.device_list = [all_device_list]  # list of DeviceData obj
        table_rows = db.get_all_devices()
        print(f'received from db \n {table_rows}')
        device_data_list = []
        for row in table_rows:
            new_device = DeviceData(row[0], row[1], row[2])
            device_data_list.append((new_device))
        print(f'ordered structure{device_data_list}')
        self.device_list.extend(device_data_list)

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
        print(f"update formated data {args}")
        id, name, desc = args[0]
        formated_data = (name, desc, id)
        print(f"update formated data {id} {name} {desc}")
        db.update_device_table(formated_data)

    def is_device_present(self, device_name):
        """Search for specified device name in a list of Device obj"""
        device_name_list = [return_name(dev_obj) for dev_obj in self.device_list]
        print(f"searched dev name list {device_name_list}")
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
