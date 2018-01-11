import io,json
import urllib2,re
import os,sys
import time

# set input data filename:
inname = "manchester_blogs_tmp.json"

# read input data from file:
input_file  = file(inname, "r")
blogs = json.loads(input_file.read().decode("utf-8-sig"))

# calculate total number of blog article:
nblogs = len(blogs)

# set output data filename:
ouname = "manchester_blogs_fb.json"

# loop through blog articles and update missing fb share counts:
for i in range(0,nblogs):

	blog = blogs[i]
	
	# only replace values that are in error:
	if blog['shares']['facebook'] == 'error':

		# rate limited...
		time.sleep(18)
		url = blog['url']
		urlFacebook = "https://graph.facebook.com/?id=" + url

		try:
			dFacebook = urllib2.urlopen(urlFacebook).read()
			data = json.loads(dFacebook)
			blogs[i]['shares']['facebook'] = str(data['share']['share_count'])

			# write the resulting list of post dictionaries to a JSON file with UTF8 encoding
			# this is slow but it doesn't matter because fb is rate limited anyway
			with io.open(ouname, 'w', encoding='utf-8') as f:
				f.write(json.dumps(blogs, ensure_ascii=False))

		except urllib2.HTTPError:
			# if this happens we've probably hit the rate limit... (200 per hour = 1 every 18 seconds)
			blogs[i]['shares']['facebook'] = 'error'
			print "Error returned at article: ",i
		
		
	#onwards = raw_input("Hit return")

# jsonfile = 'manchester_blogs_tmp.json'
# if os.path.isfile(jsonfile):
# 	os.system('rm '+jsonfile+'\n')

# # write the resulting list of post dictionaries to a JSON file with UTF8 encoding:
# with io.open(jsonfile, 'w', encoding='utf-8') as f:
#   f.write(json.dumps(blogs, ensure_ascii=False))


