
# Fermi Notify
Questa repository contiene tutti i file del progetto [Fermi Notify](ferminotify.me).
Si tratta di 3 codebase con l'obiettivo di automatizzare parte del lavoro di chi frequenta l'[Istituto Superiore Fermi di Mantova](https://www.fermimn.edu.it).

Nello specifico, si tratta di un sistema di notifica relativo al calendario giornaliero. 
Dopo che l'utente abbia inserito una serie di parole chiave (keywords), quando queste compariranno sul calendario, verrà notificato con una email e/o con un messaggio diretto su Telegram.

I 3 sistemi che permettono il funzionamento del servizio sono:
 - **Webapp** per facilitare l'esperienza utente: una interfaccia grafica web sviluppata con Node.JS è disponibile a [ferminotify.me](ferminotify.me) per la registrazione e per la configurazione delle keywords.
 - **Scraper** per inserire gli eventi del calendario giornaliero in un [documento Google SpreadSheet](https://docs.google.com/spreadsheets/d/1b7Enw5zME2qPSeRXSIIQjhyKkv7qkRJPDsOCqyygvU4/edit?usp=sharing). 
 - **Notificatore** per comunicare con l'utente nel caso venga letta sul calendario giornaliero un evento in cui è coinvolto (in base alle keywords che ha impostato).

Il corretto funzionamento dell'intero sistema è dovuto alla presenza di un database PostgreSQL dotato di 2 tabelle:

 - **Subscribers** vengono memorizzati informazioni generali sull'utente (ID, nome, email, hashed password, keywords, codice univoco alfanumerico / ID telegram, etc.)
 - **Sent** vengono memorizzati per ogni utente, gli ID degli eventi che sono già stati notificati - per evitare che lo stesso evento venga notificato più volte allo stesso utente

*Fermi Notify Team*
[master@ferminotify.me](mailto:master@ferminotify.me)
