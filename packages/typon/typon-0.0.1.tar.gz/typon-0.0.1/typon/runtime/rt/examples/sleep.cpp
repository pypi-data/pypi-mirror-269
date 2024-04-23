#include <typon/typon.hpp>
#include <typon/logger.hpp>

#include <chrono>

using namespace typon;

Task<void> sleep(int t) {
  LOG("sleep(%d)", t);
  co_await io::sleep(std::chrono::seconds(t));
  LOG("sleep(%d) >>> woke up", t);
}

Join<void> parallel() {
  for (int t = 0; t < 10; t++) {
    co_await fork(sleep(t / 2 + 1));
  }
}

Root root() {
  co_await parallel();
}

int main() {
  root().call();
  puts("done");
  return 0;
}
