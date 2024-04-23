#include <typon/typon.hpp>
#include <typon/logger.hpp>
#include <cstdio>


using namespace typon;

int fibo(int n) {
  if (n < 2) {
    return n;
  }
  return fibo(n - 1) + fibo(n - 2);
}

Task<void> hello(int id) {
  int result = fibo(20);
  LOG("            || hello(%2d), fibo(20) = %d", id, result);
  co_return;
}

Task<void> fail(int delay) {
  volatile int n = fibo(delay);
  (void) n;
  throw std::exception();
  co_return;
}

Join<void> fail_join(int delay = 0) {
  co_await fork(fail(delay));
}

Join<void> join_sync(int max) {
  for (int id = 0; id < max; id++) {
    co_await fork(hello(id));
  }
  co_await fork(fail_join());
  LOG("    ... fork(fail_join()) did not throw (stolen continuation)");
  LOG("    ... sync()");
  co_await Sync();
  LOG("    ... ERROR sync() did not throw");
}

Join<void> join_no_sync(int max) {
  for (int id = 0; id < max; id++) {
    co_await fork(hello(id));
  }
  co_await fork(fail_join());
  LOG("    ... fork(fail_join()) did not throw (stolen continuation)");
  LOG("    ... join_no_sync(%d) is exiting normally", max);
}

Join<void> join_infinite_fork_loop() {
  co_await fork(fail_join(25));
  LOG("    ... fork(fail_join()) did not throw (stolen continuation)");
  LOG("    ... now looping forever");
  for (int id = 0; ; id++) {
    co_await fork(hello(id));
  }
}

Root root_sync(int max) {
  try {
    LOG(">>> join_sync(%d)", max);
    co_await join_sync(max);
    LOG("ERROR join_sync(%d) did not throw\n", max);
  } catch(std::exception &) {
    LOG("OK join_sync(%d) did throw\n", max);
  }
}

Root root_no_sync(int max) {
  try {
    LOG(">>> join_no_sync(%d)", max);
    co_await join_no_sync(max);
    LOG("ERROR join_no_sync(%d) did not throw\n", max);
  } catch(std::exception &) {
    LOG("OK join_no_sync(%d) did throw\n", max);
  }
}

Root root_infinite_fork_loop() {
  try {
    LOG(">>> join_infinite_fork_loop()");
    co_await join_infinite_fork_loop();
  } catch(std::exception &) {
    LOG("OK join_infinite_fork_loop() did throw eventually\n");
  }
}

int main() {
  root_sync(0).call();
  root_sync(20).call();
  root_no_sync(0).call();
  root_no_sync(20).call();
  root_infinite_fork_loop().call();
  puts("done");
  return 0;
}

