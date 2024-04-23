#include <typon/typon.hpp>

#include <cstdio>

using namespace typon;

Task<int> fibo(int n) {
  if (n < 2) {
    co_return n;
  }
  int a = co_await fibo(n - 1);
  int b = co_await fibo(n - 2);
  co_return a + b;
}



int main() {
  int result = fibo(40).call();
  printf("%d\n", result);
}
