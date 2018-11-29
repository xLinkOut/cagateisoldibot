# -*- coding: utf-8 -*-
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton

# -- Start Inline Keyboard -- #
Start = InlineKeyboardMarkup(row_width=2)
IUseNetflixBtn = InlineKeyboardButton(text='✋️ Io uso Netflix!',callback_data='iousonetflix')
SiamoTuttiBtn = InlineKeyboardButton(text='Siamo tutti 👌',callback_data='siamotutti')
Start.add(IUseNetflixBtn)
Start.add(SiamoTuttiBtn)