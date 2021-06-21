#include "igen_dd_lib.h"
dd_I fun(f64_I x) {
  dd_I _t1 = _ia_set_dd(-3.1415000000000002, 1.8118839761882556e-16,
                        3.1415000000000002, -1.8118839761882554e-16);
  f64_I pi = _ia_cast_dd_to_f64(_t1);
  f64_I result;
  f64_I _t2 = _ia_mul_f64(pi, pi);
  f64_I _t3 = _ia_mul_f64(_t2, pi);
  f64_I _t4 = _ia_mul_f64(_t3, x);
  f64_I _t5 = _ia_mul_f64(_t4, x);
  f64_I _t6 = _ia_mul_f64(_t5, x);
  f64_I _t7 = _ia_set_f64(-6.0, 6.0);
  f64_I _t8 = _ia_mul_f64(pi, x);
  f64_I _t9 = _ia_div_f64(_t6, _t7);
  f64_I _t10 = _ia_mul_f64(pi, pi);
  f64_I _t11 = _ia_mul_f64(_t10, pi);
  f64_I _t12 = _ia_mul_f64(_t11, pi);
  f64_I _t13 = _ia_mul_f64(_t12, pi);
  f64_I _t14 = _ia_mul_f64(_t13, x);
  f64_I _t15 = _ia_mul_f64(_t14, x);
  f64_I _t16 = _ia_mul_f64(_t15, x);
  f64_I _t17 = _ia_mul_f64(_t16, x);
  f64_I _t18 = _ia_mul_f64(_t17, x);
  f64_I _t19 = _ia_set_f64(-120.0, 120.0);
  f64_I _t20 = _ia_sub_f64(_t8, _t9);
  f64_I _t21 = _ia_div_f64(_t18, _t19);
  result = _ia_add_f64(_t20, _t21);
  dd_I _ret;
  _ret = _ia_cast_f64_to_dd(result);
  return _ret;
}

dd_I simpsons() {

  int l;

  long diff = 0;

  int i;
  int j;
  int k;

  int n = 1000000;
  f64_I a;
  f64_I b;

  f64_I h;
  f64_I s1;
  f64_I x;

  a = _ia_set_f64(-0.0, 0.0);
  b = _ia_set_f64(-1.0, 1.0);
  int _t22 = n;
  f64_I _t23 = _ia_set_f64(-2.0, 2.0);
  f64_I _t24 = _ia_cast_int_to_f64(_t22);
  f64_I _t25 = _ia_sub_f64(b, a);
  f64_I _t26 = _ia_mul_f64(_t23, _t24);
  h = _ia_div_f64(_t25, _t26);
  s1 = _ia_set_f64(-0.0, 0.0);

  x = a;
  dd_I _t27 = fun(x);
  s1 = _ia_cast_dd_to_f64(_t27);

  for (i = 0; i < n; i++) {
    x = _ia_add_f64(x, h);
    dd_I _t28 = _ia_set_dd(-4.0, 0.0, 4.0, 0.0);
    dd_I _t29 = fun(x);
    dd_I _t30 = _ia_cast_f64_to_dd(s1);
    dd_I _t31 = _ia_mul_dd(_t28, _t29);
    dd_I _t32 = _ia_add_dd(_t30, _t31);
    s1 = _ia_cast_dd_to_f64(_t32);
    x = _ia_add_f64(x, h);
    dd_I _t33 = _ia_set_dd(-2.0, 0.0, 2.0, 0.0);
    dd_I _t34 = fun(x);
    dd_I _t35 = _ia_cast_f64_to_dd(s1);
    dd_I _t36 = _ia_mul_dd(_t33, _t34);
    dd_I _t37 = _ia_add_dd(_t35, _t36);
    s1 = _ia_cast_dd_to_f64(_t37);
  }

  dd_I _ret;
  _ret = _ia_cast_f64_to_dd(s1);
  return _ret;
}
