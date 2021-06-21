#include "bisection_root.c"
#include "igen_dd_lib.h"
#include "random_range.c"
#include <fenv.h>
#include <math.h>
#include <stdio.h>
#include <time.h>
int main() {
  fesetround(2048);
  initRandomSeed();
  dd_I return_value = _ia_set_dd(-0, 0.0, 0, 0.0);
  clock_t start = clock();
  for (long i = 0; i < 1; i++) {
    return_value = bisection_root();
  }
  clock_t end = clock();
  long diff_time = (end - start);
  FILE *file = fopen("score.cov", "w");
  fprintf(file, "%ld\n", diff_time);
  fclose(file);
	int max = 0;
	int imax = 0;
	dd_I diff_max = _ia_zero_dd();
	dd_I lower_bound = _ia_set_dd(return_value.lh, return_value.ll, -return_value.lh, -return_value.ll);
	dd_I upper_bound = _ia_set_dd(-return_value.uh, -return_value.ul, return_value.uh, return_value.ul);
	dd_I diff = _ia_sub_dd(upper_bound, lower_bound);
	if(_ia_cmpgt_dd(diff, diff_max)){
		diff_max = diff;
		max = -1;
	}
	char* answer = "false";
	double th = 10000000000;
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