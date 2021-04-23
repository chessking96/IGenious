#include "random_range.c"
#include "code_rep.c"
#include <time.h>
#include <stdio.h>
#include <fenv.h>
#include <math.h>

int main(){
	fesetround(FE_UPWARD);
	initRandomSeed();
	long double* x = malloc(32*sizeof(long double));
	for(int i = 0; i < 32; i++){
		long double h = getRandomDouble();
		x[i] = h;
	}
	printf("0: %.20f %.20f %.20f %.20f\n", x[0].lh, x[0].ll, x[0].uh, x[0].ul);
	long double* y = malloc(32*sizeof(long double));
	clock_t start = clock();
	for(int i = 0; i < 1; i++){
		DFT16(y, x);
	}
	clock_t end = clock();
	long diff_time = (long)(end-start);
	FILE* file = fopen("score.cov", "w");
	fprintf(file, "%ld\n", diff_time);
	fclose(file);
	printf("BeforeIGenReplacement");
	return 0;
}
