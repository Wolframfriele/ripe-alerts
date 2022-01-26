# ripe-alerts
This repo is a part of software build for Ripe.

# Security
This Repo is private, we don't want to share this project yet.

# How to use branches
Our main branche is litteraly the main branche. In this branche we have only the tested code, the code in the main branche is ready to go in production.
README.md, gitignore and other project wide files may be commited directly to the main branche.

Code that's writen for a storie like user storie, have to have to use the name of the devops story. SO US + number, US65413 or when it is an enabler storie please use ES and the front.

# Issues
We can start using Issues when we launched our MVP.

# How to launch this project?
We use docker to host the project. It is meant to host it on a server. Every individual user needs his own setup. To set it up please do the following steps.

1. Install docker.
2. Copy the project to the right spot on your disk.
3. Navigate to the folder and run docker-compose build
4. Run docker-compose up
5. Navigate to http://localhost:8080/

## Stop docker
Please do this only for maintainance purpose or when you want to delete the project.
If there is an anomalie, you won't be alerted.

$docker down
