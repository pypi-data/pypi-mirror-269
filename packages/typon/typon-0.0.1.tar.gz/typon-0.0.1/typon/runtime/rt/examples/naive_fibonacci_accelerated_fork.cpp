#include <typon/typon.hpp>
#include <cstdio>


using namespace typon;

int fibo(int n) {
  if (n < 2) {
    return n;
  }
  int a = fibo(n - 1);
  int b = fibo(n - 2);
  return a + b;
}

Join<int> parallel_fibo(int n) {
  if (n < 2) {
    co_return n;
  }
  if (n < 25)
  {
    int a = fibo(n - 1);
    int b = fibo(n - 2);
    co_return a + b;
  }
  auto a = co_await fork(parallel_fibo(n - 1));
  auto b = co_await fork(parallel_fibo(n - 2));
  co_await Sync();
  co_return a.get() + b.get();
}

Root root() {
  int result = co_await parallel_fibo(40);
  printf("%d\n", result);
}

int main() {
  root().call();
  puts("done");
  return 0;
}
