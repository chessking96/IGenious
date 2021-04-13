#include <time.h>
#include <stdarg.h>
#include <inttypes.h>
#include <math.h>
#include <stdio.h>

int main( int argc, char **argv) {
	FILE* file;
	double d = 2.34535f;
        clock_t start = clock();
    	double a  =  d;
        double c = a * 0.0243f;
        double arr [10]; 
        long i = 0;
        for(i = 0; i < 10; i++){
                arr[i] = i;      
        }
        for(i = 0; i < 200000000; i++){
                c = c + a * 0.02342f;
                c *= c * a * 0.1234f;
                c = c / (a * 0.1243f);
        }
        double x =  arr[5] * c;
        clock_t end = clock();
	printf("%lf\n", x);
	long diff = (long)(end-start);
	printf("diff, %ld\n", end);

        file = fopen("score.cov", "w");
        fprintf(file, "%ld\n", diff);
        fclose(file);

        file = fopen("sat.cov", "w");
        fprintf(file, "true\n");
        fclose(file);

        return 0;
}
