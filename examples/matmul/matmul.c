void matmul(long double* x, long double* y, long double* z){
  int m = 100;
  int q = 100;
  int p = 100;

  for(int c = 0; c < m; c++){
    for(int d = 0; d < q; d++){
      long double sum = 0;
      for(int k = 0; k < p; k++){
        sum = sum + x[c * p + k] * y[k * q + d];
      }
      z[c * q + d] = sum;
    }
  }
}
