#include <fenv.h>
int main(){
	fesetround(2048);
	return 0;
}
