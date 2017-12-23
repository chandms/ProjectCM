import xml.dom.minidom as  md
from xml.dom.minidom import Node
import logging
import json
from pymongo import MongoClient
import xml.etree.ElementTree as ET
from xmljson import BadgerFish
from collections import OrderedDict
from lxml.html import fromstring
import zipfile
from xml.dom import minidom
import xmltodict
import os, time
import configparser
from os.path import basename
from bson.json_util import dumps
from verb import LoggingErrorFilter


used_coord = list()
gm = 0
config = configparser.ConfigParser()
config.read("C:/Users/Pupul/Desktop/config.ini")
logger = logging.getLogger()
logging.basicConfig(filename=config.get("Section3", "path2"), filemode='w', level=logging.DEBUG,format=('%(asctime)s  -- %(message)s'), datefmt='-- %d/%m/%Y -- %I:%M:%S -- %p')
filter = LoggingErrorFilter()
logger.addFilter(filter)


def print_node(root):
    logging.info("Starting print_node", extra={"verbosity": 1})
    if root.childNodes:
        for node in root.childNodes:
            if node.nodeType == Node.ELEMENT_NODE:
                logging.info("Checking if the node is Element node?", extra={"verbosity": 1})
                print(node.tagName, "has value:", node.nodeValue, " ,and is child of:", node.parentNode.tagName)
                global gm
                if (gm == 1):
                    gm = 2
                if (node.hasAttributes()):
                    logging.info("Checking if the node has any attribute?", extra={"verbosity": 1})
                    print("has key :", node.attributes.keys())
                    for elem in node.attributes.values():
                        print("has id :", elem.firstChild.data)
                        if (elem.firstChild.data == config.get("Section4", "var")):
                            gm = 1
            if (node.nodeType == Node.TEXT_NODE):
                logging.info("Checking if the node is text node?", extra={"verbosity": 1})
                print(node.wholeText)
                if (gm == 2):
                    used_coord.append(node.wholeText)
                    gm = 0
            if (node.nodeType == 4):
                logging.info("Checking if the node contains CDATA", extra={"verbosity": 1})
                print(node.data.strip())
            print_node(node)


def kmz_to_kml(fname):
    try:
        zf = zipfile.ZipFile(fname,'r')
        logging.info("Reading the KMZ file", extra={"verbosity": 2})
        for fn in zf.namelist():
            if fn.endswith('.kml'):
                logging.info("Checking if the file ends with .kml", extra={"verbosity": 2})
                content = zf.read(fn)
                xmldoc = minidom.parseString(content)
                target_name = os.path.splitext(config.get('Section1', 'path2'))[0] + os.path.splitext(basename(fname))[0] + ".kml"
                out = open(target_name, 'w')
                logging.info("writing kml in specified file", extra={"verbosity": 2})
                out.writelines(xmldoc.toxml())
                out.close()
                return target_name
        logging.info("No kml file is there", extra={"verbosity": 2})
        print("no kml file")
        return ("no kml file")
    except Exception as e:
        print("Bad KMZ file")


path_to_watch = config.get("Section1", "path1")
before = dict()
while 1:
    time.sleep(2)
    logging.info("Monitoring starts in folderkmz", extra={"verbosity": 2})
    after = dict([(f, None) for f in os.listdir(path_to_watch)])
    added = [f for f in after if not f in before]
    removed = [f for f in before if not f in after]
    if added:
        print("Added: ", ", ".join(added))
        logging.info("New KMZ files are added", extra={"verbosity": 2})
        ll = len(added)
        for zk in range(ll):
            dir = config.get("Section1", "path1")
            fname = os.path.join(dir, added[zk])

            if(fname.endswith(".kmz")):
                logging.info("KMZ file is passed as argument to kmz_to_kml function", extra={"verbosity": 2})
                kmlfile = kmz_to_kml(fname)
                try:
                    zf = zipfile.ZipFile(fname, 'r')
                    logging.info("good KMZ file", extra={"verbosity": 2})
                    print("KMZ file is Good.")
                except Exception as e:
                    kmlfile="bad zip"
                if (kmlfile != "no kml file" and kmlfile!="bad zip"):
                    dom = md.parse(kmlfile)
                    root = dom.documentElement
                    logging.info("Obtained kml file is generically parsed", extra={"verbosity": 2})
                    print_node(root)
                    tree = ET.parse(kmlfile)
                    root1 = tree.getroot()
                    xmlstr = ET.tostring(root1, encoding='utf8', method='xml')
                    bf = BadgerFish(dict_type=OrderedDict)
                    bf_str = BadgerFish(xml_fromstring=False)
                    t_n = os.path.splitext(config.get("Section2", "path1"))[0] + os.path.splitext(basename(fname))[0] + ".geojson"
                    f_file = open(t_n, 'w')
                    logging.info("kml file is converted to geojson format1", extra={"verbosity": 2})
                    f_file.write(dumps(bf_str.data(fromstring(xmlstr))))
                    f_file.close()
                    o = xmltodict.parse(xmlstr)
                    t_s = os.path.splitext(config.get("Section2", "path2"))[0] + os.path.splitext(basename(fname))[
                        0] + ".geojson"
                    g_file = open(t_s, 'w')
                    rr = json.dumps(o)
                    logging.info("kml file is converted to geojson format2", extra={"verbosity": 2})
                    g_file.write(json.dumps(o, sort_keys=False, indent=4, separators=(',', ': ')))
                    g_file.close()
                    t_k = os.path.splitext(config.get("Section2", "path3"))[0] + os.path.splitext(basename(fname))[
                        0] + ".geojson"
                    h_file = open(t_k, 'w')
                    logging.info("kml file is converted to geojson format3", extra={"verbosity": 2})
                    h_file.write(dumps(rr))
                    h_file.close()
                    d_name = os.path.splitext(basename(fname))[0]
                    conn = MongoClient()
                    logging.info("Mongo Client is fetched", extra={"verbosity": 2})
                    db = conn.gis

                    result = db[d_name]
                    logging.info(d_name+" coleection is included in 'gis' db", extra={"verbosity": 2})
                    result.insert_one(o)
                    logging.info("id of the new collection is printed", extra={"verbosity": 2})
                    print(result.inserted_id)
            else:
                print("Not a KMZ Document ,so ignored")
                logging.info("NOT a KMZ Document ,so ignored", extra={"verbosity": 2})

    if removed:
        print("Removed: ", ", ".join(removed))
        logging.info("KMZ file is removed", extra={"verbosity": 2})
    else:
        logging.info("NO change in directory", extra={"verbosity": 2})
    before = after
