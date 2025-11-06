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
- 


## ToDo

- make a script to deploy infra
- make a script to install needed dependencies56

## Pipeline flow

### Test Pipelinep

Job_1
- test env setup
    install pylint tool
    install docker

Job_2
- lint test for the code

Job_3
- build docker image from the new code
- push to dockerhub

Job_4
- connect via ssh to vm
- run helm install on vm to dploy test env using the new test image

Job_5
- run curl tests for the app

Job_6
- clean up, helm uninstall, remove local image


### Prod pipeline

Job_1
- runner env setup
- install docker

Job_2
- build image
- push to docker hub with a new tag

## Setup flow

clone the project

```
git clone https://github.com/TheBlueDrara/Django_final_project.git
```

clone Offline installer project for the installer,
> No need to follow the installers README, just do what i say
```
cd Django_final_project
git clone https://github.com/TheBlueDrara/Offline_Vanilla_k8s_Installer.git
cd Offline_Vanilla_k8s_Installer
cd build-script
chmod +x makeself.sh
./makeself.sh
mv ../k8s_installer.run ../../
```

You can now remove the Offline k8s repo

```
sudo rm -rf Offline_Vanilla_k8s_Installer
```

Build the VMs
```
cd vagrant
vagrant up --provider=libvirt
```

Deploy the cluster and install helm
```
cd ansible/playbooks/
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook main.yaml -i ../inventory/hosts.ini
```

install the production helm chart
```
cd vagrant
vagrant global-status
vagrant ssh control_plane
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


## Config gitlab runner

If you want to config the gitlab runner to use your repo as the source you can run the config command in the gitlab_runner directory
```
./config.sh --url https://github.com/TheBlueDrara/Django_final_project --token <TOKEN>
```
than rebuild the image
```
docker build -t runner:v0.0.6 -f docker/Dockerfile.runner .
```

Now run the runner
```
docker run -d --name gh-runner   --network host   --restart unless-stopped   -v gh-runner-data:/github   runner:v0.0.7
```

# Weaknes 
- Part of the CI is to run the helm chart with the new built image, ( need to change the image tag in the values file )
- Need to install helm on VMs
- No ingress so to reach production app there is port forward from host to guest control plane VM in the vagrant file
- no special storage, can use local host nfs server (nfs-kernel-server)
- the VMs need internet access to install Helm
- docker image dynamic versions for main branch is missing 

- add a script to run the setup, include check for prerequsits

##