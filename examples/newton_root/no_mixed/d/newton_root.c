#include "igen_dd_math.h"
#include "igen_math.h"
#include "igen_lib.h"
#include "igen_dd_lib.h"
#include "igen_dd_lib.h"

dd_I func(f64_I x) {
  x = _ia_neg_f64(x);
  f64_I _t1 = _ia_mul_f64(x, x);
  f64_I _t2 = _ia_mul_f64(_t1, x);
  f64_I _t3 = _ia_mul_f64(x, x);
  f64_I _t4 = _ia_sub_f64(_t2, _t3);
  f64_I _t5 = _ia_set_f64(-2.0, 2.0);
  f64_I _t6 = _ia_add_f64(_t4, _t5);
  dd_I _ret;
  _ret = _ia_cast_f64_to_dd(_t6);
  return _ret;
}

dd_I derivFunc(f64_I x) {
  f64_I _t7 = _ia_set_f64(-3.0, 3.0);
  f64_I _t8 = _ia_mul_f64(_t7, x);
  f64_I _t9 = _ia_set_f64(-2.0, 2.0);
  f64_I _t10 = _ia_mul_f64(_t8, x);
  f64_I _t11 = _ia_mul_f64(_t9, x);
  f64_I _t12 = _ia_sub_f64(_t10, _t11);
  dd_I _ret;
  _ret = _ia_cast_f64_to_dd(_t12);
  return _ret;
}

dd_I newton_root() {
  f64_I x = {-20.0, 20.0};
  dd_I _t13 = func(x);
  dd_I _t14 = derivFunc(x);
  dd_I _t15 = _ia_div_dd(_t13, _t14);
  f64_I h = _ia_cast_dd_to_f64(_t15);
  for (int i = 0; i < 20; i++) {
    dd_I _t16 = func(x);
    dd_I _t17 = derivFunc(x);
    dd_I _t18 = _ia_div_dd(_t16, _t17);
    h = _ia_cast_dd_to_f64(_t18);
    x = _ia_sub_f64(x, h);
  }

  dd_I _ret;
  _ret = _ia_cast_f64_to_dd(x);
  return _ret;
}
