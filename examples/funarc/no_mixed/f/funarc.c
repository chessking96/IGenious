#include "igen_dd_math.h"
#include "igen_math.h"
#include "igen_lib.h"
#include "igen_dd_lib.h"
#include "igen_dd_lib.h"
#include "igen_dd_math.h"
#include "math.h"

dd_I fun(f32_I x) {
  int k;
  int n;

  f32_I t1;
  f32_I d1;

  t1 = x;

  for (k = 1; k <= n; k++) {
    f64_I _t1 = _ia_set_f64(-2.0, 2.0);
    f64_I _t2 = _ia_cast_f32_to_f64(d1);
    f64_I _t3 = _ia_mul_f64(_t1, _t2);
    d1 = _ia_cast_f64_to_f32(_t3);
    f32_I _t4 = _ia_mul_f32(d1, x);
    f64_I _t5 = _ia_cast_f32_to_f64(_t4);
    f64_I _t6 = _ia_sin_f64(_t5);
    f64_I _t7 = _ia_cast_f32_to_f64(d1);
    f64_I _t8 = _ia_cast_f32_to_f64(t1);
    f64_I _t9 = _ia_div_f64(_t6, _t7);
    f64_I _t10 = _ia_add_f64(_t8, _t9);
    t1 = _ia_cast_f64_to_f32(_t10);
  }

  dd_I _ret;
  _ret = _ia_cast_f32_to_dd(t1);
  return _ret;
}

dd_I funarc() {
  int i;
  f32_I h;
  f32_I t1;
  f32_I t2;
  dd_I dppi;

  f32_I s1;

  int n = 1000000;
  dppi = _ia_set_dd(-3.1415926535897927, 0.0, 3.1415926535897936, 0.0);
  s1 = _ia_set_f32(-0.0, 0.0);
  t1 = _ia_set_f32(-0.0, 0.0);
  int _t11 = n;
  dd_I _t12 = _ia_cast_int_to_dd(_t11);
  dd_I _t13 = _ia_div_dd(dppi, _t12);
  h = _ia_cast_dd_to_f32(_t13);

  for (i = 1; i <= n; i++) {
    int _t14 = i;
    f32_I _t15 = _ia_cast_int_to_f32(_t14);
    f32_I _t16 = _ia_mul_f32(_t15, h);
    dd_I _t17 = fun(_t16);
    t2 = _ia_cast_dd_to_f32(_t17);
    f32_I _t18 = _ia_sub_f32(t2, t1);
    f32_I _t19 = _ia_sub_f32(t2, t1);
    f32_I _t20 = _ia_mul_f32(h, h);
    f32_I _t21 = _ia_mul_f32(_t18, _t19);
    f32_I _t22 = _ia_add_f32(_t20, _t21);
    f64_I _t23 = _ia_cast_f32_to_f64(_t22);
    f64_I _t24 = _ia_cast_f32_to_f64(s1);
    f64_I _t25 = _ia_sqrt_f64(_t23);
    f64_I _t26 = _ia_add_f64(_t24, _t25);
    s1 = _ia_cast_f64_to_f32(_t26);
    t1 = t2;
  }

  dd_I _ret;
  _ret = _ia_cast_f32_to_dd(s1);
  return _ret;
}
