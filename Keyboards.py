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

# -- Function that return an updated keyboard with all users that
#    joined the bot 
def buildKeyboardForUser(users):
    # Create a new inline keyboard markup object
    newStart = InlineKeyboardMarkup()
    # If users contain only one user
    if len(users) == 1:
        # Add a button with this user
        newStart.add(InlineKeyboardButton(text="{} {}".format(Numbers[0],users[0]),callback_data='remove_{}'.format(users[0])))
    else:
        # For each user in the list
        for index,user in enumerate(users):
            # Add a button with his name
            newStart.add(InlineKeyboardButton(text="{} {}".format(Numbers[index],user),callback_data='remove_{}'.format(user)))        
    # At the bottom add those two button (as start keyboard)
    newStart.add(IUseNetflixBtn)
    newStart.add(HereWeAreBtn)
    # Return the keyboard
    return newStart

# -- Function that return an updated keyboard with all users and
#    their payment's status 
def buildKeyboardForPayment(users,status):
    # Translate integer status to emoji
    for index,stat in enumerate(status):
        # Already payed
        if stat == 1:
            status[index] = '✅'
        # Not payed yet
        elif stat == 0:
            status[index] = '❌'
        # Waiting for admin confirmation
        else:
            status[index] = '⏳'
    # Create a new inline keyboard object
    kb = InlineKeyboardMarkup()
    # For each user in list
    for index,user in enumerate(users):
        # Add a button with user name and his status
        kb.add(InlineKeyboardButton(text="{} {}".format(status[index],user),callback_data='payed_{}'.format(user)))
    return kb