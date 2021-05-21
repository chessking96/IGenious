#include <math.h>

double fun(double x )
{
  int k;
  int n = 5;
  long double t1;
  long double d1 = 1.0L;

  t1 = x;

  for( k = 1; k <= n; k++ )
  {
    d1 = 2.0 * d1;
    t1 = t1 + (d1 * x) / d1;
  }

  return t1;
}

double funarc()
{
  int l;
  long int diff = 0;

  int i;
  int j;
  int k; 
  double h;
  double t1;
  double t2;
  double dppi;
  double ans = 5.795776322412856L;
  double s1; 

  float temp;

  int n = 100;
  t1 = -1.0;
  dppi = t1;
  s1 = 0.0;
  t1 = 0.0;
  h = dppi / n;

  for( i = 1; i <= n; i++ )
  {
      t2 = fun (i * h);
      s1 = s1 + (h*h + (t2 - t1)*(t2 - t1));
      t1 = t2;
  }

  return (double)s1;
}


