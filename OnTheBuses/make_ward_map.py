from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import io,json



# ------------------------------------------------------

def get_ward_nbus():

	# set output data filename:
	inname = "manchester_wards.json"

	# read input data from file:
	input_file  = file(inname, "r")
	wards = json.loads(input_file.read().decode("utf-8-sig"))

	wardnames=[];nbuses=[]
	for ward in wards:
		wardnames.append(ward["WARDNAME"])
		if ward["no. buses"]!=0:
			nbuses.append(float(ward["no. buses"]))
		else:
			nbuses.append(1.0)

	wardnames=np.array(wardnames)
	nbuses = np.array(nbuses)

	return wardnames,nbuses


# ------------------------------------------------------


def read_ward_coords(ward):

	filename = "./WARD_BOUNDARIES/"+ward.lower().replace(" & ","").replace(" ","")+".kml"
	
	if os.path.exists(filename):
		# http://www.manchester.gov.uk/downloads/download/3946/manchester_ward_boundaries
		infile = open(filename,'r')

		lon=[];lat=[]
		while True:
			line = infile.readline()
			if not line: break

			items = line.split(',')
			if len(items)>1:
				lon.append(float(items[0]))
				lat.append(float(items[1]))

		lon = np.array(lon)
		lat = np.array(lat)
	else:
		print "No boundary data for ",ward
		lon=[];lat=[]
		
	return lon,lat



# ==========================================================================================	
# ==========================================================================================	


if __name__ == '__main__':


	man_lon = -2.2363
	man_lat = 53.445

	# create figure and axes instances
	fig = plt.figure(figsize=(12,12))
	ax = fig.add_axes([0.1,0.1,0.8,0.8])

	m = Basemap(width=15000,height=25000,
	            resolution='f',projection='stere',\
	            lat_ts=man_lat,lat_0=man_lat,lon_0=man_lon)


	wardnames,nbuses = get_ward_nbus()

	# we're going to blank this out:
	nbuses[np.where(wardnames=='City Centre')] = 10.0

	max_bus = np.max(nbuses)
	buses_n = nbuses/max_bus
	min_bus = np.max(buses_n)
	buses_n = np.log10((10./min_bus)*buses_n)



	for i in range(len(wardnames)):

		lons,lats = read_ward_coords(wardnames[i])

		if (len(lons)>0):

			# compute map proj coordinates.
			x, y = m(lons, lats) 

			# fill in colour:
			if wardnames[i]=='City Centre':
				plt.fill(x,y,'black', alpha=1.0)
			else:
				plt.fill(x,y,'b', alpha=buses_n[i])

			

	plt.savefig('manchester_map.png')
	plt.show()