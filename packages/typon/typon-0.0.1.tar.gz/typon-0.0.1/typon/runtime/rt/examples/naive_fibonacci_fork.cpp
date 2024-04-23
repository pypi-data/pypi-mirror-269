#include <typon/typon.hpp>
#include <cstdio>


using namespace typon;

Join<int> fibo(int n) {
  if (n < 2) {
    co_return n;
  }
  Forked a = co_await fork(fibo(n - 1));
  Forked b = co_await fork(fibo(n - 2));
  co_await Sync();
  co_return a.get() + b.get();
}

Root root() {
  int result = co_await fibo(40);
  printf("%d\n", result);
}

int main() {
  root().call();
  puts("done");
  return 0;
}
