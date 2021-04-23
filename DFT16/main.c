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
  	int max = 0;
	dd_I diff_max = _ia_zero_dd();
	for(int i = 0; i < 32; i++){
		dd_I lower_bound = _ia_set_dd(y[i].lh, y[i].ll, -y[i].lh, -y[i].ll);
		dd_I upper_bound = _ia_set_dd(-y[i].uh, -y[i].ul, y[i].uh, y[i].ul);
		dd_I diff = _ia_sub_dd(upper_bound, lower_bound);
		if(_ia_cmpgt_dd(diff, diff_max)){
			diff_max = diff;
			max = i;
		}
	}
	char* answer = "true";
	double th = 0.0000001;
	if(_ia_cmpgt_dd(diff_max, _ia_set_dd(-th, 0, th, 0))){
		answer = "false";
	}
	printf("1: %.20f %.20f %.20f %.20f\n", y[0].lh, y[0].ll, y[0].uh, y[0].ul);
	file = fopen("sat.cov", "w");
	fprintf(file, "%s\n", answer);
	fclose(file);

  return 0;
}
