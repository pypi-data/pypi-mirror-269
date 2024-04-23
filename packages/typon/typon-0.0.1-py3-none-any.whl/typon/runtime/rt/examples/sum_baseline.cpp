#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <random>
#include <vector>


using u64 = std::uint_fast64_t;

u64 N = u64(1) << 26;
int R = 100;

u64 sum(u64 * array, u64 size)
{
  u64 s = 0;
  for (u64 i = 0; i < size; i++) {
    s += array[i];
  }
  return s;
}

int main() {
  std::vector<u64> v;
  v.reserve(N);
  for (u64 i = 0; i < N; i++) {
    v.push_back(i);
  }
  u64 result = 0;
  for (int i = 0; i < R; i++) {
    result += sum(v.data(), v.size());
  }
  printf("sum = %lu\n", result);
  puts("done");
}
