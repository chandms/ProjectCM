
import kml2geojson
from shapely.geometry import Polygon,Point,MultiPolygon
import json
import configparser
import fiona

config=configparser.ConfigParser()
config.read("C:/Users/Pupul/Desktop/config.ini")

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


kml2geojson.main.convert(config.get("Section6","path1"),config.get("Section7","path1"))
kml2geojson.main.convert(config.get("Section6","path3"),config.get("Section7","path1"))
kml2geojson.main.convert(config.get("Section6","path2"),config.get("Section7","path1"))
pol1=Polygon()
pol2=Polygon()
with open(config.get("Section8","path7")) as f:
    data=json.load(f)
    for f in data["features"]:
        x=f["geometry"]["type"]
        print ("yes1",f["geometry"]["type"])
        k=f["geometry"]["coordinates"]
        if(x=="Polygon"):
            polr = Polygon(k[0])
            pol1 = pol1.union(polr)
        elif(x=="Point"):
            polr=Point(k)
            pol1=pol1.union(polr)
        elif(x=="MultiPolygon"):
            for j in range(len(k)):
                polr=Polygon(k[j])
                pol1=pol1.union(polr)
with open(config.get("Section8","path9")) as f:
    data=json.load(f)
    for f in data["features"]:
        x=f["geometry"]["type"]
        print ("yes",f["geometry"]["type"])
        k = f["geometry"]["coordinates"]
        if (x == "Polygon"):
                polr = Polygon(k[0])
                pol2=pol2.union(polr)
        elif (x == "Point"):
            polr = Point(k)
            pol2 = pol2.union(polr)
        elif (x == "MultiPolygon"):
            for j in range(len(k)):
                polr = Polygon(k[j])
                pol2 = pol2.union(polr)
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
















