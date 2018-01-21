import gmplot
import io,json

# set output data filename:
inname = "manchester_bus_info.json"

# read input data from file:
input_file  = file(inname, "r")
buses = json.loads(input_file.read().decode("utf-8-sig"))

heat_lons=[];heat_lats=[]
for bus in buses:

	if bus['postcodes']!='None':
		heat_lons += [float(k) for k in bus["longs"]]
		heat_lats += [float(k) for k in bus["lats"]]


man_lon = -2.2363
man_lat = 53.4801

gmap = gmplot.GoogleMapPlotter(man_lat, man_lon, 10)

gmap.heatmap(heat_lats, heat_lons)

gmap.draw("bus_map.html")