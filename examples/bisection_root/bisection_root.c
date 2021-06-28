//partially from gsl - bisection.c
long double fun(long double x){
  return x * x * x - 0.234235434 * x - x * x * 134.1236734;
}

long double bisection_root(){
  long double x_left = -2.04563456;
  long double x_right = 2.24523650;

  long double f_lower = fun(x_left);
  long double f_upper = fun(x_right);

  long double root = (x_left + x_right) * 0.5;

  int max_iters = 40;
  int iters = 0;
  while(1){
    // break if mux number of iterations is reached
    if(iters == max_iters){
      break;
    }
    long double x_middle = (x_left + x_right) / 2.0;
    long double f_middle = fun(x_middle);

    // break if root is found
    if(f_lower == 0.0){
      root = x_left;
      break;
    }
    if(f_upper == 0.0){
      root = x_right;
      break;
    }

    if(f_middle == 0.0){
      root = x_middle;
      break;
    }

    //check in which interval is the root
    if((f_lower > 0.0 && f_middle < 0.0) || (f_lower < 0.0 && f_middle > 0.0)){
      root =  (x_left + x_middle) * 0.5;
      x_right = x_middle;
      f_upper = f_middle;
    }else{
      root =  (x_right + x_middle) * 0.5;
      x_left = x_middle;
      f_lower = f_middle;
    }

    iters++;
  }
  return root;
}
