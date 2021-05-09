#!/bin/bash

#. ./unimelb-comp90024-2021-grp-52-openrc.sh; ansible-playbook mrc.yaml
ansible-playbook --vault-password-file passwords.txt mrc.yaml
