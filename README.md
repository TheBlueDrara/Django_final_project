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

- make a script to deploy infra ( clone repo, make installer, create vagrant machines, run ansible playbooks, run gh-runner container)
- make a script to install needed dependenciess





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
> Note, Remove the ```.git``` from the repo url at the end.

```
docker run \
-e URL=https://github.com/TheBlueDrara/Django_final_project \
-e TOKEN= \
--network host \
-v gh-runner-data:/github \
-v /var/run/docker.sock:/var/run/docker.sock \
runner:v0.0.9
```

# Weaknes 
- Part of the CI is to run the helm chart with the new built image, ( need to change the image tag in the values file )
- Need to install helm on VMs
- No ingress so to reach production app there is port forward from host to guest control plane VM in the vagrant file
- no special storage, can use local host nfs server (nfs-kernel-server)
- the VMs need internet access to install Helm
- docker image dynamic versions for main branch is missing 

- add a script to run the setup, include check for prerequsits

## Clean UP
- remove gh-runner container
- delete gh-ruuner volume
- remove gh-runner from gh
- remove vagrant vms
- delete the repo

docker kill $(docker ps | awk '{print $1}')
docker container rm $(docker ps -a | awk '{print $1}')
docker volume rm -f gh-runner-data

docker build -t runner:v0.0.14 -f docker/Dockerfile.runner .


docker run \
  --network host \
  -e URL="https://github.com/TheBlueDrara/Django_final_project" \
  -e TOKEN="BCG4KGLJRJBTZ32VW3Z62KLJBTWL6" \
  -v gh-runner-data:/github \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --group-add $(stat -c '%g' /var/run/docker.sock) \
  thebluedrara/github_runner:v1.0.14

cd vagrant
vagrant ssh control-plane

kubectl get pods -A -w