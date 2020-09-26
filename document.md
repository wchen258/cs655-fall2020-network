* Qijia Liu
* Weifan Chen
# Part 1
## Design
* We use Python in both client and server. There's a `util.py` that encapsulates function `sendall` and `recv` of the builtin `socket` package which handle byte arrays, to deal with strings. The `util.py` is also capable of processing command line arguments:
```
[liumeo@csa1 pa1part1]$ python3 client.py localhost
usage: client.py [-h] host port
client.py: error: the following arguments are required: port
```
* As [official document](https://docs.python.org/3/library/socket.html) suggests, we choose a relatively small power of 2 (1024) as the buffer size of `recv`.
* Although CPython has GIL, for an I/O bound application like this, it's still worth using multithreading to process requests simultaneously:
```
[liumeo@csa1 pa1part1]$ python3 server.py 58233
Connected by ('127.0.0.1', 44696)
Connected by ('127.0.0.1', 44698)
Connection ('127.0.0.1', 44696) closed
Connection ('127.0.0.1', 44698) closed
```
## Test
* To start server on csa1, choose a port (here 58233) and run:
```
[liumeo@csa1 pa1part1]$ python3 server.py 58233
```
* To start client on csa1 or other devices, run:
```
[liumeo@csa1 pa1part1]$ python3 client.py csa1.bu.edu 58233
hello world!
hello world!
```
* Type some text (here "hello world!") on the client and press Enter, the server will echo the text. The client prints what it receives and closes the connection.
