#include <stdlib.h>

double getRandomDouble() {
 	double random_value = (double)rand()/RAND_MAX*2.0-1.0;
    return random_value;
}

void initRandomSeed() {
	srand(42);
}


