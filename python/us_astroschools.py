# geopy works much better than pygeocoder (~50% failure rate)
from geopy.geocoders import GoogleV3
geolocator = GoogleV3()

# Read in data (hand-coded from Dimitri Veras' map) - http://dimitriveras.com/mapUSChrome/

with open('data/us/us_astro_cities.csv','r') as f:
    cities = [l.strip() for l in f.readlines()]

# Geocode addresses to get lat,lon and write to file

with open('data/us/us_latlon.tsv','w') as f:
    f.write('1\t0\n')
    for c in cities:
        result = geolocator.geocode(c,region='us')
        if result is not None:
            f.write('%f\t%f\n' % (n,result.latitude,result.longitude))
        # Limit for Google API is 10 requests per second
        time.sleep(0.2)

    

