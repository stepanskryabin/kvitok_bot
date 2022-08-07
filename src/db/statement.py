

class SqlStatement:
    CREATE_USER_LIST = '''CREATE TABLE IF NOT EXISTS UserList (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                login TEXT UNIQUE NOT NULL,
                                password TEXT NOT NULL,
                                user_information_id INTEGER);'''
    CREATE_USER_INFORMATION = '''CREATE TABLE IF NOT EXISTS UserInformation (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                subscriber TEXT NOT NULL,
                                address TEXT,
                                living_space REAL NULL,
                                total_space REAL NULL,
                                form_of_ownership TEXT,
                                phone INTEGER,
                                email TEXT,
                                registered_people INTEGER,
                                unavailable_people INTEGER,
                                indebtedness REAL,
                                fines REAL);'''
    CREATE_PAYS_HISTORY = '''CREATE TABLE IF NOT EXISTS PaysHistory (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                ouid TEXT UNIQUE NOT NULL,
                                page BLOB);'''
    CREATE_METERING_DEVICES = '''CREATE TABLE IF NOT EXISTS MeteringDevices (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                ouid TEXT UNIQUE NOT NULL,
                                page BLOB);'''

    DELETE_USER_LIST = '''DROP TABLE IF EXISTS UserList;'''
    DELETE_USER_INFORMATION = '''DROP TABLE IF EXISTS UserInformation;'''
    DELETE_PAYS_HISTORY = '''DROP TABLE IF EXISTS PaysHistory;'''
    DELETE_METERING_DEVICES = '''DROP TABLE IF EXISTS MeteringDevices;'''

    INSERT_MAIN_OBJECT = '''INSERT INTO UserList (ouid,
                                                    device,
                                                    _type,
                                                    _index,
                                                    gateway,
                                                    event,
                                                    value,
                                                    locked,
                                                    unconfigured)
                            VALUES (:ouid,
                                    :device,
                                    :_type,
                                    :_index,
                                    :gateway,
                                    :event,
                                    :value,
                                    :locked,
                                    :unconfigured);'''
    INSERT_MAIN_CONFIG = '''INSERT INTO UserInformation (ouid,
                                                    _offset,
                                                    raise_time,
                                                    fall_time,
                                                    _type,
                                                    _mode,
                                                    _order,
                                                    sacn_universe,
                                                    sacn_priority,
                                                    sacn_name,
                                                    sacn_pps,
                                                    address)
                            VALUES (:ouid,
                                    :_offset,
                                    :raise_time,
                                    :fall_time,
                                    :_type,
                                    :_mode,
                                    :_order,
                                    :sacn_universe,
                                    :sacn_priority,
                                    :sacn_name,
                                    :sacn_pps,
                                    :address);'''
    INSERT_PAYS_HISTORY = '''INSERT INTO PaysHistory (ouid,
                                       page)
                             VALUES (:ouid,
                                     :page)'''
    INSERT_METERING_DEVICES = '''INSERT INTO MeteringDevices (ouid,
                                       page)
                                 VALUES (:ouid,
                                         :page)'''

    UPDATE_USER_LIST = '''UPDATE OR FAIL UserList
                          SET device = :device,
                              _type = :_type,
                              _index = :_index,
                              gateway = :gateway,
                              event = :event,
                              value = :value,
                              locked = :locked,
                              unconfigured = :unconfigured
                          WHERE ouid = :ouid;'''
    UPDATE_USER_INFORMATION = '''UPDATE OR FAIL UserInformation
                                 SET _offset = :_offset,
                                     raise_time = :raise_time,
                                     fall_time = :fall_time,
                                     _type = :_type,
                                     _mode = :_mode,
                                     _order = :_order,
                                     sacn_universe = :sacn_universe,
                                     sacn_priority = :sacn_priority,
                                     sacn_name = :sacn_name,
                                     sacn_pps = :sacn_pps,
                                     address = :address
                                 WHERE ouid = :ouid;'''
    UPDATE_PAYS_HISTORY = '''UPDATE OR FAIL PaysHistory
                             SET page = :page
                             WHERE ouid = :ouid;'''
    UPDATE_METERING_DEVICES = '''UPDATE OR FAIL MeteringDevices
                                 SET page = :page
                                 WHERE ouid = :ouid;'''

    SELECT_USER_LIST = '''SELECT *
                          FROM UserList
                          WHERE ouid = :ouid;'''
    SELECT_USER_INFORMATION = '''SELECT *
                                 FROM UserInformation
                                 WHERE ouid = :ouid;'''
    SELECT_PAYS_HISTORY = '''SELECT *
                             FROM PaysHistory
                             WHERE ouid = :ouid;'''
    SELECT_METERING_DEVICES = '''SELECT *
                                 FROM MeteringDevices
                                 WHERE ouid = :ouid;'''
