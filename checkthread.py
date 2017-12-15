import os
import time
import zipfile
import configparser
import logging
from verb import LoggingErrorFilter
import random
import threading

config=configparser.ConfigParser()
config.read("C:/Users/Pupul/Desktop/config.ini")
logger= logging.getLogger()
logging.basicConfig(filename=config.get("Section5","path2"),filemode='w',level=logging.DEBUG,format=('%(asctime)s%(message)s'),datefmt='%d/%m/%Y--%I:%M:%S--%p--')
filter = LoggingErrorFilter()
logger.addFilter(filter)
path_to_watch = config.get("Section5", "path1")
before = dict()
after= dict()

def monitor():
    global before,after
    while 1:
        logging.debug("Sleeping while monitoring ",extra={"verbosity": 1})
        time.sleep(random.randint(1,3))
        logging.debug("Monitoring starts in findkmz", extra={"verbosity": 1})
        after = dict([(f, None) for f in os.listdir(path_to_watch)])
        added = [f for f in after if not f in before]
        removed = [f for f in before if not f in after]
        if added:
            logging.debug("New KMZ files are added", extra={"verbosity": 1})
            ll = len(added)
            for zk in range(ll):
                print("Added: ",added[zk])

        else:
            logging.debug("No change to the folder", extra={"verbosity": 1})
        before=after


d=threading.Thread(name="monitor",target=monitor)


def kmltokmz():
    for files in os.listdir("C:/Users/Pupul/Desktop/check"):
        logging.debug("new .py file detected in check folder", extra={"verbosity": 1})
        logging.debug("sleeping in kmltokmz", extra={"verbosity": 1})
        time.sleep(random.randint(1,2))
        print (files)
        fname=(os.path.splitext(files))[0]
        newfold="C:/Users/Pupul/Desktop/find/"
        nextfold="C:/Users/Pupul/Desktop/findkmz/"
        newfile=newfold+fname+".kml"
        logging.debug("kml file is written into find folder", extra={"verbosity": 1})
        newf=open(newfile,"w")
        newkmz=nextfold+fname+".kmz"
        zf= zipfile.ZipFile(newkmz,'w')
        logging.debug("kmz file is written into findkmz folder", extra={"verbosity": 1})
        zf.write(newfile)
        zf.close()
t=threading.Thread(name="kmltokmz",target=kmltokmz)
d.start()
t.start()



