
import zipfile

from xml.dom import minidom

def kmz_to_kml(fname):
    zf = zipfile.ZipFile(fname,'r')
    for fn in zf.namelist():
        if fn.endswith('.kml'):
            content = zf.read(fn)
            xmldoc = minidom.parseString(content)
            out_name = 'C:/Users/Pupul/Desktop/dd.kml'
            out = open(out_name,'w')
            out.writelines(xmldoc.toxml())
            out.close()
        else:
            print("no kml file")
if __name__ == "__main__":
    fname = r"C:/Users/Pupul/Desktop/dd.kmz"
    kmz_to_kml(fname)