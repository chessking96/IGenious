#include "random_range.c"
#include "matmul.c"
#include <time.h>
#include <stdio.h>
#include <fenv.h>
#include <math.h>
int main(){
	fesetround(FE_UPWARD);
	initRandomSeed();
	long double* x_0 = malloc(10000 * sizeof(long double));
	for(int i = 0; i < 10000; i++){
		long double h = getRandomDoubleDoubleInterval();
		x_0[i] = h;
	}
	long double* x_1 = malloc(10000 * sizeof(long double));
	for(int i = 0; i < 10000; i++){
		long double h = getRandomDoubleDoubleInterval();
		x_1[i] = h;
	}
	long double* x_2 = malloc(10000 * sizeof(long double));
	for(int i = 0; i < 10000; i++){
		long double h = 0;
		x_2[i] = h;
	}
	clock_t start = clock();
	for(long i = 0; i < 20; i++){
		matmul(x_0, x_1, x_2);
	}
	clock_t end = clock();
	long diff_time = (long)(end - start);
	FILE* file = fopen("score.cov", "w");
	fprintf(file, "%ld\n", diff_time);
	fclose(file);
	printf("BeforeIGenReplacement\n");
}
