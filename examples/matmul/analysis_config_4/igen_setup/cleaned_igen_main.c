#include "igen_dd_lib.h"
#include "igen_rmd_matmul.c"
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
	int max = 0;
	int imax = 0;
	dd_I diff_max = _ia_zero_dd();
	for(int i = 0; i < 10000; i++){
		dd_I lower_bound = _ia_set_dd(x_2[i].lh, x_2[i].ll, -x_2[i].lh, -x_2[i].ll);
		dd_I upper_bound = _ia_set_dd(-x_2[i].uh, -x_2[i].ul, x_2[i].uh, x_2[i].ul);
		dd_I diff = _ia_sub_dd(upper_bound, lower_bound);
		if(_ia_cmpgt_dd(diff, diff_max)){
			diff_max = diff;
			max = i;
		}
	}
	char* answer = "false";
	double th = 0.0001;
	if((int)_ia_cmpgt_dd(_ia_set_dd(-th, 0, th, 0), diff_max) == 1){
		answer = "true";
	}
	file = fopen("sat.cov", "w");
	fprintf(file, "%s\n", answer);
	fclose(file);
	file = fopen("precision.cov", "w");
	double prec = _ia_cast_dd_to_f64(diff_max).up;
	fprintf(file, "%.17g\n", prec);
	printf("Precision constraint: %s\n", answer);
	printf("Diff lower bound: %.17g %.17g\n", diff_max.lh, diff_max.ll);
	printf("Diff upper bound: %.17g %.17g\n", diff_max.uh, diff_max.ul);

}
