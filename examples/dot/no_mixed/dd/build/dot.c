#include "igen_dd_lib.h"
dd_I dot(dd_I *x, dd_I *y) {
  dd_I t = _ia_set_dd(-0, 0.0, 0, 0.0);
  long n = 10000000;
  for (int i = 0; i < n; i++) {
    dd_I _t1 = _ia_mul_dd(x[i], y[i]);
    t = _ia_add_dd(t, _t1);
  }

  return t;
}
