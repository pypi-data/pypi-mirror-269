# coding: utf-8
# norun

import sys
from socket import socket, SOCK_STREAM, AF_INET6, SOL_SOCKET, SO_REUSEADDR
from python.builtins import eval
#fork = lambda x: x()

BACKLOG = 1024
PORT = 8000

response_fmt = \
    "HTTP/1.0 200 OK\r\n" \
    "Content-type: text/plain\r\n" \
    "Content-length: {}\r\n" \
    "\r\n" \
    "{}"

def create_listening_socket(port):
    sockfd = socket(AF_INET6, SOCK_STREAM)
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(("", port))
    sockfd.listen(BACKLOG)
    return sockfd

def handle_connection(connfd):
    buf: str = connfd.recv(1024).decode("utf-8")
    resp: str
    if not buf.startswith("GET /eval?e="):
        resp = "Expression missing"
    else:
        http_pos = buf.find("HTTP/1.1\r\n")
        s = "str(" + buf[12:http_pos-1] + ")"
        context = {"req": buf}
        resp = eval(s, context)
    response = response_fmt.format(len(resp), resp)
    connfd.send(response.encode("utf-8"))
    connfd.close()

def server_loop(sockfd):
    while True:
        #connfd, _ = sockfd.accept()
        connfd = sockfd.accept()[0]

        fork(lambda: handle_connection(connfd))

if __name__ == "__main__":
    print("Serving on port", PORT)
    print()

    sockfd = create_listening_socket(PORT)

    server_loop(sockfd)
