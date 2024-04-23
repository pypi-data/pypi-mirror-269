#include <typon/typon.hpp>
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <random>
#include <vector>


using namespace typon;
using u64 = std::uint_fast64_t;

u64 N = u64(1) << 26;
int C = 256;
int R = 100;

Task<u64> sum(u64 * array, u64 size)
{
  u64 s = 0;
  for (u64 i = 0; i < size; i++) {
    s += array[i];
  }
  co_return s;
}

Join<u64> parallel_sum(u64 * array, u64 size)
{
  std::vector<Forked<u64>> v;
  v.reserve(C - 1);
  u64 start = 0;
  u64 chunk = size / C;
  for (int i = 0; i < C - 1; i++) {
    v.push_back(co_await fork(sum(&(array[start]), chunk)));
    start = start + chunk;
  }
  u64 s = co_await sum(&(array[start]), size - start);
  co_await Sync();
  for (auto & f : v) {
    s += f.get();
  }
  co_return s;
}

Root root() {
  std::vector<u64> v;
  v.reserve(N);
  for (u64 i = 0; i < N; i++) {
    v.push_back(i);
  }
  u64 result = 0;
  for (int i = 0; i < R; i++) {
    result += co_await parallel_sum(v.data(), v.size());
  }
  printf("sum = %lu\n", result);
}

int main() {
  root().call();
  puts("done");
}
