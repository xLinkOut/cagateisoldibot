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


# Put bot in polling state, waiting for incoming message
bot.polling()
