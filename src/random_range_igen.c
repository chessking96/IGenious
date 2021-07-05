#include <stdlib.h>
#include <math.h>
#include "igen_dd_lib.h"

void initRandomSeed(){
	srand(42);
}

//from Joao
double getRandomNumUniform(int magnitude){

	int rnum = rand();

	double min = pow(2, magnitude);
	double max = pow(2, magnitude + 1);

	return (max - min) * ( (double)(rnum + 1) / (double)RAND_MAX ) + min;
}

double getRandomPositiveDouble(int min_exp, int dyn_range){
	int rand_magnitude = (int)(((rand() / (double)RAND_MAX) * (dyn_range - min_exp)) + min_exp);
	return getRandomNumUniform(rand_magnitude);
}

double getRandomDouble(){
	int factor = 1;
	int min_exp = factor - 5;
	int dyn_range = factor;
	double r_num = getRandomPositiveDouble(min_exp, dyn_range);
	if(rand() % 2 == 0){
		r_num = -r_num;
	}
	//printf("%.17g\n", r_num);
	return r_num;
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

    // Do some computation, that immediate casting is not a problem
    c = _ia_add_dd(c, _ia_one_dd());
    c = _ia_sub_dd(c, _ia_one_dd());

    fesetround(rm);

    return c;
}

dd_I getRandomDoubleDoubleInterval() {
	return getRandomDDI();
}
f64_I getRandomDoubleInterval() {
	return _ia_cast_dd_to_f64(getRandomDDI());
}
f32_I getRandomFloatInterval() {
	return _ia_cast_dd_to_f32(getRandomDDI());
}
