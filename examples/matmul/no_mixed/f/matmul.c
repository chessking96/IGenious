#include "igen_lib.h"
void matmul(f32_I *x, f32_I *y, f32_I *z) {
  int m = 100;
  int q = 100;
  int p = 100;

  for (int c = 0; c < m; c++) {
    for (int d = 0; d < q; d++) {
      f32_I sum = {-0.0, 0.0};
      for (int k = 0; k < p; k++) {
        f32_I _t1 = _ia_mul_f32(x[c * p + k], y[k * q + d]);
        sum = _ia_add_f32(sum, _t1);
      }
      z[c * q + d] = sum;
    }
  }
}
