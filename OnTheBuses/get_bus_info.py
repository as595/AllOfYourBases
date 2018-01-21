from bs4 import BeautifulSoup as bs
import requests
import io,json
import urllib2,re
import os,sys
from tqdm import tqdm
import time


# ------------------------------------------------------

def get_postcode(lon,lat):

	"""
	Extracts postcodes from postcodes.io given an 
	input longitude and latitude
	"""

	# set base url:
	base = "http://api.postcodes.io/postcodes?lon="
	query = lon+"&lat="+lat

	# get list of archive pages:
	r = requests.get(base+query)
	page = json.loads(r.text)
	if page['status']==200:
		if page['result']==None:
			postcode='None'
			ward='None'
		else:
			postcode = page['result'][0]['postcode']
			ward = page['result'][0]['admin_ward']
	else:
		postcode='None'
		ward='None'
		
	return postcode,ward


# ------------------------------------------------------

def get_stops(url):

	"""
	Extracts (longitude,latitude) data for bus stops 
	listed on the given TfGM url.
	Calls get_postcode() to find out which postcode
	and administrative ward each (longitude,latitude) 
	position is in.
	"""

	# set base url:
	base = "https://www.tfgm.com"
	query = url

	# get list of archive pages:
	r = requests.get(base+query)
	page = r.text
	soup=bs(page,'lxml')

	stops = soup.findAll('li',attrs={"class":"bus-stop-link"})

	names=[];longs=[];lats=[];pcodes=[];wards=[]
	for stop in stops:

		temp = stop.text.strip('\n').replace("/ ","")
		if temp.find(',')>-1:
			loc,spot = temp.split(',')
			name = spot+', '+loc
		else:
			name = temp

		names.append(name)
		longs.append(stop['data-longitude'])
		lats.append(stop['data-latitude'])

		postcode,ward = get_postcode(stop['data-longitude'],stop['data-latitude'])
		pcodes.append(postcode)
		wards.append(ward)


	return names,longs,lats,pcodes,wards



# ==========================================================================================	
# ==========================================================================================	


if __name__ == '__main__':

	# set base url:
	base = "https://www.tfgm.com"
	query = "/public-transport/bus/routes"

	# get list of bus routes:
	r = requests.get(base+query)
	page = r.text
	soup=bs(page,'lxml')

	bus_routes = soup.findAll('a',attrs={"class":"result-button"})

	# loop through routes to extract stops for each:
	buses = []
	for each in bus_routes:

		bus = {}

		bus['route'] = each['id']
		bus['url'] = each['href']

		names,longs,lats,pcodes,wards = get_stops(bus['url'])

		bus['stops'] = names
		bus['longs'] = longs
		bus['lats'] = lats
		bus['postcodes'] = pcodes
		bus['wards'] = wards
		
		buses.append(bus)


	# set output file name:
	jsonfile = "manchester_bus_info.json"
	# write the resulting list of post dictionaries to a JSON file with UTF8 encoding:
	with io.open(jsonfile, 'w', encoding='utf-8') as f:
		output = json.dumps(buses, ensure_ascii=False)
		f.write(output)

