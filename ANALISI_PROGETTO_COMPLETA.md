---
title: Progetto Ingegneria del Software
date: \today
titlepage: true
toc: true
toc-own-page: true
---

# Analisi Completa del Progetto Smart Home

## 1. Obiettivo del Progetto

Realizzare un sistema Smart Home con interfaccia centralizzata che consenta di:

- gestire stanze, dispositivi e automazioni
- controllare lo stato operativo della casa
- registrare e consultare gli eventi di sistema
- eseguire backup e analisi statistiche.

---

## 2. Attori e Permessi

### Attori principali

- **Utente**
- **Amministratore**
- **Tempo**

### Regole di accesso

- L'**Utente** gestisce: stanze (CRUD), dispositivi (CRUD + comandi), automazioni (CRUD), monitoraggio/statistiche.
- L'**Amministratore** può fare tutto ciò che fa l'Utente e in più può consultare/esportare lo storico eventi.
- Il trigger temporale è usato per scenari automatici (es. esecuzione automazioni, backup automatico nei diagrammi dedicati).

### Diagramma attori

![Attori](image/attori.png)


---

## 3. Casi d'Uso

### 3.1 Elenco casi d'uso principali

| ID | Caso d'Uso | Attori coinvolti |
|---|---|---|
| UC1 | Accesso e dashboard | Utente, Amministratore |
| UC2 | Gestione stanze (CRUD) | Utente, Amministratore |
| UC3 | Gestione dispositivi (CRUD) | Utente, Amministratore |
| UC4 | Controllo dispositivi | Utente, Amministratore |
| UC5 | Gestione automazioni (CRUD) | Utente, Amministratore |
| UC6 | Consultazione storico eventi | Amministratore |
| UC7 | Gestione backup | Amministratore |
| UC8 | Monitoraggio e statistiche | Utente, Amministratore |

### 3.2 Vista per Utente

Contiene solo i casi d'uso operativi dell'Utente.

![Gestione utilizzatore](image/gestione_utilizzatore.png)


### 3.3 Vista per Amministratore

Contiene i casi d'uso dell'Amministratore, inclusa la consultazione storico eventi.

![Gestione amministratore](image/gestione_amministratore.png)

### 3.4 Vista sistema e monitoraggio

Focalizzata su backup/monitoraggio e registrazione eventi.

![Gestione sistema](image/gestione_sistema.png)


---

## 4. Requisiti Funzionali

### 4.1 Requisiti principali

- **Gestione casa**: visualizzazione e CRUD stanze, associazione dispositivi.
- **Gestione dispositivi**: visualizzazione, controllo comandi, aggiornamento stato, rilevamento offline.
- **Gestione automazioni**: inserimento, modifica, attivazione/disattivazione, valutazione/esecuzione.
- **Gestione storico**: consultazione, filtro, esportazione eventi.
- **Gestione sistema**: statistiche, backup, notifiche/eventi.

### 4.2 Diagramma requisiti

![Dettaglio requisiti](image/dettaglio_requisiti.png)

### 4.3 Matrice di mapping

| Requisito | UC1 | UC2 | UC3 | UC4 | UC5 | UC6 | UC7 | UC8 |
|---|---|---|---|---|---|---|---|---|
| RF1 - Visualizza stanze | X | X |  |  |  |  |  |  |
| RF2 - CRUD stanze |  | X |  |  |  |  |  |  |
| RF3 - Associa dispositivi alle stanze |  | X | X |  |  |  |  |  |
| RF4 - Visualizza dispositivi | X |  | X |  |  |  |  | X |
| RF5 - Controlla dispositivi |  |  |  | X |  |  |  |  |
| RF6 - Aggiorna stato dispositivo |  |  | X | X |  |  |  |  |
| RF7 - Rileva dispositivi offline |  |  | X |  |  |  |  | X |
| RF8 - Inserisci automazione |  |  |  |  | X |  |  |  |
| RF9 - Modifica automazione |  |  |  |  | X |  |  |  |
| RF10 - Attiva/disattiva automazione |  |  |  |  | X |  |  |  |
| RF11 - Valuta automazioni |  |  |  |  | X |  |  | X |
| RF12 - Consulta log eventi |  |  |  |  |  | X |  |  |
| RF13 - Filtra log |  |  |  |  |  | X |  |  |
| RF14 - Esporta log |  |  |  |  |  | X |  |  |
| RF15 - Genera statistiche |  |  |  |  |  |  |  | X |
| RF16 - Backup automatico |  |  |  |  |  |  | X |  |
| RF17 - Gestisci notifiche/eventi | X |  |  |  |  | X |  | X |


---

## 5. Architettura Logica

Il sistema segue una struttura a strati:

- **Presentazione** (Viste)
- **Applicazione** (Controllori)
- **Servizi** (Logica di business)
- **Persistenza** (Repository JSON)

### 5.1 Diagramma classi applicative

![Classi applicative](image/classi_applicative.png)


### 5.2 Diagramma classi di dominio

Definisce le entità principali del modello Smart Home.

![Classi dominio](image/classi_dominio.png)


### 5.3 Diagramma classi repository

Mostra interfacce repository e implementazioni JSON.

![Classi repository](image/classi_repository.png)


---

## 6. Diagrammi di Sequenza

I diagrammi di sequenza descrivono i flussi principali end-to-end.

### 6.1 Accesso e dashboard

![Sequenza accesso dashboard](image/diagramma_sequenza_accesso_dashboard.png)


### 6.2 Gestione stanze e dispositivi

![Sequenza gestione stanze e dispositivi](image/diagramma_sequenza_gestione_stanze_dispositivi.png)


### 6.3 Controllo dispositivo

![Sequenza controllo dispositivo](image/diagramma_sequenza_controllo_dispositivo.png)


### 6.4 Gestione automazioni

![Sequenza gestione automazioni](image/diagramma_sequenza_configura_automazione.png)


### 6.5 Esecuzione automazioni

![Sequenza esecuzione automazione](image/diagramma_sequenza_esecuzione_automazione.png)


### 6.6 Consultazione storico eventi (solo Amministratore)

![Sequenza consultazione storico](image/diagramma_sequenza_consulta_storico.png)


### 6.7 Backup automatico

![Sequenza backup automatico](image/diagramma_sequenza_backup_automatico.png)


### 6.8 Monitoraggio e statistiche

![Sequenza monitoraggio e statistiche](image/diagramma_sequenza_monitoraggio_statistiche.png)


---

## 7. Diagrammi di Attività

I diagrammi di attività evidenziano il flusso operativo delle funzionalità.

![Attività accesso dashboard](image/diagramma_attivita_accesso_dashboard.png)

![Attività gestione stanze](image/diagramma_attivita_gestione_stanze.png)

![Attività controllo dispositivo](image/diagramma_attivita_controllo_dispositivo.png)

![Attività configurazione automazione](image/diagramma_attivita_configura_automazione.png)

![Attività esecuzione automazione](image/diagramma_attivita_esecuzione_automazione.png)

![Attività consultazione storico](image/diagramma_attivita_consulta_storico.png)

![Attività backup automatico](image/diagramma_attivita_backup_automatico.png)

![Attività monitoraggio e statistiche](image/diagramma_attivita_monitoraggio_statistiche.png)


---

## 8. Package di Analisi

Vista modulare complessiva e per sottoinsiemi funzionali.

![Package analisi reale](image/package_analisi_reale.png)
![Package analisi attività](image/package_analisi_attivita.png)
![Package analisi servizio](image/package_analisi_servizio.png)