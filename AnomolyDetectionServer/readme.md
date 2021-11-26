# AI Server

Server voor De anomoly detectie en het genereren van alerts

## Wat voor functionaliteit er nu in zit:


- Server gemaakt met een api, die gegeven de measurement_id en type van de measurement, een initeel dataset creeërt (van de laatste 24 uur, is aanpasbaar in de code), wanneer de dataset verzameld is wordt
 er verbinding gemaakt met de streaming api om in real time de nieuwe results binnen te krijgen

## Requirements voor het opstarten van de server

- Python, installeren van de packages in requirements.txt
- Docker

## Opstarten van de server
- De docker commands uitvoeren die in docker_commands.txt staat. Deze commands zijn nodig om de mongo database 
en GUI op te starten
- de command python manage.py runserver uitvoeren
