#include "dot.c"
#include "igen_dd_lib.h"
#include "random_range_igen.c"
#include <fenv.h>
#include <math.h>
#include <stdio.h>
#include <time.h>
int main() {
  fesetround(2048);
  initRandomSeed();
  dd_I *x_0 = malloc(1000 * sizeof(dd_I));
  for (int i = 0; i < 1000; i++) {
    dd_I h = getRandomDoubleDoubleInterval();
    x_0[i] = h;
  }
  dd_I *x_1 = malloc(1000 * sizeof(dd_I));
  for (int i = 0; i < 1000; i++) {
    dd_I h = getRandomDoubleDoubleInterval();
    x_1[i] = h;
  }
  dd_I return_value = _ia_set_dd(-0, 0.0, 0, 0.0);
  clock_t start = clock();
  for (long i = 0; i < 10000; i++) {
    return_value = dot(x_0, x_1);
  }
  clock_t end = clock();
  long diff_time = (end - start);
  FILE *file = fopen("score.cov", "w");
  fprintf(file, "%ld\n", diff_time);
  fclose(file);
  printf("BeforeIGenReplacement\n");
}
