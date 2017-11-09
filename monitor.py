import xml.dom.minidom as  md
from xml.dom.minidom import Node
from xml.dom.minidom import NamedNodeMap
from xml.dom.minidom import Attr
import csv
import pymongo
import json
from pymongo import MongoClient
import kml2geojson
from xmljson import badgerfish as bf
import xml.etree.ElementTree as ET
from xmljson import BadgerFish
from numpy import fromstring
import numpy as np
from json import dumps
from collections import OrderedDict
from lxml.html import tostring,fromstring
from xmljson import parker,Parker
import zipfile
from xml.dom import minidom
import xmltodict
import os, time
from os.path import basename

def print_node(root):
    if root.childNodes:
        for node in root.childNodes:
            if node.nodeType == Node.ELEMENT_NODE:
                print(node.tagName, "has value:", node.nodeValue, " ,and is child of:", node.parentNode.tagName)
                if (node.hasAttributes()):
                    print("has key :", node.attributes.keys())
                    for elem in node.attributes.values():
                        print("has id :", elem.firstChild.data)
            if (node.nodeType == Node.TEXT_NODE):
                print(node.wholeText)
            if (node.nodeType == 4):
                print(node.data.strip())
            print_node(node)

def kmz_to_kml(fname):
          zf = zipfile.ZipFile(fname, 'r')
          for fn in zf.namelist():
              if fn.endswith('.kml'):
                  content = zf.read(fn)
                  xmldoc = minidom.parseString(content)
                  print("bo",basename(fname))
                  #print(os.path.splitext(basename(fname))[0])
                  target_name = os.path.splitext('C:/Users/Pupul/Desktop/folderkml/')[0] +os.path.splitext(basename(fname))[0]+ ".kml"
                  #target_path = os.path.join('C:/Users/Pupul/Desktop', target_name)
                  #out_name = 'C:/Users/Pupul/Desktop/folderkml/dd.kml'
                  print(target_name)
                  out = open(target_name, 'w')
                  out.writelines(xmldoc.toxml())
                  out.close()
                  return target_name
              else:
                  print("no kml file")

path_to_watch = "C:/Users/Pupul/Desktop/folderkmz"
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
while 1:
  time.sleep (10)
  after = dict ([(f, None) for f in os.listdir (path_to_watch)])
  added = [f for f in after if not f in before]
  removed = [f for f in before if not f in after]
  if added:
      ll=len(added)
      for zk in range(ll):
          print ("Added: ", ", ".join (added))
          dir='C:/Users/Pupul/Desktop/folderkmz'
          fname=os.path.join(dir,added[zk])
          print(fname)
          kmlfile=kmz_to_kml(fname)
          dom = md.parse(kmlfile)
          root = dom.documentElement
          print_node(root)
          tree = ET.parse(kmlfile)
          root1 = tree.getroot()
          xmlstr = ET.tostring(root1, encoding='utf8', method='xml')
          bf = BadgerFish(dict_type=OrderedDict)
          bf_str = BadgerFish(xml_fromstring=False)
          t_n = os.path.splitext('C:/Users/Pupul/Desktop/geofold1/')[0] + os.path.splitext(basename(fname))[0] + ".geojson"
          print(t_n)
          f_file = open(t_n, 'w')
          f_file.write(dumps(bf_str.data(fromstring(xmlstr))))
          f_file.close()
          #print(dumps(bf_str.data(fromstring(xmlstr))))
          o = xmltodict.parse(xmlstr)
          t_s = os.path.splitext('C:/Users/Pupul/Desktop/geofold2/')[0] + os.path.splitext(basename(fname))[0] + ".geojson"
          print(t_s)
          g_file = open(t_s, 'w')
          rr = json.dumps(o)
          g_file.write(json.dumps(o, sort_keys=False, indent=4, separators=(',', ': ')))
          g_file.close()
          from bson.json_util import dumps

          t_k = os.path.splitext('C:/Users/Pupul/Desktop/geofold3/')[0] + os.path.splitext(basename(fname))[0] + ".geojson"
          print(t_k)
          h_file = open(t_k, 'w')
          h_file.write(dumps(rr))
          h_file.close()
          d_name=os.path.splitext(basename(fname))[0]
          conn=MongoClient()
          db = conn.newcook
          result=db[d_name]
          result.insert_one(o)
          print(result.inserted_id)
  if removed: print ("Removed: ", ", ".join (removed))
  before = after