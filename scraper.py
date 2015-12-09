
import scraperwiki
from lxml import html
import lxml
from datetime import datetime
import csv
import urllib
import re
import string

extractedOn = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
dictReader = csv.DictReader(open('suburbs.csv', 'rb'))
errorValue=''

def getNextLink(root):

    try:
       return "http://www.realestate.com.au" + root.cssselect('li[class=nextLink] a[href]')[0].get('href') 
    
    except:
       return ''      


def getStartURL(suburb, postcode):
    return "http://www.realestate.com.au/rent/with-2-bedrooms-in-"+ re.sub(" ","+",suburb) +"%2c+vic+" + postcode + "%3b/list-1?includeSurrounding=false"

def parseHouse(houseEl, suburb):
        #get the address
        try:
            h_address = houseEl.cssselect('a[class=name]')[0].text
        except:
            h_address = errorValue

        #print 'address: ' + h_address

        try:
            features=houseEl.cssselect('dl[class^=rui-property-features] dd')

            h_bedrooms = features[0].text
            h_bathrooms = features[1].text
            h_carparks = features[2].text


        except:
            h_bedrooms = errorValue
            h_bathrooms = errorValue
            h_carparks = errorValue


        try:
            h_price = houseEl.cssselect('p[class=priceText]')[0].text

        except:
            h_price = errorValue

        try:
            h_salesType = houseEl.cssselect('div[class="propertyStats"] p[class=type]')[0].text

        except:
            h_salesType = errorValue

        # Save found data
        #scraperwiki.sqlite.save(unique_keys=['extracted_on','address'], data={
        #    "extracted_on": extractedOn,
        #    "suburb": suburb,
	#    "address": h_address,
        #    "bedrooms": h_bedrooms,
        #    "bathrooms": h_bathrooms,
        #    "carparks": h_carparks,
        #    "sales_type": h_salesType,
        #    "price_text": h_price
        #    })
        print h_address
        print h_bedrooms
        print h_bathrooms
        print h_price
        print h_salesType
        print '----------------------------------------------------'


def parse(url, suburb):

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    #iterate through houses
    for houseEl in root.cssselect('article[class^=resultBody]'):
        
        try:
            parseHouse(houseEl, suburb)
        except:
            print 'Error: Cannot parse house!'


    nextLink = getNextLink(root)

    if nextLink == '':
        print suburb + ' parsed'
    else:
        parse(nextLink, suburb)

parse(getStartURL('cheltenham', '3030'))

#for line in dictReader:
#    print 'Scraping ' + line["Suburb"]  	
#    parse(getStartURL(
#       suburb=line["Suburb"],
#       postcode=line["PostCode"]), line["Suburb"])

