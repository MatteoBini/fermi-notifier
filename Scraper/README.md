
# Scraper
Questa cartella contiene codice in linguaggio google script, implementato nel documento [calendar-spreadsheet](https://docs.google.com/spreadsheets/d/1b7Enw5zME2qPSeRXSIIQjhyKkv7qkRJPDsOCqyygvU4/edit?usp=sharing). 
La codebase in python, riesce ad accedere al documento tramite uno speciale link che restituisce la tabella in formato `csv`.

Questo scraper ha come prima funzione principale (`listUpcomingEvents`) la estrazione delle informazioni rilevanti di tutti gli eventi presenti nel calendario giornaliero. Ogni riga dello spreadsheet rappresenta un evento. Ho impostato nell'IDE fornita da google, l'esecuzione automatica ogni 5 minuti.

La seconda funzione principale (`removeOldEvents`) si occupa invece dell'eliminazione degli eventi passati, così da ottimizzare il lavoro svolto dalla codebase in python su vasta scala. Questa funzione controlla la eventuale scadenza dei primi 500 eventi in tabella (eventuali  eventi successivi diventano non eliminabili automaticamente). Ho impostato nell'IDE fornita da google, l'esecuzione automatica ogni notte dopo mezzanotte (CET/CEST).

La parte più delicata di questo script coinvolge la gestione della tabella: è importante stabilire bene i range da eliminare/sovrascrivere, a questo proposito vi è la funzione `getRangeString` preposta appunto a generare, nel corretto formato, il range di tabella che si può sovrascrivere/estrarre.

Altre funzioni come `isoToDate`, `getTomorrow` e `getYesterday` restituiscono date in un formato oggetto che ne semplifica le operazioni. 
NB: `getTomorrow` e `getYesterday` non restituiscono esattamente domani e oggi, ma gli estremi da tenere in considerazione per l'importazione/eliminazione degli eventi. `isoToDate` si occupa della conversione delle stringhe degli eventi da [standard ISO](https://en.wikipedia.org/wiki/ISO_8601) al formato oggetto che utilizzo nel resto del codice.
