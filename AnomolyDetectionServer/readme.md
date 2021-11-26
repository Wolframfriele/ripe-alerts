# AI Server

Server voor De anomoly detectie en het genereren van alerts

## Wat voor functionaliteit er nu in zit:


- Server gemaakt met een api, die gegeven de measurement_id en type van de measurement, een initeel dataset creeërt (van de laatste 24 uur, is aanpasbaar in de code), wanneer de dataset verzameld is wordt
 er verbinding gemaakt met de streaming api om in real time de nieuwe results binnen te krijgen
 De intiiele dataset verzamelen kan een aantal minuten duren het kan aardig wat data zijn.

## Requirements voor het opstarten van de server

- Python, installeren van de packages in requirements.txt
- Docker

## Opstarten van de server
Bij de 1e keer opstarten:
- De docker commands uitvoeren die in docker_commands.txt staat. Deze commands zijn nodig om de mongo database 
en GUI op te starten, voor als je data wilt zien.
- de command python manage.py runserver uitvoeren

Als de Docker commands al eens uitgevoerd zijn:
- docker start mongodb
- docker start mongo-express
- python manage.py runserver


## De API om zelf een measurement toe te voegen.
- POST http://localhost:8000/monitor
- DE API verwacht een json met daarin 
         {
          "measurement_id": int,
          "type": str }
Om aan de measurement_id en type te kunnen komen zou je hier kunnen kijken: https://atlas.ripe.net/api/v2/anchor-measurements
bijd de field "measurements", zie je een url van de volgende vorm https://atlas.ripe.net/api/v2/measurements/{measuremnt_id}/

## De verzamelde data kunnen zien
Mongo Express is als het goed is opgestart, als je de docker commands hebt uitgevoerd. http://localhost:8081/ , is waar je Mongo Express staat. Dit is een GUI voor MongoDB.
