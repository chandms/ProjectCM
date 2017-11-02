
import kml2geojson
from shapely.geometry import Polygon
import json
import fiona

def mintolerance(pol1,pol2,l,u,x):
    m=(l+u)/2
    if(u-l<=x):
        return m
    polygon=pol2.buffer(m)
    pol=polygon.intersection(pol1)
    #print("buffered",polygon)
    #print("intersect",pol)
    if(pol1.equals(pol)):
        #print("yes")
        if(pol1.touches(polygon) or pol1.equals(polygon)):
            print("hey")
            return m
        return mintolerance(pol1,pol2,l,m,x)
    else:
        return mintolerance(pol1,pol2,m,u,x)


kml2geojson.main.convert('C:/Users/Pupul/Desktop/ma1.kml','C:/Users/Pupul/Desktop')
kml2geojson.main.convert('C:/Users/Pupul/Desktop/ma2.kml','C:/Users/Pupul/Desktop')
pol1=Polygon([(0,0),(0,1),(1,1),(0,0)])
pol2=Polygon([(0,0),(0,1),(1,1),(0,0)])
with open('C:/Users/Pupul/Desktop/ma1.geojson') as f:
    data=json.load(f)

    for f in data["features"]:
        print (f["geometry"]["type"])
        k=f["geometry"]["coordinates"]
        pol1=Polygon(k[0])
with open('C:/Users/Pupul/Desktop/ma2.geojson') as f:
    data=json.load(f)

    for f in data["features"]:
        print (f["geometry"]["type"])
        k=f["geometry"]["coordinates"]
        pol2=Polygon(k[0])
print(pol1)
area1=pol1.area
area2=pol2.area
print(pol2)
if(pol1.equals(pol2)):
    print("both geometries are equal")
else:
    print("have  difference")
print("area of given polygon",area1,area2)
pol=Polygon([(0,0),(0,1),(1,1),(0,0)])
if(pol1.intersects(pol2)):
    pol=pol1.intersection(pol2)
    print(pol)
    print ("intersected area",pol.area)
    print(pol.boundary)
else:
    print ("does not intersect")
polu=pol1.union(pol2)
print (polu)
print("union area",polu.area)

l=0
u=1000
x=0.5
d=mintolerance(pol1,pol2,l,u,x)
print ("min tolerance",d)
















