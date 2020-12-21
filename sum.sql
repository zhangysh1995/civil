-- roof volume
select sum(volume) from roofSchedule;
-- walls
select sum(volume) from wallSchedule where BaseConstraint="G/F" and type NOT LIKE "Curtain%";
640.46
sqlite> select sum(volume) from wallSchedule where BaseConstraint="1/F" and type NOT LIKE "Curtain%";
216.75
sqlite> select sum(volume) from wallSchedule where BaseConstraint="2F" and type NOT LIKE "Curtain%";
193.02
sqlite> select sum(volume) from wallSchedule where BaseConstraint="3F" and type NOT LIKE "Curtain%";
171.93
sqlite> select sum(volume) from wallSchedule where BaseConstraint="4F" and type NOT LIKE "Curtain%";
186.45
sqlite> select sum(volume) from wallSchedule where BaseConstraint="5F" and type NOT LIKE "Curtain%";
168.55
sqlite> select sum(volume) from wallSchedule where BaseConstraint="RF" and type NOT LIKE "Curtain%";
124.75
sqlite> select sum(Area) from wallSchedule where type LIKE "Curtain%" and BaseConstraint="G/F";
329.0
sqlite> select sum(Area) from wallSchedule where type LIKE "Curtain%" and BaseConstraint="1/F";
1053.0
sqlite> select sum(Area) from wallSchedule where type LIKE "Curtain%" and BaseConstraint="2F";
470.0
sqlite> select sum(Area) from wallSchedule where type LIKE "Curtain%" and BaseConstraint="3F";
455.0
sqlite> select sum(Area) from wallSchedule where type LIKE "Curtain%" and BaseConstraint="4F";
469.0
sqlite> select sum(Area) from wallSchedule where type LIKE "Curtain%" and BaseConstraint="5F";
443.0
sqlite> select sum(Area) from wallSchedule where type LIKE "Curtain%" and BaseConstraint="RF";
10.0

-- floor
sqlite> select sum(volume) from floorSchedule where level="G/F";
316.92

sqlite> select sum(volume) from floorSchedule where level="1/F";
175.62

sqlite> select sum(volume) from floorSchedule where level="2F";
177.78

sqlite> select sum(volume) from floorSchedule where level="3F";
177.24

sqlite> select sum(volume) from floorSchedule where level="4F";
176.94

sqlite> select sum(volume) from floorSchedule where level="5F";
178.72

sqlite> select sum(volume) from floorSchedule where level="RF";
220.11