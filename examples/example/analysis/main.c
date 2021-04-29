#include "random_range.c"
#include "example.c"
#include <time.h>
#include <stdio.h>
#include <fenv.h>
#include <math.h>
int main(){
	fesetround(FE_UPWARD);
	initRandomSeed();
	long double* y = malloc(32 * sizeof(long double));
	clock_t start = clock();
	for(int i = 0; i < 1; i++){
		example(y);
	}
	clock_t end = clock();
	long diff_time = (long)(end-start);
	FILE* file = fopen("score.cov", "w");
	fprintf(file, "%ld\n", diff_time);
	fclose(file);
	printf("BeforeIGenReplacement");
}
