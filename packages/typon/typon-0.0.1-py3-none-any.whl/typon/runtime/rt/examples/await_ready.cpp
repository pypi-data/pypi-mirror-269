#include <typon/typon.hpp>

using namespace typon;

int fibo(int n) {
  if (n < 2)
    return n;
  return fibo(n - 1) + fibo(n - 2);
}

Task<int> fibo_task(int n) {
  int r = co_await fibo(n);
  co_return r;
}

Join<int> fibo_join(int n) {
  if (n < 8) {
    int x = co_await fibo(n - 1);
    int y = co_await fibo_task(n - 2);
    co_return x + y;
  }
  Forked a = co_await fork(fibo_join(n - 1));
  int b = co_await fibo_join(n - 2);
  co_await Sync();
  co_return a.get() + b;
}

Root root() {
  int result = co_await fibo_join(40);
  printf("%d\n", result);
}

int main() {
  root().call();
  return 0;
}
