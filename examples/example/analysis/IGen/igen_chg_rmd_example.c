#include "igen_dd_lib.h"
#include <math.h>
void example(dd_I *y) {
  dd_I a = _ia_set_dd(-1.0, 0.0, 1.0, 0.0);
  dd_I _t1 = _ia_set_dd(-0.29999999999999993, 0.0, 0.30000000000000004, 0.0);
  y[0] = _ia_mul_dd(a, _t1);
}
