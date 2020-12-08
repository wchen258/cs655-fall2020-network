#!/bin/bash

sudo apt update
sudo apt install -y openjdk-11-jdk
git clone -b final --depth 1 https://github.com/wchen258/cs655-fall2020-network
cd cs655-fall2020-network/tomcat/bin
sudo ./catalina.sh start
