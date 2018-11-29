# -*- coding: utf-8 -*-
import telebot, logging, os
import Settings, Statements

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

# Put bot in polling state, waiting for incoming message
bot.polling()
