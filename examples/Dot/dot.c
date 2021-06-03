long double dot(long double* x, long double* y){
  long double t = 0;
  int n = 100000;
  for (int i = 0; i < n; i++){
    t = t + x[i]*y[i];
  }

  return t;
}


