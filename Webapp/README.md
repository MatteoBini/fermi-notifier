
# WebApp
Questa cartella contiene il codice in linguaggio javascript ([Node.JS](https://nodejs.org/)) della webapp.

I file contenuti nella cartella "public" sono accessibili direttamente dal web (la usiamo per fogli di stile, immagini, etc.).

I file contenuti nella cartella "views" sono [template EJS](https://ejs.co/), ovvero file che vengono letti dal programma principale (server.js) e generati in base all'utente e alle informazioni fornite. 

Il file `passportConfig.js` gestisce i cookie e le impostazioni sui login/logout.

Il file `dbConfig.js` gestisce la connessione con il database.

Per eseguire:
`node server.js`
che gestirà tutte le richieste grazie al framework [Express](https://expressjs.com/).
