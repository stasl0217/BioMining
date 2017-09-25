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
with open('women_age.csv', 'w') as fc1:
    pass
with open('men_age.csv', 'w') as fc2:
    pass

for file in files:
    with open('women_age.csv', 'a') as f1:
        with open('men_age.csv', 'a') as f2:
            with open(join(txt_dir, file)) as f:
                content = f.read().lower()

                # get rid of anything after references
                reference = content.find('references')
                content = content[:reference]

                # perhaps there are more than one cases in one paper
                cases = prog.finditer(content)

                n_cases = 0
                for match in cases:
                    n_cases += 1
                    age = int(match.group(1))  # the first bracket
                    age = 1 if match.group(2) == 'month' or match.group(2) == 'day' else age

                    sex = match.group(3)
                    if sex == 'woman' or sex == 'female' or sex == 'girl':
                        n_woman += 1
                        f1.write('%s\t%d\n' % (file, age))
                    elif sex == 'man' or sex == 'male' or sex == 'boy':
                        n_man += 1
                        f2.write('%s\t%d\n' % (file, age))
                    else:
                        print('not man or woman')

                    nfound += 1
                if n_cases == 0:
                    print file

                if n_cases > 1:
                    print file, n_cases

print('found:')
print nfound
print('woman: %d' % n_woman)
print('man: %d' % n_man)
