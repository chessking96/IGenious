#include "igen_dd_math.h"
#include "igen_math.h"
#include "igen_lib.h"
#include "igen_dd_lib.h"
#include "igen_dd_lib.h"
#include "igen_dd_math.h"
#include "math.h"

dd_I fun(f64_I x) {
  int k;
  int n;

  f64_I t1;
  f64_I d1;

  t1 = x;

  for (k = 1; k <= n; k++) {
    f64_I _t1 = _ia_set_f64(-2.0, 2.0);
    d1 = _ia_mul_f64(_t1, d1);
    f64_I _t2 = _ia_mul_f64(d1, x);
    f64_I _t3 = _ia_sin_f64(_t2);
    f64_I _t4 = _ia_div_f64(_t3, d1);
    t1 = _ia_add_f64(t1, _t4);
  }

  dd_I _ret;
  _ret = _ia_cast_f64_to_dd(t1);
  return _ret;
}

dd_I funarc() {
  int i;
  f64_I h;
  f64_I t1;
  f64_I t2;
  dd_I dppi;

  f64_I s1;

  int n = 1000000;
  dppi = _ia_set_dd(-3.1415926535897927, 0.0, 3.1415926535897936, 0.0);
  s1 = _ia_set_f64(-0.0, 0.0);
  t1 = _ia_set_f64(-0.0, 0.0);
  int _t5 = n;
  dd_I _t6 = _ia_cast_int_to_dd(_t5);
  dd_I _t7 = _ia_div_dd(dppi, _t6);
  h = _ia_cast_dd_to_f64(_t7);

  for (i = 1; i <= n; i++) {
    int _t8 = i;
    f64_I _t9 = _ia_cast_int_to_f64(_t8);
    f64_I _t10 = _ia_mul_f64(_t9, h);
    dd_I _t11 = fun(_t10);
    t2 = _ia_cast_dd_to_f64(_t11);
    f64_I _t12 = _ia_sub_f64(t2, t1);
    f64_I _t13 = _ia_sub_f64(t2, t1);
    f64_I _t14 = _ia_mul_f64(h, h);
    f64_I _t15 = _ia_mul_f64(_t12, _t13);
    f64_I _t16 = _ia_add_f64(_t14, _t15);
    f64_I _t17 = _ia_sqrt_f64(_t16);
    s1 = _ia_add_f64(s1, _t17);
    t1 = t2;
  }

  dd_I _ret;
  _ret = _ia_cast_f64_to_dd(s1);
  return _ret;
}
