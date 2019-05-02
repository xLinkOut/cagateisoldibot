# -*- coding: utf-8 -*-
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardMarkup,KeyboardButton
from Utils import getAllUsers
Numbers = ["1️⃣","2️⃣","3️⃣","4️⃣"]

# -- Start Inline Keyboard -- #
Start = InlineKeyboardMarkup(row_width=2)
IUseNetflixBtn = InlineKeyboardButton(text='✋️ Io uso Netflix!',callback_data='iusenetflix')
HereWeAreBtn = InlineKeyboardButton(text='Ci siamo tutti 👌',callback_data='hereweare')
Start.add(IUseNetflixBtn)
Start.add(HereWeAreBtn)

# -- Confirm Inline Keyboard -- #
Confirm = InlineKeyboardMarkup()
YesBtn = InlineKeyboardButton(text='Si ✅',callback_data='yes')
NoBtn = InlineKeyboardButton(text='No ❌',callback_data='no')
Confirm.add(YesBtn,NoBtn)

def buildKeyboardForUser(group_id):
    # Create a new inline keyboard markup object
    newStart = InlineKeyboardMarkup()
    users = getAllUsers(group_id)
    print(users)
    # If there aren't users in db
    if not users:
        pass
    # If users contain only one user    
    elif len(users) == 1:
        # Add a button with this user
        newStart.add(InlineKeyboardButton(text="{} {}".format(Numbers[0],users[0][2]),callback_data='remove_{}'.format(users[0][0])))
    else:
        # For each user in the list
        for index,user in enumerate(users):
            # Add a button with his name
            newStart.add(InlineKeyboardButton(text="{} {}".format(Numbers[index],user[2]),callback_data='remove_{}'.format(user[0])))
    # At the bottom add those two button (as start keyboard)
    newStart.add(IUseNetflixBtn)
    newStart.add(HereWeAreBtn)
    # Return the keyboard
    return newStart

# Function that return an updated keyboard with all users and their payment's status 
def buildKeyboardForPayment(group_id,status):
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
    users = getAllUsers(group_id)    
    # For each user in list
    for index,user in enumerate(users):
        # Add a button with user name and his status
        kb.add(InlineKeyboardButton(text="{} {}".format(status[index],user[2]),callback_data='payed_{}'.format(user[0])))
    return kb

# -- Reset Inline Keyboard -- #
Reset = InlineKeyboardMarkup()
Reset.add(InlineKeyboardButton('💀 Reset 💀',callback_data='reset'))

# -- Date Inline Keyboard -- #
DateKeyboard = InlineKeyboardMarkup()
DateKeyboard.add(
    InlineKeyboardButton(text='1',callback_data='date_1'),
    InlineKeyboardButton(text='2',callback_data='date_2'),
    InlineKeyboardButton(text='3',callback_data='date_3'),
    InlineKeyboardButton(text='4',callback_data='date_4'),
    InlineKeyboardButton(text='5',callback_data='date_5'),
    InlineKeyboardButton(text='6',callback_data='date_6'),
    InlineKeyboardButton(text='7',callback_data='date_7'),
    InlineKeyboardButton(text='8',callback_data='date_8'),
    InlineKeyboardButton(text='9',callback_data='date_9'),
    InlineKeyboardButton(text='10',callback_data='date_10'),
    InlineKeyboardButton(text='11',callback_data='date_11'),
    InlineKeyboardButton(text='12',callback_data='date_12'),
    InlineKeyboardButton(text='13',callback_data='date_13'),
    InlineKeyboardButton(text='14',callback_data='date_14'),
    InlineKeyboardButton(text='15',callback_data='date_15'),
    InlineKeyboardButton(text='16',callback_data='date_16'),
    InlineKeyboardButton(text='17',callback_data='date_17'),
    InlineKeyboardButton(text='18',callback_data='date_18'),
    InlineKeyboardButton(text='19',callback_data='date_19'),
    InlineKeyboardButton(text='20',callback_data='date_20'),
    InlineKeyboardButton(text='21',callback_data='date_21'),
    InlineKeyboardButton(text='22',callback_data='date_22'),
    InlineKeyboardButton(text='23',callback_data='date_23'),
    InlineKeyboardButton(text='24',callback_data='date_24'),
    InlineKeyboardButton(text='25',callback_data='date_25'),
    InlineKeyboardButton(text='26',callback_data='date_26'),
    InlineKeyboardButton(text='27',callback_data='date_27'),
    InlineKeyboardButton(text='28',callback_data='date_28'),
    InlineKeyboardButton(text='29',callback_data='date_29'),
    InlineKeyboardButton(text='30',callback_data='date_30')
    #InlineKeyboardButton(text='31',callback_data='date_31')
)

# -- Start Keyboard -- #
StartPrivate = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
DonateBtn = KeyboardButton("🎁 Donate")
AboutBtn = KeyboardButton("❓ About")
StartPrivate.add(DonateBtn,AboutBtn)