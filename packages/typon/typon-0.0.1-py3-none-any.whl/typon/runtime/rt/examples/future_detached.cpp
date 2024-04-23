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
  Future f = co_await future(producer(40));
  printf("[%u] leaking future\n", Scheduler::thread_id);
}

Root root() {
  co_await consumer();
}

int main() {
  root().call();
  puts("done");
  return 0;
}
