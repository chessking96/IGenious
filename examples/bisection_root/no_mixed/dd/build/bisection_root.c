#include "igen_dd_lib.h"

dd_I fun(dd_I x) {
  dd_I _t1 = _ia_mul_dd(x, x);
  dd_I _t2 = _ia_set_dd(-0.23423543399999996, 0.0, 0.23423543400000002, 0.0);
  dd_I _t3 = _ia_mul_dd(_t1, x);
  dd_I _t4 = _ia_mul_dd(_t2, x);
  dd_I _t5 = _ia_mul_dd(x, x);
  dd_I _t6 = _ia_set_dd(-134.12367339999997, 0.0, 134.12367340000003, 0.0);
  dd_I _t7 = _ia_sub_dd(_t3, _t4);
  dd_I _t8 = _ia_mul_dd(_t5, _t6);
  dd_I _ret;
  _ret = _ia_sub_dd(_t7, _t8);
  return _ret;
}

dd_I bisection_root() {
  dd_I x_left = _ia_set_dd(2.0456345600000003, 0.0, -2.0456345599999994, 0.0);
  dd_I x_right = _ia_set_dd(-2.2452364999999994, 0.0, 2.2452365000000003, 0.0);

  dd_I a;
  dd_I b;
  dd_I c;
  dd_I d;
  dd_I e;

  dd_I fa;
  dd_I fb;
  dd_I fc;

  dd_I f_lower = fun(x_left);
  dd_I f_upper = fun(x_right);

  dd_I _t9 = _ia_add_dd(x_left, x_right);
  dd_I _t10 = _ia_set_dd(-0.5, 0.0, 0.5, 0.0);
  dd_I root = _ia_mul_dd(_t9, _t10);

  int max_iters = 40;
  int iters = 0;
  while (1) {

    if (iters == max_iters) {
      break;
    }
    dd_I _t11 = _ia_add_dd(x_left, x_right);
    dd_I _t12 = _ia_set_dd(-2.0, 0.0, 2.0, 0.0);
    dd_I x_middle = _ia_div_dd(_t11, _t12);
    dd_I f_middle = fun(x_middle);

    dd_I _t13 = _ia_set_dd(-0.0, 0.0, 0.0, 0.0);
    if (_ia_cmpeq_dd(f_lower, _t13)) {
      root = x_left;
      break;
    }
    dd_I _t14 = _ia_set_dd(-0.0, 0.0, 0.0, 0.0);
    if (_ia_cmpeq_dd(f_upper, _t14)) {
      root = x_right;
      break;
    }

    dd_I _t15 = _ia_set_dd(-0.0, 0.0, 0.0, 0.0);
    if (_ia_cmpeq_dd(f_middle, _t15)) {
      root = x_middle;
      break;
    }

    dd_I _t16 = _ia_set_dd(-0.0, 0.0, 0.0, 0.0);
    dd_I _t17 = _ia_set_dd(-0.0, 0.0, 0.0, 0.0);
    int _t18 = _ia_cmpgt_dd(f_lower, _t16);
    int _t19 = _ia_cmplt_dd(f_middle, _t17);
    dd_I _t20 = _ia_set_dd(-0.0, 0.0, 0.0, 0.0);
    dd_I _t21 = _ia_set_dd(-0.0, 0.0, 0.0, 0.0);
    int _t22 = _ia_cmplt_dd(f_lower, _t20);
    int _t23 = _ia_cmpgt_dd(f_middle, _t21);
    int _t24 = (_ia_and_tb(_t18, _t19));
    int _t25 = (_ia_and_tb(_t22, _t23));
    if (_ia_or_tb(_t24, _t25)) {
      dd_I _t26 = _ia_add_dd(x_left, x_middle);
      dd_I _t27 = _ia_set_dd(-0.5, 0.0, 0.5, 0.0);
      root = _ia_mul_dd(_t26, _t27);
      x_right = x_middle;
      f_upper = f_middle;
    } else {
      dd_I _t28 = _ia_add_dd(x_right, x_middle);
      dd_I _t29 = _ia_set_dd(-0.5, 0.0, 0.5, 0.0);
      root = _ia_mul_dd(_t28, _t29);
      x_left = x_middle;
      f_lower = f_middle;
    }

    iters++;
  }
  return root;
}
