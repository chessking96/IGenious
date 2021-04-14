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

# change declarations
python3 ../multideclaration.py DFT16

# rename to standard name
cp config_$1.json config_orig.json

# copy helper files
cp ../random_range.c random_range.c

cp ../CMakeLists.txt CMakeLists.txt

# create main function for time measurement
touch main.c
include1="#include \"random_range.c\"\n"
include2="#include \"code_rep.c\"\n"
include3="#include <time.h>\n"
include4="#include <stdio.h>\n"
include=$include1$include2$include3$include4"\n"

mainIntro="int main(){\n"
m1="\tinitRandomSeed();\n"
m2="\tdouble* x = malloc(16*sizeof(double));\n"
m3="\tfor(int i = 0; i < 16; i++){\n"
m4="\t\tdouble h = getRandomDouble();\n"
m5="\t\tx[i] = h;\n"
m6="\t}\n"
m7="\tdouble* y = malloc(16*sizeof(double));\n"
m8="\tclock_t start = clock();\n"
m9="\t"$2"(x, y);\n"
m10="\tclock_t end = clock();\n"
m11="\tlong diff = (long)(end-start);\n"
m12='\tprintf("diff: %ld\\n", end);\n'
m13='\tFILE* file = fopen("score.cov", "w");\n'
m14='\tfprintf(file, "%ld\\n", diff);\n'
m15="\tfclose(file);\n"

m16="\tfile = fopen(\"sat.cov\", \"w\");\n"
m17='\tfprintf(file, "true\\n");\n'
m18="\tfclose(file);\n"
m19="\treturn 0;\n"
mainBody=$m1$m2$m3$m4$m5$m6$m7$m8$m9$m10$m11$m12$m13$m14$m15$m16$m17$m18$m19
main=$mainIntro$mainBody"}"

code="$include$main"

echo -e $code > main.c

cd ..




