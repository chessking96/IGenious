#include <stdlib.h>
#include <stdio.h>


int main(){
	srand(42);
	double r = ((double)rand())/(RAND_MAX);
	printf("%.20g\n", r);
}
