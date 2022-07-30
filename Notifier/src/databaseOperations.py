import os
from dotenv import load_dotenv
import psycopg2
from src.utility import *

class NotifierDB():
    # Operazioni di notifica email/telegram col database. Verranno usate 
    # in produzione solo le funzioni di richiesta dati (inserimento dati 
    # verrà fatto da sito).

    # Descrizione account status:
    # A : Novizio - non è stata inviata la mail di benvenuto
    # B : Utente a cui è stata inviata la mail di benvenuto
    # mantenibile


    def __init__(self):
        # Inizializzatore della connessione

        load_dotenv()
        HOSTNAME = os.getenv('HOSTNAME')
        DATABASE = os.getenv('DATABASE')
        USERNAME = os.getenv('USERNAME')
        PASSWORD = os.getenv('PASSWORD')
        PORT_ID = os.getenv('PORT_ID')

        self.Connection = psycopg2.connect(
            host = HOSTNAME,
            dbname = DATABASE,
            user = USERNAME,
            password = PASSWORD,
            port = PORT_ID,
        )

        self.Cursor = self.Connection.cursor()

    def closeConnection(self):
        # Chiude la connessione con il database

        self.Connection.close()
        return


    def getSubscribers(self):
        # Restituisce il database (lista di tuple)

        self.Cursor.execute(f"SELECT * FROM subscribers")
        response = self.Cursor.fetchall()
        self.Connection.commit()

        all_users = []
        for _ in response:
            user = {}
            user["id"] = _[0]
            user["name"] = _[1]
            user["surname"] = _[2]
            user["email"] = _[3]
            user["telegram"] = _[5]
            user["tags"] = _[6]
            user["n_not"] = _[7]
            
            all_users.append(user)

        return all_users

    def getSub(self):
        self.Cursor.execute(f"SELECT * FROM subscribers;")
        response = self.Cursor.fetchall()
        self.Connection.commit()

        all_elements = []
        for _ in response:
            all_elements.append(_)

        return(all_elements)

    def getUserSentId(self, user_id):
        # Query sucks but function works
        self.Cursor.execute("SELECT * FROM sent;")
        response = self.Cursor.fetchall()
        self.Connection.commit()

        all_id = []
        for _ in response:
            all_id.append(_[2])

        return all_id

    def incrementNumNot(self, user_id):
        self.Cursor.execute(f"""
            UPDATE subscribers
                SET notifications = notifications + 1
            WHERE id = {user_id};
        """)
        self.Connection.commit()
        
        return

    def updateTelegramId(self, user_email, telegram_id):
        self.Cursor.execute(f"""
            UPDATE subscribers
                SET telegram = '{telegram_id}'
            WHERE subscribers.email = '{user_email}';
        """)
        self.Connection.commit()
        return

    def storeNotification(self, user_id, event_id):
        pattern = "INSERT INTO sent(sub_id, evt) VALUES (%s, %s)"
        self.Cursor.execute(pattern, (user_id, event_id))
        self.Connection.commit()
        
        return

def storeSent(user_id, event_id):
    DB = NotifierDB()
    DB.storeNotification(user_id, event_id)
    DB.closeConnection()

    return

def getUserSentId(user_id):
    DB = NotifierDB()
    k = DB.getUserSentId(user_id)
    DB.closeConnection

    return k

def incrementNumNot(user_id):
    DB = NotifierDB()
    DB.incrementNumNot(user_id)
    DB.closeConnection()
    return

def getSubscribers():
    DB = NotifierDB()
    k = DB.getSubscribers()
    DB.closeConnection()

    return k

def updateTelegramId(user_email, telegram_id):
    DB = NotifierDB()
    DB.updateTelegramId(user_email, telegram_id)
    DB.closeConnection()

def db_notification(user_id, notified_events):
    for _ in notified_events:
        storeSent(user_id, _["id"])
        incrementNumNot(user_id)
    return
