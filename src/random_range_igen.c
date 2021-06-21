#include <stdlib.h>
#include <math.h>
#include "igen_dd_lib.h"

void initRandomSeed(){
	srand(42);
}

double getRandomDouble(){
	return ((double)rand())/(RAND_MAX);
}

// from Joao
dd_I getRandomDDI() {
    int rm = fegetround();
    int n;

    double a = getRandomDouble();
    double b = frexp(getRandomDouble(), &n) * 2.0;

    fesetround(FE_DOWNWARD);
    double s_lo  = a * b;
    double t_lo  = fma(a, b, -s_lo);

    fesetround(FE_UPWARD);
    double s_up  = a * b;
    double t_up  = fma(a, b, -s_up) + DBL_MIN;

    dd_I c = _ia_set_dd(-s_lo, -t_lo, s_up, t_up);

    fesetround(rm);
    return c;
}

dd_I getRandomDoubleDoubleInterval() {
	return _ia_cast_f64_to_dd(_ia_cast_dd_to_f64(getRandomDDI()));
}
f64_I getRandomDoubleInterval() {
	return _ia_cast_dd_to_f64(getRandomDDI());
}
f32_I getRandomFloatInterval() {
	return _ia_cast_dd_to_f32(getRandomDDI());
}
