from src.databaseOperations import get_subscribers, store_notification
from src.telegramOperations import register_new_telegram_user, tg_notification
from src.emailOperations import pending_registration, welcome_notification, \
                                email_notification
from src.fermiCalendar import collect_notifications

"""
Main.
"""

def deliver_notification(notification: dict) -> None:
    """This function delegates the notification delivery to the appropriate 
    functions.

    Such as:
    - Send email notification.
    - Send telegram notification.
    - Store the notification in the database.

    Args:
        notification (list): list of dictionaries containing all the 
        subscribers that need to be notified and
        the corresponding events.
    """
    email_notification(notification)
    tg_notification(notification)
    store_notification(notification["id"], notification["events"])
    return

def main():
    """Being the main function of the program, it will call all the other 
    functions.

    Such as:
    - Handling the pending registrations.
    - Collecting the notifications.
    - Deliver the notifications.
    """
    while True:
        # Collect all the subscribers data from
        # the database
        subs = get_subscribers()

        pending_registration(subs)  # Send the confirmation email
        welcome_notification(subs)  # Welcome the new users
        register_new_telegram_user(subs)
        
        # Collect all the new notifications
        notifications = collect_notifications(subs)

        for user in notifications:
            deliver_notification(user)  # Deliver the notifications.

    return "fuck."


if __name__ == "__main__":
    main()
