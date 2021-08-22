#include "igen_dd_math.h"
#include "igen_math.h"
#include "igen_lib.h"
#include "igen_dd_lib.h"
#include "igen_dd_lib.h"
void gsl_fit_linear(dd_I *x, dd_I *y, dd_I *c0, dd_I *c1, dd_I *cov_00,
                    dd_I *cov_01, dd_I *cov_11, dd_I *sumsq) {
  int xstride = 1;
  int ystride = 1;
  int n = 100;

  dd_I m_x = _ia_set_dd(-0, 0.0, 0, 0.0);
  dd_I m_y = _ia_set_dd(-0, 0.0, 0, 0.0);
  dd_I m_dx2 = _ia_set_dd(-0, 0.0, 0, 0.0);
  dd_I m_dxdy = _ia_set_dd(-0, 0.0, 0, 0.0);

  int i;

  for (i = 0; i < n; i++) {
    int _t1 = i;
    f64_I _t2 = _ia_cast_int_to_f64(_t1);
    f64_I _t3 = _ia_set_f64(-1.0, 1.0);
    f64_I _t4 = _ia_add_f64(_t2, _t3);
    dd_I _t5 = _ia_sub_dd(x[i * xstride], m_x);
    dd_I _t6 = _ia_cast_f64_to_dd(_t4);
    dd_I _t7 = _ia_div_dd(_t5, _t6);
    m_x = _ia_add_dd(m_x, _t7);
    int _t8 = i;
    f64_I _t9 = _ia_cast_int_to_f64(_t8);
    f64_I _t10 = _ia_set_f64(-1.0, 1.0);
    f64_I _t11 = _ia_add_f64(_t9, _t10);
    dd_I _t12 = _ia_sub_dd(y[i * ystride], m_y);
    dd_I _t13 = _ia_cast_f64_to_dd(_t11);
    dd_I _t14 = _ia_div_dd(_t12, _t13);
    m_y = _ia_add_dd(m_y, _t14);
  }

  for (i = 0; i < n; i++) {
    dd_I dx = _ia_sub_dd(x[i * xstride], m_x);
    dd_I dy = _ia_sub_dd(y[i * ystride], m_y);

    dd_I _t15 = _ia_mul_dd(dx, dx);
    int _t16 = i;
    f64_I _t17 = _ia_cast_int_to_f64(_t16);
    f64_I _t18 = _ia_set_f64(-1.0, 1.0);
    f64_I _t19 = _ia_add_f64(_t17, _t18);
    dd_I _t20 = _ia_sub_dd(_t15, m_dx2);
    dd_I _t21 = _ia_cast_f64_to_dd(_t19);
    dd_I _t22 = _ia_div_dd(_t20, _t21);
    m_dx2 = _ia_add_dd(m_dx2, _t22);
    dd_I _t23 = _ia_mul_dd(dx, dy);
    int _t24 = i;
    f64_I _t25 = _ia_cast_int_to_f64(_t24);
    f64_I _t26 = _ia_set_f64(-1.0, 1.0);
    f64_I _t27 = _ia_add_f64(_t25, _t26);
    dd_I _t28 = _ia_sub_dd(_t23, m_dxdy);
    dd_I _t29 = _ia_cast_f64_to_dd(_t27);
    dd_I _t30 = _ia_div_dd(_t28, _t29);
    m_dxdy = _ia_add_dd(m_dxdy, _t30);
  }

  {
    dd_I s2 = _ia_set_dd(-0, 0.0, 0, 0.0);
    dd_I d2 = _ia_set_dd(-0, 0.0, 0, 0.0);
    dd_I b = _ia_div_dd(m_dxdy, m_dx2);
    dd_I _t31 = _ia_mul_dd(m_x, b);
    dd_I a = _ia_sub_dd(m_y, _t31);

    *c0 = a;
    *c1 = b;

    for (i = 0; i < n; i++) {
      dd_I dx = _ia_sub_dd(x[i * xstride], m_x);
      dd_I dy = _ia_sub_dd(y[i * ystride], m_y);
      dd_I _t32 = _ia_mul_dd(b, dx);
      dd_I d = _ia_sub_dd(dy, _t32);
      dd_I _t33 = _ia_mul_dd(d, d);
      d2 = _ia_add_dd(d2, _t33);
    }

    int _t34 = n;
    f64_I _t35 = _ia_cast_int_to_f64(_t34);
    f64_I _t36 = _ia_set_f64(-2.0, 2.0);
    f64_I _t37 = _ia_sub_f64(_t35, _t36);
    dd_I _t38 = _ia_cast_f64_to_dd(_t37);
    s2 = _ia_div_dd(d2, _t38);

    int _t39 = n;
    f64_I _t40 = _ia_set_f64(-1.0, 1.0);
    f64_I _t41 = _ia_cast_int_to_f64(_t39);
    f64_I _t42 = _ia_div_f64(_t40, _t41);
    dd_I _t43 = _ia_cast_f64_to_dd(_t42);
    dd_I _t44 = _ia_mul_dd(m_x, m_x);
    dd_I _t45 = _ia_set_dd(-1, 0.0, 1, 0.0);
    dd_I _t46 = _ia_div_dd(_t44, m_dx2);
    dd_I _t47 = _ia_mul_dd(s2, _t43);
    dd_I _t48 = _ia_add_dd(_t45, _t46);
    *cov_00 = _ia_mul_dd(_t47, _t48);
    dd_I _t49 = _ia_set_dd(-1.0, 0.0, 1.0, 0.0);
    int _t50 = n;
    dd_I _t51 = _ia_cast_int_to_dd(_t50);
    dd_I _t52 = _ia_mul_dd(s2, _t49);
    dd_I _t53 = _ia_mul_dd(_t51, m_dx2);
    *cov_11 = _ia_div_dd(_t52, _t53);

    dd_I _t54 = _ia_neg_dd(m_x);
    int _t55 = n;
    dd_I _t56 = _ia_cast_int_to_dd(_t55);
    dd_I _t57 = _ia_mul_dd(s2, _t54);
    dd_I _t58 = _ia_mul_dd(_t56, m_dx2);
    *cov_01 = _ia_div_dd(_t57, _t58);

    *sumsq = d2;
  }
}
