from os import listdir, getcwd, mkdir, rename

from tqdm import tqdm

l = [x for x in listdir(getcwd()) if '.csv' in x]

for i in tqdm(l):
    name = i.split('.csv')[0]
    try:
        mkdir(name)
    except FileExistsError:
        pass

    rename(i, name + '\\all.csv')
