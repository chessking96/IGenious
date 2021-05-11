#include <stdlib.h>

double dot(double* x, double* y){
  double  t = 0;
  int n = 10;
  for (int i = 0; i < n; i ++){
    t += x[i]*y[i];
  }

  return t;
}


int main(){
  double* x = malloc(sizeof(double) * 10);
  double* y = malloc(sizeof(double) * 10);

  dot(x, y);
}
