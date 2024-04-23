#include <typon/typon.hpp>

#include <cstdio>
#include <string>

using namespace typon;

Task<int> cat(const char * path) {
  struct statx statxbuf;
  if (int err = co_await io::statx(AT_FDCWD, path, 0, STATX_SIZE, &statxbuf))
  {
    co_return err;
  }
  int fd = co_await io::openat(AT_FDCWD, path, O_RDONLY, 0);
  if (fd < 0) {
    co_return fd;
  }

  auto size = statxbuf.stx_size;
  std::string buf(size, '\0');
  int nbytes = co_await io::read(fd, buf.data(), size);

  co_await io::close(fd);

  if (nbytes < 0) {
    co_return nbytes;
  }

  co_return co_await io::write(1, buf);
}


Root root(int argc, char * argv[]) {
  if (argc < 2) {
    fprintf(stderr, "Usage: %s [file name] <[file name] ...>\n", argv[0]);
  }

  for (int i = 1; i < argc; i++) {
    int res = co_await cat(argv[i]);
    if (res < 0) {
      fprintf(stderr, "Failed to cat %s\n", argv[i]);
    }
  }
}

int main(int argc, char * argv[]) {
  root(argc, argv).call();
}
