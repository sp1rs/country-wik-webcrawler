
import sys 

## To Extract link from the html doc
from bs4 import BeautifulSoup

## To Convert the page into html format
import urllib2

## Get the list of countries
import pycountry


## Use OrderedDict so that the output can be  shown in proper format
import collections



## Since number of countries are less than 200, we will store it in the array
## List of all the countries
country_list={}

## All the countries whose wiki has been visited
country_visited={}

## All the countries whose wiki has not been visited
country_to_be_visited=[]

json=collections.OrderedDict()


def get_country():
	global country_list
	for x in pycountry.countries:
		country_list[x.name]=1



def extract_country_link(country):
	hyperlink= "http://en.wikipedia.org/wiki/"
	if( country_visited.has_key(country) == False):
		country_visited[country]=1
		response = urllib2.urlopen(hyperlink+country)
		html = response.read()
		soup = BeautifulSoup(html)
		has={}
		for link in soup.find_all('a'):
			link_country=link.get('href')
			if ( link_country != None ):
				link_country = link_country.split('/')
				if(len(link_country) >=3):
					coun = link_country[2]
					if( coun!=country and country_list.has_key(coun)  and has.has_key(coun) == False ):
						if json.has_key(country)==True:
							json[country].append(coun)
						else:
							json[country]=[coun]
						has[coun]=1
						if country_visited.has_key(coun) == False:
							country_to_be_visited.append(coun)

		
	if ( len(country_to_be_visited)!=0 ):
		country=country_to_be_visited.pop(0)	
		extract_country_link(country)	
		
	
			
				
			
if __name__ == "__main__":
	
	## take input as a country from the user
	print "Enter the country : "
	country=raw_input()
	
	## Get all the countries using pycountry module
	get_country()	

	## Parse all the wiki pages of the countries
	for x in country_list.keys():
		if x.lower() == country.lower():
			extract_country_link(country)	
	        	## Print the formated output in similar way it is given
			print json
			sys.exit(0)
			
	print "No such Country exists"
