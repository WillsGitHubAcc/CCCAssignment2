#!/usr/bin/bash

# COMP90024 2021 Semester 2 Assignment 2
# Group 52
# William Lazarus Kevin Dean 834444 Melbourne, Australia
# Kenneth Huynh 992680 Melbourne, Australia
# Joel Kenna 995401 Melbourne, Australia
# Quinten van der Leest 1135216 Melbourne, Australia
# Walter Zhang 761994 Melbourne, Australia

#. ./unimelb-comp90024-2021-grp-52-openrc.sh; ansible-playbook mrc.yaml
# ansible-playbook --vault-password-file passwords.txt generate_vms.yaml
ansible-playbook --vault-password-file passwords.txt views_load.yaml