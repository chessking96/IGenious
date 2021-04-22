if [ "$1" = "" ] || [ "$2" = "" ] ; then
  echo "Argument missing."
  exit
fi

cd $1

# prepare files for precimonious
../../precimonious/scripts/compile.sh $1 .
../../precimonious/scripts/dependencies.sh $1 $2 .
touch exclude.txt # would allow to add variables which should not be considered in analysis
../../precimonious/scripts/pconfig.sh $1 .
../../precimonious/scripts/search.sh $1 .

# prepare copy of c code
cp $1.c code_temp.c
python3 ../scripts/multideclaration.py DFT16

# rename to standard name
cp config_$1.json config_orig.json

# copy helper files
cp ../src/random_range.c random_range.c

cp ../src/CMakeLists.txt CMakeLists.txt

# create main function for time measurement
touch main.c
include1="#include \"random_range.c\"\n"
include2="#include \"code_rep.c\"\n"
include3="#include <time.h>\n"
include4="#include <stdio.h>\n"
include=$include1$include2$include3$include4"\n"

mainIntro="int main(){\n"
m1="\tinitRandomSeed();\n"
m2="\tlong double* x = malloc(32*sizeof(long double));\n"
m3="\tfor(int i = 0; i < 32; i++){"
m4="\t\tlong double h = getRandomDouble();\n"
m5="\t\tx[i] = h;\n"
m6="\t}\n"
m65='\tprintf("0: %.20f %.20f %.20f %.20f\\n", x[0].lh, x[0].ll, x[0].uh, x[0].ul);\n'
m7="\tlong double* y = malloc(32*sizeof(long double));\n"
m8="\tclock_t start = clock();\n"
m9="\tfor(int i = 0; i < 2000000; i++){\n"
m10="\t\t"$2"(y, x);\n"
m11="\t}\n"
m12="\tclock_t end = clock();\n"

# time print and save
m13="\tlong diff_time = (long)(end-start);\n"
m14='\tprintf("diff: %ld\\n", diff_time);\n'
m15='\tFILE* file = fopen("score.cov", "w");\n'
m16='\tfprintf(file, "%ld\\n", diff_time);\n'
m17="\tfclose(file);\n"

# accuraccy print and save (has to be overwritten after IGen compilation)
m18='\tprintf("BeforeIGenReplacement");\n'
#m18='\tprintf("corr: %d\\n", y[0]);\n'
#m19="\tfile = fopen(\"sat.cov\", \"w\");\n"
#m20='\tfprintf(file, "true\\n");\n'
#m21="\tfclose(file);\n"


m19="\treturn 0;\n"
mainBody=$m1$m2$m3$m4$m5$m6$m65$m7$m8$m9$m10$m11$m12$m13$m14$m15$m16$m17$m18$m19 #$m20$m21$m22
main=$mainIntro$mainBody"}"

code="$include$main"

echo -e $code > main.c

python3 ../../IGen/bin/igen.py main.c
python3 ../../IGen/bin/igen.py random_range.c
cp main.c orig_main.c
cp random_range.c orig_random_range.c
cp igen_main.c main.c
cp igen_random_range.c random_range.c

python3 ../scripts/precision_support.py



cd ..

