import io,json
import os,sys
import csv


def get_bus_names(ward):

	"""
	For a given ward (input) checks all 
	the bus route data to see if a particular 
	route has bus stops in that ward. Returns 
	the total number of routes passing through
	that ward and a list of the route names.
	"""

	# set output data filename:
	inname = "manchester_bus_info.json"

	# read input data from file:
	input_file  = file(inname, "r")
	buses = json.loads(input_file.read().decode("utf-8-sig"))

	# get the bus routes that pass through the ward:
	bus_names = []
	for bus in buses:
		if ward.replace("&",'and') in bus["wards"]:
			bus_names.append(bus['route'])


	# number of buses:
	nbus = len(bus_names)

	return nbus, bus_names




# ==========================================================================================	
# ==========================================================================================	


if __name__ == '__main__':

	csvfile = open('ward_data.csv', 'rU')
	reader = csv.reader(csvfile)

	keys = next(csvfile, None).split(',')

	wards=[]
	for row in reader:

		ward = {}
		for i in range(0,len(keys)):
			
			ward[str(keys[i])] = str(row[i]).strip('\n')

		nbus,bus_names = get_bus_names(row[0])
		ward['buses'] = bus_names
		ward['no. buses'] = nbus

		wards.append(ward)


	jsonfile = "manchester_wards.json"
	# write the resulting list of post dictionaries to a JSON file with UTF8 encoding:
	with io.open(jsonfile, 'w', encoding='utf-8') as f:
  		f.write(json.dumps(wards, ensure_ascii=False))


