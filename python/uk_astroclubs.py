from bs4 import BeautifulSoup
import requests
import time

# geopy works much better than pygeocoder (~50% failure rate)
from geopy.geocoders import GoogleV3
geolocator = GoogleV3()

root_url = 'http://www.astronomyclubs.co.uk/Clubs/Details.aspx?ClubId='
nums = [n + 1 for n in range(300)]

addresses = []
names = []

# Download the address field from webform at http://www.astronomyclubs.co.uk/Clubs/Counties.aspx

for n in nums:
    url = '%s%i' % (root_url,n)
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    p = soup.findAll('p')

    for pp in p:
        xlen = len(pp('strong'))
        if xlen > 0:
            if(pp('strong')[0].text) == 'Address: ':
                a = pp.text.split('Address: ')[-1]
                addresses.append(a)
                names.append(soup.find('h1').text)

# Geocode addresses to get lat,lon and write to file

results = []
uk_countries = ('United Kingdom','Guernsey','Jersey','Isle of Man')

with open('../data/uk/uk_latlon.csv','w') as f:
    # Header line
    f.write('name,latitude,longitude\n')
    for a,n in zip(addresses,names):
        result = geolocator.geocode(a,region='uk')
        if result is not None:
            # Check to make sure geocoding is accurate for the UK
            for r in result.raw['address_components']:
                if r['types'][0] == 'country':
                    country = r['long_name']
                    if country in uk_countries:
                        # Write acceptable rows to file
                        f.write('%s,%f,%f\n' % (n,result.latitude,result.longitude))
                    else:
                        print '%s in %s improperly geocoded for %s' % (n,a,country)
        # Limit for Google API is 10 requests per second
        time.sleep(0.2)

    
