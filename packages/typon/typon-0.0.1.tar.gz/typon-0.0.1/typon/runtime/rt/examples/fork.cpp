#include <typon/typon.hpp>
#include <typon/logger.hpp>

using namespace typon;

int fibo(int n) {
  if (n < 2)
    return n;
  return fibo(n - 1) + fibo(n - 2);
}

Task<void> hello(int id) {
  int n = fibo(40);
  LOG("hello(%d), fibo(20) = %d", id, n);
  co_return;
}

Join<void> parallel() {
  for (int id = 0; id < 30; id++) {
    co_await fork(hello(id));
    LOG("resume after fork(hello(%d))", id);
  }
  LOG("sync()");
  co_await Sync();
  LOG("resume after sync()");
  for (int id = 30; id < 60; id++) {
    co_await fork(hello(id));
    LOG("resume after fork(hello(%d))", id);
  }
}

Root root() {
  co_await parallel();
  LOG("resume root after parallel()");
}

int main() {
  root().call();
  puts("done");
  return 0;
}
