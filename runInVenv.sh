#!/bin/bash
# Script to initiate the Virtual Environment and run the code within

source ~/Documents/Venvironments/sandbox/bin/activate

#python3 ~/Documents/Proyects/pricesTracker/sandbbox.py
#python3 ~/Documents/Proyects/pricesTracker/pricesCollector.py

# Share ffiles over github
cd /home/pi/Documents/Proyects/pricesTracker/
git add /home/pi/Documents/Proyects/pricesTracker/data/*
git push
