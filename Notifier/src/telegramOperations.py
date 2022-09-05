import os
from datetime import datetime, time
from dotenv import load_dotenv
import telepot
from src.databaseOperations import get_tg_offset, update_tg_offset, update_telegram_id
from src.utility import get_daily_notification_tg_message, get_last_minute_message

"""
Summary of all the operations involving Telegram.
"""

###############################################
#                                             #
#                                             #
#               GENERAL PURPOSE               #
#                                             #
#                                             #
###############################################

class Telegram:
    """
    Class methods for the telegram operations.

    Such as:
    - Sending a notification to a chat
    - Sending a welcome message to a user
    - Registering a new user

    Attributes:
        API_KEY (str): The telegram API key.
        bot (telepot.Bot): The telegram bot.
    """

    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv('TELEGRAM_API_KEY')
        self.bot = telepot.Bot(self.API_KEY)

    def chat_notification(self, message: dict) -> None:
        """Sends a notification to the chat trough the bot.

        Args:
            message (dict): A dictionary containing the receiver's id and the message to be sent.
        """
        self.bot.sendMessage(
            message["receiver"], 
            message["body"], 
            parse_mode='MARKDOWN'
        )

        return

    def user_welcome(self, telegram_id: str) -> None:
        """Sends a welcome confirmation message to the user to notify him
        that the connection between the account id and the service
        has been established with success.

        Args:
            telegram_id (str): The user's telegram id.
        """
        self.chat_notification(message = {
            "receiver": telegram_id, 
            "body": "Registrazione effettuata correttamente" 
        })
        return
    
    def register_new_telegram_user(self, subs: list[dict]) -> None:
        """Associates a telegram account to a subscriber of the service
        using a unique id.

        The id is recieved in the inbox of the telegram bot and if
        it is present in the database, the user is registered.

        Args:
            subs (list): A list of dictionaries containing the user's info.
        """

        inbox_messages = self.bot.getUpdates(offset=get_tg_offset())
        for i in inbox_messages:
            
            for j in subs:
                # The next lines I check if I got messages from any
                # new user or some stranger (first 2 lines to check 
                # if I didn't get messages from groups, last one 
                # check for the message that i got from my new user)
                if "my_chat_member" not in i.keys():
                    if ("new_chat_participant" not in i["message"]) and ("left_chat_participant" not in i["message"]):
                        if i["message"]["text"] == j["telegram"]:
                            user_email = j["email"]
                            telegram_id = i["message"]["from"]["id"]

                            update_tg_offset(i["update_id"])

                            update_telegram_id(user_email, telegram_id)
                            self.user_welcome(telegram_id)

        return

###############################################
#                                             #
#                                             #
#           HANDLE USER REGISTRATION          #
#                                             #
#                                             #
###############################################

def register_new_telegram_user(subs: list[dict]) -> None:
    """Associates a telegram account to a subscriber of the service.

    Args:
        subs (list): A list of dictionaries containing the user's info.
    """
    TG = Telegram()
    TG.register_new_telegram_user(subs)

    return 


###############################################
#                                             #
#                                             #
#         USER NOTIFICATION MESSAGES          #
#                                             #
#                                             #
###############################################

def tg_notification(notification: dict) -> None:
    """Selects when to send the notification.

    The notification can be sent either daily or last minute.

    Args:
        notification (dict): dictionary containing all the events that a 
        subscriber need to be notified.
    """
    
    if str(notification["telegram"])[0] == 'X':
        # Exit the function when the user did not connect telegram.
        return

    user = {
        "id": notification["id"],
        "name": notification["name"],
        "telegram": notification["telegram"]
    }
    message = {
        "receiver_id": user["id"],
        "receiver": user["telegram"],
    }

    is_dailynotification_time =  time(7,55) < datetime.now().time() < time(8,10)
    has_school_started = datetime.now().time() > time(8,10)

    if is_dailynotification_time:
        message["body"] = get_daily_notification_tg_message(user, 
                                                        notification["events"])

    elif has_school_started:
        message["body"]: get_last_minute_message(user, notification["events"])

    TG = Telegram()
    TG.chat_notification(message)
    
    return
