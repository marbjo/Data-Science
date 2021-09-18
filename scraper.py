from urllib.request import urlopen
from bs4 import BeautifulSoup
#import numpy as np

def main():
    #Opening file for saving results, and writing headers
    filename = 'houses.csv'
    f = open(filename, 'w')
    headers = 'Adress, Area, Size (in m^2), Price (in NOK), Bedrooms \n'
    f.write(headers)

    n = 20 #Number of web pages to scrape

    counter = 0 #Test counter

    #Page numbers on Finn.no are numbered by & page = 1,2,3,4... &
    for i in range(1,n+1):
        
        #This reads only Oslo. If you want the whole of Norway, remove 'location=X.XXXXX', or change for another area.
        url_to_scrape = 'https://www.finn.no/realestate/homes/search.html?location=0.20061&page=' + str(i) + '&sort=PUBLISHED_DESC'

        #Opening url, reading and closing
        request_page = urlopen(url_to_scrape)
        page_html = request_page.read()
        request_page.close()

        #Parsing page with BeautifulSoup and finding all relevant divs (housing ads)
        html_soup = BeautifulSoup(page_html, 'html.parser')
        listings = html_soup.find_all('div', class_='ads__unit__content')

        #Looping over house listings

        for listing in listings:
            area = listing.find('div', class_='ads__unit__content__details').get_text()
            keys = listing.find('div', class_='ads__unit__content__keys') #.get_text()

            #Make sure only to get street address and area (county) 
            loc_string = area.split(',')
            address = loc_string[-2]
            area = loc_string[-1]

            #Loop over divs in same class = ads__unit__content__keys
            list = []
            for item in keys:
                list.append(item.get_text())

            try:
                sqm = list[0] #Size in square meters
                sqm = sqm.split('m')[0] #Remove m^2

                price = list[1] #Prize in NOK
                price = price.split('kr')[0] #Remove kr
            except:
                if len(sqm) < 2:
                    sqm = 'NaN'
                if ((len(price)) < 2) or (len(list) < 2):
                    price = 'NaN'
                print('Exception in page', i, ' for element', counter)

            bedrooms = listing.find('div', class_='u-float-left').get_text()
            if 'soverom' in bedrooms:
                start = bedrooms.find('soverom')
                #print('Found soverom')
                bedrooms = bedrooms[(start-2) : (start-1)]        
            else:
                bedrooms = 'NaN'

            #print(bedrooms[start:])

            f.write(address + ',' + area + ',' + sqm + ',' + price + ',' + bedrooms + '\n')

            counter += 1

        print('Done page number', i)

    f.close()

if __name__ == "__main__":
    main()
