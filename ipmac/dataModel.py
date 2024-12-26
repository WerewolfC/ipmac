"""Data model to interract with SQLite"""

from functools import wraps
import sqlite3

import ipmac.queries as queries


def db_operation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(queries.DATA_DB_FILE)
        # conn = sqlite3.connect("ipmacData.db")
        cursor = conn.cursor()
        f_ret = func(cursor, *args, **kwargs)
        conn.commit()
        conn.close()
        return f_ret
    return wrapper


class sqlData:
    """Class to interract to SQLite db"""

    def __init__():
        pass

    def get_device_struct(self):
        """Get all elements from device table """
        pass

    def add_device_data(self, device_data):
        """Writes device data to device table"""
        pass

    def remove_device_data(self, device_id):
        """Writes device data to device table"""
        pass

    def update_device_data(self, new_device_data):
        """Update device data to device table"""
        pass

    def get_if_struct(self):
        """Get all elements from interface table """
        pass

    def add_if_data(self, if_data):
        """Writes if data to interface table"""
        pass

    def remove_if_data(self, if_id):
        """Writes if data to if table"""
        pass

    def update_if_data(self, new_if_data):
        """Update if data to interface table"""
        pass

    def search_in_db(self):
        """Search in SQLite db"""
        pass
