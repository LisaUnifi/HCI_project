# Mattoni 2.0
> Attualmente nel servizio sanitario di emergenza locale di Regione Toscana i soccorritori sulle ambulanze sono tenuti a compilare un documento cartaceo, **Scheda Mattoni**, per delineare l'anamnesi del paziente durante un servizio e comunicarla alla Centrale Operativa 118 per provvedere al ricovero. Questo però è un sistema "outdated" che non permette una comunicazione immediata tra soccorritore e medico di centrale; è infatti richiesta una chiamata a valle del servizio per spiegare quello che il soccorritore ha scritto nella scheda. 
>
> In questo progetto abbiamo deciso di implementare una versione digitale di tale documento capace di essere compilato velocemente e che permetta la possibilità di invio diretto in Centrale. Questo è vantaggioso perchè potrebbe permettere un notevole risparmio di tempo, essenziale durante un servizio.
> 
> Con questa reimplementazione vogliamo anche migliorare la specificità delle informazioni che andranno raccolte nella scheda adattandole alla casistica di intervento (attualmente comunicate a voce) rendendo questo più strutturato e immediato, e al contempo rendendo la scheda più di supporto ai soccorritori.

## Table of Contents
* [General Info](#general-information)
* [Installation](#installation)
* [Tools and Techniques](#tools-and-techniques)
* [Expected Outcomes](#expected-outcomes)
* [Summary and Applications](#summary-and-applications )


## General Information
- Anno accademico: 2021-2022
- Titolo: Mattoni 2.0
- Studenti: Lisa Cresti e Lorenzo Caselli
- CFU: 9


## Installation
Il progetto richiede l'installazione preventiva di python nella versione 3.10.0 e di pip.

### Con pip
Per installare le dependencies in un virtual enviroment di pip, da terminale eseguire:
```bash
pip install -r requirements.txt
```
Scaricare da GitHub il progetto in locale.
Da terminale raggiungere la cartella ../HCI_project/mattoni ed eseguire:
```bash
python manage.py runserver 0.0.0.0:8000

```
per aprire il server. Per accedere all'applicativo collegarsi alla url indicata in output.

### Con Anaconda 
Una volta installata [Anaconda](https://www.anaconda.com/) eseguire:
```bash
conda create --name <env> --file requirements_conda.txt
```
per creare un conda virtual enviroment con le dependencies richieste.
Scaricare da GitHub il progetto in locale.
Da terminale raggiungere la cartella ../HCI_project/mattoni ed eseguire:
```bash
python manage.py runserver 0.0.0.0:8000

```
per aprire il server. Per accedere all'applicativo collegarsi alla url indicata in output.

## Tools and Techniques
La scelta di digitalizzare la scheda attraverso la creazione di un applicativo web ci permette di creare un'applicazione che possa essere usata senza la necessità di scaricare o installare particolari applicativi. Questo implica che sia facilmente utilizzabile su tutti i tipi di dispositivi, requisito per noi fondamentale visto che soccorritori e Operatori di Centrale lavorano e comunicano attraverso device diversi, nel primo caso mobili e nel secondo fissi.
Allo scopo di creare un applicativo completo abbiamo realizzato sia la parte di back-end che quella di front-end. 
Una delle prime tecnologie che vogliamo menzionare è il python web framework Django.
Django implementa nel suo codice un pattern definito Model-View-Template finalizzato a gestire la comunicazione tra database e server e che permette una facile gestione delle informazioni derivanti dall'interazione dell'utente col frontend, ispirandosi al pattern Model-View-Controller.
Allo scopo di rendere l'interfaccia utente più accessibile e "visually appealing", la scelta è stata quella di affiancare un altro strumento all'utilizzo di Django: Bootstrap.
Bootstrap è un CSS framework che supporta la creazione di pagine web responsive: nello specifico abbiamo deciso di utilizzare la versione 4 con l'estensione finalizzata all'utilizzo del Material Design.
Insieme all'utilizzo dei framework sopra menzionati abbiamo anche utilizzato:
- JavaScript
- CSS
- HTML
- Ajax
- SQLite
- Python


## Expected Outcomes
Gli obiettivi che vorremmo raggiungere sono:
- creare un'interfaccia digitale della scheda Mattoni rivisitata per essere più intuitiva all'utilizzo
- possibilità di adattare i contenuti della scheda in base al tipo d'intervento e al protocollo da attuare 
- simulare la comunicazione tra soccorritore e medico di centrale tramite l'applicativo
- fornire un report stampabile/inviabile dell'intervento


## Summary and Applications 
Con questo progetto vogliamo sperimentare se la reimplementazione digitale di tale documento può effettivamente migliorare l'intervento sanitario locale in situazioni di emergenza, migliorando l'efficienza e l'efficacia del servizio. 

Abbiamo intenzione di testare l'applicazione durante la formazione e il retraining dei soccorritori della nostra associazione così da verificarne l'impatto che potrebbe avere in situazioni reali comprendendone così i vantaggi e i limiti di tale approccio.

