#include "igen_dd_lib.h"
#include <stdlib.h>

int main() {
  dd_I a;
  dd_I b;
  
  long double r1 = 2.28475245235323453245234523523542345223532522490720L;
  long double r2 = 0.0L;
  long double r3 = 5.9077634754352345234532634534755634634564636453620L;
  long double r4 = 0.0L;
  
 
  a = _ia_set_dd(-r1, -r2, r1, r2);
  b = _ia_set_dd(-r3, -r4, r3, r4);
 
  dd_I c = _ia_add_dd(a, b);
 
 
  dd_I lb = _ia_set_dd(c.lh, c.ll, -c.lh, -c.ll);
  dd_I ub = _ia_set_dd(-c.uh, -c.ul, c.uh, c.ul);
  dd_I diff = _ia_sub_dd(ub, lb);

  printf("%.17g %.17g %.17g %.17g\n", a.lh, a.ll, a.uh, a.ul);
  printf("%.17g %.17g %.17g %.17g\n", b.lh, b.ll, b.uh, b.ul);
  printf("%.17g %.17g %.17g %.17g\n", c.lh, c.ll, c.uh, c.ul);
  printf("%.17g %.17g %.17g %.17g\n", diff.lh, diff.ll, diff.uh, diff.ul);
  printf("%.17g %.17g %.17g %.17g\n", lb.lh, lb.ll, lb.uh, lb.ul);
  printf("%.17g %.17g %.17g %.17g\n", ub.lh, ub.ll, ub.uh, ub.ul);
}
