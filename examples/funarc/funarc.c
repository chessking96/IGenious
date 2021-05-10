#include <inttypes.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double fun( long double x )
{
  int k, n;
  k = 5;
  n = 5;
  long double t1, d1;
  t1 = 1.0L;
  d1 = 1.0L;

  t1 = x;

  for( k = 1; k <= n; k++ )
  {
    d1 = 2.0 * d1;
    t1 = t1 + sin(d1 * x) / d1;
  }

  return t1;
}

int funarc()
{
  int l;
  long int diff = 0;

  int i, j, k; 
  long double h = 5.795776322412856L;
  long double t1 = 5.795776322412856L;
  long double t2 = 5.795776322412856L;
  long double dppi = 5.795776322412856L;
  long double ans = 5.795776322412856L;
  long double s1; 

  // variables for logging/checking
  long double log;

  // 0. read input from the file final_inputs
  int finputs = 10000;


  // dummy calls
  sqrtf(0);
  acosf(0);
  sinf(0);

  for (l = 0; l < 1; l++)
  {
    int n = finputs;
    t1 = -1.0;
    dppi = acos(t1);
    s1 = 0.0;
    t1 = 0.0;
    h = dppi / n;

    for( i = 1; i <= n; i++ )
    {
      t2 = fun (i * h);
      s1 = s1 + sqrt (h*h + (t2 - t1)*(t2 - t1));
      t1 = t2;
    }

    log = (long double) s1;

  }

}


