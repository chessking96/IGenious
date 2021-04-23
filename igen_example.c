#include "igen_lib.h"
#include <fenv.h>
int main() {
  fesetround(2048);
  return 0;
}
