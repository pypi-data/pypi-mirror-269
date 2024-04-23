#include <typon/task.hpp>

#include <cstdio>

using namespace typon;

Task<int> add(int a, int b) {
  co_return a + b;
}

Task<int> loop(int n) {
  int result = 0;
  for (int i = 0; i < n; i++) {
    result = result + co_await add(i, i+1);
  }
  co_return result;
}

int main() {
  int result = loop(100000000).call();

  printf("%d\n", result);
}
