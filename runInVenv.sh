#!/bin/bash
# Script to initiate the Virtual Environment and run the code 

source ~/Documents/Venvironments/sandbox/bin/activate

# Gather prices
python3 ~/Documents/Proyects/pricesTracker/pricesCollector.py

# Share files over github
cd /home/pi/Documents/Proyects/pricesTracker/
git add /home/pi/Documents/Proyects/pricesTracker/data/* 
git commit -m "new datafile"
git push
