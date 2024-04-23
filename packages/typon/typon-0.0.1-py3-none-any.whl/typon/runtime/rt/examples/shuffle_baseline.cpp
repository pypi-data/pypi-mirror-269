#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <random>
#include <vector>


using u32 = std::uint_fast32_t;

u32 N = u32(1) << 26;

int main() {
  std::vector<u32> v;
  v.reserve(N);
  for (u32 i = 0; i < N; i++) {
    v.push_back(i);
  }
  std::shuffle(v.begin(), v.end(), std::mt19937{std::random_device{}()});
  printf("v[0] = %lu\n", v[0]);
  puts("done");
}
