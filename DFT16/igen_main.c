#include "code_rep.c"
#include "igen_dd_lib.h"
#include "random_range.c"
#include <fenv.h>
#include <math.h>
#include <stdio.h>
#include <time.h>

int main() {
  fesetround(2048);
  initRandomSeed();
  dd_I *x = malloc(32 * sizeof(dd_I));
  for (int i = 0; i < 32; i++) {
    dd_I h = getRandomDouble();
    x[i] = h;
  }
  printf("0: %.20f %.20f %.20f %.20f\n", x[0].lh, x[0].ll, x[0].uh, x[0].ul);
  dd_I *y = malloc(32 * sizeof(dd_I));
  clock_t start = clock();
  for (int i = 0; i < 1; i++) {
    DFT16(y, x);
  }
  clock_t end = clock();
  long diff_time = (end - start);
  FILE *file = fopen("score.cov", "w");
  fprintf(file, "%ld\n", diff_time);
  fclose(file);
  printf("BeforeIGenReplacement");
  return 0;
}
