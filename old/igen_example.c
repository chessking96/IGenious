#include "igen_dd_lib.h"
dd_I function(dd_I x) { return x; }

int main() {
  f32_I f = {-1.0, 1.0};
  f64_I g = {-2.0, 2.0};
  dd_I h = _ia_set_dd(-3.0, 0.0, 3.0, 0.0);
  h = function(h);
  return 0;
}
