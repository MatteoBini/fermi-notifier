import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from datetime import datetime, time
from src.utility import *
from src.databaseOperations import increment_notification_number


###############################################
#                                             #
#                                             #
#               GENERAL PURPOSE               #
#                                             #
#                                             #
###############################################

class Email:

    def __init__(self):
        load_dotenv()
        EMAIL_PASSWORD = os.getenv('EMAIL_SERVICE_PASSWORD')
        PORT = os.getenv('EMAIL_SERVICE_PORT')
        URL = os.getenv('EMAIL_SERVICE_URL')
        self.client = smtplib.SMTP(URL, PORT)

        self.client.starttls()
        self.client.login("master@ferminotify.me", EMAIL_PASSWORD)
        
        return


    def notify_admin(self, new_user: str) -> None:
        msg = EmailMessage()
        msg["Subject"] = "Nuovo iscritto Calendar Notifier"
        msg["From"] = "Fermi Notify Team <master@ferminotify.me>"
        msg["To"] = "master@ferminotify.me"
        msg.set_content(f"Salve,\n{new_user} si e' iscritto.\n\n\
                            Fermi Notify Team")
        self.client.send_message(msg)
        
        return


    def sendHTMLMail(self, receiver: str, subject: str, 
                        body: str, html_body: str) -> None:
        data = MIMEMultipart('alternative')
        data["Subject"] = subject
        data["From"] = "Fermi Notify Team <master@ferminotify.me>"
        data["To"] = receiver
        
        part1 = MIMEText(body, "plain")
        part2 = MIMEText(html_body, "html")
        data.attach(part1)
        data.attach(part2)
        
        self.client.sendmail("master@ferminotify.me", receiver,
                                data.as_string())

        return


    def closeConnection(self) -> None:
        self.client.quit()

        return

def send_email(email: dict) -> None:
    EM = Email()

    EM.sendHTMLMail(
        email["Receiver"], email["Subject"],
        email["Raw"], email["Body"]
    )
    EM.closeConnection()

    return 


def notify_admin(new_user: str) -> None:
    EM = Email()

    EM.notify_admin(new_user)
    EM.closeConnection()

    return 

###############################################
#                                             #
#                                             #
#           USER REGISTRATION EMAILs          #
#                                             #
#                                             #
###############################################

def pending_registration(subs: list[dict]) -> None:
    # Check if there are users not yet fully registered 
    # (missing email confirmation)
    for sub in subs:
        if sub["n_not"] == -2:
            verification_code = sub["telegram"]

            email = {
                "Receiver_id": sub["id"],
                "Receiver": sub["email"],
                "Uid": ["conferma_registrazione"],
                "Subject": get_registration_mail_subject(),
                "Raw": get_mail_raw(),
                "Body": get_registration_mail_body(sub["name"], 
                                                    verification_code),
            }

            send_email(email)
            increment_notification_number(sub["id"])

    return

def welcome_notification(subs: list[dict]) -> None:
    # Check for new users and send them the welcome notification.

    for sub in subs:
        # If the number of notifications is == 0 I have to send the welcome 
        # notification (because the user has just been properly registered)
        if sub["n_not"] == 0: 
            email = {
                "Receiver_id": sub["id"],
                "Receiver": sub["email"],
                "Subject": get_welcome_mail_subject(),
                "Raw": get_mail_raw(),
                "Body": get_welcome_mail_body(sub),
                "receiver_id": sub["id"]
            }
            send_email(email)
            increment_notification_number(sub["id"])
            notify_admin(email["Receiver"])
    
    return



###############################################
#                                             #
#                                             #
#           USER NOTIFICATION EMAIL           #
#                                             #
#                                             #
###############################################

def email_notification(notification: dict) -> None:
    # Check if I have to send the notification now

    user = {
        "id": notification["id"],
        "name": notification["name"],
        "email": notification["email"]
    }
    email = {
        "Receiver_id": user["id"],
        "Receiver": user["email"],
        "Raw": get_mail_raw(),
        "Uid": [i["id"] for i in notification["events"]],
    }

    is_dailynotification_time =  time(6,00) < datetime.now().time() < time(6,15)
    has_school_started = datetime.now().time() > time(6,15)

    if is_dailynotification_time:
        email["Subject"] = get_daily_notification_mail_subject(
                                                len(notification["events"]))
        email["Body"] = get_daily_notification_mail_body(user, 
                                                        notification["events"])
    
    elif has_school_started:
        email["Subject"] = get_last_minute_notification_mail_subject()
        email["Body"] = get_last_minute_notification_mail_body(user, 
                                                        notification["events"])

    send_email(email)

    return
