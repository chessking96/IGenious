// Dummy file for Precimonious setup

#include <stdlib.h>
void initRandomSeed(){
	srand(42);
}
long double getRandomDoubleDoubleInterval() { //Interval naming is ok for now, but should be changed later
	long double r1 = ((long double)rand())/(RAND_MAX);
	return r1;
}
double getRandomDoubleInterval() {
	double r = ((double)rand())/(RAND_MAX);
	return r;
}
float getRandomFloatInterval() {
	float r = ((float)rand())/(RAND_MAX);
	return r;
}
