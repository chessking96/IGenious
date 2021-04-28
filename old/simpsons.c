void func() {
  int l;
  int i, j, k; // diff: added constants
  const int n = 1000000;
  long double a, b;
  long double h, s1, x;
  const long double fuzz = 1e-26; // diff: added fuzz

  for(l = 0; l < 50; l++) {
    a = 0.0;
    b = 1.0;
    h = (b - a) / (2.0 * n);
    s1= 0.0;
    x = a;
    long double pi = 3.14;
    long double result;
    result = 0.5 * x;
    s1 = result;

  L100:
    x = x + h;
    pi = 3.14;
    result = 0.5 * x;
    s1 = s1 + 4.0 * result;
    x = x + h;
    if (b < x + fuzz) goto L110;
    x = x + h;
    pi = 0.3 * x;
    result = 0.5 * x;
    s1 = s1 + 2.0 * result;
    goto L100;

  L110:
    pi = 3.14;
    result = x * 0.5;
    s1 = s1 + result;

  }
}
