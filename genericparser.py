import xml.dom.minidom as  md
from xml.dom.minidom import Node
from xml.dom.minidom import NamedNodeMap
from xml.dom.minidom import Attr
import csv

def print_node(root):
    if root.childNodes:
        for node in root.childNodes:
           if node.nodeType == Node.ELEMENT_NODE :
               print (node.tagName,"has value:", node.nodeValue," ,and is child of:", node.parentNode.tagName)
               if(node.hasAttributes()):
                   print("has attrib:",node.attributes.keys())
           if (node.nodeType == Node.TEXT_NODE):
               print(node.wholeText)
           print_node(node)

dom = md.parse("C:/Users/Pupul/Desktop/dd.kml")
root = dom.documentElement
print_node(root)

