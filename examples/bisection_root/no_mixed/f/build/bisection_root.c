#include "igen_dd_lib.h"

dd_I fun(f32_I x) {
  f32_I _t1 = _ia_mul_f32(x, x);
  f32_I _t2 = _ia_mul_f32(_t1, x);
  f64_I _t3 = _ia_set_f64(-0.23423543399999996, 0.23423543400000002);
  f64_I _t4 = _ia_cast_f32_to_f64(x);
  f64_I _t5 = _ia_cast_f32_to_f64(_t2);
  f64_I _t6 = _ia_mul_f64(_t3, _t4);
  f32_I _t7 = _ia_mul_f32(x, x);
  f64_I _t8 = _ia_cast_f32_to_f64(_t7);
  f64_I _t9 = _ia_set_f64(-134.12367339999997, 134.12367340000003);
  f64_I _t10 = _ia_sub_f64(_t5, _t6);
  f64_I _t11 = _ia_mul_f64(_t8, _t9);
  f64_I _t12 = _ia_sub_f64(_t10, _t11);
  dd_I _ret;
  _ret = _ia_cast_f64_to_dd(_t12);
  return _ret;
}

dd_I bisection_root() {
  f32_I x_left = {2.0456347, -2.0456345};
  f32_I x_right = {-2.2452364, 2.2452366};

  f32_I a;
  f32_I b;
  f32_I c;
  f32_I d;
  f32_I e;

  f32_I fa;
  f32_I fb;
  f32_I fc;

  dd_I _t13 = fun(x_left);
  f32_I f_lower = _ia_cast_dd_to_f32(_t13);
  dd_I _t14 = fun(x_right);
  f32_I f_upper = _ia_cast_dd_to_f32(_t14);

  f32_I _t15 = _ia_add_f32(x_left, x_right);
  f64_I _t16 = _ia_cast_f32_to_f64(_t15);
  f64_I _t17 = _ia_set_f64(-0.5, 0.5);
  f64_I _t18 = _ia_mul_f64(_t16, _t17);
  f32_I root = _ia_cast_f64_to_f32(_t18);

  int max_iters = 40;
  int iters = 0;
  while (1) {

    if (iters == max_iters) {
      break;
    }
    f32_I _t19 = _ia_add_f32(x_left, x_right);
    f64_I _t20 = _ia_cast_f32_to_f64(_t19);
    f64_I _t21 = _ia_set_f64(-2.0, 2.0);
    f64_I _t22 = _ia_div_f64(_t20, _t21);
    f32_I x_middle = _ia_cast_f64_to_f32(_t22);
    dd_I _t23 = fun(x_middle);
    f32_I f_middle = _ia_cast_dd_to_f32(_t23);

    f64_I _t24 = _ia_cast_f32_to_f64(f_lower);
    f64_I _t25 = _ia_set_f64(-0.0, 0.0);
    if (_ia_cmpeq_f64(_t24, _t25)) {
      root = x_left;
      break;
    }
    f64_I _t26 = _ia_cast_f32_to_f64(f_upper);
    f64_I _t27 = _ia_set_f64(-0.0, 0.0);
    if (_ia_cmpeq_f64(_t26, _t27)) {
      root = x_right;
      break;
    }

    f64_I _t28 = _ia_cast_f32_to_f64(f_middle);
    f64_I _t29 = _ia_set_f64(-0.0, 0.0);
    if (_ia_cmpeq_f64(_t28, _t29)) {
      root = x_middle;
      break;
    }

    f64_I _t30 = _ia_cast_f32_to_f64(f_lower);
    f64_I _t31 = _ia_set_f64(-0.0, 0.0);
    f64_I _t32 = _ia_cast_f32_to_f64(f_middle);
    f64_I _t33 = _ia_set_f64(-0.0, 0.0);
    int _t34 = _ia_cmpgt_f64(_t30, _t31);
    int _t35 = _ia_cmplt_f64(_t32, _t33);
    f64_I _t36 = _ia_cast_f32_to_f64(f_lower);
    f64_I _t37 = _ia_set_f64(-0.0, 0.0);
    f64_I _t38 = _ia_cast_f32_to_f64(f_middle);
    f64_I _t39 = _ia_set_f64(-0.0, 0.0);
    int _t40 = _ia_cmplt_f64(_t36, _t37);
    int _t41 = _ia_cmpgt_f64(_t38, _t39);
    int _t42 = (_ia_and_tb(_t34, _t35));
    int _t43 = (_ia_and_tb(_t40, _t41));
    if (_ia_or_tb(_t42, _t43)) {
      f32_I _t44 = _ia_add_f32(x_left, x_middle);
      f64_I _t45 = _ia_cast_f32_to_f64(_t44);
      f64_I _t46 = _ia_set_f64(-0.5, 0.5);
      f64_I _t47 = _ia_mul_f64(_t45, _t46);
      root = _ia_cast_f64_to_f32(_t47);
      x_right = x_middle;
      f_upper = f_middle;
    } else {
      f32_I _t48 = _ia_add_f32(x_right, x_middle);
      f64_I _t49 = _ia_cast_f32_to_f64(_t48);
      f64_I _t50 = _ia_set_f64(-0.5, 0.5);
      f64_I _t51 = _ia_mul_f64(_t49, _t50);
      root = _ia_cast_f64_to_f32(_t51);
      x_left = x_middle;
      f_lower = f_middle;
    }

    iters++;
  }
  dd_I _ret;
  _ret = _ia_cast_f32_to_dd(root);
  return _ret;
}
