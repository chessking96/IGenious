#include "igen_dd_lib.h"

void DFT16(dd_I *Y, dd_I *X) {
  dd_I _t1 = _ia_set_dd(-1, 0.0, 1, 0.0);
  dd_I _t2 = _ia_add_dd(X[0], _t1);
  f64_I a = _ia_cast_dd_to_f64(_t2);
  Y[0] = _ia_cast_f64_to_dd(a);
}
