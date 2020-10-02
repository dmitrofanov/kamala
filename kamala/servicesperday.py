# Load the Pandas libraries with alias 'pd'
import os
import pandas as pd
import re
import csv

def rstrip_comma(x):
    return x.rstrip(',').strip()

def convert_to_csv(file):
    data = pd.read_csv(file, sep=';', encoding='cp1251')

    lis = data.astype(str).values.tolist()

    target = []
    for rows in lis:
        date = rows[1]
        services = re.findall(r'([^;]+?, \d+,)', rows[3])
        l = map(rstrip_comma, services)
        for x in l:
            rvs = x[::-1]
            i = rvs.find(',')
            t1 = x[:-i - 1].strip()
            t2 = x[-i:].strip()
            target.append([date, t1, t2])
    return target

def write_file(full_path, list_of_lists):
    with open(full_path, "w+", newline="", encoding='cp1251') as f:
        writer = csv.writer(f)
        writer.writerows(list_of_lists)