#include <stdlib.h>

long double getRandomDouble() {
	long double rv = (((long double)rand())/(RAND_MAX)*1000);
 	//printf("%.20g %.20g %.20g %.20g\n", rv.lh, rv.ll, rv.uh, rv.ul);
 	//printf("%.20g %.20g %.20g %.20g\n", rv.lo.h, rv.lo.l, rv.up.h, rv.up.l);
    return rv;
}

void initRandomSeed() {
	srand(42);
}


