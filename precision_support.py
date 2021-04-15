import re

def main():
	with open ("main.c", "r") as myfile:
		c = myfile.read()
	print(c)

	#exp1 = r'printf\("%d\\n"'
	exp1 = r'printf\("corr: %d\\n", y\[0\]\);'
	print(exp1)
	exp2 = r'printf("%f %f\\n", y[4].lo, y[4].up);'
	c = re.sub(exp1, exp2, c)

	print(c)

	f = open("main.c", "w+")
	f.write(c)
	f.close()


if __name__ == "__main__":
	main()
