#include <typon/typon.hpp>
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <random>
#include <vector>


using namespace typon;

long N = 1 << 26;
long C = N >> 8;

template <typename RandomIt>
Task<void> shuffle(RandomIt first, RandomIt last)
{
  std::shuffle(first, last, std::mt19937{std::random_device{}()});
  co_return;
}

template <typename RandomIt>
Join<void> parallel_shuffle(RandomIt first, RandomIt last)
{
  auto it = first;
  for (; it < last; it += C) {
    co_await fork(shuffle(it, it + C));
  }
  if (it < last)
  {
    co_await fork(shuffle(it, last));
  }
}

Root root() {
  std::vector<long> v;
  v.reserve(N);
  for (long i = 0; i < N; i++) {
    v.push_back(i);
  }
  co_await parallel_shuffle(v.begin(), v.end());
  printf("v[0] = %lu\n", v[0]);
}

int main() {
  root().call();
  puts("done");
}
