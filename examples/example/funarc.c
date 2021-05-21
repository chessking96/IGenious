#include <math.h>

double fun(double x)
{
  int k;
  int n = 5;
  long double t11, d11 = 1.0L;

  t11 = x;

  for(k = 1; k <= n; k++)
  {
    d11 = 2.0 * d11;
    t11 = t11 + (d11 * x) / d11;
  }

  return t11;
}

double funarc()
{
  int l;
  long int diff = 0;

  int i;
  int j;
  int k; 
  double h, t1, t2, dppi, ans = 5.795776322412856L;
  double s1; 

  float temp;

  int n = 100;
  t1 = -1.0;
  dppi = t1;
  s1 = 0.0;
  t1 = 0.0;
  h = dppi / n;

  for(i = 1; i <= n; i++)
  {
      t2 = fun (i * h);
      s1 = s1 + (h*h + (t2 - t1)*(t2 - t1));
      t1 = t2;
  }

  return (double)s1;
}


