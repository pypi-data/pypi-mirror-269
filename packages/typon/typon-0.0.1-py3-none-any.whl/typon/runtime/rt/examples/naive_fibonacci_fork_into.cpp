#include <typon/typon.hpp>
#include <cstdio>


using namespace typon;

Join<int> fibo(int n) {
  if (n < 2) {
    co_return n;
  }
  // Danger !
  // The memory for a and b could be freed before the forks complete
  int a; co_await fork(fibo(n - 1), a);
  int b; co_await fork(fibo(n - 2), b);
  // This sync() ensures that the forks complete before a and b are freed
  // As long as there are no exceptions...
  co_await Sync();
  co_return a + b;
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
