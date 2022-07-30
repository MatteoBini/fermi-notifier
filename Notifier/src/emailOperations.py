import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from datetime import datetime, time
from src.utility import *
from src.databaseOperations import incrementNumNot


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
        PORT = 587
        self.client = smtplib.SMTP("smtp.zoho.eu", PORT)

        self.client.starttls()
        self.client.login("servizi@matteobini.me", EMAIL_PASSWORD)
        
        return


    def notifyAdmin(self, new_user):
        msg = EmailMessage()
        msg["Subject"] = "Nuovo iscritto Calendar Notifier"
        msg["From"] = "servizi@matteobini.me"
        msg["To"] = "servizi@matteobini.me"
        msg.set_content(f"Salve,\n{new_user} si e' iscritto.\n\nFermi Notifier Team")

        self.client.send_message(msg)


    def sendHTMLMail(self, receiver: str, subject: str, body: str, html_body: str):
        data = MIMEMultipart('alternative')
        data["Subject"] = subject
        data["From"] = "Eventi Calendario Giornaliero <servizi@matteobini.me>"
        data["To"] = receiver
        
        part1 = MIMEText(body, "plain")
        part2 = MIMEText(html_body, "html")
        data.attach(part1)
        data.attach(part2)
        
        self.client.sendmail("servizi@matteobini.me", receiver, data.as_string())

        return


    def closeConnection(self):
        self.client.quit()

        return

def send_email(email: dict):
    EM = Email()

    if email["isWelcome"]:
        EM.sendHTMLMail(
            email["Receiver"],
            "Registrazione completata a Fermi Notifier",
            "Registrazione completata. Visita servizi.matteobini.me/fermi-notifier . Per informazioni: servizi@matteobini.me",
            email["Body"]
        )
        EM.notifyAdmin(email["Receiver"])
        return EM.closeConnection()

    EM.sendHTMLMail(
        email["Receiver"],
        email["Subject"],
        email["Raw"],
        email["Body"]
    )
    EM.closeConnection()

    return 



###############################################
#                                             #
#                                             #
#           USER REGISTRATION EMAILs          #
#                                             #
#                                             #
###############################################

def welcome_notification(subs):
    # Check for new users and send them the welcome
    # notification.

    for sub in subs:
        if sub["n_not"] == 0:
            email = {
                "Receiver": sub["email"],
                "Body": get_welcome_mail_body(sub["name"]),
                "isWelcome": True,
                "receiver_id": sub["id"]
            }
            send_email(email)
            incrementNumNot(sub["id"])
    
    return


def pending_registration(subs):
    # Check if there are users not yet fully registered 
    # (missing email confirmation)
    for sub in subs:
        if sub["n_not"] == -2:
            verification_code = sub["telegram"]

            email = {
                "Receiver_id": sub["id"],
                "Receiver": sub["email"],
                "Uid": ["conferma_registrazione"],
                "isWelcome": False,
                "Subject": get_registration_mail_subject(),
                "Raw": get_registration_mail_raw(sub["name"], verification_code),
                "Body": get_registration_mail_body(sub["name"], verification_code),
            }

            send_email(email)
            incrementNumNot(sub["id"])

    return



###############################################
#                                             #
#                                             #
#           USER NOTIFICATION EMAILs          #
#                                             #
#                                             #
###############################################

def daily_email(receiver: dict, events: list):
    # Set up email for daily roundup notification

    email = {
        "Receiver_id": receiver["id"],
        "Receiver": receiver["email"],
        "Uid": [],
        "isWelcome": False,
        "Subject": get_notification_mail_subject(receiver, events),
        "Raw": get_notification_mail_raw(),
        "Body": get_notification_mail_body(receiver, events)
    }

    for event in events:
        # Adding up the ids of all events that I 
        email["Uid"].append(event["id"])
        
    send_email(email)
    return


def last_minute_email(receiver: dict, events: list):
    # TODO IMPLEMENTARE SUPPORTO PIÙ EVENTI LAST MINUTE

    # Set up email for last minute notification
    email = {
        "Receiver_id": receiver["id"],
        "Receiver": receiver["email"],
        "Uid": [],
        "isWelcome": False,
        "Subject": get_last_minute_notification_mail_subject(),
        "Raw": get_last_minute_notification_mail_raw(receiver, events),
        "Body": get_last_minute_notification_mail_body(receiver, events)
    }

    for _ in events:
        email["Uid"].append(_["id"])

    send_email(email)
    return


def email_notification(notification: dict):
    # I manipulate the subscribers' events and I choose if 
    # notify: I could send it another day, send it later today
    # or send it now (because is last minute or because it's 
    # time for daily roundup notification)

    # Check the current time slot
    isSchoolHour = datetime.now().time() > time(8,10)
    isDaily =  time(7,55) < datetime.now().time() < time(8,10)

    receiver = {
        "id": notification["id"],
        "name": notification["name"],
        "email": notification["email"]
    }

    if isDaily:
        # It's time for the daily notification!
        daily_email(receiver, notification["events"])
    
    elif isSchoolHour:
        # The daily notification has already been sent 
        # but there're is a last minute events 

        last_minute_email(receiver, notification["events"]) # FIX THIS !!! ADD SUPPORT FOR MULTIPLE EVENTS LAST MINUTE EMAIL TODO

    return
