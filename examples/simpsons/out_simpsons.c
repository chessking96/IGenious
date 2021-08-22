#include "igen_dd_math.h"
#include "igen_math.h"
#include "igen_lib.h"
#include "igen_dd_lib.h"
#include "igen_dd_lib.h"
#include "math.h"

dd_I fun(dd_I x) {
  dd_I pi = _ia_set_dd(-3.1415926535897931, -1.2246203653145581e-16,
                       3.1415926535897931, 1.2246203653145583e-16);
  dd_I result;
  dd_I _t1 = _ia_mul_dd(pi, pi);
  dd_I _t2 = _ia_mul_dd(_t1, pi);
  dd_I _t3 = _ia_mul_dd(_t2, x);
  dd_I _t4 = _ia_mul_dd(_t3, x);
  dd_I _t5 = _ia_mul_dd(_t4, x);
  dd_I _t6 = _ia_set_dd(-6, 0.0, 6, 0.0);
  dd_I _t7 = _ia_mul_dd(pi, x);
  dd_I _t8 = _ia_div_dd(_t5, _t6);
  dd_I _t9 = _ia_mul_dd(pi, pi);
  dd_I _t10 = _ia_mul_dd(_t9, pi);
  dd_I _t11 = _ia_mul_dd(_t10, pi);
  dd_I _t12 = _ia_mul_dd(_t11, pi);
  dd_I _t13 = _ia_mul_dd(_t12, x);
  dd_I _t14 = _ia_mul_dd(_t13, x);
  dd_I _t15 = _ia_mul_dd(_t14, x);
  dd_I _t16 = _ia_mul_dd(_t15, x);
  dd_I _t17 = _ia_mul_dd(_t16, x);
  dd_I _t18 = _ia_set_dd(-120, 0.0, 120, 0.0);
  dd_I _t19 = _ia_sub_dd(_t7, _t8);
  dd_I _t20 = _ia_div_dd(_t17, _t18);
  result = _ia_add_dd(_t19, _t20);
  return result;
}

dd_I simpsons() {

  int l;

  long diff = 0;

  int i;
  int j;
  int k;

  int n = 1000000;
  dd_I a;
  dd_I b;
  dd_I h;
  dd_I s1;
  dd_I x;

  a = _ia_set_dd(-0.0, 0.0, 0.0, 0.0);
  b = _ia_set_dd(-1.0, 0.0, 1.0, 0.0);
  int _t21 = n;
  dd_I _t22 = _ia_set_dd(-2.0, 0.0, 2.0, 0.0);
  dd_I _t23 = _ia_cast_int_to_dd(_t21);
  dd_I _t24 = _ia_sub_dd(b, a);
  dd_I _t25 = _ia_mul_dd(_t22, _t23);
  h = _ia_div_dd(_t24, _t25);
  s1 = _ia_set_dd(-0.0, 0.0, 0.0, 0.0);

  x = a;
  s1 = fun(x);

  for (i = 0; i < n; i++) {
    x = _ia_add_dd(x, h);
    dd_I _t26 = _ia_set_dd(-4.0, 0.0, 4.0, 0.0);
    dd_I _t27 = fun(x);
    dd_I _t28 = _ia_mul_dd(_t26, _t27);
    s1 = _ia_add_dd(s1, _t28);
    x = _ia_add_dd(x, h);
    dd_I _t29 = _ia_set_dd(-2.0, 0.0, 2.0, 0.0);
    dd_I _t30 = fun(x);
    dd_I _t31 = _ia_mul_dd(_t29, _t30);
    s1 = _ia_add_dd(s1, _t31);
  }

  return s1;
}
