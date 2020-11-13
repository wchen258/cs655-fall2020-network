#!/bin/bash

CSP200='200 OK: Ready'
CSP404='404 ERROR: Invalid Connection Setup Message'
MP404='404 ERROR: Invalid Measurement Message'
CTP200='200 OK: Closing Connection'
CTP404='404 ERROR: Invalid Connection Termination Message'

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

declare -i i=0
while read exp msg
do
    i=i+1
    res=$(echo -en "$msg" | timeout 1 nc $1 $2 | tail -n 1)
    if [[ ${!exp} == $res ]]; then
        echo -e $i "${GREEN}passed${NC}"
    else
        echo -e $i "${RED}failed${NC}"
    fi
done <testcases
