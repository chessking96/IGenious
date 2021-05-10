import re

def main():
	with open ("main.c", "r") as myfile:
		c = myfile.read()

	exp1 = 'printf\("BeforeIGenReplacement"\);'

	# calculate error
	c1 = '\tint max = 0;\n'
	c2 = '\tdd_I diff_max = _ia_zero_dd();\n'
	c3 = '\tfor(int i = 0; i < 1; i++){\n'
	#c3 = '\tfor(int i = 0; i < 32; i++){\n'
	c4 = '\t\tdd_I lower_bound = _ia_set_dd(y[i].lh, y[i].ll, -y[i].lh, -y[i].ll);\n'
	c41= '\t\tdd_I upper_bound = _ia_set_dd(-y[i].uh, -y[i].ul, y[i].uh, y[i].ul);\n'
	c42= '\t\tdd_I diff = _ia_sub_dd(upper_bound, lower_bound);\n'
	c5 = '\t\tif(_ia_cmpgt_dd(diff, diff_max)){\n'
	c6 = '\t\t\tdiff_max = diff;\n'
	c7 = '\t\t\tmax = i;\n'
	c8 = '\t\t}\n'
	c9 = '\t}\n'


	c_new = c1 + c2 + c3 + c4 + c41 + c42 + c5 + c6 + c7 + c8 + c9

	# store answer in variable
	s1 = '\tchar* answer = "false";\n'
	s11 = '\tdouble th = 0.0000001;\n'
	s12 = '\tprintf("%i' + r"\\n" + '", (int)_ia_cmpgt_dd(_ia_set_dd(-th, 0, th, 0),diff_max));\n'
	s2 = '\tif((int)_ia_cmpgt_dd(_ia_set_dd(-th, 0, th, 0), diff_max) == 1){\n'

	s3 = '\t\tanswer = "true";\n'
	s4 = '\t}\n'
	c_new = c_new + s1 + s11 + s12 + s2 + s3 + s4
	# print error
	#p1 = '\tprintf("%f' + r"\\n" + '", diff_max);\n'
	p2 = '\tprintf("1: %.20f %.20f' + r"\\n" + '", y[max].lh, y[max].ll);\n'
	p3 = '\tprintf("2: %.20f %.20f' + r"\\n" + '", y[max].uh, y[max].ul);\n'
	p4 = '\tprintf("3: %.20f %.20f' + r"\\n" + '", diff_max.lh, diff_max.ll);\n'
	p5 = '\tprintf("4: %.20f %.20f' + r"\\n" + '", diff_max.uh, diff_max.ul);\n'
	p6 = '\tfile = fopen("sat.cov", "w");\n'
	p7 = '\tfprintf(file, "%s' + r"\\n" + '", answer);\n'
	p8 = '\tfclose(file);\n'

	c_new = c_new + p2 + p3 + p4 + p5 + p6 + p7 + p8


	c = re.sub(exp1, c_new, c)


	f = open("main.c", "w+")
	f.write(c)
	f.close()


	c1 = '#include <stdlib.h>\n'
	c2 = 'void initRandomSeed() { srand(42);}\n'
	c3 = 'dd_I getRandomDouble() {\n'
	c4 = 'long double r1 = ((long double)rand())/(RAND_MAX);\n'
	c5 = 'long double r2 = ((long double)rand())/(RAND_MAX);\n'
	c6 = 'return _ia_set_dd(-r1, -r2, r1, r2);}\n'


	c = c1 + c2 + c3 + c4 + c5 + c6


	with open ("random_range.c", "w") as myfile:
		myfile.write(c)



if __name__ == "__main__":
	main()
