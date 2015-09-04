
from flask import Flask, request, render_template
import math
import urlparse
import urllib
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

dates = []			#list to hold all timestamps extracted
span =  []
date_o = []			#list to hold all date objects

app = Flask('Shipping assignment') 


# index template
@app.route('/')
def form():
    return render_template('index.html')

# fetch and display the number of issues
@app.route('/result/', methods=['POST'])
def result():
	#get the url to be fetched
	url=request.form['url']

	try:
		#fetch the Url
		response = urllib.urlopen(url).read()

		#parse response	 
		soup = BeautifulSoup(response,"lxml")		
				
		# find all a tag with class "btn-link selected"
		name = soup.findAll("a",{ "class" : "btn-link selected" }) 

		# convert all elements bs4 class elements to string and apppend to span
		for x in name:												
			span.append(str(x))

		# since git has not embedded total no of issues inside any tag hence treat it as a string split and extract
		res = span[0].split('>')
		res = res[3].split(' ')

		#convert res[6] i.e no of pages into integer
		noOfPages = int(res[6])/25 

		#list to hold all time tags
		result = [] 	

		# crawl through all the apges one by one
		for i in range(1,noOfPages+2): 
			#fetch page no i
			response = urllib.urlopen(url + '?page='+str(i)+'+&q=is%3Aissue+is%3Aopen').read()
							
			#parse the fetched page
			soup = BeautifulSoup(response,"lxml")

			#list to hold all time tags form each page
			result = result + soup.findAll(attrs={"is" : "relative-time"}) 

		# get timestamp for each issue and appent it to the dates list 
		for attr in result:
			time = attr.get('datetime')
			ts = time.replace("T", " ")
			ts = ts.replace("Z", " ")
			dates.append(str(ts))

		# convert each timestamp into date object
		for i in range(len(dates)):
			date_object = datetime.strptime(dates[i][:-1], '%Y-%m-%d %H:%M:%S')
			date_o.append(date_object)

		#get last24hrs timestamp
		last24hrs = datetime.now() - timedelta(days=1)

		#get last7days timestamp	
		last7days = datetime.now() - timedelta(days=7)

		#get last30days timestamp		
		last30days = datetime.now() - timedelta(days=30)

		#initalize count 
		count = count1 = count2 = 0

		#for every date in date_o list check the range
		for date in date_o:
			#check if the date is within 24 hours
			if date > last24hrs:
				count = count + 1
			if date < last24hrs and date > last7days:
				count1 = count1 + 1

		issuesOpen  = res[6]
		within24 = str(count)
		within7 = str(count1)
		after7 = str(int(res[6]) - count1 - count)

		#clear all the list values
		dates[:] = []
		span[:] = []
		date_o[:] = []
		result[:] = []
		return render_template('result.html', issuesOpen=issuesOpen,within24 = within24,within7 = within7, after7 = after7)
	except:
		return render_template('error.html')



								
if __name__=='__main__':
	app.run(debug=True,host='0.0.0.0')
