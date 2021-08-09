#include "math.h"


long double funarc()
{
  int i;
  long double h, t1, t2, dppi;
  long double s1;

	int n = 100000;
	dppi = 3.14159265358979323846;
	s1 = 0.0;
	t1 = 0.0;
	h = dppi / n;

	for(i = 1; i <= n; i++){ 		
 		long double x = i * h;
		int k, m = 5;
		long double t1, d1 = 1.0;
		t1 = x;
		for(k = 1; k <= m; k++)
		{
			d1 = 2.0 * d1;
			t1 = t1 + sin(d1 * x) / d1;
		}
		t2 = t1;
		s1 = s1 + sqrt(h*h + (t2 - t1)*(t2 - t1));
		t1 = t2;
	}

	return s1;
}
