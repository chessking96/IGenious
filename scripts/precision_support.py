import re

def main():
	with open ("main.c", "r") as myfile:
		c = myfile.read()
	#print(c)

	#exp1 = r'printf\("%d\\n"'
	exp1 = 'printf\("BeforeIGenReplacement"\);'
	#print(exp1)

	# calculate error
	c1 = '\tint max = 0;\n'
	c2 = '\tdd_I diff_max = _ia_zero_dd();\n'
	c3 = '\tfor(int i = 0; i < 32; i++){\n'
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
	s1 = '\tchar* answer = "true";\n'
	s11 = '\tdouble th = 0.0000001;\n'
	s2 = '\tif(_ia_cmpgt_dd(diff_max, _ia_set_dd(-th, 0, th, 0))){\n'
	s3 = '\t\tanswer = "false";\n'
	s4 = '\t}\n'

	c_new = c_new + s1 + s11 + s2 + s3 + s4

	# print error
	#p1 = '\tprintf("%f' + r"\\n" + '", diff_max);\n'
	p5 = '\tprintf("1: %.20f %.20f' + r"\\n" + '", y[max].lh, y[max].ll);\n'
	p0 = '\tprintf("2: %.20f %.20f' + r"\\n" + '", y[max].uh, y[max].ul);\n'
	p1 = '\tprintf("3: %.20f %.20f' + r"\\n" + '", diff_max.uh, diff_max.ul);\n'
	p15= '\tprintf("4: %.20f %.20f %.20f %.20f' + r"\\n" + '", y[0].lh, y[0].ll, y[0].uh, y[0].ul);\n'
	p2 = '\tfile = fopen("sat.cov", "w");\n'
	p3 = '\tfprintf(file, "%s' + r"\\n" + '", answer);\n'
	p4 = '\tfclose(file);\n'

	c_new = c_new + p5 + p0 + p1 + p15 + p2 + p3 + p4

	#print(c_new)

	c = re.sub(exp1, c_new, c)

	#print(c)

	f = open("main.c", "w+")
	f.write(c)
	f.close()


if __name__ == "__main__":
	main()
