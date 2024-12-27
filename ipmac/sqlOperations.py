"""SQLite actions"""

import sqlite3
from functools import wraps

import ipmac.queries as queries


def db_operation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(queries.DATA_DB_FILE)
        cursor = conn.cursor()
        f_ret = func(cursor, *args, **kwargs)
        conn.commit()
        conn.close()
        return f_ret
    return wrapper


@db_operation
def add_to_device_table(cursor, *args):
    cursor.execute(queries.QUERY_ADD_DEVICE, *args)


@db_operation
def add_to_if_table(cursor, *args):
    cursor.execute(queries.QUERY_ADD_IF, *args)


@db_operation
def get_all_interfaces(cursor):
    table_rows = cursor.execute(queries.QUERY_SELECT_ALL_IF).fetchall()
    return table_rows


@db_operation
def get_all_devices(cursor):
    table_rows = cursor.execute(queries.QUERY_SELECT_ALL_DEVICES).fetchall()
    return table_rows


@db_operation
def get_device_id(cursor, device_id=""):
    """Return the device id based on device name"""
    table_row = cursor.execute(queries.QUERY_GET_DEVICE_ID, [device_id]).fetchone()
    return table_row[0]


@db_operation
def delete_from_device_table(cursor, device_id):
    """Deletes from device table based on suplied idx"""
    cursor.execute(queries.QUERY_DELETE_DEVICE, [device_id])


@db_operation
def update_device_table(cursor, *args):
    """Update device table based on suplied idx"""
    cursor.execute(queries.QUERY_UPDATE_DEVICE, *args)
