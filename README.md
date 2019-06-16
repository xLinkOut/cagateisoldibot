# 💰 CagateISoldiBot 💰
Telegram bot to manage Netflix's shared account with your friends and family. 🎬
_(In english 'cagate i soldi' is something like 'give me your money')_

## Installation:
```bash
    $ virtualenv -p python3 venv # optional
    $ source venv/bin/activate # optional
    $ pip3 install -r requirements.txt
    # Obviously replace YOUR_TOKEN with bot's token given by BotFather.
    $ sed 's/INSERT_TOKEN_HERE/YOUR_TOKEN/' -i src/Settings.py
    $ python3 CreateDB.py
    $ python3 Main.py
```
[![asciicast](https://asciinema.org/a/215057.svg)](https://asciinema.org/a/215057)

## TODO
- [x] Notify a member when his payment is confimed by the admin;
- [ ] Notify the admin if the bot is removed from a group;
- [ ] Send a bunch of other messages if someone's money is missing;
- [ ] Add screenshots to this readme;

## Try it here!
It's still in beta and can stop working/losing data without warning, but you can give a try: [http://t.me/cagateisoldibot](http://t.me/cagateisoldibot) 
