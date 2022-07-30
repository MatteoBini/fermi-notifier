import pandas as pd
from src.databaseOperations import getUserSentId
from datetime import datetime
from src.utility import *

def getEvents():
    # Get events from Google Sheets (format output: csv).
    # Google Script gets calendar events thru API without oauth
    # and put them in the google sheet automatically. 
    # My g script also delete them the day after to optimize the
    # operations.
    URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSn-iVUb73XGXN7qWU0S2njYO8yl8LFv0V-1a3VTU7mPB6rJUqYasGPJcmWyc1wGvjDd7IWH3qci75l/pub?gid=0&single=true&output=csv"

    data = []
    try:
        data = pd.read_csv(URL, sep=',')
        data = data.to_numpy(na_value=None) # Parameter means that I convert nan obj (np.nan class) in None variables to manipulate them
    except:
        pass
    

    all_events = []
    for _ in data:
        evt = {}
        evt["id"] = _[0]
        evt["subject"] = _[1]
        evt["desc"] = _[2]
        evt["startDate"] = _[3]
        evt["startDateTime"] = _[4]
        evt["startTimeZone"] = _[5]
        evt["endDate"] = _[6]
        evt["endDateTime"] = _[7]
        evt["endTimeZone"] = _[8]

        all_events.append(evt)
    
    return all_events

def collect_notifications(subs):
    # Return list of notifications to be sent
    events = getEvents()
    notifications = []
    
    for sub in subs:
        usrKw = sub["tags"]
        sent = getUserSentId(sub["id"])
        user_events = []

        for evt in events:
            
            if usrKw != None:
                kwInSubject = any(i.lower() in evt["subject"].lower() for i in usrKw)
                evtNotInDB = evt["id"] not in sent
                        
                if kwInSubject and evtNotInDB and isEventToday(evt):
                    user_events.append(evt)

        if len(user_events) > 0:
            notifications.append({
                "id": sub["id"],
                "name": sub["name"],
                "email": sub["email"],
                "telegram": sub["telegram"],
                "events": user_events
            })

    return notifications
