

import csv
import os
import os.path

folders = os.listdir(".")
folders = [f for f in folders if os.path.isdir(f)]

for folder in folders:
    for txt in os.listdir(folder):
        if ".txt" not in txt:
            continue
        with open(os.path.join(folder, txt), "r", encoding="utf-8") as s:
            print(txt)
            lines = s.readlines()
            lines = [line.replace(" ", "").replace("\t","").replace("\"\"","\"").split("\"")[1:-1] for line in lines]
            
            with open(os.path.join(folder, txt[:-4]+".csv").replace(" ", ""), "w+", encoding='utf-8') as c:
                writer = csv.writer(c, dialect='excel', delimiter=',', quotechar="'")
                for i, line in enumerate(lines):
                    nullnum = 0
                    for j, l in enumerate(line):
                        if l == "" or l == '':
                            line[j] = "NULL"
                            nullnum += 1
                    if nullnum == len(line):
                        continue
                    writer.writerow(line) 
