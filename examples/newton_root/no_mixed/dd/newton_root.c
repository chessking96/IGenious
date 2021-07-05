#include "igen_dd_math.h"
#include "igen_math.h"
#include "igen_lib.h"
#include "igen_dd_lib.h"
#include "igen_dd_lib.h"

dd_I func(dd_I x) {
  x = _ia_neg_dd(x);
  dd_I _t1 = _ia_mul_dd(x, x);
  dd_I _t2 = _ia_mul_dd(_t1, x);
  dd_I _t3 = _ia_mul_dd(x, x);
  dd_I _t4 = _ia_sub_dd(_t2, _t3);
  dd_I _t5 = _ia_set_dd(-2, 0.0, 2, 0.0);
  dd_I _ret;
  _ret = _ia_add_dd(_t4, _t5);
  return _ret;
}

dd_I derivFunc(dd_I x) {
  dd_I _t6 = _ia_set_dd(-3, 0.0, 3, 0.0);
  dd_I _t7 = _ia_mul_dd(_t6, x);
  dd_I _t8 = _ia_set_dd(-2, 0.0, 2, 0.0);
  dd_I _t9 = _ia_mul_dd(_t7, x);
  dd_I _t10 = _ia_mul_dd(_t8, x);
  dd_I _ret;
  _ret = _ia_sub_dd(_t9, _t10);
  return _ret;
}

dd_I newton_root() {
  dd_I x = _ia_set_dd(-20, 0.0, 20, 0.0);
  dd_I _t11 = func(x);
  dd_I _t12 = derivFunc(x);
  dd_I h = _ia_div_dd(_t11, _t12);
  for (int i = 0; i < 20; i++) {
    dd_I _t13 = func(x);
    dd_I _t14 = derivFunc(x);
    h = _ia_div_dd(_t13, _t14);
    x = _ia_sub_dd(x, h);
  }

  return x;
}
