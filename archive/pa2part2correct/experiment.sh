#!/usr/bin/env bash

if [ -f drop_exp ]; then
    rm -f drop_exp
fi
if [ -f corrupt_exp ]; then
    rm -f corrupt_exp
fi

prefix_cmt="Average communication time: "
prefix_rtt="Average RTT: "
prefix_retran="Number of retransmissions by A: "
prefix_tput="Throughput: "
prefix_gput="Goodput: "
echo "Start drop probability experiment"
for p in $(seq 0.0 0.1 0.9)
do
for i in {1000..1019}; do
    echo 100 "$p" 0.1 200 8 15 1 "$i" | ./pa2 > temp
    result=$(grep "Average communication time: " temp)
    res_rtt=$(grep "Average RTT: " temp)
    res_retran=$(grep "Number of retransmissions by A: " temp)
    res_tput=$(grep "Throughput: " temp)
    res_gput=$(grep "Goodput: " temp)
    res_tput=${res_tput#$prefix_tput}
    res_gput=${res_gput#$prefix_gput}
    res_rtt=${res_rtt#$prefix_rtt}
    res_retran=${res_retran#$prefix_retran}
    result=${result#$prefix_cmt}
    echo "$result","$p","$i","$res_rtt","$res_retran","$res_tput","$res_gput" >> drop_exp
    echo "prob $p rands $i done"
done
done
rm -f temp

echo "Start corrupt probability experiment"
for p in $(seq 0.0 0.1 0.9)
do
for i in {1000..1019}; do
    echo 100 0.1 "$p" 200 8 15 1 "$i" | ./pa2 > temp
    result=$(grep "Average communication time: " temp)
    res_rtt=$(grep "Average RTT: " temp)
    res_retran=$(grep "Number of retransmissions by A: " temp)
    res_tput=$(grep "Throughput: " temp)
    res_gput=$(grep "Goodput: " temp)
    res_tput=${res_tput#$prefix_tput}
    res_gput=${res_gput#$prefix_gput}
    res_rtt=${res_rtt#$prefix_rtt}
    res_retran=${res_retran#$prefix_retran}
    result=${result#$prefix_cmt}
    echo "$result","$p","$i","$res_rtt","$res_retran","$res_tput","$res_gput" >> corrupt_exp
    echo "prob $p rands $i done"
done
done
rm -f temp
