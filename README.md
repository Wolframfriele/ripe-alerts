<div id="top"></div>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url] 
[![Issues][issues-shield]][issues-url] 
[![Last Commits][last-commit-shield]][last-commit-url] 
[![Pull Request][pull-request-shield]][pull-request-url] 
[![MIT License][license-shield]][license-url]
# ⚠ RIPE Alerts
> Monitoring and anomaly detection based on RIPE Atlas data.

This is project is made by 5 IT-students of Hogeschool Utrecht and is commissioned by [RIPE NCC](https://www.ripe.net/).
<!-- TABLE OF CONTENTS -->
<details>
  <summary><ins><b>Table of Contents</b></ins></summary>
  <ol>
    <li>
      <a href="#about-the-project">Intro</a>
      <ul>
        <li><a href="#goal">Goal</a></li>
        <li><a href="#features">Features</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#how-to-use-the-database">How to use the database?</a></li>
      </ul>
    </li>
    <li><a href="#api-reference">API Reference</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->



### Goal
Our main goal of this project is to find anomalies in the RIPE ATLAS network and report this to the user. We do this through various ways, including the following:

* Web server 
* ~~Webhooks~~ (still in development)
* Email 
* API

Currently, most of this is still in development. We will be adding more in the near future. You may also suggest changes by forking this repo and creating a pull request or opening an issue.

### Features

* Automatically analyze measurements from Ripe Atlas.
* View anomalies in a human-readable format
* Easily extend functionality with plugins
* Receive alerts via Email.

### Built With

We're currently using the following frameworks. 

* [Vue.js](https://vuejs.org/)
* [Django](https://www.djangoproject.com/)
* [Docker](https://www.docker.com/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get a local server up and running, follow these steps.

### Prerequisites

To run this application, you'll need the latest version of Docker and Python installed on your computer. 


### Installation

1. If you're reinstalling the app, please delete the currently existing ripe-alert app first. Installing for the first time? Skip to step 4.<br/>

2. Delete the ripe-alerts from Docker.<br>
Open Docker Desktop → Go to Containers / Apps → ripe-alerts → Delete
3. Delete the database folder.<br> 
Open folder 'ripe-alerts' → Delete folder 'data'
4. After you've cloned the repository. Build all component images with Docker, by using the command:
```bash
  docker compose build
```
5. Initialize the database. Open the terminal, and run the following command: 
```bash
  docker compose run --name database --rm db
```
Wait, until it says: 
```bash
  PostgreSQL init process complete; ready for start up.
```
6. Close the container (CTRL+C). 
7. Start the application, by using the command:
```bash
  docker-compose up
```
8. Open Docker.
9. Go to the backend-container, and open the Command Line Interface (CLI).
10. Migrate the database, by using the command:
```bash
  python manage.py migrate
```
11. To manage access to the database we need a superuser. So let's create one! <br/>
To create a superuser, use the command:
```bash
  python manage.py createsuperuser
```
12. Go to the anomaly-container, and open the Command Line Interface (CLI).
13. Migrate the database, by using the command:
```bash
  python manage.py migrate
```
14. Congratulations! You're done! You can access the site at [http://localhost:8080/](http://localhost:8080/).


<!-- HOW TO USE THE DATABASE? -->
### How to use the database?

To access the database you'll need go to the Django admin page. This can be found at [http://localhost:8000/admin](http://localhost:8000/admin). 

After, opening the link. You can log in with the default user:

| Info     |            Value |
|----------|-----------------:|
| username |            admin |
| email    | `admin@ripe.net` |
| password |         password |


We highly recommend changing your password after logging in. This can be done in by navigating to the top right of the Django admin page.
<p align="right">(<a href="#top">back to top</a>)</p>

<!-- API REFERENCE -->
## API Reference

To check out live examples and docs, visit [our wiki.](https://github.com/Wolframfriele/ripe-alerts/wiki)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [x] Anomaly detection
- [x] Base API
- [ ] Improve Docker installation
- [ ] Add additional alerting methods like Webhooks, API
- [ ] Personalize alerts by giving feedback to anomalies
- [ ] Better API documentation


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GNU License. See [here](https://github.com/Wolframfriele/ripe-alerts/blob/main/LICENSE)
 for more information.

<p align="right">(<a href="#top">back to top</a>)</p>
<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

We highly recommend to check out all the [Atlas API](https://beta-docs.atlas.ripe.net/). 

Also, we are grateful for having [Emile Aben](https://github.com/emileaben) for guiding the development of this project.

Copyright (c) 2022 by Floris, Wolfram, Sybren and Koen


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Wolframfriele/ripe-alerts?style=for-the-badge
[contributors-url]: https://github.com/Wolframfriele/ripe-alerts/graphs/contributors
[issues-shield]: https://img.shields.io/github/issues/Wolframfriele/ripe-alerts?style=for-the-badge
[issues-url]: https://github.com/Wolframfriele/ripe-alerts/issues
[last-commit-shield]: https://img.shields.io/github/last-commit/Wolframfriele/ripe-alerts?style=for-the-badge
[last-commit-url]: https://github.com/Wolframfriele/ripe-alerts/commits/main
[pull-request-shield]: https://img.shields.io/github/issues-pr/Wolframfriele/ripe-alerts?style=for-the-badge
[pull-request-url]: https://github.com/Wolframfriele/ripe-alerts/pulls
[license-shield]: https://img.shields.io/badge/License-GPLv3-blue.svg?style=for-the-badge
[license-url]: https://www.gnu.org/licenses/gpl-3.0.nl.html
