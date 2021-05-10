#include <stdlib.h>


int main() {
    long double* X = calloc(sizeof(long double*), 16);
    long double* Y = calloc(sizeof(long double*), 16);
    
    long double a = (*(X + 16) + *(X + 0));
    
    *Y = 3.2312342;
   
   printf("%.17g %.17g %.17g %.17g\n", Y->ll, Y->lh, Y->ul, Y->uh);
}
