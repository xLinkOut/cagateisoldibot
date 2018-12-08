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
# | GROUP_ID     | INT(50) | NOT NULL PRIMARY KEY UNIQUE | Telegram group's ID                               |
# | START_MSG_ID | INT(20) | DEFAULT NULL                | First setup message's ID                          |
# | NETFLIXERS   | INT(1)  | NOT NULL DEFAULT 0          | Number of Netflix's users                         |
# | EXPIRATION   | INT(2)  | DEFAULT NULL                | Day of the month when subscription will be renewd |
# | ADMIN_ID     | INT(2)  | NOT NULL                    | Telegram admin's ID                               |
# +--------------+---------+-----------------------------+---------------------------------------------------+
Cursor.execute("CREATE TABLE GROUPS ("
                 "GROUP_ID INT(50) PRIMARY KEY NOT NULL UNIQUE,"
                 "START_MSG_ID INT(20) DEFAULT NULL,"
                 "NETFLIXERS INT(1) NOT NULL DEFAULT 0,"
                 "EXPIRATION INT(2) NULL,"
                 "ADMIN_ID INT(50) NOT NULL"
                ")")

# Create a table named USERS that contain information about each user for each group
# +------------+-----------+--------------------+--------------------------+
# | GROUP_ID   | INT(50)   | NOT NULL           | Telegram group's ID      |
# | CHAT_ID    | INT(50)   | PRIMARY KEY        | Telegram user's ID       |
# | USERNAME   | TEXT(255) | DEFAULT NULL       | User's Telegram username |
# | FIRST_NAME | TEXT(255) | DEFAULT NULL       | User's first name        |
# +------------+-----------+--------------------+--------------------------+
Cursor.execute("CREATE TABLE USERS ("
                 "GROUP_ID INT(50) NOT NULL,"
                 "CHAT_ID INT(50) NOT NULL,"
                 "USERNAME TEXT(255) DEFAULT NULL,"
                 "FIRST_NAME TEXT(255) DEFAULT NULL,"
                 "PRIMARY KEY (GROUP_ID,CHAT_ID)"
                ")")

# Create a table named PAYMENTS that contain information about payment for each user for each group
# +------------+-----------+----------------------+----------------------------------------------------------------+
# | EXPIRATION | DATE      | NOT NULL PRIMARY KEY | Subscription's expiration date                                 |
# | GROUP_ID   | INT(50)   | NOT NULL PRIMARY KEY | Telegram group's ID                                            |
# | FIRST_NAME | TEXT(255) | DEFAULT NULL         | User's first name                                              |
# | STATUS     | INT(1)    | NOT NULL DEFAULT 0   | Payment status: 0=Not payed; 1=Payed; -1=Wait for confirmation |
# +------------+-----------+----------------------+----------------------------------------------------------------+
Cursor.execute("CREATE TABLE PAYMENTS("
                 "EXPIRATION DATE NOT NULL,"
                 "GROUP_ID INT(50) NOT NULL,"
                 "FIRST_NAME TEXT(255) NOT NULL,"
                 "STATUS INT(1) NOT NULL DEFAULT 0,"
                 "PRIMARY KEY (EXPIRATION,FIRST_NAME)"
                ")")

# Create a table named PAYMENTS that contain information about payment notification's trigger
# +---------------+------------+-----------------------+-----------------------------------------------------+
# | TRIGGER_ID    | TEXT(255)  | NOT NULL PRIMARY KEY  | Trigger ID                                          |
# | GROUP_ID      | INT(50)    | NOT NULL              | Telegram group's ID                                 |
# | EXPIRATION    | INT(2)     | DEFAULT NULL          | Day of the month when subscription will be renewd | |
# +---------------+------------+-----------------------+-----------------------------------------------------+
Cursor.execute("CREATE TABLE TRIGGER("
                "TRIGGER_ID TEXT(255) NOT NULL PRIMARY KEY,"
                "GROUP_ID INT(50) NOT NULL,"
                "EXPIRATION INT(2) NOT NULL"
                ")")

# Write changes in db file
DB.commit()
# Close connection with db
DB.close()
# Print successful message and exit
print("Database created!")
