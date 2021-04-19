#include "igen_dd_lib.h"
int main() {

  dd_I c = _ia_set_dd(-0.024299999999999995, 0.0, 0.024300000000000002, 0.0);
  dd_I _t1 = _ia_set_dd(-0.12339999999999998, 0.0, 0.12340000000000001, 0.0);
  c = _ia_mul_dd(c, _t1);

  return 0;
}
