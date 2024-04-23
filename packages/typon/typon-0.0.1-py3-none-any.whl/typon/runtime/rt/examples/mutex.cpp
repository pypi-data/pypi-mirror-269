#include <typon/typon.hpp>
#include <typon/logger.hpp>


using namespace typon;

Mutex mutex;

int N = 30;

int fibo(int n) {
  if (n < 2)
    return n;
  return fibo(n - 1) + fibo(n - 2);
}

Task<void> with_lock(int id)
{
  {
    LOG("with_lock(%d), locking", id);
    auto lock = mutex.lock();
    co_await lock;
    LOG("with_lock(%d), acquired", id);
    int n = fibo(N);
    LOG("with_lock(%d), fibo(%d) = %d", id, N, n);
    LOG("with_lock(%d), releasing", id);
  }
  LOG("with_lock(%d), released", id);
}

Join<void> parallel() {
  for (int id = 0; id < 10; id++) {
    co_await fork(with_lock(id));
  }
}

Root root() {
  co_await parallel();
}

int main() {
  root().call();
  puts("done");
  return 0;
}
