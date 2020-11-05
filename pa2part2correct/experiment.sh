#!/usr/bin/env bash

if [ -f drop_exp ]; then
    rm -f drop_exp
fi
if [ -f corrupt_exp ]; then
    rm -f corrupt_exp
fi

prefix_cmt="Average communication time: "
echo "Start drop probability experiment"
for p in $(seq 0.0 0.1 0.9)
do
for i in {1000..1019}; do
    echo 1000 "$p" 0.1 200 8 15 1 "$i" | ./pa2 > temp
    result=$(grep "Average communication time: " temp)
    result=${result#$prefix_cmt}
    echo "$result","$p","$i" >> drop_exp
    echo "prob $p rands $i done"
done
done
rm -f temp

echo "Start corrupt probability experiment"
for p in $(seq 0.0 0.1 0.7)
do
for i in {1000..1019}; do
    echo 1000 0.1 "$p" 200 8 15 1 "$i" | ./pa2 > temp
    result=$(grep "Average communication time: " temp)
    result=${result#$prefix_cmt}
    echo "$result","$p","$i" >> corrupt_exp
    echo "prob $p rands $i done"
done
done
rm -f temp
