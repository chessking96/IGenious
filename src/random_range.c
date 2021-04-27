#include <stdlib.h>

long double getRandomDouble() {
	long double r1 = (((long double)rand())/(RAND_MAX)*1000);
	long double r2 = (((long double)rand())/(RAND_MAX)*1000);
 	//printf("%.20g %.20g %.20g %.20g\n", rv.lh, rv.ll, rv.uh, rv.ul);
 	//printf("%.20g %.20g %.20g %.20g\n", rv.lo.h, rv.lo.l, rv.up.h, rv.up.l);
    return r1;
}

void initRandomSeed() {
	srand(42);
}


