[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
![License](https://img.shields.io/github/license/Wolframfriele/ripe-alerts)
![Commit Activity](https://img.shields.io/github/commit-activity/m/Wolframfriele/ripe-alerts)
![Contributors](https://img.shields.io/github/contributors/Wolframfriele/ripe-alerts)
![Last Commit](https://img.shields.io/github/last-commit/Wolframfriele/ripe-alerts)

⚠ RIPE Alerts
==============

Monitoring and anomaly detection based on RIPE Atlas data.


## Features
* Automatically analyze measurements from Ripe Atlas.
* View anomalies in a human-readable format
* Easily extend functionality with plugins
* Receive alerts via Email.


## Roadmap
- [ ] Improve docker installation
- [ ] Add additional alerting methods like Webhooks, API
- [ ] Personalize alerts by giving feedback to anomalies
- [ ] Better API documentation


## Installation
The easiest way to install is to use Docker:
Make sure you have docker installed and running and have cloned the repository.

Remove line 11 from the `Backend/notifications/apis.py` file.
```python
  station = Station(PostgresInterface())
```

Run the docker-compose file.
```bash
  docker-compose up
```

Open a new terminal and ssh into the container.
```bash
  docker exec -it web-server bash
```

Migrate the database.
```bash
  python manage.py migrate
```

Create a superuser to access the database. (optional)
```bash
  python manage.py createsuperuser
```

Stop the container and uncomment line 11 in the `Backend/notifications/apis.py` file and build the container again.
```bash
  docker-compose down
  docker-compose build
  docker-compose up
```
It should be running now. you can access the site at `http://localhost:8080/`.


## Contributing
Contributions are always welcome!


## Acknowledgements
[Emile Aben](https://github.com/emileaben) - Guiding the development of this project

[Ripe Atlas](https://atlas.ripe.net/) - Data source