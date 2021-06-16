#include "igen_dd_lib.h"
#include "matmul.c"
#include "random_range_igen.c"
#include <fenv.h>
#include <math.h>
#include <stdio.h>
#include <time.h>
int main() {
  fesetround(2048);
  initRandomSeed();
  dd_I *x_0 = malloc(10000 * sizeof(dd_I));
  for (int i = 0; i < 10000; i++) {
    dd_I h = getRandomDoubleDoubleInterval();
    x_0[i] = h;
  }
  dd_I *x_1 = malloc(10000 * sizeof(dd_I));
  for (int i = 0; i < 10000; i++) {
    dd_I h = getRandomDoubleDoubleInterval();
    x_1[i] = h;
  }
  dd_I *x_2 = malloc(10000 * sizeof(dd_I));
  for (int i = 0; i < 10000; i++) {
    dd_I h = _ia_set_dd(-0, 0.0, 0, 0.0);
    x_2[i] = h;
  }
  clock_t start = clock();
  for (long i = 0; i < 20; i++) {
    matmul(x_0, x_1, x_2);
  }
  clock_t end = clock();
  long diff_time = (end - start);
  FILE *file = fopen("score.cov", "w");
  fprintf(file, "%ld\n", diff_time);
  fclose(file);
  printf("BeforeIGenReplacement\n");
}
