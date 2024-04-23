#include <cstdio>

int fibo(int n) {
  if (n < 2) {
    return n;
  }
  int a = fibo(n - 1);
  int b = fibo(n - 2);
  return a + b;
}


int main() {
  int result = fibo(40);
  printf("%d\n", result);
  puts("done");
  return 0;
}
