# -*- coding: utf-8 -*-
"""
Created on Mon Nov 09 10:21:10 2015

@author: RLH
"""

import pandas as pd
import sys
import re
import fortranformat as ff

line_dat_file = sys.argv[1]
midship = sys.argv[2]

fin = open(line_dat_file,'r')
fout = open('tmp.grd','w')

nodes = {}
quads = []

node_format = ff.FortranRecordReader('(A1,A3,A2,I5,I4,I5,3F10.0)')
quad_format = ff.FortranRecordReader('(A1,A3,A2,A4,A5,I5,A60)')

lines = fin.readlines()
for line in lines:
    if re.match('^\s+\d\s+(\d+)\s+',line):
        coords = ()
        tmp = node_format.read(line)
        node_num = tmp[3]
        coords = (tmp[6],tmp[7],tmp[8])
        nodes[node_num] = coords
    elif re.match('^\s+\dQPPL',line):
        tmp_quads = ()
        tmp = quad_format.read(line)
        tmp = re.findall('\d+',tmp[6])
        tmp_quads = (tmp[1],tmp[2],tmp[3],tmp[4])
        quads.append(tmp_quads)
        #quads.append(tmp[1],tmp[2],tmp[3],tmp[4])
fin.close()

# Loop through element definitions and write to grd file
# Write infro
fout.write(line_dat_file + '\n')
fout.write('1.0   9.81' + '\n')
fout.write('0     0       ' + '\n')
fout.write(str(len(quads)) + '\n')

for quad in quads:
    for element in quad:
        vert = nodes[int(element)]
        x = vert[0] - float(midship)
        y = vert[1]
        z = vert[2]
        vert = (x,y,z)
        str1 = ''.join(str('{:^8.3f}'.format(e)) for e in vert)
        fout.write(str1 +'\n')

fout.close()