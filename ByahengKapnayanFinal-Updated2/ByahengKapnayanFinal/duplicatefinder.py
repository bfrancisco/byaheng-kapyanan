f = open("unblnced_equations.txt", "r")
a = set()
c = 1
for line in f.readlines():
    if line in a:
        print(c)
    a.add(line)
    c += 1
f.close()