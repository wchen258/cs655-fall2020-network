#!/bin/bash

python3 -m pip install torchvision
git clone -b final --depth 1 https://github.com/wchen258/cs655-fall2020-network
cd cs655-fall2020-network
nohup python3 model.py &
