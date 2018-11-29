# -*- coding: utf-8 -*-
import telebot, logging, os
import Settings, Statements, Keyboards

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
@bot.callback_query_handler(func=lambda call: call.data == 'iousonetflix')
def addMember(call):
    # Max reached 
    if Utils.numeroPartecipanti(call.message.chat.id) == 4:
        bot.answer_callback_query(call.id,Statements.IT.MaxReached,show_alert=True)
    # Duplicated user
    elif call.from_user.first_name in Utils.listaPartecipanti(call.message.chat.id):
        bot.answer_callback_query(call.id,Statements.IT.AlreadySigned,show_alert=True)
    else:
        # Add user in USERS table
        Utils.executeQuery("INSERT INTO USERS(GROUP_ID,CHAT_ID,USERNAME,FIRST_NAME) VALUES (?,?,?,?)",[call.from_user.id,call.from_user.username,call.from_user.first_name,call.message.chat.id])
        # Update record in GROUPS table, increment number of user joined
        Utils.executeQuery("UPDATE GROUPS SET NETFLIXERS=NETFLIXERS+1 WHERE GROUP_ID=?",[call.message.chat.id])
        # Create an updated keyboard with new member
        updatedKeyboard = Keyboards.buildKeyboardForUser(Utils.listaPartecipanti(call.message.chat.id))
        # Edit the keyboard markup of the same message
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=updatedKeyboard)

# Remove user that already tapped 'I Use Netflix' button
@bot.callback_query_handler(func=lambda call: 'remove_' in call.data)
def removeUser(call):    
    # Delete user from db
    Utils.executeQuery("DELETE FROM PARTECIPANTI WHERE CHAT_ID=? AND GROUP_ID=?",[call.from_user.id,call.message.chat.id])
    # Decrement counter in GROUPS table
    Utils.executeQuery("UPDATE GROUPS SET NUMERO_PARTECIPANTI=NUMERO_PARTECIPANTI - 1 WHERE GROUP_ID=?",[call.message.chat.id])
    # Create an updated keyboard
    updatedKeyboard = Keyboards.buildKeyboardForUser(Utils.listaPartecipanti(call.message.chat.id))
    # Edit keyboard markup in the same message
    bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=updatedKeyboard)


# Put bot in polling state, waiting for incoming message
bot.polling()
