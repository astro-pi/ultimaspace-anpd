#Python 2.7!
#UlltimaSpace ANPD Version 1.0
#Update TLE if possible!

#Libs
from sense_hat import SenseHat
from time import sleep
from datetime import datetime
import csv
import ephem
import time
#Config
sense = SenseHat()
FILENAME = ""
WRITE_FREQUENCY = 1
avgtemp = 25.6457
sense.low_light = True

#######UPDATE TLE HERE(updated: 08/03/2017)######
name = "ISS (ZARYA)";             

line1 = "1 25544U 98067A   17214.86432128  .00000490  00000-0  14639-4 0  9999"
line2 = "2 25544  51.6423 165.6346 0006340  96.8361 359.3851 15.54247166 69011"
#################################################

lati = 0
longt = 0
ast = 0
e = [255,255,255]
u = [0,100,255]
s = [255,255,0]
g = [0,255,0]
r = [255,0,0]
n = [0,0,0]

presence=[e,u,s,s,s,s,u,e,
e,u,s,n,n,n,u,e,
e,u,s,s,s,s,u,e,
e,u,n,n,n,s,u,e,
e,u,s,s,s,s,u,e,
e,e,u,u,u,u,e,e,
e,e,g,g,g,g,e,e,
e,e,g,g,g,g,e,e]

unpresence=[e,u,s,s,s,s,u,e,
e,u,s,n,n,n,u,e,
e,u,s,s,s,s,u,e,
e,u,n,n,n,s,u,e,
e,u,s,s,s,s,u,e,
e,e,u,u,u,u,e,e,
e,e,r,r,r,r,e,e,
e,e,r,r,r,r,e,e]

#Functions
def file_setup(filename):
    header  =["temp","presence","mag_x","mag_y","mag_z","latitude","longtitude","timestamp"]

    with open(filename,"w") as f:
        f.write(",".join(str(value) for value in header)+ "\n")

def log_data():
    output_string = ",".join(str(value) for value in sense_data)
    batch_data.append(output_string)

def get_sense_data():
    sense_data=[]

    sense_data.append(sense.get_temperature_from_pressure())
    sense_data.append(ast)
    
    mag = sense.get_compass_raw()
    mag_x = mag["x"]
    mag_y = mag["y"]
    mag_z = mag["z"]
    sense_data.extend([mag_x,mag_y,mag_z])

    sense_data.append(lati)
    sense_data.append(longt)
    sense_data.append(datetime.now())
    

    return sense_data

#Main program

batch_data= []

if FILENAME == "":
    filename = "UltimaLog-"+str(datetime.now())+".csv"
else:
    filename = FILENAME+"-"+str(datetime.now())+".csv"

file_setup(filename)

while True:
 sense_data = get_sense_data()
 log_data()

 t=sense.get_temperature_from_pressure()

 if t >= avgtemp :

  sense.set_pixels(presence)
  ast = 1

 else :

  sense.set_pixels(unpresence)
  ast = 0
   
 time.sleep(0.5)
 tle_rec = ephem.readtle(name, line1, line2)
 tle_rec.compute()
    
 
 lat2string = str(tle_rec.sublat)
 long2string = str(tle_rec.sublong)

 lati = lat2string.split(":")
 longt = long2string.split(":")

#Print some relevant data
 print lati[0]
 print longt[0]
 print(t)
 print(ast)

#Write to csv file
 if len(batch_data) >= WRITE_FREQUENCY:
     print("Writing to file..")
     with open(filename,"a") as f:
         for line in batch_data:
             f.write(line + "\n")
         batch_data = []

 sleep(10)
