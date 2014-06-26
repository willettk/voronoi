# geopy works much better than pygeocoder (~50% failure rate)
from geopy.geocoders import GoogleV3
import time

# Read in data (hand-coded from Dimitri Veras' map) - http://dimitriveras.com/mapUSChrome/

with open('../data/us/us_astro_cities.csv','r') as f:
    cities = [l.strip() for l in f.readlines()]

# Geocode addresses to get lat,lon and write to file

geolocator = GoogleV3()

with open('../data/us/us_latlon.tsv','w') as f:
    f.write('1\t0\n')
    for c in cities:
        result = geolocator.geocode(c,region='us')
        if result is not None:
            # Check to make sure geocoding is accurate for the US
            for r in result.raw['address_components']:
                if r['types'][0] == 'country':
                    country = r['long_name']
                    if country is 'United States':
                        # Write acceptable rows to file
                        f.write('%f\t%f\n' % (result.latitude,result.longitude))
                    else:
                        print '%s in %s improperly geocoded for %s' % (n,a,country)
        # Limit for Google API is 10 requests per second
        time.sleep(0.2)

