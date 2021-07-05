#include "igen_dd_lib.h"
dd_I dot(f32_I *x, f32_I *y) {
  f32_I t = {-0.0, 0.0};
  long n = 1000000;
  for (int i = 0; i < n; i++) {
    f32_I _t1 = _ia_mul_f32(x[i], y[i]);
    t = _ia_add_f32(t, _t1);
  }

  dd_I _ret;
  _ret = _ia_cast_f32_to_dd(t);
  return _ret;
}
