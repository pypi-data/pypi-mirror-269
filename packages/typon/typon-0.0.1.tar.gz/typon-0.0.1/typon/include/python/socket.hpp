//
// Created by Tom on 13/06/2023.
//

#ifndef TYPON_SOCKET_HPP
#define TYPON_SOCKET_HPP

#include "builtins.hpp"
#include <netdb.h>
#include <netinet/in.h>
#include <tuple>

namespace py_socket {
template <typename _Unused = void>
struct socket__oo : referencemodel::moduletype<socket__oo<>> {
#undef SOCK_STREAM
#undef AF_INET6
#undef SOL_SOCKET
#undef SO_REUSEADDR
#undef AF_UNIX
  static constexpr int SOCK_STREAM = 1;
  static constexpr int AF_INET6 = 10;
  static constexpr int SOL_SOCKET = 1;
  static constexpr int SO_REUSEADDR = 2;
  static constexpr int AF_UNIX = 1;

  template <typename _Base0 = object>
  struct socket_t__oo : referencemodel::classtype<_Base0, socket_t__oo<>> {

    template <typename T>
    struct Obj : referencemodel::instance<socket_t__oo<>, Obj<T>> {
      Obj(int fd = -1) : fd(fd) {}

      Obj(const Obj &other) : fd(other.fd) {}

      int fd;
    };

    struct : referencemodel::method {
      template <typename T = void>
      auto operator()(auto self) -> typon::Task<
          std::tuple<decltype(rc(Obj<T>{-1})), decltype(""_ps)>> const {
        int connfd = co_await typon::io::accept(self->fd, NULL, NULL);
        if (connfd < 0) {
          system_error(-connfd, "accept()");
        }
        co_return std::make_tuple(rc(Obj<T>{connfd}),
                                  ""_ps); // TODO
      }
    } static constexpr accept{};

    struct : referencemodel::method {
      auto operator()(auto self, int level, int optname, int optval) const {
        if (::setsockopt(self->fd, level, optname, &optval, sizeof(int)) < 0) {
          system_error(errno, "setsockopt()");
        }
        return None;
      }
    } static constexpr setsockopt{};

    // bind
    struct : referencemodel::method {
      auto operator()(auto self, std::tuple<std::string, int> address) const {
        auto [host, port] = address;
        sockaddr_in6 addr;
        std::memset(&addr, 0, sizeof(addr));
        addr.sin6_family = AF_INET6;
        addr.sin6_port = htons(port);
        addr.sin6_addr = in6addr_any;
        if (::bind(self->fd, (const sockaddr *)&addr, sizeof(addr)) < 0) {
          system_error(errno, "bind()");
        }
        return None;
      }
    } static constexpr bind{};

    struct : referencemodel::method {
      typon::Task<typon::TyNone> operator()(auto self, int backlog) const {
        if (::listen(self->fd, backlog) < 0) {
          co_await dot(self, close)();
          system_error(errno, "listen()");
        }
        co_return None;
      }
    } static constexpr listen{};

    struct : referencemodel::method {
      typon::Task<typon::TyNone> operator()(auto self) const {
        co_await typon::io::close(self->fd);
        co_return None;
      }
    } static constexpr close{};

    struct : referencemodel::method {
      typon::Task<typon::TyBytes__oo<>::Obj> operator()(auto self,
                                                        int bufsize) const {
        std::string buf(bufsize, '\0');
        co_await typon::io::recv(self->fd, buf.data(), buf.size(), 0);
        co_return typon::TyBytes(std::move(buf));
      }
    } static constexpr recv{};

    struct : referencemodel::method {
      typon::Task<typon::TyNone> operator()(auto self, auto data) const {
        if (int sbytes = co_await typon::io::send(self->fd, data->value, 0);
            sbytes < 0) {
          co_await dot(self, close)();
          system_error(-sbytes, "send()");
        }
        co_return None;
      }
    } static constexpr send{};

    /*METHOD(typon::Task<void>, close, (Self self),
           { co_await typon::io::close(self->fd); })

    METHOD(void, listen, (Self self, int backlog), {
      if (::listen(self->fd, backlog) < 0) {
        dotp(self, close)();
        system_error(errno, "listen()");
      }
    })

    METHOD(void, setsockopt, (Self self, int level, int optname, int optval),
           {
             if (::setsockopt(self->fd, level, optname, &optval,
                              sizeof(int)) < 0) {
               system_error(errno, "setsockopt()");
             }
           })

    METHOD(void, bind,
           (Self self, std::tuple<std::string COMMA() int> address), {
             auto [host, port] = address;
             sockaddr_in6 addr;
             std::memset(&addr, 0, sizeof(addr));
             addr.sin6_family = AF_INET6;
             addr.sin6_port = htons(port);
             addr.sin6_addr = in6addr_any;
             if (::bind(self->fd, (const sockaddr *)&addr, sizeof(addr)) <
                 0) {
               system_error(errno, "bind()");
             }
           })

    METHOD(typon::Task<TyBytes>, recv, (Self self, int bufsize), {
      TyBytes buf(bufsize, '\0');
      co_await typon::io::recv(self->fd, buf.data(), buf.size(), 0);
      co_return std::move(buf);
    })

    METHOD(typon::Task<void>, send, (Self self, TyBytes data), {
      if (int sbytes = co_await typon::io::send(self->fd, data, 0);
          sbytes < 0) {
        co_await dotp(self, close)();
        system_error(-sbytes, "send()");
      }
    })*/

    template <typename T = void> auto operator()(int family, int type_) const {
      if (int fd = ::socket(family, type_, 0); fd >= 0) {
        return rc(Obj<T>{fd});
      } else {
        system_error(errno, "socket()");
      }
    }

    using ObjType = Obj<void>;
  };
  static constexpr socket_t__oo<> socket{};

  struct : referencemodel::staticmethod {
    auto operator()(std::string host, int port, int family = 0, int type_ = 0,
                    int proto = 0, int flags = 0) const {
      addrinfo hints;
      std::memset(&hints, 0, sizeof(hints));
      hints.ai_family = family;
      hints.ai_socktype = type_;
      hints.ai_protocol = proto;
      hints.ai_flags = flags;
      addrinfo *res;
      // convert port to string
      std::string port_str = std::to_string(port);
      if (int err = ::getaddrinfo(host.c_str(), port_str.c_str(), &hints, &res);
          err != 0) {
        system_error(err, "getaddrinfo()");
      }
      auto rlist = typon::TyList(
          {// make tuple (family, type, proto, canonname, sockaddr)
           // (int, int, int, str, str)
           std::make_tuple(
               typon::TyInt(res->ai_family), typon::TyInt(res->ai_socktype),
               typon::TyInt(res->ai_protocol),
               typon::TyStr(res->ai_canonname ? res->ai_canonname : ""),
               typon::TyStr(res->ai_addr ? res->ai_addr->sa_data : ""))});
      ::freeaddrinfo(res);
      return rlist;
    }
  } static constexpr getaddrinfo{};

  /*FUNCTION(auto, getaddrinfo,
           (std::string host, int port, int family = 0, int type_ = 0,
            int proto = 0, int flags = 0),
           {
             addrinfo hints;
             std::memset(&hints, 0, sizeof(hints));
             hints.ai_family = family;
             hints.ai_socktype = type_;
             hints.ai_protocol = proto;
             hints.ai_flags = flags;
             addrinfo *res;
             // convert port to string
             std::string port_str = std::to_string(port);
             if (int err = ::getaddrinfo(host.c_str(), port_str.c_str(), &hints,
                                         &res);
                 err != 0) {
               system_error(err, "getaddrinfo()");
             }
             return res;
           })*/
};
socket__oo<> all;
} // namespace py_socket

namespace typon {
// using PySocket = TyObj<py_socket::socket_t::socket_s>;
}

#endif // TYPON_SOCKET_HPP
