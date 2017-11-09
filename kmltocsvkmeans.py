
import csv
from itertools import groupby
from xml.etree import ElementTree as ET
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import zipfile
from xml.dom import minidom

zf = zipfile.ZipFile(r"C:/Users/Pupul/Desktop/kmz/world.kmz",'r')
for fn in zf.namelist():
    if fn.endswith('.kml'):
        content = zf.read(fn)
        xmldoc = minidom.parseString(content)
        out_name = 'C:/Users/Pupul/Desktop/kmz/world.kml'
        out = open(out_name,'w')
        out.writelines(xmldoc.toxml())
        out.close()
    else:
        print("no kml file")
tree= ET.parse('C:/Users/Pupul/Desktop/kmz/world.kml')
root= tree.getroot()
print (root)
with open("C:/Users/Pupul/Desktop/kmz/world.csv","w",newline='') as f_file,open("C:/Users/Pupul/Desktop/kmz/worldnn.csv", "w",newline='') as fp_out,open("C:/Users/Pupul/Desktop/kmz/world.csv","r") as re_file:
    csvwr = csv.writer(f_file)
    r=[]
    c=0
    d=0
    n=0
    g=0
    h=0
    for i in root.findall('{http://earth.google.com/kml/2.1}Document'):
        vv=[]
        if n==0:
            r.append("NAME")
            n=n+1
        name=i.find('{http://earth.google.com/kml/2.1}name').text
        vv.append(name)
        ff=[]
        ii=1
        for m in i.findall('{http://earth.google.com/kml/2.1}Style'):
            if g==0:
                r.append("STYLE ID")
                r.append("color")
                r.append("scale")
                r.append("href")
                r.append("labcolor")
                g=g+1
                ii=ii+1
            if g==1:
                ff.append(m.get('id'))
                color=(m.find('{http://earth.google.com/kml/2.1}IconStyle')).find('{http://earth.google.com/kml/2.1}color').text
                ff.append(color)
                x=(m.find('{http://earth.google.com/kml/2.1}IconStyle')).find('{http://earth.google.com/kml/2.1}scale')
                if x is None:
                    ff.append(" ")
                else:
                    scale=x.text
                    ff.append(scale)
                href=((m.find('{http://earth.google.com/kml/2.1}IconStyle')).find('{http://earth.google.com/kml/2.1}Icon').find('{http://earth.google.com/kml/2.1}href')).text
                ff.append(href)
                labcolor=(m.find('{http://earth.google.com/kml/2.1}LabelStyle')).find('{http://earth.google.com/kml/2.1}color').text
                ff.append(labcolor)
                g=0
        mm=[]
        for o in i.findall('{http://earth.google.com/kml/2.1}StyleMap'):
            if h==0:
                r.append("key1")
                r.append("styleUrl1")
                r.append("key2")
                r.append("styleUrl2")
                h=h+1
            if h==1:
                k1=(o.find('{http://earth.google.com/kml/2.1}Pair')).find('{http://earth.google.com/kml/2.1}key').text
                s1=(o.find('{http://earth.google.com/kml/2.1}Pair')).find('{http://earth.google.com/kml/2.1}styleUrl').text
                k2=(o.find('{http://earth.google.com/kml/2.1}Pair')).find('{http://earth.google.com/kml/2.1}key').text
                s2=(o.find('{http://earth.google.com/kml/2.1}Pair')).find('{http://earth.google.com/kml/2.1}styleUrl').text
                mm.append(k1)
                mm.append(s1)
                mm.append(k2)
                mm.append(s2)
                h=0
        for k in i.findall('{http://earth.google.com/kml/2.1}Folder'):
            dd=[]
            if d==0:
                r.append("name")
                r.append("open")
                r.append("description")
                d=d+1
            name=k.find('{http://earth.google.com/kml/2.1}name').text
            dd.append(name)
            open=k.find('{http://earth.google.com/kml/2.1}open').text
            dd.append(open)
            des=k.find('{http://earth.google.com/kml/2.1}description').text
            dd.append(des)
            for j in k.findall('{http://earth.google.com/kml/2.1}Placemark'):
                cc=[]
                if c==0:
                    r.append("place-name")
                    r.append("place-description")
                    r.append("lon")
                    r.append("lat")
                    r.append("alt")
                    r.append("ran")
                    r.append("tilt")
                    r.append("head")
                    r.append("styleUrl")
                    r.append("co-ordinate")
                    csvwr.writerow(r)
                    c=c+1
                name2=j[0].text
                cc.append(name2)
                des2=j[1].text
                cc.append(des2)
                lon=j[2][0].text
                lat=j[2][1].text
                alt=j[2][2].text
                ran=j[2][3].text
                tilt=j[2][4].text
                head=j[2][5].text
                stu=j[3].text
                coor=j[4][0].text
                cc.append(lon)
                cc.append(lat)
                cc.append(alt)
                cc.append(ran)
                cc.append(tilt)
                cc.append(head)
                cc.append(stu)
                cc.append(coor)
                ee=[]
                ee.extend(vv)
                ee.extend(ff)
                ee.extend(mm)
                ee.extend(dd)
                ee.extend(cc)
                csvwr.writerow(ee)
    f_file.close()
    reader = csv.reader(re_file)
    writer = csv.writer(fp_out)
    ls=[]
    for j in reader:
        ls.append(j)
    v=[]
    for key, group in groupby(ls,lambda x: x[0]):
        if (key=="NAME"):
            rows=list(group)
            lt=""
            for i in range(len(rows[0])):
                lt="".join(rows[0][i])
                v.append(lt)
            writer.writerow(v)
            v=[]
        else:
            rows=list(group)
            lt=""
            for i in range(130):
                lt="".join(rows[0][i])
                v.append(lt)
            j=130
            while(j<140):
                i=0
                d=[]
                while(i<9):
                    lt="".join(rows[i][j])
                    d.append(lt)
                    i=i+1
                v.append(d)
                j=j+1
            writer.writerow(v)
re_file.close()
fp_out.close()



df=pd.read_csv('C:/Users/Pupul/Desktop/kmz/world.csv',dtype={'lon': np.float64,'lat':np.float64})

f1=df['lon'].values
f2=df['lat'].values

X=np.matrix(list(zip(f1,f2)))
print (X)
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=2).fit(X)

print ("labels:")
print (kmeans.labels_)



print ("cluster center")
print (kmeans.cluster_centers_)

sns.lmplot('lon','lat',data=df)
plt.title("lon vs lat")
plt.xlabel("lon")
plt.ylabel("lat")
fname='C:/Users/Pupul/Desktop/kmz/ff.pdf'
plt.savefig(fname)


















