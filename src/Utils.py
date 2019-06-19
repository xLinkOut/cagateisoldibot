# -*- coding: utf-8 -*-
import sqlite3, datetime, calendar, Settings

# Execute a generic SQL query
def executeQuery(query, args):
    DB = sqlite3.connect(Settings.DATABASE)
    Cursor = DB.cursor()
    Cursor.execute(query,args)
    DB.commit()
    DB.close()

# Get START_MSG_ID from GROUPS table
def getMessageID(group_id):
    DB = sqlite3.connect(Settings.DATABASE)
    Cursor = DB.cursor()
    results = Cursor.execute("SELECT START_MSG_ID FROM GROUPS WHERE GROUP_ID=?",[group_id]).fetchone()
    DB.close()
    if results and len(results) > 0:
        return results[0]
    else:
        return None

# Get Admin Telegram ID from GROUPS table
def getAdminID(group_id):
    DB = sqlite3.connect(Settings.DATABASE)
    Cursor = DB.cursor()
    results = Cursor.execute("SELECT ADMIN_ID FROM GROUPS WHERE GROUP_ID=?",[group_id]).fetchone()
    DB.close()
    if results and len(results) > 0:
        return int(results[0])
    else:
        return None

# Get user data from DB by groupID and chatID
def getUser(group_id,chat_id):
    DB = sqlite3.connect(Settings.DATABASE)
    Cursor = DB.cursor()
    result = Cursor.execute("SELECT CHAT_ID,USERNAME,FIRST_NAME FROM USERS WHERE GROUP_ID=? AND CHAT_ID=?",[group_id,chat_id]).fetchone()
    DB.close()
    if result and len(result) > 0:
        return list(result)
        # List format:
        #   [0] = ChatID
        #   [1] = Username
        #   [2] = First name
    else:
        return None

# Get all user that joined a group from DB by groupID
def getAllUsers(group_id):
    DB = sqlite3.connect(Settings.DATABASE)
    Cursor = DB.cursor()
    results = Cursor.execute("SELECT CHAT_ID,USERNAME,FIRST_NAME FROM USERS WHERE GROUP_ID=?",[group_id]).fetchall()
    DB.close()
    if results and len(results) > 0:
        return results
    else:
        return None    

# Return a list with name of users in a group
def listNetflixers(group_id):
    DB = sqlite3.connect(Settings.DATABASE)
    Cursor = DB.cursor()    
    results = Cursor.execute("SELECT FIRST_NAME FROM USERS WHERE GROUP_ID=? ORDER BY FIRST_NAME",[group_id]).fetchall()
    DB.close()
    if results and len(results) > 0:
        lista = []
        for row in results:
            lista.append(row[0])
        return lista
    else:
        return []

# Return (as int) the number of users that joined a group
def countNetflixers(group_id):
    DB = sqlite3.connect(Settings.DATABASE)
    Cursor = DB.cursor()    
    results = int(Cursor.execute("SELECT NETFLIXERS FROM GROUPS WHERE GROUP_ID=?",[group_id]).fetchone()[0])
    DB.close()
    return results

# Return true if a group is already registered into db, false otherwise
def groupAlreadyExists(group_id):
    DB = sqlite3.connect(Settings.DATABASE)
    Cursor = DB.cursor()
    results = Cursor.execute("SELECT * FROM GROUPS WHERE GROUP_ID=?",[group_id]).fetchone()
    DB.close()
    if results and len(results) > 0:
        return True
    else:
        return False

# Return the payment's status of a specific user on a specific date
def getStatus(group_id,expiration,chat_id):
    DB = sqlite3.connect(Settings.DATABASE)
    Cursor = DB.cursor()
    results = Cursor.execute("SELECT STATUS FROM PAYMENTS WHERE EXPIRATION=? AND GROUP_ID=? AND CHAT_ID=?",[expiration,group_id,chat_id]).fetchone()
    DB.close()
    return results[0]

# Return a list with all the payments status for each user on a specific date
def getAllStatus(group_id,expiration):
    DB = sqlite3.connect(Settings.DATABASE)
    Cursor = DB.cursor()
    results = Cursor.execute("SELECT STATUS FROM PAYMENTS WHERE GROUP_ID=? AND EXPIRATION=?",[group_id,expiration]).fetchall()
    DB.close()
    status = []
    for stat in results:
        status.append(stat[0])
    return status

# Return the expiration date of a specified group in the format YYYY-MM-DD
def getExpiration(group_id):
    DB = sqlite3.connect(Settings.DATABASE)
    Cursor = DB.cursor()
    results = Cursor.execute("SELECT EXPIRATION FROM GROUPS WHERE GROUP_ID=?",[group_id]).fetchone()
    DB.close()
    return "{}-{}-{}".format(datetime.datetime.now().year,datetime.datetime.now().month,results[0])

# Save the trigger into db
def saveTrigger(trigger_id,group_id,data):
    DB = sqlite3.connect(Settings.DATABASE)
    Cursor = DB.cursor()
    Cursor.execute("INSERT INTO TRIGGER VALUES(?,?,?)",[trigger_id,group_id,data])
    DB.commit()
    DB.close()

# Return a list with all the triggers saved into db
def getTriggers():
    DB = sqlite3.connect(Settings.DATABASE)
    Cursor = DB.cursor()
    results = Cursor.execute("SELECT * FROM TRIGGER").fetchall()
    DB.close()
    return results

# Return the trigger ID for a specified group
def getTriggerID(group_id):
    DB = sqlite3.connect(Settings.DATABASE)
    Cursor = DB.cursor()
    results = Cursor.execute("SELECT TRIGGER_ID FROM TRIGGER WHERE GROUP_ID=?",[group_id]).fetchone()
    DB.close()
    if results and len(results) > 0:
        return results[0]
    else:
        return None

# Return amount of money for each user 
# :TODO Improve this function, that's too bad
def moneyEach(group_id):
    n = countNetflixers(group_id)
    if n == 4:
        return "3.50"
    elif n == 3:
        return "4.50"
    elif n == 2:
        return "6"
    else:
        return "8"

# Return next expiration date in string and explicit form
def newExpiration(sourcedate,months=1):
    # https://stackoverflow.com/questions/4130922/how-to-increment-datetime-by-custom-months-in-python-without-using-library
    sourcedate = datetime.datetime.strptime(sourcedate,'%Y-%m-%d')
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    months = ["Gennaio","Febbraio","Marzo","Aprile","Maggio","Giugno","Luglio","Agosto","Settembre","Ottobre","Novembre","Dicembre"]
    return "{} {} {}".format(day,months[month-1],year)
    #return datetime.datetime.strftime(datetime.date(year,month,day),'%Y-%m-%d')

def newPayment(expiration,group_id,user):
    try:
        executeQuery("INSERT INTO PAYMENTS VALUES(?,?,?,?,?)",[expiration,group_id,user[0],user[2],0])
    except sqlite3.IntegrityError as e:
        print(e)


# Debug function that reset payment status when admin send 'pay' msg, here just to fire trigger job with a message)
def __resetPayments(group_id,bot):
    import Keyboards
    import Statements
    results = executeQuery("SELECT * FROM PAYMENTS WHERE GROUP_ID=? AND EXPIRATION=?",[group_id,getExpiration(group_id)])    
    n_p = countNetflixers(group_id)
    status = []
    for i in range(0,n_p):
        status.append(0)
    if results:
        executeQuery("UPDATE PAYMENTS SET STATUS=0 WHERE GROUP_ID=? AND EXPIRATION=?",[group_id,getExpiration(group_id)])
        bot.send_message(group_id,Statements.IT.TimeToPay.replace('$$',moneyEach(group_id)),reply_markup=Keyboards.buildKeyboardForPayment(group_id,status),parse_mode='markdown')
    else:
        expiration = getExpiration(group_id)
        for user in getAllUsers(group_id):
            try:
                executeQuery("INSERT INTO PAYMENTS VALUES(?,?,?,?,?)",[expiration,group_id,user[0],user[2],0])
            except sqlite3.IntegrityError:
                pass
        bot.send_message(group_id,Statements.IT.TimeToPay.replace('$$',moneyEach(group_id)),reply_markup=Keyboards.buildKeyboardForPayment(group_id,[0,0,0,0]),parse_mode='markdown')