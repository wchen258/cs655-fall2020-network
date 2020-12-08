#!/bin/bash

sudo apt update
sudo apt install -y openjdk-11-jdk
git clone -b final --depth 1 https://github.com/wchen258/cs655-fall2020-network
cd cs655-fall2020-network/tomcat/webapps/Servlet/WEB-INF/classes/servletclass
javac -cp '../../lib/*' Servlet.java
cd ../../../../../bin
mkdir -p ../logs
sudo ./catalina.sh start

# local crawling test
sudo apt install -y python3-pip
python3 -m pip install scrapy
export PATH="${PATH}:${HOME}/.local/bin"
cd ../../geni_test
scrapy crawl -L DEBUG -s CONCURRENT_REQUESTS=2 -a n=5 -a ip=localhost geni
