#!/bin/bash

prefix_cmt="Average communication time: "
for i in {1000..1020}
do
    echo 1000 0.1 0.1 200 8 30 3 "$i" | ./pa2 > temp
    result=$(cat temp | grep "Average communication time: ")
    result=${result#$prefix_cmt}
    echo $result >> cmttest
done
rm -f temp