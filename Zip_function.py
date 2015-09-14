#-*- coding=gbk -*-
import os,zipfile
from os.path import join

def zip_folder( foldername, filename):
    zip = zipfile.ZipFile( filename, 'w', zipfile.ZIP_DEFLATED )
    for root,dirs,files in os.walk(foldername):
        #files of cur file
        for filename in files:
            print "compressing",join(root,filename).encode("gbk")
            zip.write(join(root,filename).encode("gbk"))

        # empty dir 
        if  len(files) == 0:
            print 'empty dir'
            zif=zipfile.ZipInfo((root+'/').encode("gbk"+"/"))
            zip.writestr(zif,"")
    zip.close()
    print "Finish compressing"


if __name__ == "__main__":
    folder = 'E:\\git_factest2\\Report\\oldtest\\'
    filename = 'E:\\git_factest2\\test.zip'
    zip_folder( folder, filename )
