
# Game of Life


## Table of Contents
* [General Info](#general-information)
* [Installation](#installation)
* [Tools and Techniques](#tools-and-techniques)
* [Implemented Features](#implemented-features)
* [Extra Features](#extra-features)


## General Information
- Anno accademico: 2021-2022
- Titolo: Game of Life
- Studenti: Lorenzo Caselli


## Installation
Per l'installazione, riferirsi al README.md per l'installazione del progetto generale (Mattoni 2.0).
Una volta che il progetto di Django è "up and running", è possibile raggiungere l'applicativo raggiungendo l'url 0.0.0.0:8000/game_of_life/ ,
oppure dalla main page dell'applicativo Mattoni, fare click sul nome in basso Lorenzo Caselli per essere portati alla sezione di Game of Life.



## Tools and Techniques
Allo scopo di sviluppare questa implementazione, è stato utilizzato il web framework di Django, con base di progetto la stessa della 
web app di Mattoni 2.0. Quindi, dal punto di vista di HTML e gestione della pagina col server, ci si affida a Django. Dal punto di vista di 
funzionalità però, quasi la totalità delle funzioni sono implementate all'interno del file gol.js, situato nella cartella 
game_of_life/static/js. 
All'interno di tale file è situata l'implementazione del MVC (Model-View-Cotroller) che gestisce il funzionamento del Game of Life e della sua interazione con 
l'interfaccia HTML.
Il model è identificato dalla classe Grid, al cui interno sono situate tutte le regole per gestire il Game of Life dal punto di vista di 
aggiornamento di quali tiles sono vivi, quali morti e per quanto tempo sono sopravvissuti. Inoltre sono situate alcune funzioni base per
randomizzare la griglia e fare un clear.
Il Controller è identificato dalla classe Controller e gestisce al suo interno l'interazione tra il modello, ovvero la classe Grid e 
la view, ovvero la classe View. In particolare, gestisce le funzioni da attivare nel momento in cui l'interfaccia cattura delle azioni
dell'utente, specificando quali effettuare, anche raccogliendo le informazioni della Grid, aggiornandole in base a tali 
interazioni.
Infine la View è la classe che si occupa di gestire gli elementi del DOM HTML, catturare gli eventi dati dall'interazione degli utenti
con esse e le funzioni che specificano come disegnare il canvas, in base alle informazioni che derivano dal Controller (che a suo tempo ha
derivato dalla classe Grid).


## Implemented Features
Questa implementazioni del Game of Life fornisce una interfaccia grafica funzionante e animata del Game of Life, partendo da una configurazione 
iniziale che l'utente può modificare in qualsiasi momento con un click sui tiles rappresentati sul canvas. Attraverso l'utilizzo dei buttons di
START, PAUSE, RANDOM e CLEAR è possibile effettuare le omonime azioni e si permette di modificare la velocità di simulazione con uno slider.


## Extra Features 
L'implementazione qui proposta permette di effettuare panning e zooming sul canvas, attraverso l'interazione con mouse. 
Infine, in base al colore delle tiles è possibile individuare l'età di una cella,
in base ad un gradiente di colori, con blu scuro che individua tiles appena nati e rosso che individua quelle più anziane.