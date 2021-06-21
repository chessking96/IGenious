#include "igen_dd_lib.h"
dd_I fun(f32_I x) {
  dd_I _t1 = _ia_set_dd(-3.1415000000000002, 1.8118839761882556e-16,
                        3.1415000000000002, -1.8118839761882554e-16);
  f32_I pi = _ia_cast_dd_to_f32(_t1);
  f32_I result;
  f32_I _t2 = _ia_mul_f32(pi, pi);
  f32_I _t3 = _ia_mul_f32(_t2, pi);
  f32_I _t4 = _ia_mul_f32(_t3, x);
  f32_I _t5 = _ia_mul_f32(_t4, x);
  f32_I _t6 = _ia_mul_f32(_t5, x);
  f32_I _t7 = _ia_set_f32(-6.0, 6.0);
  f32_I _t8 = _ia_mul_f32(pi, x);
  f32_I _t9 = _ia_div_f32(_t6, _t7);
  f32_I _t10 = _ia_mul_f32(pi, pi);
  f32_I _t11 = _ia_mul_f32(_t10, pi);
  f32_I _t12 = _ia_mul_f32(_t11, pi);
  f32_I _t13 = _ia_mul_f32(_t12, pi);
  f32_I _t14 = _ia_mul_f32(_t13, x);
  f32_I _t15 = _ia_mul_f32(_t14, x);
  f32_I _t16 = _ia_mul_f32(_t15, x);
  f32_I _t17 = _ia_mul_f32(_t16, x);
  f32_I _t18 = _ia_mul_f32(_t17, x);
  f32_I _t19 = _ia_set_f32(-120.0, 120.0);
  f32_I _t20 = _ia_sub_f32(_t8, _t9);
  f32_I _t21 = _ia_div_f32(_t18, _t19);
  result = _ia_add_f32(_t20, _t21);
  dd_I _ret;
  _ret = _ia_cast_f32_to_dd(result);
  return _ret;
}

dd_I simpsons() {

  int l;

  long diff = 0;

  int i;
  int j;
  int k;

  int n = 1000000;
  f32_I a;
  f32_I b;

  f32_I h;
  f32_I s1;
  f32_I x;

  a = _ia_set_f32(-0.0, 0.0);
  b = _ia_set_f32(-1.0, 1.0);
  f32_I _t22 = _ia_sub_f32(b, a);
  int _t23 = n;
  f64_I _t24 = _ia_set_f64(-2.0, 2.0);
  f64_I _t25 = _ia_cast_int_to_f64(_t23);
  f64_I _t26 = _ia_cast_f32_to_f64(_t22);
  f64_I _t27 = _ia_mul_f64(_t24, _t25);
  f64_I _t28 = _ia_div_f64(_t26, _t27);
  h = _ia_cast_f64_to_f32(_t28);
  s1 = _ia_set_f32(-0.0, 0.0);

  x = a;
  dd_I _t29 = fun(x);
  s1 = _ia_cast_dd_to_f32(_t29);

  for (i = 0; i < n; i++) {
    x = _ia_add_f32(x, h);
    dd_I _t30 = _ia_set_dd(-4.0, 0.0, 4.0, 0.0);
    dd_I _t31 = fun(x);
    dd_I _t32 = _ia_cast_f32_to_dd(s1);
    dd_I _t33 = _ia_mul_dd(_t30, _t31);
    dd_I _t34 = _ia_add_dd(_t32, _t33);
    s1 = _ia_cast_dd_to_f32(_t34);
    x = _ia_add_f32(x, h);
    dd_I _t35 = _ia_set_dd(-2.0, 0.0, 2.0, 0.0);
    dd_I _t36 = fun(x);
    dd_I _t37 = _ia_cast_f32_to_dd(s1);
    dd_I _t38 = _ia_mul_dd(_t35, _t36);
    dd_I _t39 = _ia_add_dd(_t37, _t38);
    s1 = _ia_cast_dd_to_f32(_t39);
  }

  dd_I _ret;
  _ret = _ia_cast_f32_to_dd(s1);
  return _ret;
}
