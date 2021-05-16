# Setup
install ansible https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html
(on Ubuntu)
$ sudo apt update
$ sudo apt install software-properties-common
$ sudo apt-add-repository --yes --update ppa:ansible/ansible
$ sudo apt install ansible




Run '$sudo apt update' before any scripts, to cache sudo privileges for a while

# Scripts

## Spawning instances
### Do not recommend running, as VMs often error in creation these days. Keep current VMs if possible.
Run make_vms.sh to spawn the VMs. 
Currently commented out VMs Slave1 and Slave2 from ansible/host_vars/mrc.yaml so they wont be made. Similarly, their volumes are also commented out.

## Cloning repo
Run clone_gits.sh to clone the CCCAssignment2 repo to all VMs. If it errors on the initial clone for a VM, try running again. Resultant from an inconsistent bug to be squashed.

## Preparing Docker
To ready docker service to work through the proxies, and likewise for docker containers, run setup_docker.sh.