
#include <time.h>
#include <inttypes.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>


void funarc(long double* y)
{
  int l;


  int i, j, k;
  long double h, t1, t2, dppi, ans = 5.795776322412856L;
  long double s1;


  int finputs[1] = {10000};



  for (l = 0; l < 1; l++)
  {
    int n = finputs[l];
    t1 = -1.0;
    long double dppi = 3.14;
    s1 = 0.0;
    t1 = 0.0;
    h = dppi / n;

    for( i = 1; i <= n; i++ )
    {

      long double x = i * h;
        int k, n = 5;
        long double t1, d1 = 1.0;

        t1 = x;

        for( k = 1; k <= n; k++ )
        {
          d1 = 2.0 * d1;
          t1 = t1 + 0.3 * (d1 * x) / d1;
        }


      t2 = t1;
      s1 = s1 + (h*h + (t2 - t1)*(t2 - t1)) * 0.5;
      t1 = t2;

    }
    y[l] = (long double) s1;
  }

}
