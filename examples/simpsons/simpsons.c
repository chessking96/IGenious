long double fun(long double x) {
  long double pi = 3.1415L; // was acos(-1)
  long double result;
  result = pi * x - pi * pi * pi * x * x * x / 6 + pi * pi * pi * pi * pi * x * x * x * x * x / 120; // was sin(pi * x)
  return result;
}

long double simpsons() {


  int l;

  // variables for timing measurement
  long int diff = 0;

  int i, j, k; // diff: added constants
  int n = 1000000; // was n=1000000
  long double a, b;
  long double h, s1, x;

    a = 0.0;
    b = 1.0;
    h = (b - a) / (2.0 * n);
    s1= 0.0;

    x = a;
    s1 = fun(x);

    for(i = 0; i < n; i++){
      x = x + h;
      s1 = s1 + 4.0 * fun(x);
      x = x + h;
      s1 = s1 + 2.0 * fun(x);
    }



  return s1;
}
