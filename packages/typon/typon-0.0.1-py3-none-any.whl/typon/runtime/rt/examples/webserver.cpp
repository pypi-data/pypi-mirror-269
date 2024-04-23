#include <typon/typon.hpp>

#include <cerrno>
#include <cstdio>
#include <cstring>
#include <exception>
#include <string>
#include <string_view>
#include <system_error>

#include <netdb.h>
#include <netinet/in.h>

#include <fmt/format.h>


constexpr int BACKLOG = 1024;
constexpr int PORT = 8000;


using namespace typon;


#define system_error(err, message) \
  do { puts(message); throw fmt::system_error(err, message); } while(0)


constexpr const char * response_fmt = \
  "HTTP/1.0 200 OK\r\n"
  "Content-type: text/plain\r\n"
  "Content-length: {}\r\n"
  "\r\n"
  "{}";


Task<int> create_listening_socket(int port) {
  // asynchronous socket() system call with io_uring
  // is only supported starting with kernel version 5.19
  int sockfd = socket(PF_INET6, SOCK_STREAM, 0);
  if (sockfd < 0) {
    system_error(errno, "socket()");
  }

  int yes = 1;
  if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int)) < 0) {
    co_await io::close(sockfd);
    system_error(errno, "setsockopt(SO_REUSEADDR)");
  }

  sockaddr_in6 addr;
  std::memset(&addr, 0, sizeof(addr));
  addr.sin6_family = AF_INET6;
  addr.sin6_port = htons(port);
  addr.sin6_addr = in6addr_any;

  if (bind(sockfd, (const sockaddr *) &addr, sizeof(addr)) < 0) {
    co_await io::close(sockfd);
    system_error(errno, "bind()");
  }

  if (listen(sockfd, BACKLOG) < 0) {
    co_await io::close(sockfd);
    system_error(errno, "listen()");
  }

  co_return sockfd;
}


Task<std::string> read_file(const char * path) {
  struct statx statxbuf;
  if (int err = co_await io::statx(AT_FDCWD, path, 0, STATX_SIZE, &statxbuf)) {
    system_error(-err, "statx()");
  }

  int fd = co_await io::openat(AT_FDCWD, path, O_RDONLY, 0);
  if (fd < 0) {
    system_error(-fd, "openat()");
  }

  auto size = statxbuf.stx_size;
  std::string buf(size, '\0');
  int nbytes = co_await io::read(fd, buf.data(), size);

  co_await io::close(fd);

  if (nbytes < 0) {
    system_error(-nbytes, "read()");
  }

  co_return std::move(buf);
}


Task<void> handle_connection(int connfd, const char * filepath) {
  std::string buf(1024, '\0');
  int nbytes = co_await io::recv(connfd, buf.data(), buf.size(), 0);
  auto length = buf.find("\r\n\r\n");
  if (length == std::string::npos) {
    length = nbytes;
  }
  std::string_view message(buf.data(), length);

  std::string content;
  try {
    content = co_await read_file(filepath);
  } catch(std::exception &) {
    co_await io::close(connfd);
    throw;
  }

  std::string response = fmt::format(response_fmt, content.size(), content);

  int sbytes = co_await io::send(connfd, response, 0);
  if (sbytes < 0) {
    co_await io::close(connfd);
    system_error(-sbytes, "send()");
  }

  co_await io::close(connfd);
}


Join<void> server_loop(int sockfd, const char * filepath) {
  for(;;) {
    int connfd = co_await io::accept(sockfd, NULL, NULL);
    if (connfd < 0) {
      system_error(-connfd, "accept()");
    }

    co_await fork(handle_connection(connfd, filepath));
  }
}


Join<void> server_loops(int sockfd, const char * filepath) {
  for (int i = 0; i < 20; i++) {
    co_await fork(server_loop(sockfd, filepath));
  }
}


Root root(int argc, char * argv[]) {
  if (argc > 2)
  {
    co_await io::write(1, "Usage: webserver [ filepath ]\n");
    co_return;
  }

  const char * filepath = argc == 2 ? argv[1] : "webserver.cpp";

  int sockfd = co_await create_listening_socket(PORT);

  try {
    co_await server_loops(sockfd, filepath);
  } catch(std::exception & e) {
    puts(e.what());
  }

  co_await io::close(sockfd);
}


int main(int argc, char * argv[]) {
  root(argc, argv).call();
}
