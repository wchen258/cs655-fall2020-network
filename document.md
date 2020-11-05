* Qijia Liu (U19831657)
* Weifan Chen (U51902184)
# Selective Repeat
## Design
* We use C++ to implement the SR. The choice of data structure is as the following.

### Sender A

**Message/retransmission buffer**: Everytime when layer 5 uses the service, a packet would be created, as the seqence number could be determined right away. No matter whether the sender window still has space or not, the packet would be enqued into a packet double linked list. The logical sender window size is maintained by the base sender window index. Given a base index and the window size, the packets in the logical sender window could be identified. As a consequence, packets not in the logical window are the 'buffered message'. The buffer and the index are declared as `deque<pkt> A_queue` and `unsigned first_unacked`. 

**Checksum calculation**: The calculation of the `get_checksum` is done by viewing a packet as a sequence of bytes, adding them up, and keeping only the least 8 significant bits. Prior to the checksum calculation, the checksum field in the packet is initialized to be zero as defined in `make_pkt`, and would be assigned to the complement of the return of the checksum function. By doing so, on the receiver side, the validation could be compared with the return value of the checksum function and 0xFF. 

**A_input implementation**: Upon a successful reception of a packet, the difference between the acknowledgement number and the sender window base number, could tell how many indices the window could advance, and pop the packets in the buffer accordingly. With the new base index, the sender would also send the packets newly fallen into the logical window range if any. As the base index is adjusted based on reception information, any duplicated packet's acknowledgement nubmers would not be larger than the base index, thus ignored. 

**A_timer**: Given the A_input implementation, upon a timer goes off, the packet at the front of the doubly linked list would be sent, as it is the first unacked packet in the sender window.

### Receiver B

**Receiver window**: The Receiver window is represented by a deque of two fields `vector<pair<bool, char[20]>> B_window`. The first is the messaged carried in the packet, and the second field is an boolean indicating whether the current index of the window has already buffered a message or not. As the base index (the next expected seqno) is changing, it's important to have an variable `next_expected_index` to indicate which index is used as the base of the receiver window. By doing so, upon B successfully received a packet, an offset could be calculated, and buffer the message into the correct place, and marked it as buffered. If the packet is the next expected packet by the reciever, advance the `next_expected_index` by 1 as well, and mark the delivered index as unbuffered, as it is used as the tail of the receiver buffer window.


### Stat collection and trace 

An instance of `struct statistic` is dedicated to store all the statistical information. Since the simulation is built upon event, `collect_stat` could take appropriate action based upon the event type parameter. It would also write to the statistic instance. 

`print_message` would handle some of the trace print based upon the event type. As the type traces varies a lot, some trace prints are directly done in the corresponding rountine without invoking `print_message`. 

## Experiment 

`experiment.sh` can run a range of randome seeds with loss/corrupt probability increases, and output the experiment statistics to a file. `plot.py` can read the generated stat file and do the ploting. To reproduce our experiment, do
```
make draw
```
### Experiment setup

Exp | Loss Prob. | Corrupt Prob. | Num of messages | avg. time from layer5 | Window size | Retrans. timeout | Random Seed
--------| --------|----|--------|--------|---------|--------|---------|
trace | 0.1 | 0.1 | 1000 | 200 | 8 | 30 | 1234 | 
exp1| 0~0.9 | 0.1 | 100 | 200 | 8 | 15 | 1000~1019|
exp2 | 0.1 | 0~0.9 | 100 | 200 | 8 | 15 | 1000~1019|


Below is the statistical result for trace

Num of original packets transmitted | Num of retransmissions | Num of packets delivered to layer 5 | Num of ACK packets sent| Num of corrupted packets| Ratio of lost packets | Ratio of corrupted packets |Average RTT|Average communication time|
-----|------|-----|-----|-----|-----|-----|-----|-----|
1000  | 487 | 1000 | 1216 | 227| 0.0961894 | 0.0929185| 10.8078 | 26.1019|






