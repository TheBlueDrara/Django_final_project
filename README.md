# Overview

a simple voting web application app using Django, Gunicorn and Nginx
for the CI, will use GitLab CI, Ansible that will deploy on a k8s cluster


# Flow

- Make the webapp work locally, DOD - a working webapp with a database (use a Postgress DB and Docker compose)
- Containerize the app with the DB as a docker compose
- Create a CI to test and build a new docker image artifact
- Create a k8s cluster using my k8s offline installer project
- Use ansible to run a rollout and update the app pods
- Use DockerHub for my container regeistry,Bounes, Create my own registry
- Will be used a multibranch monorepo for source control in GitHub


## Prerequsists
- Vagrant
- Qemu
- Libvert
- Ansible
- Makeself

## Setup flow

clone Offline installer project for the installer,
> No need to follow the installers README, just do what i say
```
git clone https://github.com/TheBlueDrara/Offline_Vanilla_k8s_Installer.git
cd Offline_Vanilla_k8s_Installer
cd build-script
chmod +x makeself.sh
./makeself.sh
mv k8s_installer.run ../
```

Build the VMs
```
cd vagrant
vagrant up --provider=libvirt
```

Deploy the cluster and install helm
```
cd cd/playbooks/
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook main.yaml -i ../inventory/hosts.ini
```

install the production helm chart
```
cd vagrant
vagrant global-status
vagrant ssh <control_plane_ID>
git clone https://github.com/TheBlueDrara/Django_final_project.git
cd Django_final_project/kubernetes/production_helm_chart
helm install prod-voteapp .
``` 

To access the production app, go to your hosts webpage
```
http://localhost:8081

or

http://192.168.56.11:30081
```
Done
