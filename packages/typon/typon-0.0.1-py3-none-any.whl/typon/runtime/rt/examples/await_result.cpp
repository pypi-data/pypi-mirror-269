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

template <typename F, typename T>
constexpr bool await_of_same = std::is_same_v<meta::AwaitResult<F>, T>;

Task<void> truc() {
  // this first one requires being in a Task or Join,
  // otherwise we can't co_await a 'normal' value.
  static_assert(await_of_same<decltype(fibo(0)), decltype(co_await fibo(0))>);

  static_assert(
    await_of_same<decltype(fibo_task(0)), decltype(co_await fibo_task(0))>);

  static_assert(
    await_of_same<decltype(fibo_join(0)), decltype(co_await fibo_join(0))>);

  co_return;
}

int main() {
  truc().call();

  static_assert(await_of_same<decltype(fibo(0)), int>);
  static_assert(await_of_same<decltype(fibo_task(0)), int &>);
  static_assert(await_of_same<decltype(fibo_join(0)), int &>);

  return 0;
}
