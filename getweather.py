#!/usr/bin/python
import urllib
import json
import datetime as dt
import os
import tempconv
import csv
#import pandas as p

now = dt.datetime.today()
todate = now.strftime('%Y%m%d')
wdir = os.path.dirname(os.path.realpath(__file__))+'/'

fp = open(wdir+'key','r')
key = fp.readline().strip()
fp.close()
City = {
	'Zizkov': 3061412,
	'Stodulky': 3070270,
	'Tunis': 2464470,
	'Sfax': 2467454,
	'Monastir': 2473493,
	'Paris': 2988507,
	'Hamburg':2911298,
	'Malta':2562501, 
	'Gozo': 2562274,
	'Zabrze':3080985,
	'Brno':3078610
}

C1 = {v: k for k, v in City.items()}

cols = '"Date","Lon","Lat","City","Cid","Wid","Temp","Dew","Feel","Press","Hum","Tmin","Tmax","WS","WD","Cloud","Sunrise","Sunset","Weather"'
#lcols = eval('['+cols+']')

cid = ','.join([str(i) for i in City.values()])
url = 'http://api.openweathermap.org/data/2.5/group?id = {0}&units = metric&appid = {1}'.format(cid,key)

#print url
u = urllib.urlopen(url)
wdata = json.load(u)

fw = open(wdir+'data/original_'+str(todate)+'.json','a')
fw.write(json.dumps(wdata, indent = 4))
fw.close()

csvfile = wdir+'data/weather_'+str(todate)+'.csv'

fc = open(csvfile, 'a+')
if not os.path.isfile(csvfile) or os.path.getsize(csvfile) == 0:
	fc.write(cols+'\n')

for p in wdata['list']:
	ltime = dt.datetime.fromtimestamp(p['dt']).strftime('%Y-%m-%d %H:%M:%S')
	
	cid = p['id']
	for e in ['coord','main','sys','wind']:
		for k,v in p[e].items():
			exec(k+' = v')
	for k,v in p['weather'][0].items():
		exec('w'+k+' = v')
	town = C1[cid]+', '+country
	cloud = p['clouds']['all']
	dew = tempconv.dew(temp,humidity)
	feel = tempconv.feels(temp,humidity,speed)
	srise = dt.datetime.fromtimestamp(sunrise).strftime('%H:%M:%S')
	sset = dt.datetime.fromtimestamp(sunset).strftime('%H:%M:%S')
	#print lon,lat
	a = csv.writer(fc,delimiter = ',')
	data = [[ltime,lon,lat,town,cid,wid,temp,dew,feel,pressure,humidity,temp_min,temp_max,speed*3.6,deg,cloud,srise,sset,wdescription]]
	a.writerows(data)
fc.close()	
