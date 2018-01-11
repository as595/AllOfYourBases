from bs4 import BeautifulSoup as bs
import requests
import io,json
import urllib2,re
import os,sys
from tqdm import tqdm
import time
import share_counters as scs

query_fb = True
if (query_fb):
	print "===================================="
	print " This script is throttled to avoid  "
	print " the Facebook rate limit. It will   "
	print " run very slowly.                   "
	print "===================================="
	

# set base url:
base = "http://blog.policy.manchester.ac.uk/"

# set first page as the base url: 
page = base
npage= 1

# initiate empty list of blogs:
blogs=[]

while True:
	
	# print progress:
	print "Reading Page ",npage
		
	# in subsequent loops page = nextpage
	r = requests.get(page)
	page = r.text
	soup=bs(page,'html.parser')

	# find all the blog articles on this page:
	articles = soup.findAll('article')

	# loop through the articles extracting the info for each:
	for article in tqdm(articles):

		# initiate empty dictionary for this post:
		post = {}

		# start extracting info from html"
		title = article.find('h2',attrs={'class':"entry-title"})
		date = article.find('time',attrs={'class':"entry-time"})  # changed from 'time' --> 'date' to avoid Nonetype error with time library...

		post['title'] = title.text
		post['date'] = date.text
		
		# extract author list:
		authors = article.findAll('a',attrs={'class':"author url fn"})
		alist=[]
		for author in authors:
			alist.append(author.text)
		post['authors'] = alist

		# extract categories:
		categories = article.findAll('a', attrs={'rel':"category tag"})
		clist=[]
		for category in categories:
			clist.append(category.text)
		post['categories'] = clist

		# extract tags:
		tags = article.findAll('a', attrs={'rel':"tag"})
		tlist=[]
		for tag in tags:
			tlist.append(tag.text)
		post['tags'] = tlist

		post['shares'] = {}

		# Get pinterest shares:
		pinterest = article.find(attrs={'class':"pinterest"})
		r = requests.get('http://api.pinterest.com/v1/urls/count.json', params={'callback':None, 'url':pinterest["data-urlalt"]})
		result = json.loads(r.text.lstrip('receiveCount(').rstrip(')'))
		pins = int(result['count'])
		r = requests.get('http://api.pinterest.com/v1/urls/count.json', params={'callback':None, 'url':pinterest["data-url"]})
		result = json.loads(r.text.lstrip('receiveCount(').rstrip(')'))
		pins += int(result['count'])
		post['shares']['pinterest'] = str(pins)

		if (query_fb):
			# Get facebook shares:
			facebook = article.find(attrs={'class':"facebook"})
			# add in a wait time to avoid facebook API rate limit [200 calls in 60 minutes = 1 call per 18 seconds]:
			time.sleep(18)
			urlFacebook = "https://graph.facebook.com/?id=" + facebook["data-url"]
			dFacebook = urllib2.urlopen(urlFacebook).read()
			data = json.loads(dFacebook)
			try:
				post['shares']['facebook'] = str(data["shares"])
			except KeyError:
				post['shares']['facebook'] = 'error'	

		# Get googlePlus shares:
		urlGplus = 'https://plusone.google.com/_/+1/fastbutton?url='+pinterest["data-url"]
		data = urllib2.urlopen(urlGplus).read()
		match = re.findall('window.__SSR = {c: ([\d]+)', data)
		if match:
			post['shares']['googleplus'] = str(match[0])
		else:
			post['shares']['googleplus'] = str(0)

		# Get linkedin shares:
		urlLinkedin = "http://www.linkedin.com/countserv/count/share?url=" + pinterest["data-url"] + "&format=json"
		dLinkedin = urllib2.urlopen(urlLinkedin).read()
		data = json.loads(dLinkedin)
		try:
			post['shares']['linkedin'] = str(data["count"])
		except KeyError:
			post['shares']['linkedin'] = str(0)

		# finally put the url of the article into the dictionary too:
		post['url'] = pinterest["data-url"]

		# append article dictionary into list of blogs:
		blogs.append(post)

	
	# find out if there is a next page of blogs:
	onwards = soup.find('li', attrs={'class':"pagination-next"})
	if (onwards==None): 
		# exit loop:
		break
	else:
		# extract url for next page:
		nextpage = onwards.find('a')["href"]
	
		# set page to nextpage:
		page = nextpage

		# increment page number:
		npage += 1


jsonfile = 'manchester_blogs.json'
if os.path.isfile(jsonfile):
	os.system('rm '+jsonfile+'\n')

# write the resulting list of post dictionaries to a JSON file with UTF8 encoding:
with io.open(jsonfile, 'w', encoding='utf-8') as f:
  f.write(json.dumps(blogs, ensure_ascii=False))

