import csv
import sys

# input source list from PyBDSF:
filename = sys.argv[1]+'.csv'

# open the CSV file using universal read:
csvfile = open(filename, 'rU') 

# set up the output annotation file:
outname = sys.argv[1]+'.ann'
outfile = open(outname,'w')

# get the FOV:
ra0 = sys.argv[2]
dec0= sys.argv[3]
hwhm= 10./60.
hwhm=str(hwhm)

# set up a CSV reader:
readCSV = csv.reader(csvfile, delimiter=',')
	
# skip the header:
next(csvfile, None)
next(csvfile, None)
next(csvfile, None)
next(csvfile, None)

# skip the column headings:
next(csvfile, None)
next(csvfile, None)

# read the source data:
for row in readCSV:
	ra = row[2]
	dec = row[4]
	bmaj = row[14]
	bmin = row [16]
	pa = row[18]

	bpa = float(pa)+90. 
	
	outfile.write('ELLIPSE '+ra+' '+dec+' '+bmaj+' '+bmin+' '+str(bpa)+'  \n')

outfile.write('COLOR RED  \n')
outfile.write('CIRCLE '+ra0+' '+dec0+' '+hwhm+'  \n')
outfile.close()


		