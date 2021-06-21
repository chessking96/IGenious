#include "igen_dd_lib.h"

dd_I fun(f64_I x) {
  f64_I _t1 = _ia_mul_f64(x, x);
  f64_I _t2 = _ia_set_f64(-0.23423543399999996, 0.23423543400000002);
  f64_I _t3 = _ia_mul_f64(_t1, x);
  f64_I _t4 = _ia_mul_f64(_t2, x);
  f64_I _t5 = _ia_mul_f64(x, x);
  f64_I _t6 = _ia_set_f64(-134.12367339999997, 134.12367340000003);
  f64_I _t7 = _ia_sub_f64(_t3, _t4);
  f64_I _t8 = _ia_mul_f64(_t5, _t6);
  f64_I _t9 = _ia_sub_f64(_t7, _t8);
  dd_I _ret;
  _ret = _ia_cast_f64_to_dd(_t9);
  return _ret;
}

dd_I bisection_root() {
  f64_I x_left = {2.0456345600000003, -2.0456345599999994};
  f64_I x_right = {-2.2452364999999994, 2.2452365000000003};

  f64_I a;
  f64_I b;
  f64_I c;
  f64_I d;
  f64_I e;

  f64_I fa;
  f64_I fb;
  f64_I fc;

  dd_I _t10 = fun(x_left);
  f64_I f_lower = _ia_cast_dd_to_f64(_t10);
  dd_I _t11 = fun(x_right);
  f64_I f_upper = _ia_cast_dd_to_f64(_t11);

  f64_I _t12 = _ia_add_f64(x_left, x_right);
  f64_I _t13 = _ia_set_f64(-0.5, 0.5);
  f64_I root = _ia_mul_f64(_t12, _t13);

  int max_iters = 40;
  int iters = 0;
  while (1) {

    if (iters == max_iters) {
      break;
    }
    f64_I _t14 = _ia_add_f64(x_left, x_right);
    f64_I _t15 = _ia_set_f64(-2.0, 2.0);
    f64_I x_middle = _ia_div_f64(_t14, _t15);
    dd_I _t16 = fun(x_middle);
    f64_I f_middle = _ia_cast_dd_to_f64(_t16);

    f64_I _t17 = _ia_set_f64(-0.0, 0.0);
    if (_ia_cmpeq_f64(f_lower, _t17)) {
      root = x_left;
      break;
    }
    f64_I _t18 = _ia_set_f64(-0.0, 0.0);
    if (_ia_cmpeq_f64(f_upper, _t18)) {
      root = x_right;
      break;
    }

    f64_I _t19 = _ia_set_f64(-0.0, 0.0);
    if (_ia_cmpeq_f64(f_middle, _t19)) {
      root = x_middle;
      break;
    }

    f64_I _t20 = _ia_set_f64(-0.0, 0.0);
    f64_I _t21 = _ia_set_f64(-0.0, 0.0);
    int _t22 = _ia_cmpgt_f64(f_lower, _t20);
    int _t23 = _ia_cmplt_f64(f_middle, _t21);
    f64_I _t24 = _ia_set_f64(-0.0, 0.0);
    f64_I _t25 = _ia_set_f64(-0.0, 0.0);
    int _t26 = _ia_cmplt_f64(f_lower, _t24);
    int _t27 = _ia_cmpgt_f64(f_middle, _t25);
    int _t28 = (_ia_and_tb(_t22, _t23));
    int _t29 = (_ia_and_tb(_t26, _t27));
    if (_ia_or_tb(_t28, _t29)) {
      f64_I _t30 = _ia_add_f64(x_left, x_middle);
      f64_I _t31 = _ia_set_f64(-0.5, 0.5);
      root = _ia_mul_f64(_t30, _t31);
      x_right = x_middle;
      f_upper = f_middle;
    } else {
      f64_I _t32 = _ia_add_f64(x_right, x_middle);
      f64_I _t33 = _ia_set_f64(-0.5, 0.5);
      root = _ia_mul_f64(_t32, _t33);
      x_left = x_middle;
      f_lower = f_middle;
    }

    iters++;
  }
  dd_I _ret;
  _ret = _ia_cast_f64_to_dd(root);
  return _ret;
}
