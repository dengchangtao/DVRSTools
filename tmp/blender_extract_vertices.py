F:/PROJECT_BACKUP/SA (S2018) LNG Medium Term IPP/01_Data/DesignVessels/FSRU/177K

import bpy

fout = open('177K_Test.grd','w')


for item in bpy.data.objects:  
      
    print(item.name)  
    if item.type == 'MESH':  
        vert_list = [vertex.co for vertex in item.data.vertices]  
        for vert in vert_list:  
            str1 = ''.join(str('{:^8.3f}'.format(e)) for e in vert)
            fout.write(str1 +'\n')

fout.close()




import bpy

# http://blender.stackexchange.com/questions/2776/how-to-read-vertices-of-quad-faces-using-python-api


import bpy

fout = open('177K_half_Test.grd','w')


obj = bpy.data.objects['177K Rev01 Half Hull']
# obj = bpy.context.active_object

for f in obj.data.polygons:
    for idx in f.vertices:
        vert = obj.data.vertices[idx].co
        str1 = ''.join(str('{:^8.3f}'.format(e)) for e in vert)
        print (str1)
        fout.write(str1 +'\n')

fout.close()


fout = open('DebMar.xyz','w')


obj = bpy.data.objects['Test']
# obj = bpy.context.active_object

for f in obj.data.polygons:
    for idx in f.vertices:
        vert = obj.data.vertices[idx].co
        #str1 = ''.join(str('{:^8.3f}'.format(e)) for e in vert)
        str1 = '\t'.join(str(e) for e in vert)
        #print (str1)
        fout.write(str1 +'\n')

fout.close()

