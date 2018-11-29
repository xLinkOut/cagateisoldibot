# -*- coding: utf-8 -*-
import telebot, logging, os
import Settings, Statements, Keyboards, Utils

from time import strftime as current_date
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

# Check for database file
if not (os.path.isfile(Settings.DatabaseFile)):
    print('Database not found!')
    exit(-1)

# Check for token
if Settings.API_TOKEN == '':
    print('Token not valid!')
    exit(-1)

# Create a logger, then set its level to DEBUG (alternatively, INFO)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
# Create bot obj with token in settings file
bot = telebot.TeleBot(Settings.API_TOKEN)

# Notify group when is time to pay!
def paymentNotify(group_id):
    # (debug that reset payment status when admin send 'pay' msg, here just to fire trigger job with a message)
    # DEBUG, delete...
    DB = sqlite3.connect(Settings.DatabaseFile)
    Cursor = DB.cursor()
    results = Cursor.execute("SELECT * FROM PAYMENTS WHERE GROUP_ID=? AND EXPIRATION=?",[group_id,Utils.getExpiration(group_id)]).fetchall()
    DB.close()
    n_p = Utils.countNetflixers(group_id)
    status = []
    for i in range(0,n_p):
        status.append(0)
    if results:
        Utils.executeQuery("UPDATE PAYMENTS SET STATUS=0 WHERE GROUP_ID=? AND EXPIRATION=?",[group_id,Utils.getExpiration(group_id)])
        bot.send_message(group_id,Statements.IT.TimeToPay.replace('$$',Utils.calcolaSoldi(group_id)),reply_markup=Keyboards.buildKeyboardForPayment(Utils.listNetflixers(group_id),status),parse_mode='markdown')
    else:
        ## until here.
        for user in Utils.listNetflixers(group_id):
            Utils.executeQuery("INSERT INTO PAYMENTS VALUES(?,?,?,?)",[Utils.getExpiration(group_id),group_id,user,0])
        bot.send_message(group_id,Statements.IT.TimeToPay.replace('$$',Utils.calcolaSoldi(group_id)),reply_markup=Keyboards.buildKeyboardForPayment(Utils.listNetflixers(group_id),status),parse_mode='markdown')

# APScheduler background object
scheduler = BackgroundScheduler()
# List of all scheduled job
jobScheduledList = []
# Get trigger from db and load into memory
results = Utils.getTrigger()
for trigger in results:
    jobScheduledList.append(scheduler.add_job(paymentNotify,CronTrigger('*','*',trigger[2],hour=8,minute=00),[trigger[1]]))
# Start the scheduler
scheduler.start()

# Bot added in a group (also during group's creation)
@bot.message_handler(content_types=['group_chat_created','new_chat_members'])
def added_in_a_group(message):
    # If the member added is the bot itself
    if int(message.new_chat_member.id) == int(bot.get_me().id):
        # Send start message, with start keyboard and save the message id into database
        msg_id = bot.send_message(message.chat.id,Statements.IT.Start.replace('$$',message.from_user.first_name),reply_markup=Keyboards.Start,parse_mode='markdown').message_id
        # Create an half-empty record for the new group
        Utils.executeQuery("INSERT INTO GROUPS(GROUP_ID,START_MSG_ID,ADMIN_ID) VALUES(?,?,?)",[message.chat.id,msg_id,message.from_user.id])

# Received start command
@bot.message_handler(commands=['start'])
def start(message):
    # If is a group chat
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        # If the group not already exists in db
        if not Utils.groupAlreadyExists(message.chat.id):
            # Send start message, with start keyboard and save the message id into database
            msg_id = bot.send_message(message.chat.id,Statements.IT.Start.replace('$$',message.from_user.first_name),reply_markup=Keyboards.Start,parse_mode='markdown').message_id
            # Create an half-empty record for the new group            
            Utils.executeQuery("INSERT INTO GROUPS(GROUP_ID,START_MSG_ID,ADMIN_ID) VALUES(?,?,?)",[message.chat.id,msg_id,message.from_user.id])
        else:
            # If START_MSG_ID == -1 then the group was already configured
            if Utils.getMessageID(message.chat.id) == -1:
                bot.send_message(message.chat.id,Statements.IT.AlreadyConfigured,reply_markup=Keyboards.Reset,parse_mode='markdown')
            else:
                # Reply to the first start message
                bot.send_message(message.chat.id,Statements.IT.UseThis,reply_to_message_id=Utils.getMessageID(message.chat.id),parse_mode='markdown',reply_markup=Keyboards.Reset)
    # Else if is a private chat
    elif message.chat.type == 'private':
        bot.send_message(message.chat.id,Statements.IT.AddMeInAGroup,parse_mode='markdown')

# User that tap on 'I Use Netflix' button and join the bot
@bot.callback_query_handler(func=lambda call: call.data == 'iusenetflix')
def addMember(call):
    # Max reached 
    if Utils.countNetflixers(call.message.chat.id) == 4:
        bot.answer_callback_query(call.id,Statements.IT.MaxReached,show_alert=True)
    # Duplicated user
    elif call.from_user.first_name in Utils.listNetflixers(call.message.chat.id):
        bot.answer_callback_query(call.id,Statements.IT.AlreadySigned,show_alert=True)
    else:
        # Add user in USERS table
        Utils.executeQuery("INSERT INTO USERS(GROUP_ID,CHAT_ID,USERNAME,FIRST_NAME) VALUES (?,?,?,?)",[call.from_user.id,call.from_user.username,call.from_user.first_name,call.message.chat.id])
        # Update record in GROUPS table, increment number of user joined
        Utils.executeQuery("UPDATE GROUPS SET NETFLIXERS=NETFLIXERS+1 WHERE GROUP_ID=?",[call.message.chat.id])
        # Create an updated keyboard with new member
        updatedKeyboard = Keyboards.buildKeyboardForUser(Utils.listNetflixers(call.message.chat.id))
        # Edit the keyboard markup of the same message
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=updatedKeyboard)

# Remove user that already tapped 'I Use Netflix' button
@bot.callback_query_handler(func=lambda call: 'remove_' in call.data)
def removeUser(call):    
    # Delete user from db
    Utils.executeQuery("DELETE FROM USERS WHERE CHAT_ID=? AND GROUP_ID=?",[call.from_user.id,call.message.chat.id])
    # Decrement counter in GROUPS table
    Utils.executeQuery("UPDATE GROUPS SET NETFLIXERS=NETFLIXERS - 1 WHERE GROUP_ID=?",[call.message.chat.id])
    # Create an updated keyboard
    updatedKeyboard = Keyboards.buildKeyboardForUser(Utils.listNetflixers(call.message.chat.id))
    # Edit keyboard markup in the same message
    bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=updatedKeyboard)

# Confirm netflixers's list
@bot.callback_query_handler(func=lambda call: call.data == 'hereweare')
def hereweare(call):
    # If user is not admin
    if call.from_user.id != Utils.getAdminID(call.message.chat.id):
        bot.answer_callback_query(call.id,Statements.IT.NotAdmin,show_alert=True,cache_time=10)
    else:
        # If there aren't netflixers
        if Utils.countNetflixers(call.message.chat.id) == 0:
            bot.answer_callback_query(call.id,Statements.IT.AtLeastOneUser,show_alert=True)
        else:
            netflixers = ''
            # Create an updated list of netflixers
            for index, user in enumerate(Utils.listNetflixers(call.message.chat.id)):
                netflixers += "{} {}\n".format(Keyboards.Numbers[index],user)
            # Update the same message with a new list 
            bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="{}\n\n*{}*".format(Statements.IT.ConfirmList,netflixers),reply_markup=Keyboards.Confirm,parse_mode='markdown')

# Handler for general 'yes' callback
@bot.callback_query_handler(func=lambda call: call.data == 'yes')
def yes(call):
    # If user is not admin
    if call.from_user.id != Utils.getAdminID(call.message.chat.id):
        bot.answer_callback_query(call.id,Statements.IT.NotAdmin,show_alert=True,cache_time=10)
    else:
        # Netflixers's list confirmation 
        if call.message.text[:34] == Statements.IT.ConfirmList:
            bot.edit_message_text(Statements.IT.Schedule,call.message.chat.id,call.message.message_id,reply_markup=Keyboards.DateKeyboard,parse_mode='markdown')
        # Expiration's date confirmation
        elif call.message.text[:-4] == Statements.IT.ConfirmSchedule[:-6]:
            # Save expiration date in a var
            Expiration = ''.join(i for i in call.message.text if i.isdigit())
            # Update expiration date into db            
            Utils.executeQuery("UPDATE GROUPS SET EXPIRATION=? WHERE GROUP_ID=?",[Expiration,call.message.chat.id])
            netflixers = ''
            # Create an updated list
            for index, user in enumerate(Utils.listNetflixers(call.message.chat.id)):
                netflixers += "{} {}\n".format(Keyboards.Numbers[index],user)
            # Edit message text with new list
            bot.edit_message_text(Statements.IT.Done.replace('$$',netflixers,1).replace('$$',Expiration),call.message.chat.id,call.message.message_id,reply_markup={},parse_mode='markdown')
            # Edit START_MSG_ID into db, set to -1 that mean 'group already configured'
            Utils.executeQuery("UPDATE GROUPS SET START_MSG_ID=-1 WHERE GROUP_ID=?",[call.message.chat.id])
            # Add a new scheduled job for the group, on expiration day of every month at 08:00 AM
            job = scheduler.add_job(paymentNotify,CronTrigger('*','*',int(Expiration),hour=8,minute=00),[call.message.chat.id])
            # Append job object in jobScheduledList 
            jobScheduledList.append(job)
            # Save trigger into db
            Utils.saveTrigger(job.id,call.message.chat.id,Expiration)
        # Reset confiration
        elif call.message.text == Statements.IT.ConfirmReset.replace('*','',2):
            # Delete information from db, PAYMENTS and USERS tables
            Utils.executeQuery("DELETE FROM PAYMENTS WHERE GROUP_ID=? AND EXPIRATION=?",[call.message.chat.id,Utils.getExpiration(call.message.chat.id)])
            Utils.executeQuery("DELETE FROM USERS WHERE GROUP_ID=?",[call.message.chat.id])
            
            # Get trigger ID from db
            triggerID = Utils.getTriggerID(call.message.chat.id)
            # Remove trigger from scheduled job
            for index,job in enumerate(jobScheduledList):
                if job.id == triggerID:
                    jobScheduledList.pop(index)
                    break
            # Delete information from db, TRIGGER and GROUPS tables
            Utils.executeQuery("DELETE FROM TRIGGER WHERE ID=?",[triggerID])
            Utils.executeQuery("DELETE FROM GROUPS WHERE GROUP_ID=?",[call.message.chat.id])

            # Edit message with NewConfig statements
            bot.edit_message_text(Statements.IT.NewConfig,call.message.chat.id,call.message.message_id,reply_markup={},parse_mode='markdown')
            # Answer with a sucess message
            bot.answer_callback_query(call.id,Statements.IT.Resetted,show_alert=True,cache_time=10)

# Handler for general 'no' callback
@bot.callback_query_handler(func=lambda call: call.data == 'no')
def no(call):
    # If user is not admin
    if call.from_user.id != Utils.getAdminID(call.message.chat.id):
        bot.answer_callback_query(call.id,Statements.IT.NotAdmin,show_alert=True,cache_time=10)
    else:
        # If callback is coming from list's confirmation message
        if call.message.text[:34] == Statements.IT.ConfirmList:
            bot.edit_message_text(Statements.IT.Start.replace('$$',call.from_user.first_name),call.message.chat.id,call.message.message_id,reply_markup=Keyboards.buildKeyboardForUser(Utils.listNetflixers(call.message.chat.id)),parse_mode='markdown')
        # If callback is coming from expiration's confirmation message
        elif call.message.text[:-4] == Statements.IT.ConfirmSchedule[:-6]:
            bot.edit_message_text(Statements.IT.Schedule,call.message.chat.id,call.message.message_id,reply_markup=Keyboards.DateKeyboard,parse_mode='markdown')
        # If callback is coming from reset's confirmation message        
        elif call.message.text == Statements.IT.ConfirmReset.replace('*','',2):
            bot.edit_message_text(Statements.IT.AlreadyConfigured,call.message.chat.id,call.message.message_id,reply_markup=Keyboards.Reset,parse_mode='markdown')

# Expiration date confirmation
@bot.callback_query_handler(func=lambda call: 'date_' in call.data)
def confirmExpiration(call):
    # If user is not admin
    if call.from_user.id != Utils.getAdminID(call.message.chat.id):
        bot.answer_callback_query(call.id,Statements.IT.NotAdmin,show_alert=True,cache_time=10)
    else:
        bot.edit_message_text(Statements.IT.ConfirmSchedule.replace('$$',call.data[5:]),call.message.chat.id,call.message.message_id,reply_markup=Keyboards.Confirm,parse_mode='markdown')

# When user tap on his name in payment list
@bot.callback_query_handler(func=lambda call: 'payed_' in call.data)
def payed(call):
    # Get current status of the user from db
    stato = Utils.getSingleStatus(call.message.chat.id,Utils.getExpiration(call.message.chat.id),call.data[7:])
    # If the user has already payed
    if stato == 1:
            bot.answer_callback_query(call.id,Statements.IT.AlreadyPayed.replace('$$',call.data[7:]),show_alert=True)
    else:
        # If the user is the admin
        if call.from_user.id == Utils.getAdminID(call.message.chat.id):
            # Update payment status into db to payed
            Utils.executeQuery("UPDATE PAYMENTS SET STATUS=1 WHERE GROUP_ID=? AND FIRST_NAME=? AND EXPIRATION=?",[call.message.chat.id,call.data[7:],Utils.getExpiration(call.message.chat.id)])
            # Get current status of all users
            results = Utils.getStatus(call.message.chat.id,Utils.getExpiration(call.message.chat.id))
            everyonePayed = True
            for status in results:
                if status != 1:                
                    everyonePayed = False
            # If everyone has already payed
            if everyonePayed:
                bot.edit_message_text(Statements.IT.EveryonePaid.replace('$$',Utils.getExpiration(call.message.chat.id)),call.message.chat.id,call.message.message_id,reply_markup={},parse_mode='markdown')
                return
        else:
            # If the user is not the admin, the payment's status is set to -1, mean 'waiting for admin confirm'
            Utils.executeQuery("UPDATE PAYMENTS SET STATUS=-1 WHERE GROUP_ID=? AND FIRST_NAME=? AND EXPIRATION=?",[call.message.chat.id,call.data[7:],Utils.getExpiration(call.message.chat.id)])
        
        # Get current status of all users
        status = Utils.getStatus(call.message.chat.id,Utils.getExpiration(call.message.chat.id))
        # Create an update keyboard with new status
        kb = Keyboards.buildKeyboardForPayment(Utils.listNetflixers(call.message.chat.id),status)
        # Edit message markup with updated keyboard
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=kb)

# Reset current group's configuration 
@bot.callback_query_handler(func=lambda call: call.data == 'reset')
def reset(call):
    # If user is not the admin
    if call.from_user.id != Utils.getAdminID(call.message.chat.id):
        bot.answer_callback_query(call.id,Statements.IT.NotAdmin,show_alert=True,cache_time=10)
    else:
        bot.edit_message_text(Statements.IT.ConfirmReset,call.message.chat.id,call.message.message_id,reply_markup=Keyboards.Confirm,parse_mode='markdown')

# Put bot in polling state, waiting for incoming message
bot.polling()
