import sqlite3
import csv

files = [
#"MechanicalEquipmentSchedule.csv",
#"PipeFittingSchedule.csv",
#"PipeSchedule.csv",
#"RoofSchedule.csv",
"FloorSchedule.csv",
"StairSchedule.csv",
"StructuralColumnSchedule.csv",
"WallSchedule.csv"]

conn = sqlite3.connect('schedule.db')
c = conn.cursor()
c.execute("SELECT 'DROP TABLE ' || name || ';' FROM sqlite_master;")

# for f in files:
#     fname = f.split(".")[0]
#     tname = fname[0].lower() + fname[1:]
#     with open(f, "r") as c:
#         header = c.readline()
#         hs = header.split(";")
#         c.execute("create table " + tname + "( " + header + ")")
#         dr = csv.DictReader(fin) # comma is default delimiter
        
import pandas as pd
for f in files:
    fname = f.split(".")[0]
    tname = fname[0].lower() + fname[1:]
    with open(f, "r") as cf:
        header = cf.readline()
        hs = header.split(";")
        print(f)
        pd.read_csv(f).to_sql(tname, conn,  index=False)
        cf.close()
