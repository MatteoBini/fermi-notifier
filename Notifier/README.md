`Development status`
# Notifier
Questa cartella contiene il codice in linguaggio Python che viene eseguito runtime sui server [Heroku](https://www.heroku.com/) (le indicazioni di esecuzione sono nel `Procfile`).

Lo scopo di questa codebase è gestire tutte le comunicazioni con l'utente.

## Operazioni di aggiornamento di iscritti e eventi `src/fermiCalendar.py`
La prima operazione che svolgo in loop è scaricare le informazioni degli  iscritti in un array di dizionari tramite la funzione `getSubscribers`.
Successivamente, necessiterò di abbinare ogni iscritto a tutti gli eventi che ha programmato per oggi (e che non siano già stati notificati) tramite la funzione `collect_notifications` che restituisce una lista di dizionari (che a loro interno contengono un ulteriore array di dizionari per gli eventi).
A questo punto, mi metto in contatto con ogni utente della lista tramite la funzione `deliver_notification`
## Fase di registrazione degli iscritti
Appena un utente inserisce un account di posta sulla Webapp per registrarsi al servizio, le informazioni di questo vengono inserite nel database regolarmente ma con il numero di notifiche impostato a -1 (e una stringa univoca casuale al posto dell'ID Telegram).
Solo dopo alla visita del link inviato con la mail di autenticazione questo numero verrà normalizzato a 0 e l'account verrà considerato registrato completamente. 
### Autenticazione account di posta elettronica `pending_registration`
Il codice python invia al futuro utente una mail con il link alla webapp. Il link è caratterizzato da una parte costante e un'ultima parte univoca: la stringa temporanea dell'ID Telegram. 
Quando il server riceverà una richiesta `http`/`https` con un ID già presente nel database, incrementerà il numero di notifiche dell'utente a 0, completandone la registrazione.
#### Mail di benvenuto `welcome_notification`
Quando questa funzione "vedrà" un utente con 0 notifiche, immediatamente gli invia una mail di benvenuto per comunicargli la conferma della registrazione.
Così, nel momento in cui l'utente effettua il log-in il numero di notifiche sarà impostato a 1.
### Abbinamento account Telegram `register_new_user`
La stringa univoca sostitutiva all'ID di Telegram presente nel database viene mostrata nella dashboard utente.
Quando l'utente invia un messaggio a `@ciin_gcalendar_bot` su Telegram contenente questo codice, grazie a questa funzione sarà possibile abbinare l'ID dell'utente al suo esistente profilo.
## Operazioni di notifica
Tramite la funzione `deliver_notification` eseguo le funzioni che gestiscono la notifica tramite i servizi email e, se impostato, Telegram. Infine, aggiungo gli eventi notificati al database (così che non vengano notificati più) tramite la funzione `db_notification` che riceve come parametri l'ID dell'utente e gli ID degli eventi di cui è stato notificato.

### Tipi di notifiche
Sia tramite email, sia eventualmente tramite Telegram, il servizio invia due tipi di notifiche:

 - **Daily notification**:  Notifica che arriva dalle 7.55 alle 8.10 e contiene tutti gli eventi della giornata dell'utente. È una notifica pensata per ricordare all'utente di tutti quegli eventi già fissati. Qualora non ci fossero eventi, questa notifica non verrà inviata.
 - **Last minute notification**: Notifica che arriva in qualsiasi momento e contiene eventuali eventi aggiunti in orario scolastico o comunque non segnati entro le 8.10. È una notifica pensata per far sapere all'utente tempestivamente eventuali nuovi eventi in giornata.
 
**Nessuna notifica verrà inviata prima dell'inizio della giornata scolastica alle 7.55**.

### Operazioni di notifica tramite e-mail `src/emailOperations.py`
Le operazioni di notifica via mail sono gestiti da una funzione principale (`email_notification`), che a sua volta esegue altre funzioni in base al tipo di notifica (last-minute/quotidiana). Tutte le iterazioni con il server di posta elettronica sono nel file indicato.
### Operazioni di notifica tramite Telegram `src/telegramOperations.py`
Le operazioni di notifica via mail sono gestiti da una funzione principale (`tg_notification`), che a sua volta esegue altre funzioni in base al tipo di notifica (last-minute/quotidiana). Tutte le iterazioni con Telegram sono nel file indicato.

## Varie
È presente un file `databaseOperations` per le operazioni che riguardano il database PostgreSQL che ho usato in tutto il progetto.

È presente un file di `utility` per generare i messaggi a partire da templeate standard. Contiene inoltre funzioni generiche.
