# da riadattare.

import telepot
from dotenv import load_dotenv
import os
from random import randint
from datetime import datetime, time
from src.databaseOperations import updateTelegramId
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
    
    def register_new_user(self,last_update_id, subs):
        # Check the inbox for new messages (watchout the offest),
        # and if a message is idential to a unique alphanumeric 
        # id (stored in "telegram" column into the database) I 
        # associate the sender's telegram id with my subscriber. 

        inboxMessages = self.bot.getUpdates(offset=last_update_id)
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

                            last_update_id = _["update_id"] if _["update_id"] > last_update_id else last_update_id

                            updateTelegramId(user_email, telegram_id)
                            self.user_welcome(telegram_id)

        return last_update_id

###############################################
#                                             #
#                                             #
#           HANDLE USER REGISTRATION          #
#                                             #
#                                             #
###############################################

def register_new_user(subs, last_update_id):
    # Executes the registration without initializing no objects
    # outside this function
    TG = Telegram()
    TG.register_new_user(last_update_id, subs)

    return 


###############################################
#                                             #
#                                             #
#         USER NOTIFICATION MESSAGES          #
#                                             #
#                                             #
###############################################


def daily_message(notification: dict):
    # Set up message for daily roundup notification

    message = {
        "receiver_id": notification["id"],
        "receiver": notification["telegram"],
        "uid": [],
        message["body"]: get_notification_tg_message(notification)
    }

    for event in notification["events"]:
        message["uid"].append(event["id"])
    
    TG = Telegram()
    TG.chatNotification(message)
    
    return


def last_minute_message(receiver: str, event: dict):
    # TODO IMPLEMENTARE SUPPORTO PIÙ EVENTI LAST MINUTE

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
        last_minute_message(receiver, notification["events"]) # FIX THIS !!! ADD SUPPORT FOR MULTIPLE EVENTS LAST MINUTE MESSAGE TODO

    return

