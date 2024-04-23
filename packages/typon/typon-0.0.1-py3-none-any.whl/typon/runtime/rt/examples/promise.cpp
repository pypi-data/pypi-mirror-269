#include <typon/typon.hpp>
#include <cstdio>


using namespace typon;

int fibo(int n) {
  if (n < 2)
    return n;
  return fibo(n - 1) + fibo(n - 2);
}

Task<void> consume(Promise<int> & f) {
  printf("[%u] waiting on promise\n", Scheduler::thread_id);
  int value = co_await f;
  printf("[%u] promise yielded %d\n", Scheduler::thread_id, value);
}

Task<void> produce(Promise<int> & f, int n) {
  int value = fibo(n);
  printf("[%u] producing %d\n", Scheduler::thread_id, value);
  f.put(value);
  co_return;
}

Join<void> parallel() {
  Promise<int> f;
  printf("[%u] fork(consume())\n", Scheduler::thread_id);
  co_await fork(consume(f));
  printf("[%u] fork(produce())\n", Scheduler::thread_id);
  co_await fork(produce(f, 20));
}

Root root() {
  co_await parallel();
}

int main() {
  root().call();
  puts("done");
  return 0;
}
