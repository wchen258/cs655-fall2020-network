#!/bin/bash

sudo apt update
sudo apt install -y python3-pip
python3 -m pip --no-cache-dir install torchvision
git clone -b final --depth 1 https://github.com/wchen258/cs655-fall2020-network
cd cs655-fall2020-network
nohup python3 model.py &
