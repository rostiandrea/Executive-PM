---
name: CreaASUPPORT
description: Apre in autonomia una richiesta (ticket) sul portale SU&GO Arcese (https://aplatform.arcese.com/support). Usare quando l'utente chiede di aprire un ticket/richiesta/segnalazione sul portale Arcese SU&GO, indicando descrizione, applicativo e tipo (request o bug).
---

# CreaASUPPORT — Apertura ticket sul portale SU&GO Arcese

## Scopo

Questa skill permette di aprire autonomamente un ticket di supporto sul portale
Arcese SU&GO (https://aplatform.arcese.com/support), seguendo esattamente la
procedura mostrata da Andrea passo-passo il 28/08/2026.

## Informazioni obbligatorie prima di iniziare

Quando l'utente chiede di aprire un ticket, servono sempre tre informazioni:

1. **Descrizione** della richiesta o del problema (eventualmente accompagnata
   da file/documenti di dettaglio che l'utente allega alla conversazione).
2. **Applicativo di riferimento** (es. BI Manager, SGA, Arcese.Net, Arcese.Web,
   D365 FO, D365 CE, Arcese WMS, ecc.).
3. **Tipo di richiesta**: "request" (nuova richiesta o piccola modifica) oppure
   "bug" (segnalazione di malfunzionamento).

Se anche una sola di queste tre informazioni manca, chiedila esplicitamente
all'utente prima di procedere. Non inventare o assumere questi dati.

## Prerequisiti

- L'utente deve essere già loggato sul portale (https://aplatform.arcese.com).
  Il login (credenziali) non va mai gestito in autonomia: se l'utente non è
  loggato, chiedigli di autenticarsi lui stesso nel browser.

## Procedura passo-passo

1. Vai alla pagina https://aplatform.arcese.com/support.
2. Clicca sull'icona a griglia (9 puntini) situata a destra della barra di
   ricerca "How can I help you?" per aprire l'elenco delle categorie
   principali.
3. Seleziona la categoria principale:
   - **"Transformation and Technology"** → default per qualunque richiesta
     tecnica/applicativa (usare sempre questa a meno che l'utente non chieda
     esplicitamente qualcosa relativo a "People", cioè servizi HR).
   - "People" → solo se l'utente lo richiede esplicitamente (servizi HR).
4. All'interno di "Transformation and Technology" scegli la sottocategoria in
   base all'applicativo indicato dall'utente. Il caso più comune (default) è:
   - **"Programs and Applications"** (Office 365, browser, SGA, Arcese.NET,
     WMS, BI Manager, ecc.)
   Altre sottocategorie disponibili: "PCs, smartphones, and company
   peripherals", "Internet/Intranet Connectivity", "Cybersecurity", "Accounts
   and Passwords", "General" (usale solo se l'ambito della richiesta
   corrisponde chiaramente a una di queste invece che a Programs and
   Applications).
5. Dentro "Programs and Applications" (o la sottocategoria scelta) ci sono
   sempre due schede, identiche per struttura ma con significato diverso:
   - **"Do you want to make a request regarding ...?"** → usare per tipo =
     **request** (nuove richieste, installazioni, modifiche). Questo è il
     default se l'utente non specifica che si tratta di un bug.
   - **"Do you want to report a problem with ...?"** → usare per tipo =
     **bug** (malfunzionamenti, errori, segnalazioni). Usare solo se
     l'utente lo chiede esplicitamente.
   La schermata del form successiva è identica in entrambi i casi.
6. Compila il form con i seguenti campi:
   - **Titolo** (obbligatorio): riassumi in una riga la richiesta, includendo
     applicativo e contesto/cliente se rilevante. Esempio: "Richiesta nuovo
     report BI Manager - Date Consegna CD (Christian Dior)".
   - **Seleziona Applicazione** (obbligatorio): clicca sul menu a tendina,
     scrivi nel campo filtro il nome dell'applicativo indicato dall'utente e
     seleziona la voce corrispondente dalla lista (es. "BI Manager", "SGA",
     "Arcese.Net", "D365 FO", ecc.).
   - **Descrizione della richiesta** (obbligatorio): scrivi una descrizione
     completa e strutturata basata su quanto detto dall'utente e su eventuali
     file allegati/condivisi (leggili prima per estrarne i dettagli). Se
     disponibili, includi: descrizione generale, BU/area, destinatari,
     frequenza, sistema sorgente, regole/filtri, campi richiesti, ecc. Chiudi
     con una riga tipo "In allegato il documento di dettaglio dei requisiti"
     se è stato allegato un file.
7. **Allegati**: il bottone "Allega file" apre il file picker nativo del
   sistema operativo, NON raggiungibile dagli strumenti di automazione
   browser. Quindi, ogni volta che serve allegare un file:
   - Chiedi all'utente di cliccare lui stesso su "Allega file" (indica quale
     dei 3 slot, di solito il primo libero) e di selezionare il file dal
     proprio computer.
   - Aspetta la sua conferma/il suo messaggio che conferma l'allegato fatto
     (comparirà come chip con nome file e icona) prima di proseguire.
8. **STOP obbligatorio prima di inviare**: mostra sempre all'utente un
   riepilogo di Titolo, Applicazione selezionata, Descrizione e allegati
   presenti, e ASPETTA una conferma esplicita ("ok", "vai", "invia", ecc.)
   prima di cliccare "Invia". Non cliccare mai "Invia" di tua iniziativa.
9. Dopo la conferma esplicita dell'utente, clicca "Invia".
   - Il backend (BMC Helix, caricato in un iframe di dominio esterno) può
     essere lento: dopo il click aspetta almeno 5-10 secondi prima di
     considerare il tentativo fallito o di ricliccare.
   - NON cliccare ripetutamente "Invia" in rapida successione: se il form
     sembra "bloccato"/senza risposta, aspetta di più invece di ricliccare
     subito, per evitare il rischio (anche se non osservato finora) di creare
     ticket duplicati.
   - Il successo è confermato esclusivamente da questa schermata: un'icona a
     spunta verde (✓) con il testo **"Your ticket has been successfully
     created!"**. Solo quando vedi questa schermata puoi confermare
     all'utente che il ticket è stato aperto con successo. Se non compare,
     segnala il problema all'utente invece di assumere che sia andato a buon
     fine.
10. (Facoltativo) Per verificare il ticket appena creato, apri il pannello
    "My tickets" (icona con freccia in alto a destra della pagina, oppure il
    bottone "Open support tab") e controlla la tab "In progress": dovrebbe
    comparire il nuovo ticket con numero (es. "INC000000150493"), titolo,
    stato, data di creazione.

## Preferenze note di Andrea

- Categoria di default: **Transformation and Technology > Programs and
  Applications**, a meno che non specifichi diversamente.
- Scheda di default dentro Programs and Applications: **"make a request"**
  (nuova richiesta/modifica). Usa **"report a problem"** solo se Andrea
  chiede esplicitamente di segnalare un bug.

## Limiti noti / cose da NON fare

- Non è possibile allegare file in autonomia: il file picker è nativo del
  sistema operativo e non è raggiungibile dagli strumenti di automazione
  browser. Chiedi sempre all'utente di allegare lui stesso.
- Non gestire mai le credenziali di login: l'utente deve autenticarsi da solo
  sul portale prima di iniziare la procedura.
- Non cliccare mai "Invia" senza una conferma esplicita dell'utente sul
  contenuto del form.
- Non considerare mai un ticket come creato senza aver visto la schermata di
  conferma con la spunta verde "Your ticket has been successfully created!".
