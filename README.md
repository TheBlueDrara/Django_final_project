# Overview

a simple voting web application app using Django, Gunicorn and Nginx
for the CI, will use GitLab CI, Ansible that will deploy on a k8s cluster


# Flow

- Make the webapp work locally, DOD - a working webapp with a database 
- Containerize the app with the DB as a docker compose
- Create a CI to test and build a new docker image artifact
- Create a k8s cluster using my k8s offline installer project
- Use ansible to run a rollout and update the app pods
- Use DockerHub for my container regeistry,Bounes, Create my own registry
- Will be used a multibranch monorepo for source control in GitHub

