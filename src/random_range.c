#include <stdlib.h>
void initRandomSeed(){
	srand(42);
}
long double getRandomDoubleDouble() {
	long double r1 = ((long double)rand())/(RAND_MAX);
	return r1;
}
double getRandomDouble() {
	double r = ((double)rand())/(RAND_MAX);
	return r;
}
float getRandomFloat() {
	double r = ((float)rand())/(RAND_MAX);
	return r;
}
