from datetime import datetime, time
from random import choice

###############################################
#                                             #
#                                             #
#               GENERAL PURPOSE               #
#                                             #
#                                             #
###############################################

def is_event_today(event: dict) -> bool:
    # Check if the notification has to be sent now (considering the 
    # current time and the datetime of the event)
    
    if (not event["startDate"]) and (not event["startDateTime"]):
        # In case there are no events today
        return False

    if event["startDate"]:
        event_time = event["startDate"]
    else:
        event_time = event["startDateTime"]
    event_is_today = str(datetime.fromisoformat(event_time))[:10] \
                    == str(datetime.today())[:10]
    is_notification_time = time(7,55) < datetime.now().time()

    return (event_is_today and is_notification_time)

def get_event_colors() -> tuple:
    # Returns a tuple of colors for events card in the emails. The first 
    # element is for the background and the second one for text

    colors = [
        ("#1B5E20", "#A5D6A7"), ("#FF6F00", "#FFE082"), ("#1A237E", "#9FA8DA"),
        ("#BF360C", "#FFAB91"), ("#01579B", "#81D4FA"), ("#33691E", "#A5D6A7"),
        ("#880E4F", "#F48FB1"), ("#E65100", "#FFCC80"), ("#311B92", "#B39DDB"),
        ("#B71C1C", "#EF9A9A"), ("#004D40", "#80CBC4"), ("#F57F17", "#FFF59D"),
        ("#0D47A1", "#90CAF9"), ("#827717", "#E6EE9C"), ("#006064", "#80DEEA"),
        ("#4A148C", "#CE93D8"),
    ]

    return choice(colors)

def get_mail_raw() -> str:
    return "Ci sono nuovi eventi che ti coinvolgono sul calendario giornaliero"

###############################################
#                                             #
#                                             #
#                    EMAIL                    #
#                                             #
#                                             #
###############################################

###      MESSAGGIO DI CONFERMA ACCOUNT      ###

def get_registration_mail_subject() -> str:
    return "Fermi Notifier - Confirm registration"

def get_registration_mail_body(name: str, verification_code: str) -> str:
    body = ""

    with open("emails/Confirm-registration/1.htm") as f:
        body += f.read()

    body += name

    with open("emails/Confirm-registration/2.htm") as f:
        body += f.read()

    body += verification_code

    with open("emails/Confirm-registration/3.htm") as f:
        body += f.read()

    body += verification_code

    with open("emails/Confirm-registration/4.htm") as f:
        body += f.read()
    
    body += verification_code

    return body



###          MESSAGGIO DI BENVENUTO         ###

def get_welcome_mail_subject() -> str:
    return "Fermi Notifier - Welcome!"

def get_welcome_mail_body(username: str) -> str:
    body = ""
    
    with open("emails/Welcome/1.htm") as f:
        body += f.read()

    body += username

    with open("emails/Welcome/2.htm") as f:
        body += f.read()

    return body



###     MESSAGGIO DI NOTIFICA QUOTIDIANO    ###

def get_daily_notification_mail_subject(n_events: int) -> str:
    return f"Fermi Notifier - Daily notification ({n_events} eventi)"

def get_daily_notification_mail_body(receiver: dict, events: list) -> str:

    # DA RIVEDERE !!! TODO !!! NON HO UTILIZZATO txt_color !!!
    body = ""

    with open("emails/Daily-notification/1.htm") as f:
        body += f.read()
    
    body += receiver["name"]

    with open("emails/Daily-notification/2.htm") as f:
        body += f.read()

    body += str(len(events))

    with open("emails/Daily-notification/3.htm") as f:
            body += f.read()

    for i in events:
        bg_color, txt_color = get_event_colors()

        with open("emails/Daily-notification/4.1.htm") as f:
            body += f.read()

        body += bg_color

        with open("emails/Daily-notification/4.2.htm") as f:
            body += f.read()

        body += i["subject"]

        with open("emails/Daily-notification/4.3.htm") as f:
            body += f.read()
        
        body += bg_color

        with open("emails/Daily-notification/5.htm") as f:
            body += f.read()

        if i["startDate"]:
            body += f"""{i["startDate"][8:9]}-{i["startDate"][5:6]}-\
                {i["startDate"][:4]}"""
        else:
            body += f"""{i["startDateTime"][11:16]}"""

        with open("emails/Daily-notification/6.htm") as f:
            body += f.read()

        if i["endDate"]:
            body += f"""{i["endDate"][8:9]}-{i["endDate"][5:6]}-\
                {i["endDate"][:4]}"""
        else:
            body += f"""{i["endDateTime"][11:16]}"""

        with open("emails/Daily-notification/7.htm") as f:
            body += f.read()
        
    with open("emails/Daily-notification/8.htm") as f:
            body += f.read()

    return body


###    MESSAGGIO DI NOTIFICA LAST MINUTE    ###

def get_last_minute_notification_mail_subject():
    return "Fermi Notifier - Last Minute Notification"

def get_last_minute_notification_mail_body(receiver: dict, events: list) -> str:
    body = ""
    
    with open("emails/Last-minute-notification/1.htm") as f:
        body += f.read()

    body += receiver["name"]

    with open("emails/Last-minute-notification/2.htm") as f:
        body += f.read()

    body += "un evento" if len(events) == 1 else f"{len(events)} eventi"

    with open("emails/Last-minute-notification/3.htm") as f:
        body += f.read()

    for i in events:
        bg_color, txt_color = get_event_colors()

        with open("emails/Last-minute-notification/4.1.htm") as f:
            body += f.read()
        
        body += bg_color

        with open("emails/Last-minute-notification/4.2.htm") as f:
            body += f.read()

        body += i["subject"]

        with open("emails/Last-minute-notification/4.3.htm") as f:
            body += f.read()

        body += bg_color

        with open("emails/Last-minute-notification/4.4.htm") as f:
            body += f.read()

        body += txt_color

        with open("emails/Last-minute-notification/5.htm") as f:
            body += f.read()

        if i["startDate"]:
            body += f"""{i["startDate"][8:9]}-{i["startDate"][5:6]}-\
                {i["startDate"][:4]}"""
        else:
            body += f"""{i["startDateTime"][11:16]}"""

        with open("emails/Last-minute-notification/6.htm") as f:
            body += f.read()
        
        if i["endDate"]:
            body += f"""{i["endDate"][8:9]}-{i["endDate"][5:6]}-\
                {i["endDate"][:4]}"""
        else:
            body += f"""{i["endDateTime"][11:16]}"""

        with open("emails/Last-minute-notification/7.htm") as f:
            body += f.read()
    
    with open("emails/Last-minute-notification/8.htm") as f:
        body += f.read()

    return body


###############################################
#                                             #
#                                             #
#                  TELEGRAM                   #
#                                             #
#                                             #
###############################################

def get_daily_notification_tg_message(receiver: dict, events: list) -> str:
    body = ""
    body += f"""Ciao {receiver["name"]}, ecco il tuo daily roundup\n"""
    for _ in events:
        body += f"""Nome evento: `{_["subject"]}`\n"""
        body += "*Inizio*: "
        if _["startDate"] != None:
            body += f"""`{_["startDate"][8:9]}-{_["startDate"][5:6]}-\
                        {_["startDate"][:4]}`\n"""
        else:
            body += f"""`{_["startDateTime"][11:16]}`\n"""
        
        body += "*Fine*: "

        if _["endDate"] != None:
            body += f"""`{_["endDate"][8:9]}-{_["endDate"][5:6]}-\
                        {_["endDate"][:4]}`"""
        else:
            body += f"""`{_["endDateTime"][11:16]}`"""

    body += f"""\n\Buona giornata <3\nFermi Notifier Team.\n\
                servizi@matteobini.me"""

    return body


def get_last_minute_message(receiver: dict, events: list) -> str:
    # header
    body =  f"""Ciao {receiver["name"]}.\nAbbiamo trovato {len(events)} \
                eventi dell'ultimo minuto:\n"""

    for _ in events:
        body += f"""*Titolo*: `{_["subject"]}` \n"""
    
        # date/time begin
        if _["startDate"] != None:
            body += f"""*Inizio*: `{_["startDate"][8:]}-{_["startDate"][5:6]}-\
                        {_["startDate"][:3]}` \n"""
        else:
            body += f"""*Inizio*: `{_["startDateTime"][11:16]}` \n"""
        
        # date/time end
        if _["endDate"] != None:
            body += f"""*Fine*: `{_["endDate"][8:]}-{_["endDate"][5:6]}-\
                        {_["endDate"][:3]}` \n"""
        else:
            body += f"""*Fine*: `{_["endDateTime"][11:16]}` \n\n"""

    # footer
    body += f"""Ti auguriamo buon proseguimento di giornata.\n\n_Fermi \
        Notifier Team._ \nservizi@matteobini.me"""
    return body
