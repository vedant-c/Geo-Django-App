from django.contrib.gis.geoip2 import GeoIP2

def get_geo(ip):
    g= GeoIP2()
    country=g.country(ip)
    city=g.city(ip)
    lat,lon=g.lat_lon(ip)
    return country,city,lat,lon

def get_center_coordinates(latA,lonA,latB,lonB):
    coord=[(latA+latB)/2 , (lonA+lonB)/2]
    return coord

def get_zoom(distance):
    if distance<=300:
        return 8
    elif 100<distance<=1000:
        return 6
    else:
        return 4
