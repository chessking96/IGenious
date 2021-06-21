#include "igen_lib.h"
void matmul(f64_I *x, f64_I *y, f64_I *z) {
  int m = 100;
  int q = 100;
  int p = 100;

  for (int c = 0; c < m; c++) {
    for (int d = 0; d < q; d++) {
      f64_I sum = {-0.0, 0.0};
      for (int k = 0; k < p; k++) {
        f64_I _t1 = _ia_mul_f64(x[c * p + k], y[k * q + d]);
        sum = _ia_add_f64(sum, _t1);
      }
      z[c * q + d] = sum;
    }
  }
}
