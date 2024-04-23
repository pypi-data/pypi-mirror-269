#include <typon/typon.hpp>
#include <typon/logger.hpp>


using namespace typon;

int fibo(int n) {
  if (n < 2)
    return n;
  return fibo(n - 1) + fibo(n - 2);
}

Task<int> hello(int n) {
  int r = fibo(30);
  LOG("hello(%d)", n);
  co_return r;
}

Join<void> parallel() {
  LOG("Forked f = co_await fork(hello(10))");
  Forked f = co_await fork(hello(1));

  LOG("co_await fork(hello(10), {})");
  co_await fork(hello(2), {});

  // Careful! r must not be unwound before the fork finishes.
  LOG("int r; co_await fork(hello(10), r)");
  int r; co_await fork(hello(3), r);
  // Sync to ensure the fork finished before r is unwound.
  // Assuming there are no exceptions...
  co_await Sync();
}

Root root() {
  co_await parallel();
}

int main() {
  root().call();
  puts("done");
  return 0;
}
