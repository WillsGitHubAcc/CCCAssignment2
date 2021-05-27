#!/usr/bin/bash
sh ./make_vms.sh
sh ./clone_gits.sh
sh ./setup_docker.sh
sh ./initialise_database.sh
sh ./load_view.sh
sh ./initialise_harvesters.sh
sh ./initialise_tweet_analysis.sh
sh ./initialise_frontend.sh
sh ./initialise_frontend_api.sh