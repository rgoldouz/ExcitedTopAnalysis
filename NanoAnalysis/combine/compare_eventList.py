a = []
b = []


with open('list.tex') as f:
   for line in f:
       a.append(line)
       if 'str' in line:
          break
with open('SH_list.tex') as f:
   for line in f:
       b.append(line)
       if 'str' in line:
          break
c = set(a) - set(b)
print c

print "       ******      "
d = set(b) - set(a)
print d
