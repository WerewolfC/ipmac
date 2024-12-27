"""SQLite queries module"""

DATA_DB_FILE = "data/ipmacData.db"

QUERY_CREATE_DEV_TABLE = """CREATE TABLE IF NOT EXISTS tbl_devices
                 (device_id INTEGER NOT NULL PRIMARY KEY,
                 device_name TEXT UNIQUE,
                 device_desc TEXT);"""

QUERY_CREATE_IF_TABLE = """CREATE TABLE IF NOT EXISTS tbl_interfaces
                 (if_id INTEGER NOT NULL PRIMARY KEY,
                 device_id INTEGER,
                 ip TEXT,
                 mac TEXT,
                 if_type INTEGER);"""

QUERY_ADD_DEVICE = "INSERT INTO tbl_devices (device_name, device_desc) VALUES (?, ?);"
QUERY_ADD_IF = "INSERT INTO tbl_interfaces (device_id, ip, mac, if_type) VALUES (?, ?, ?, ?);"

QUERY_SELECT_ALL_IF = "SELECT * FROM tbl_interfaces"
QUERY_SELECT_ALL_DEVICES = "SELECT * FROM tbl_devices"

QUERY_GET_DEVICE_ID = "SELECT device_id FROM tbl_devices WHERE device_name = ?;"

QUERY_DELETE_DEVICE = "DELETE FROM tbl_devices WHERE device_id = ?"

QUERY_UPDATE_DEVICE = """UPDATE tbl_devices
                         SET device_name = ?,
                            device_desc = ?
                         WHERE device_id = ?;"""
