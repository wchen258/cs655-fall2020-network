#!/bin/bash

sudo apt update
sudo apt install -y openjdk-11-jdk
git clone -b final --depth 1 https://github.com/wchen258/cs655-fall2020-network
cd cs655-fall2020-network/tomcat/webapps/Servlet/WEB-INF/classes/servletclass
javac -cp '../../lib/*' Servlet.java
cd ../../../../../bin
mkdir -p ../logs
sudo ./catalina.sh start
