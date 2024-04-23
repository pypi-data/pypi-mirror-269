#include <typon/typon.hpp>
#include <cstdio>


using namespace typon;

int fibo(int n) {
  if (n < 2)
    return n;
  return fibo(n - 1) + fibo(n - 2);
}

Task<int> producer(int n) {
  int value = fibo(n);
  printf("[%u] producing %d\n", Scheduler::thread_id, value);
  co_return value;
}

Task<void> consumer() {
  printf("[%u] launching future\n", Scheduler::thread_id);
  Future f = co_await future(producer(20));
  printf("[%u] waiting on future\n", Scheduler::thread_id);
  int value = co_await f.get();
  printf("[%u] future yielded %d\n", Scheduler::thread_id, value);
}

Root root() {
  co_await consumer();
}

int main() {
  root().call();
  puts("done");
  return 0;
}
