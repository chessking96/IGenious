#include <stdlib.h>
void initRandomSeed(){
	srand(42);
}
dd_I getRandomDouble() {
	long double r1 = ((long double)rand())/(RAND_MAX);
	long double r2 = ((long double)rand())/(RAND_MAX);
	return _ia_set_dd(-r1, -r2, r1, r2);
}
