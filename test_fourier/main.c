#include "random_range.c"
#include "DFT16.c"
#include <stdio.h>

int main(){
	double* y = malloc(128*sizeof(double));
	double* x = malloc(128*sizeof(double));
	
	for(int i = 0; i < 128; i++){
		x[i] = 0;
		y[i] = 0;
	}
	
	for(int i = 0; i < 32; i++){
		x[i] = 10;
	}
	
	//x[31] = 9000;
	
	

	DFT16(y, x);

	for(int i = 0; i < 128; i++){
		printf("%d %f  %f\n", i, x[i], y[i]);
	}


	return 0;
}
