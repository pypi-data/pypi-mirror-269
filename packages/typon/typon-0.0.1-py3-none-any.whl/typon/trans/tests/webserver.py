# coding: utf-8
# norun

import sys
from socket import socket, SOCK_STREAM, AF_INET6, SOL_SOCKET, SO_REUSEADDR
#from typon import fork
#fork = lambda x: x()




def create_listening_socket(port):
    BACKLOG = 1024

    sockfd = socket(AF_INET6, SOCK_STREAM)
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(("", port))
    sockfd.listen(BACKLOG)
    return sockfd

def read_file(path):
    fd = open(path, "r")
    content = fd.read()
    fd.close()
    return content

def handle_connection(connfd, filepath):
    buf = connfd.recv(1024).decode("utf-8")
    #length = buf.find("\r\n\r\n")
    content = read_file(filepath)
    response_fmt = \
        "HTTP/1.0 200 OK\r\n" \
        "Content-type: text/plain\r\n" \
        "Content-length: {}\r\n" \
        "\r\n" \
        "{}"
    response = response_fmt.format(len(content), content)
    connfd.send(response)
    connfd.close()

def server_loop(sockfd, filepath):
    while True:
        connfd = sockfd.accept()[0]

        fork(lambda: handle_connection(connfd, filepath))

if __name__ == "__main__":
    PORT = 8000

    # if len(sys.argv) > 2:
    #     print("Usage: webserver [ filepath ]")
    #     sys.exit(1)

    l = len(sys.argv)
    filepath = sys.argv[1] if l == 2 else "requirements.txt"
    filepath = "requirements.txt"
    print("Serving", filepath, "on port", PORT)

    sockfd = create_listening_socket(PORT)

    server_loop(sockfd, filepath)