    WIP

# Fermi Notifier
Questa repository contiene tutti i file del progetto [Fermi Notifier](servizi.matteobini.me/fermi-notifier). Si tratta di 3 codebase con l'obiettivo di automatizzare parte del lavoro di chi frequenta l'[istituto Fermi di Mantova](https://www.fermimn.edu.it).

Nello specifico, si tratta di un sistema di notifica relativo al calendario giornaliero. 
Dopo che l'utente abbia inserito una serie di parole chiave, quando queste compariranno sul calendario, l'utente verrà notificato con una email e, se lo desidera, con un messaggio diretto su Telegram.

I 3 sistemi che permettono il funzionamento del servizio sono:
 - **Webapp** per facilitare l'esperienza utente: una interfaccia grafica web sviluppata con Node.JS è disponibile a [servizi.matteobini.me/fermi-notifier](servizi.matteobini.me/fermi-notifier). Non vi sono altri metodi per effettuare registrarsi al servizio se non chiedere supporto a [servizi@matteobini.me](mailto:servizi@matteobini.me).
 - **Scraper** per inserire gli eventi del calendario giornaliero in un [documento Google SpreadSheet](https://docs.google.com/spreadsheets/d/1b7Enw5zME2qPSeRXSIIQjhyKkv7qkRJPDsOCqyygvU4/edit?usp=sharing). 
 - **Notificatore** per comunicare con l'utente nel caso venga letta sul calendario giornaliero un evento in cui è coinvolto (in base alle parole chiave che ha impostato).

Il corretto funzionamento dell'intero sistema è dovuto alla presenza di un database PostgreSQL dotato di 2 tabelle:

 - **Subscribers** vengono memorizzati informazioni generali sull'utente (id, nome, email, hashed password, keywords, codice univoco alfanumerico / id telegram, etc.)
 - **Sent** vengono memorizzati per ogni utente, gli id degli eventi che sono già stati notificati - per evitare che lo stesso evento venga notificato più volte allo stesso utente

*Fermi Notifier Team*
[servizi@matteobini.me](mailto:servizi@matteobini.me)
