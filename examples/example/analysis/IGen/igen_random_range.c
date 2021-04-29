#include "igen_dd_lib.h"
#include <stdlib.h>

dd_I getRandomDouble() {
  int _t1 = rand();
  int _t2 = (2147483647);
  dd_I _t3 = _ia_cast_int_to_dd(_t1);
  dd_I _t4 = _ia_cast_int_to_dd(_t2);
  dd_I _t5 = _ia_div_dd(_t3, _t4);
  dd_I _t6 = _ia_set_dd(-1000, 0.0, 1000, 0.0);
  dd_I r1 = _ia_mul_dd(_t5, _t6);
  int _t7 = rand();
  int _t8 = (2147483647);
  dd_I _t9 = _ia_cast_int_to_dd(_t7);
  dd_I _t10 = _ia_cast_int_to_dd(_t8);
  dd_I _t11 = _ia_div_dd(_t9, _t10);
  dd_I _t12 = _ia_set_dd(-1000, 0.0, 1000, 0.0);
  dd_I r2 = _ia_mul_dd(_t11, _t12);

  return r1;
}

void initRandomSeed() { srand(42); }
