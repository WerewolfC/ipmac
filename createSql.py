import pprint
import sqlite3
# from contextlib import closing
from functools import wraps

import ipmac.queries as queries


STUB_DEVICE_DATA = [
    ("1Storm", "some other pc"),
    ("2Cyclops", "Multimedia PC"),
    ("3Wolverine", "Working pC"),
]

STUB_IF_DATA = [
    (1, "192.168.0.11", "00:11:22:33:44:55:16", 0),  # Storm
    (1, "192.168.0.111", "aa:11:22:33:44:55:16", 0),  # Storm
    (1, "192.168.0.121", "aa:11:22:33:44:55:00", 0),  # Storm
    (2, "192.168.0.21", "00:11:22:33:44:55:26", 0),  # Cyclops
    (3, "192.168.0.31", "00:11:22:33:44:55:36", 0),  # Wolverine
    (3, "192.0.0.0", "00:11:22:33:44:55:36", 0),  # Wolverine

]


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


@db_operation
def create_device_table(cursor):
    cursor.execute(queries.QUERY_CREATE_DEV_TABLE)


@db_operation
def create_if_table(cursor):
    cursor.execute(queries.QUERY_CREATE_IF_TABLE)


@db_operation
def add_to_device_table(cursor, *args):
    cursor.execute(queries.QUERY_ADD_DEVICE, *args)


@db_operation
def add_to_if_table(cursor, *args):
    cursor.execute(queries.QUERY_ADD_IF, *args)


@db_operation
def read_all_interfaces(cursor):
    table_rows = cursor.execute(queries.QUERY_SELECT_ALL_IF).fetchall()
    return table_rows


@db_operation
def read_all_devices(cursor):
    table_rows = cursor.execute(queries.QUERY_SELECT_ALL_DEVICES).fetchall()
    return table_rows


@db_operation
def get_device_id(cursor, device_id=""):
    """Return the device id based on device name"""
    table_row = cursor.execute(queries.QUERY_GET_DEVICE_ID, [device_id]).fetchone()
    return table_row[0]


if __name__ == "__main__":
    # conn, cursor = connect_to_sql()
    create_device_table()
    create_if_table()
    device_list = []
    # only for testing purposes, otherwise needs to be commented
    for device_data in STUB_DEVICE_DATA:
        add_to_device_table(device_data)
        device_list.append(device_data[0])

    # zipped_data = zip(device_list, STUB_IF_DATA)
    # for item in zipped_data:
    #     add_to_if_table((item[0], *item[1]))
    for item in STUB_IF_DATA:
        print(item)
        add_to_if_table(item)
    pprint.pprint(read_all_devices())
    pprint.pprint(read_all_interfaces())
