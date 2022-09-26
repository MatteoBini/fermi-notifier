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
    is_notification_time = time(6,00) < datetime.now().time()

    return (event_is_today and is_notification_time)

def get_event_color() -> str:
    # Returns a RBG color for event card in the emails

    colors = [
        "#1B5E20", "#FF6F00", "#1A237E", "#BF360C", "#01579B", "#33691E",
        "#880E4F", "#E65100", "#311B92", "#B71C1C", "#004D40", "#F57F17",
        "#0D47A1", "#827717", "#006064", "#4A148C", 
    ]

    return choice(colors)

def get_pronominal_particle(gender) -> str:
    if gender == 'M':
        return 'o'
    elif gender == 'F':
        return 'a'
    else:
        return 'ǝ'

def get_mail_raw() -> str:
    return "Ci sono nuovi eventi che ti coinvolgono sul calendario giornaliero"

###############################################
#                                             #
#                                             #
#                    EMAIL                    #
#                                             #
#                                             #
###############################################

###      ACCOUNT CONFIRMATION EMAIL      ###

def get_registration_mail_subject() -> str:
    return "Fermi Notify - Confirm registration"

def get_registration_mail_body(name: str, verification_code: str) -> str:
    body = ""

    with open("emails/Confirm-registration/01.htm") as f:
        body += f.read()

    body += name

    with open("emails/Confirm-registration/02.htm") as f:
        body += f.read()

    body += verification_code

    with open("emails/Confirm-registration/03.htm") as f:
        body += f.read()

    body += verification_code

    with open("emails/Confirm-registration/04.htm") as f:
        body += f.read()
    
    body += verification_code

    with open("emails/Confirm-registration/05.htm") as f:
        body += f.read()

    return body



###          WELCOME EMAIL         ###

def get_welcome_mail_subject() -> str:
    return "Fermi Notify - Welcome!"

def get_welcome_mail_body(user: dict) -> str:
    body = ""
    
    with open("emails/Welcome/01.htm") as f:
        body += f.read()

    body += user["name"]

    with open("emails/Welcome/02.htm") as f:
        body += f.read()

    body += get_pronominal_particle(user["gender"])

    with open("emails/Welcome/03.htm") as f:
        body += f.read()

    body += get_pronominal_particle(user["gender"])
    
    with open("emails/Welcome/04.htm") as f:
        body += f.read()

    body += get_pronominal_particle(user["gender"])

    with open("emails/Welcome/05.htm") as f:
        body += f.read()

    return body



###     DAILY NOTIFICATION EMAIL    ###

def get_daily_notification_mail_subject(n_events: int) -> str:
    subject = f"Fermi Notify - Daily notification ({n_events} "
    subject += f"event{'i' if n_events > 1 else 'o'})"
    return subject
    

def get_daily_notification_mail_body(receiver: dict, events: list) -> str:
    body = ""

    with open("emails/Daily-notification/01.htm") as f:
        body += f.read()
    
    body += receiver["name"]

    with open("emails/Daily-notification/02.htm") as f:
        body += f.read()

    body += str(len(events))

    with open("emails/Daily-notification/03.htm") as f:
            body += f.read()

    for i in events:
        card_color = get_event_color()

        with open("emails/Daily-notification/04.htm") as f:
            body += f.read()

        body += card_color

        with open("emails/Daily-notification/05.htm") as f:
            body += f.read()

        body += i["subject"]

        with open("emails/Daily-notification/06.htm") as f:
            body += f.read()

        if i["startDate"]:
            body += f"""{i["startDate"][8:9]}-{i["startDate"][5:6]}"""
            body += f"""-{i["startDate"][:4]}"""
        else:
            body += f"""{i["startDateTime"][11:16]}"""

        with open("emails/Daily-notification/07.htm") as f:
            body += f.read()

        if i["endDate"]:
            body += f"""{i["endDate"][8:9]}-{i["endDate"][5:6]}"""
            body += f"""-{i["endDate"][:4]}"""
        else:
            body += f"""{i["endDateTime"][11:16]}"""

        with open("emails/Daily-notification/08.htm") as f:
            body += f.read()
        
    with open("emails/Daily-notification/09.htm") as f:
            body += f.read()

    return body


###    LAST MINUTE EMAIL NOTIFICATION    ###

def get_last_minute_notification_mail_subject():
    return "Fermi Notify - Last Minute Notification"

def get_last_minute_notification_mail_body(receiver: dict, events: list) -> str:
    body = ""
    
    with open("emails/Last-minute-notification/01.htm") as f:
        body += f.read()

    body += receiver["name"]

    with open("emails/Last-minute-notification/02.htm") as f:
        body += f.read()

    body += f"{len(events)} event{'i' if len(events) > 1 else 'o'}"

    with open("emails/Last-minute-notification/03.htm") as f:
        body += f.read()

    for i in events:
        card_color = get_event_color()

        with open("emails/Last-minute-notification/04.htm") as f:
            body += f.read()
        
        body += card_color

        with open("emails/Last-minute-notification/05.htm") as f:
            body += f.read()

        body += i["subject"]

        with open("emails/Last-minute-notification/06.htm") as f:
            body += f.read()

        if i["startDate"]:
            body += f"""{i["startDate"][8:9]}-{i["startDate"][5:6]}-\
                {i["startDate"][:4]}"""
        else:
            body += f"""{i["startDateTime"][11:16]}"""

        with open("emails/Last-minute-notification/07.htm") as f:
            body += f.read()
        
        if i["endDate"]:
            body += f"""{i["endDate"][8:9]}-{i["endDate"][5:6]}-\
                {i["endDate"][:4]}"""
        else:
            body += f"""{i["endDateTime"][11:16]}"""

        with open("emails/Last-minute-notification/08.htm") as f:
            body += f.read()
    
    with open("emails/Last-minute-notification/09.htm") as f:
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

    body += f"""Ciao {receiver["name"]}, ecco il tuo daily roundup:\n"""

    for _ in events:
        body += f"""\n· `{_["subject"]}`"""
        body += "\n· *Inizio* ⏰ "
        if _["startDate"] != None:
            body += f"""`{_["startDate"][8:9]}-{_["startDate"][5:6]}-\
                        {_["startDate"][:4]}`"""
        else:
            body += f"""`{_["startDateTime"][11:16]}`"""

        body += "\n· *Fine* 🔚 "

        if _["endDate"] != None:
            body += f"""`{_["endDate"][8:9]}-{_["endDate"][5:6]}-\
                        {_["endDate"][:4]}`\n"""
        else:
            body += f"""`{_["endDateTime"][11:16]}`\n"""
        
    body += "\nBuona giornata <3\n_Fermi Notify Team_\n"
    body += "master@ferminotify.me"

    return body


def get_last_minute_message(receiver: dict, events: list) -> str:
    # header
    body =  f"""Ciao {receiver["name"]}.\nAbbiamo trovato {len(events)} """
    body += f"event{'i' if len(events) > 1 else 'o'} dell'ultimo minuto:\n"

    for _ in events:
        body += f"""*Titolo*: `{_["subject"]}` \n"""
    
        # date/time begin
        if _["startDate"] != None:
            body += f"""*Inizio*: `{_["startDate"][8:]}-"""
            body += f"""{_["startDate"][5:6]}-{_["startDate"][:3]}`\n"""
        else:
            body += f"""*Inizio*: `{_["startDateTime"][11:16]}` \n"""
        
        # date/time end
        if _["endDate"] != None:
            body += f"""*Fine*: `{_["endDate"][8:]}-"""
            body += f"""{_["endDate"][5:6]}-{_["endDate"][:3]}` \n"""
        else:
            body += f"""*Fine*: `{_["endDateTime"][11:16]}` \n\n"""

    # footer
    body += f"""Ti auguriamo buon proseguimento di giornata.\n\n"""
    body += f"""_Fermi Notify Team_ \nmaster@ferminotify.me"""
    return body
