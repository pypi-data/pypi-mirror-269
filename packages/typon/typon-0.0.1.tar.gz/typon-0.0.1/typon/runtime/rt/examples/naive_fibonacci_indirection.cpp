#include <typon/task.hpp>

#include <cstdio>

using namespace typon;


template <typename T>
Task<typename T::promise_type::value_type> call(T task)
{
  co_return co_await std::move(task);
}

Task<int> fibo(int n) {
  if (n < 2) {
    co_return n;
  }
  int a = co_await call(fibo(n - 1));
  int b = co_await call(fibo(n - 2));
  co_return a + b;
}

int main() {
  int result = fibo(40).call();
  printf("%d\n", result);
}
