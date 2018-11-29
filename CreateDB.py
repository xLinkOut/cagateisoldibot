# -*- coding: utf-8 -*-
import sqlite3, os, Settings

# Delete old db and create new one
if(os.path.isfile(Settings.DatabaseFile)):
    os.remove(Settings.DatabaseFile)

# Create a connection to the db file (filaname saved into Settings.py)
DB = sqlite3.connect(Settings.DatabaseFile)
# Create a cursor to interact with db
Cursor = DB.cursor()

# Create a table named GROUP that contain general information about groups
# +--------------+---------+-----------------------------+---------------------------------------------------+
# | GROUP_ID     | INT(50) | NOT NULL PRIMARY KEY UNIQUE | Telegram Group's ID                               |
# | START_MSG_ID | INT(20) | DEFAULT NULL                | First setup message's ID                          |
# | NETFLIXERS   | INT(1)  | NOT NULL DEFAULT 0          | Number of Netflix's users                         |
# | EXPIRATION   | INT(2)  | DEFAULT NULL                | Day of the month when subscription will be renewd |
# | ADMIN_ID     | INT(2)  | NOT NULL                    | Telegram Admin's ID                               |
# +--------------+---------+-----------------------------+---------------------------------------------------+

Cursor.execute("CREATE TABLE GROUPS ("
                 "GROUP_ID INT(50) PRIMARY KEY NOT NULL UNIQUE,"
                 "START_MSG_ID INT(20) DEFAULT NULL,"
                 "NETFLIXERS INT(1) NOT NULL DEFAULT 0,"
                 "EXPIRATION INT(2) NULL,"
                 "ADMIN_ID INT(50) NOT NULL"
                ")")