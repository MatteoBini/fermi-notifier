from src.databaseOperations import getSubscribers, db_notification
from src.telegramOperations import register_new_user, tg_notification
from src.emailOperations import *
from src.fermiCalendar import *
from src.utility import *

def deliver_notification(n):
    # This function delegates the operations to
    # be done when I decide to notify someone: 
    # send email, send messaage and store the 
    # notification
    email_notification(n)
    tg_notification(n)
    db_notification(n["id"], n["events"])

    return

def main(last_update_id):

    while True:
        ###           COLLECT SUBSCRIBERS DATA          ###
        subs = getSubscribers()
        
        ###           USER REGISTRATION EVENTS          ###
        pending_registration(subs)
        welcome_notification(subs)

        ###        TELEGRAM REGISTRATION EVENTS         ###
        last_update_id = register_new_user(subs, last_update_id)

        ###        COLLECT & SEND NOTIFICATIONS         ###
        notifications = collect_notifications(subs)
        for user in notifications:
            deliver_notification(user)

    return "merda."


if __name__ == "__main__":
    main(last_update_id=0)




























