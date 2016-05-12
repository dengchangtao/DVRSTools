import os 
import sys
import ConfigParser

root_dir = "/Users/rhydarharris/Desktop/bluewhale1444982483400/Tutorial1_2016/Tutorial1_2016/DVRS"
xml_file = "DVRS_Tutorial1.dvrsf"

xml_file = root_dir + "/" + xml_file
ini_file = root_dir + "/130m8knts/130m8knts.dvref"

import xml.etree.ElementTree as ET



tree = ET.parse(xml_file)
root = tree.getroot()

# Top-level elements
root.findall(".")

# All 'neighbor' grand-children of 'country' children of the top-level
# elements
#root.findall("./country/neighbor")

# Nodes with name='Singapore' that have a 'year' child
#root.findall(".//year/..[@name='Singapore']")

# 'year' nodes that are children of nodes with name='Singapore'
#root.findall(".//*[@name='Singapore']/year")

# All 'neighbor' nodes that are the second child of their parent
#root.findall(".//neighbor[2]")
print tree

# Elements
# for lines in root.findall('./Lines/XmlLine/.'):
#... 	lines.find('Name').text

