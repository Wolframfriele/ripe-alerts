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
  <summary>Table of Contents</summary>
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
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#api">API docs</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
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

1. After you've cloned the repository. Comment line #11 from the `Backend/notifications/apis.py` file. 
It will look like the example below.
```python
#  station = Station(PostgresInterface())
```
2. Build all component images with Docker, by using the command:
```bash
  docker-compose
```
3. Open Docker.
4. Start the application and go to the Webserver-container to open the Command Line Interface (CLI).
5. Migrate the database, by using the command:
```bash
  python manage.py migrate
```
6. To manage access to the database we need a superuser. So let's create one! <br/>
To create a superuser, use the command:
```bash
  python manage.py createsuperuser
```
7. After succesfully creating the superuser, stop the Docker container.
8. Now, go back to the project and uncomment line #11 from the `Backend/notifications/apis.py` file. <br/>
So it will looks like the code below.
```python
  station = Station(PostgresInterface())
```
9. Repeat step 2 and start the application.
10. Congratulations! It should be running now. You can access the site at [http://localhost:8080/](http://localhost:8080/).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Add Changelog
- [x] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

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

Distributed under the GNU License. See `LICENSE.txt` for more information.

Copyright (c) 2021 by Floris, Wolfram, Maarten, Sybren and Koen

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search)

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