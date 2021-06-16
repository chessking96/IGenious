#include "igen_dd_lib.h"
void matmul(dd_I *x, dd_I *y, dd_I *z) {
  int m = 100;
  int q = 100;
  int p = 100;

  for (int c = 0; c < m; c++) {
    for (int d = 0; d < q; d++) {
      dd_I sum = _ia_set_dd(-0, 0.0, 0, 0.0);
      for (int k = 0; k < p; k++) {
        dd_I _t1 = _ia_mul_dd(x[c * p + k], y[k * q + d]);
        sum = _ia_add_dd(sum, _t1);
      }
      z[c * q + d] = sum;
    }
  }
}
