import os
from os.path import isfile, join
import re


def is_man(sex):
    """
    :param sex:
    :return:
    """
    if sex == 'woman' or sex == 'female' or sex == 'girl':
        return False
    elif sex == 'man' or sex == 'male' or sex == 'boy':
        return True
    else:
        raise ValueError('not man or woman')

os.chdir(r'C:\Users\sinte\LULU\lab\biomining\SUBGROUP')
txt_dir = r'.\txt'
files = [f for f in os.listdir(txt_dir) if isfile(join(txt_dir, f))]
pattern = r'(\d+)[\s-](year|month|day)[\s-]old.*?(man|woman|male|female|girl|boy)'
prog = re.compile(pattern)

n_ok_paper = 0
n_man = 0
n_woman = 0
total_cases = 0

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
                # (unrelated info)
                reference = content.find('references')
                content = content[:reference]

                # perhaps there are more than one cases in one paper
                cases = prog.finditer(content)

                n_cases = 0
                last_age = 0  # test if it's duplicate info
                last_sex = True
                for match in cases:
                    age = int(match.group(1))  # the first bracket
                    age = 1 if match.group(2) == 'month' or match.group(2) == 'day' else age
                    is_male = is_man(match.group(3))

                    if age != last_age or is_male != last_sex:
                        # new case
                        n_cases += 1
                        last_sex = is_male
                        last_age = age

                        if not is_male:
                            n_woman += 1
                            f1.write('%s\t%d\n' % (file, age))
                        else:
                            n_man += 1
                            f2.write('%s\t%d\n' % (file, age))

                total_cases += n_cases

                if n_cases == 0:
                    print file
                else:
                    n_ok_paper += 1

                if n_cases > 1:
                    print file, n_cases

print('found:')
print n_ok_paper
print('woman: %d' % n_woman)
print('man: %d' % n_man)
print 'total cases:%d' % total_cases
