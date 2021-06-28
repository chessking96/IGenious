#include "igen_dd_math.h"
#include "igen_math.h"
#include "igen_lib.h"
#include "igen_dd_lib.h"
#include "igen_dd_lib.h"
#include "igen_dd_math.h"
#include "math.h"

dd_I fun(dd_I x) {
  int k;
  int n;

  dd_I t1;
  dd_I d1;

  t1 = x;

  for (k = 1; k <= n; k++) {
    dd_I _t1 = _ia_set_dd(-2.0, 0.0, 2.0, 0.0);
    d1 = _ia_mul_dd(_t1, d1);
    dd_I _t2 = _ia_mul_dd(d1, x);
    f64_I _t3 = _ia_cast_dd_to_f64(_t2);
    f64_I _t4 = _ia_sin_f64(_t3);
    dd_I _t5 = _ia_cast_f64_to_dd(_t4);
    dd_I _t6 = _ia_div_dd(_t5, d1);
    t1 = _ia_add_dd(t1, _t6);
  }

  return t1;
}

dd_I funarc() {
  int i;
  dd_I h;
  dd_I t1;
  dd_I t2;
  dd_I dppi;

  dd_I s1;

  int n = 1000000;
  dppi = _ia_set_dd(-3.1415926535897927, 0.0, 3.1415926535897936, 0.0);
  s1 = _ia_set_dd(-0.0, 0.0, 0.0, 0.0);
  t1 = _ia_set_dd(-0.0, 0.0, 0.0, 0.0);
  int _t7 = n;
  dd_I _t8 = _ia_cast_int_to_dd(_t7);
  h = _ia_div_dd(dppi, _t8);

  for (i = 1; i <= n; i++) {
    int _t9 = i;
    dd_I _t10 = _ia_cast_int_to_dd(_t9);
    dd_I _t11 = _ia_mul_dd(_t10, h);
    t2 = fun(_t11);
    dd_I _t12 = _ia_sub_dd(t2, t1);
    dd_I _t13 = _ia_sub_dd(t2, t1);
    dd_I _t14 = _ia_mul_dd(h, h);
    dd_I _t15 = _ia_mul_dd(_t12, _t13);
    dd_I _t16 = _ia_add_dd(_t14, _t15);
    f64_I _t17 = _ia_cast_dd_to_f64(_t16);
    f64_I _t18 = _ia_sqrt_f64(_t17);
    dd_I _t19 = _ia_cast_f64_to_dd(_t18);
    s1 = _ia_add_dd(s1, _t19);
    t1 = t2;
  }

  return s1;
}
