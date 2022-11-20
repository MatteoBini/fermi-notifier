from random import choice

def get_event_color() -> str:
    # Returns a RBG color for event card in the emails

    colors = [
        "#1B5E20", "#FF6F00", "#1A237E", "#BF360C", "#01579B", "#33691E",
        "#880E4F", "#E65100", "#311B92", "#B71C1C", "#004D40", "#F57F17",
        "#0D47A1", "#827717", "#006064", "#4A148C", 
    ]

    return choice(colors)

def get_daily_notification_mail_body(receiver: dict, events: list) -> str:
    body = ""

    with open("01.htm", encoding="utf8") as f:
        body += f.read()
    
    body += receiver["name"]

    with open("02.htm", encoding="utf8") as f:
        body += f.read()

    body += str(len(events))

    with open("03.htm", encoding="utf8") as f:
            body += f.read()

    for i in events:
        card_color = get_event_color()

        with open("04.htm", encoding="utf8") as f:
            body += f.read()

        body += card_color

        with open("05.htm", encoding="utf8") as f:
            body += f.read()

        body += i["subject"]

        with open("06.htm", encoding="utf8") as f:
            body += f.read()

        if i["startDate"]:
            body += f"""{i["startDate"][8:9]}-{i["startDate"][5:6]}"""
            body += f"""-{i["startDate"][:4]}"""
        else:
            body += f"""{i["startDateTime"][11:16]}"""

        with open("07.htm", encoding="utf8") as f:
            body += f.read()

        if i["endDate"]:
            body += f"""{i["endDate"][8:9]}-{i["endDate"][5:6]}"""
            body += f"""-{i["endDate"][:4]}"""
        else:
            body += f"""{i["endDateTime"][11:16]}"""

        with open("08.htm", encoding="utf8") as f:
            body += f.read()
        
    with open("09.htm", encoding="utf8") as f:
            body += f.read()

    return body

events = [
    {
                'id': '175kism1teadmku9if9q5kr969', 
                'subject': 'CLASSE 3AIIN - AULA 16 - CORSO RECUPERO INGLESE - PROF. NOMEPROF', 
                'desc': None, 
                'startDate': None, 
                'startDateTime': '2022-07-19T12:00:00+02:00', 
                'startTimeZone': 'Europe/Rome', 
                'endDate': None, 
                'endDateTime': '2022-07-19T13:00:00+02:00', 
                'endTimeZone': 'Europe/Rome'
    }
]

user = {
        "id": 'id',
        "name": "name",
        "email": "email"
}

body = get_daily_notification_mail_body(user, events)

with open("test.htm", "w") as f:
	f.write(body)
