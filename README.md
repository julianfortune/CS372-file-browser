# CS372 File Browser
An extra credit project from CS 372 Fall 2019 at Oregon State that transfers files between two processes using only sockets and TCP.

## Demo

### 1. Start the server

```
$ python3 server.py [port name]
```

![Screen Shot 2020-09-23 at 3 54 16 PM](https://user-images.githubusercontent.com/25210657/94082303-8164db80-fdb5-11ea-96f0-a369e8ff4314.png)

The names of the two programs are a play on words (the course was taught by Prof. Pfeil).

### 2. Open the client

```
$ cd client/
$ python3 client.py [the same port name as the server]
```

![Screen Shot 2020-09-23 at 3 54 51 PM](https://user-images.githubusercontent.com/25210657/94082307-82960880-fdb5-11ea-9d64-1a0ecda0378d.png)

### 3. `get` a file

```
get [file name]
```

The file name needs to be the name of a file in the same directory as the server, e.g. `alice.txt`.

![Screen Shot 2020-09-23 at 3 55 05 PM](https://user-images.githubusercontent.com/25210657/94082310-83c73580-fdb5-11ea-8211-deb266ea4ead.png)

Observe the server program logs the request:

![Screen Shot 2020-09-23 at 3 55 08 PM](https://user-images.githubusercontent.com/25210657/94082311-84f86280-fdb5-11ea-9604-a5081657689b.png)

### 4. Close the programs

To quit the client just type `quit` and hit return.

```
> quit
```

To quit the server, use `ctr-C`. The server will catch the `SIG-TERM` and will release any connections and close the socket.
