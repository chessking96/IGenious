#include "igen_dd_lib.h"
dd_I dot(f64_I *x, f64_I *y) {
  f64_I t = {-0.0, 0.0};
  long n = 1000000;
  for (int i = 0; i < n; i++) {
    f64_I _t1 = _ia_mul_f64(x[i], y[i]);
    t = _ia_add_f64(t, _t1);
  }

  dd_I _ret;
  _ret = _ia_cast_f64_to_dd(t);
  return _ret;
}
