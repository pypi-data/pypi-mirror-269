#ifndef TYPON_IO_HPP_INCLUDED
#define TYPON_IO_HPP_INCLUDED

#include <chrono>
#include <coroutine>
#include <string_view>

#include <linux/time_types.h>

#include <liburing.h>

#include <typon/scheduler.hpp>
#include <typon/syscall_completion.hpp>


namespace typon::io
{

  struct SyscallAwaitable : std::suspend_always
  {
    union
    {
      SyscallCompletion _completion;
      io_uring_sqe * _sqe;
    };

    SyscallAwaitable() noexcept
    {
      io_uring * ring = Scheduler::ring();
      _sqe = io_uring_get_sqe(ring);
    }

    void await_suspend(std::coroutine_handle<> continuation) noexcept
    {
      auto stack = Scheduler::suspend(continuation);
      io_uring_sqe * sqe = _sqe;
      _completion._stack = stack;
      io_uring_sqe_set_data(sqe, &(_completion));
      io_uring * ring = Scheduler::ring();
      io_uring_submit(ring);
    }

    auto await_resume() noexcept
    {
      return _completion._result;
    }
  };

  template <typename Rep, typename Period>
  auto sleep(std::chrono::duration<Rep, Period> duration) noexcept
  {
    struct awaitable : SyscallAwaitable
    {
      __kernel_timespec _ts;

      awaitable(std::chrono::duration<Rep, Period> duration) noexcept
      {
        using namespace std::chrono;
        auto sec = duration_cast<seconds>(duration);
        auto nsec = duration_cast<nanoseconds>(duration - sec);
        _ts = __kernel_timespec({sec.count(), nsec.count()});

        io_uring_prep_timeout(_sqe, &(_ts), 0, 0);
      }
    };

    return awaitable(duration);
  }

  auto write(int fd, std::string_view bytes, __u64 offset = -1) noexcept
  {
    SyscallAwaitable awaitable;
    io_uring_prep_write(awaitable._sqe, fd, bytes.data(), bytes.size(), offset);
    return awaitable;
  }

  auto read(int fd, void * buf, unsigned nbytes, __u64 offset = -1) noexcept
  {
    SyscallAwaitable awaitable;
    io_uring_prep_read(awaitable._sqe, fd, buf, nbytes, offset);
    return awaitable;
  }

  auto openat(int dfd, const char * path, int flags, mode_t mode) noexcept
  {
    SyscallAwaitable awaitable;
    io_uring_prep_openat(awaitable._sqe, dfd, path, flags, mode);
    return awaitable;
  }

  auto close(int fd) noexcept
  {
    SyscallAwaitable awaitable;
    io_uring_prep_close(awaitable._sqe, fd);
    return awaitable;
  }

  auto fsync(int fd, unsigned fsync_flags = 0) noexcept
  {
    SyscallAwaitable awaitable;
    io_uring_prep_fsync(awaitable._sqe, fd, fsync_flags);
    return awaitable;
  }

  auto statx(int dfd,
             const char * path,
             int flags,
             unsigned mask,
             struct statx * statxbuf) noexcept
  {
    SyscallAwaitable awaitable;
    io_uring_prep_statx(awaitable._sqe, dfd, path, flags, mask, statxbuf);
    return awaitable;
  }

  auto socket(int domain, int type, int protocol) noexcept
  {
    SyscallAwaitable awaitable;
    io_uring_prep_socket(awaitable._sqe, domain, type, protocol, 0);
    return awaitable;
  }

  auto accept(int sockfd,
              sockaddr * addr,
              socklen_t * addrlen,
              int flags = 0) noexcept
  {
    SyscallAwaitable awaitable;
    io_uring_prep_accept(awaitable._sqe, sockfd, addr, addrlen, flags);
    return awaitable;
  }

  auto connect(int sockfd, const sockaddr * addr, socklen_t addrlen) noexcept
  {
    SyscallAwaitable awaitable;
    io_uring_prep_connect(awaitable._sqe, sockfd, addr, addrlen);
    return awaitable;
  }

  auto recv(int sockfd, void * buf, size_t len, int flags) noexcept
  {
    SyscallAwaitable awaitable;
    io_uring_prep_recv(awaitable._sqe, sockfd, buf, len, flags);
    return awaitable;
  }

  auto send(int sockfd, std::string_view bytes, int flags) noexcept
  {
    SyscallAwaitable awaitable;
    auto len = bytes.size();
    io_uring_prep_send(awaitable._sqe, sockfd, bytes.data(), len, flags);
    return awaitable;
  }

  auto shutdown(int sockfd, int how) noexcept
  {
    SyscallAwaitable awaitable;
    io_uring_prep_shutdown(awaitable._sqe, sockfd, how);
    return awaitable;
  }

}


#endif // TYPON_IO_HPP_INCLUDED
