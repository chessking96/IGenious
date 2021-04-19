import re

def main():
	with open ("main.c", "r") as myfile:
		c = myfile.read()
	#print(c)

	#exp1 = r'printf\("%d\\n"'
	exp1 = 'printf\("AfterIGenReplacement"\);'
	#print(exp1)

	# calculate error
	c1 = '\tint max = 0;\n';
	c2 = '\tdouble diff_max = 0;\n'
	c3 = '\tfor(int i = 0; i < 32; i++){\n'
	c4 = '\t\tdouble diff = y[i].up + y[i].lo;\n'
	c5 = '\t\tif(diff > diff_max){\n'
	c6 = '\t\t\tdiff_max = diff;\n'
	c7 = '\t\t\tmax = i;\n'
	c8 = '\t\t}\n'
	c9 = '\t}\n'


	c_new = c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 + c9

	# store answer in variable
	s1 = '\tchar* answer = "true";\n'
	s2 = '\tif(diff_max > 0.00001){\n'
	s3 = '\t\tanswer = "false";\n'
	s4 = '\t}\n'

	c_new = c_new + s1 + s2 + s3 + s4

	# print error
	#p1 = '\tprintf("%f' + r"\\n" + '", diff_max);\n'
	p5 = '\tprintf("%.100g' + r"\\n" + '", y[max].lo);\n'
	p0 = '\tprintf("%.100g' + r"\\n" + '", y[max].up);\n'
	p1 = '\tprintf("%.100g' + r"\\n" + '", diff_max);\n'
	p2 = '\tfile = fopen("sat.cov", "w");\n'
	p3 = '\tfprintf(file, "%s' + r"\\n" + '", answer);\n'
	p4 = '\tfclose(file);\n'

	c_new = c_new + p5 + p0 + p1 + p2 + p3 + p4

	#print(c_new)

	c = re.sub(exp1, c_new, c)

	#print(c)

	f = open("main.c", "w+")
	f.write(c)
	f.close()


if __name__ == "__main__":
	main()
