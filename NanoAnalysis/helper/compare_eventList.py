a = []
b = []

import Apr21_PhB
with open('event_2017_B_SinglePhoton.tex') as f:
   content=f.readlines()
   for line in content:
       a.append(line.strip())
       if 'str' in line:
          break

#with open('Apr21_PhB.txt') as f:
#   for line in f:
#       b.append(line)
#       if 'str' in line:
#          break
b= Apr21_PhB.Apr21_PhB
c = set(a) - set(b)
print c

print "       ******      "
d = set(b) - set(a)
print d
