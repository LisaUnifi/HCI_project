# Exif Viewer 
>Cose...

## Table of Contents
* [General Info](#general-information)
* [Installation](#installation)
* [Overview](#overview)
* [Tools and Techniques](#tools-and-techniques)
* [Features](#features)
* [Extra Features](#extra-features)
* [More](#more)


## General Information
- Anno accademico: 2021-2022
- Titolo: Exif Viewer
- Studente: Lisa Cresti 


## Installation
Per quanto riguarda l'installazione, riferirsi al README del progetto **Mattoni 2.0**.
Una volta conclusa l'installazione apparirà la pagina principale: in basso, sul footer, sarà possibile cliccare su "Lisa Cresti" per accedere alla paginna principale del progetto. 


## Tools and Techniques
...


## Features
Di seguito andrò ad analizzare e spiegare le features implementate.

#### Visualization of images
L'interfaccia supporta la visualizzazione delle immagini. Queste mantengono le proporzioni originali ma vengono scalate per essere visualizzate sullo schermo ad una larghezza o altezza massima di 512px. 

#### Visualization of image EXIF data
Insieme alla visualizzazione dell'immagine, appaiono alla nostra destra due tabelle contenenti rispettivamente: 
- dati generali dell'immagine, cioè quelli scelti in fase di caricamento,
- dati EXIF.
Per la generazione dei dati EXIF mi sono avvalsa della libreria [exif](https://pypi.org/project/exif/) di Python. Tramite questa libreria è possibile leggere e modificare gli exif di una immagine. 
...


#### Rescaling 
È possibile fare il rescaling dell'interfaccia: l'immagine mantiene la proporzione originale e le dimensioni imposte dall'applicativo (altezza o larghezza massima di 512px) mentre invece la posizione dei dati dell'immagine si adatta alla grandezza della finestra. Nel caso la finestra sia più di ...px in larghezza e più di ...px in altezza, immagine e tabelle dei dati si troveranno sulla stessa riga ma in due colonne separate, mentre invece nel caso opposto, immagine e tabelle si troveranno una dopo l'altra.


#### Image rotation
L'applicazione supporta la rotazione delle immagini tramite i bottoni ... e ..., che si trovano al di sotto dell'immagine principale, oppure tramite tastiera grazie alla combinazione di tasti ALT+... per ruotare a destra di 90° e ALT+... per ruotare a sinistra di 90°.


## Extra features


#### Geolocalization
Se nell'immagine sono presenti i tag GPS è possibile, premendo il bottone ..., aprire Google Maps con le seguenti caratteristiche:
- una mappa centrata nel punto specifico riportato dalle coordinate estratte dai dati exif e segnalato dalla goccia rossa di google map
- una mappa centrata nel punto specifico ma con la possibilità di poter scegliere lo zoom, la tipologia di mappa e se si vuole visualizzare dei livelli aggiuntivi
- il panorama che si vede dal punto con la possibilità di settare l'angolo della camera e il campo visivo.
Nel caso in cui i tag GPS non siano presenti non sarà quindi possibile visualizzare la mappa ma verrà visualizzato un messaggio che ci avvertirà dell'assenza di questi dati.


#### View multiple images
L'applicativo supporta la memorizzazione e gestione di più immagini. Quando si vuole caricare un'immagine è possibile farlo dal pulsante GESTIONE IMMAGINI in alto a destra. Si aprirà quindi una modal di riepilogo delle immagini caricate e da lì sarà possibile aggiungere una nuova immagine, specificando i dati richiesti (nome, album, note, ...).
Nella parte 
Una volta caricate, è possibile visualizzare le immagini 
