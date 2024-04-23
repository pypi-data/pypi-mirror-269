#include <typon/typon.hpp>
#include <cstdio>


using namespace typon;

Task<int> fibo(int n) {
  if (n < 2) {
    co_return n;
  }
  Future a = co_await future(fibo(n - 1));
  Future b = co_await future(fibo(n - 2));
  co_return co_await a.get() + co_await b.get();
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
