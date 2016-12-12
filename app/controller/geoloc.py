import urllib2
import json

def geoloc():
    f = urllib2.urlopen('http://freegeoip.net/json/')
    json_string = f.read()
    f.close()
    location = json.loads(json_string)

    arra=[]
    location_city = location['city']
    location_state = location['region_name']
    location_country = str(location['country_name'])
    time_zone = str(location['time_zone'])
    arra= time_zone,location_country
    return arra
