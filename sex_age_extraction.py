import os
from os.path import isfile, join
import re

os.chdir(r'C:\Users\sinte\LULU\lab\biomining\SUBGROUP')
txt_dir = r'.\txt'
files = [f for f in os.listdir(txt_dir) if isfile(join(txt_dir, f))]
pattern = r'(\d+)[\s-](year|month|day)[\s-]old.*?(man|woman|male|female|girl|boy)'
prog = re.compile(pattern)




nfound = 0
n_man = 0
n_woman = 0

# clear fle
with open('age.csv', 'w') as fc1:
    pass
with open('sex.csv', 'w') as fc2:
    pass

for file in files:
    with open('age.csv', 'a') as f1:
        with open('sex.csv', 'a') as f2:
            with open(join(txt_dir, file)) as f:
                content = f.read().lower()
                match = prog.search(content)
                if match:
                    age = int(match.group(1))  # the first bracket
                    age = 1 if match.group(2) == 'month' or match.group(2) == 'day' else age
                    f1.write(str(age) + '\n')

                    sex = match.group(3)
                    if sex == 'woman' or sex == 'female' or sex == 'girl':
                        n_woman += 1
                        f2.write('F' + '\n')
                    elif sex == 'man' or sex == 'male' or sex == 'boy':
                        n_man += 1
                        f2.write('M' + '\n')
                    else:
                        print('not man or woman')

                    nfound += 1
                else:
                    print file

print('found:')
print nfound
print('woman: %d' % n_woman)
print('man: %d' % n_man)
