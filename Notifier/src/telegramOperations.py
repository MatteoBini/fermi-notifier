# da riadattare.

import telepot
from dotenv import load_dotenv
import os
from random import randint
from datetime import datetime, time
from src.databaseOperations import *
from src.utility import * 

###############################################
#                                             #
#                                             #
#               GENERAL PURPOSE               #
#                                             #
#                                             #
###############################################

class Telegram:

    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv('TELEGRAM_API_KEY')
        self.bot = telepot.Bot(self.API_KEY)

    def chatNotification(self, message: dict):
        self.bot.sendMessage(
            message["receiver"], 
            message["body"], 
            parse_mode='MARKDOWN'
        )

        return

    def user_welcome(self, telegram_id):
        # Sends the confirmation for connecting telegram 
        # account id to service
        self.chatNotification(message = {
            "receiver": telegram_id, 
            "body": "Registrazione effettuata correttamente" 
        })
    
    def register_new_user(self, subs):
        # Check the inbox for new messages (watchout the offest),
        # and if a message is idential to a unique alphanumeric 
        # id (stored in "telegram" column into the database) I 
        # associate the sender's telegram id with my subscriber. 

        inboxMessages = self.bot.getUpdates(offset=getTgOffset())
        for _ in inboxMessages:
            
            for i in subs:
                # The next lines I check if I got messages from any
                # new user or some stranger (first 2 lines to check 
                # if I didn't get messages from groups, last one 
                # check for the message that i got from my new user)
                if "my_chat_member" not in _.keys():
                    if ("new_chat_participant" not in _["message"]) and ("left_chat_participant" not in _["message"]):
                        if _["message"]["text"] == i["telegram"]:
                            user_email = i["email"]
                            telegram_id = _["message"]["from"]["id"]

                            updateTgOffset(_["update_id"])

                            updateTelegramId(user_email, telegram_id)
                            self.user_welcome(telegram_id)

        return

###############################################
#                                             #
#                                             #
#           HANDLE USER REGISTRATION          #
#                                             #
#                                             #
###############################################

def register_new_user(subs):
    # Executes the registration without initializing no objects
    # outside this function
    TG = Telegram()
    TG.register_new_user(subs)

    return 


###############################################
#                                             #
#                                             #
#         USER NOTIFICATION MESSAGES          #
#                                             #
#                                             #
###############################################


def daily_message(receiver: dict, events: list):
    # Set up message for daily roundup notification

    message = {
        "receiver_id": receiver["id"],
        "receiver": receiver["telegram"],
        "uid": [],
        "body": get_notification_tg_message(receiver, events)
    }

    for event in events:
        message["uid"].append(event["id"])
    
    TG = Telegram()
    TG.chatNotification(message)
    
    return


def last_minute_message(receiver: str, event: dict):

    # Set up message for last minute notification

    message = {
        "receiver_id": receiver["id"],
        "receiver": receiver["telegram"],
        "body": get_last_minute_message(receiver, event)
    }
    
    TG = Telegram()
    TG.chatNotification(message)
    
    return

def tg_notification(notification: dict):
    # I manipulate the subscribers' events and I choose if 
    # notify: I could send it another day, send it later today
    # or send it now (because is last minute or because it's 
    # time for daily roundup notification)
    
    if str(notification["telegram"])[0] == 'X':
        # I exit the function when the user did not 
        # connect telegram
        return

    # Check the current time slot
    isSchoolHour = datetime.now().time() > time(8,10)
    isDaily =  time(7,55) < datetime.now().time() < time(8,10)

    receiver = {
        "id": notification["id"],
        "name": notification["name"],
        "telegram": notification["telegram"]
    }
    if isDaily:
        # It's time for the daily notification!
        daily_message(receiver, notification["events"])

    elif isSchoolHour:
        # The daily notification has already been sent 
        # but there're is a last minute events 
        last_minute_message(receiver, notification["events"])

    return

