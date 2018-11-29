# -*- coding: utf-8 -*-
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton

# -- Start Inline Keyboard -- #
Start = InlineKeyboardMarkup(row_width=2)
IUseNetflixBtn = InlineKeyboardButton(text='✋️ I use Netflix!',callback_data='iusenetflix')
HereWeAreBtn = InlineKeyboardButton(text='Here we are 👌',callback_data='hereweare')
Start.add(IUseNetflixBtn)
Start.add(HereWeAreBtn)

# -- Confirm Inline Keyboard -- #
Confirm = InlineKeyboardMarkup()
YesBtn = InlineKeyboardButton(text='Yes ✅',callback_data='yes')
NoBtn = InlineKeyboardButton(text='No ❌',callback_data='no')
Confirm.add(YesBtn,NoBtn)
