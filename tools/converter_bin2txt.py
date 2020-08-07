# convert point cloud containing (x,y,z,intensity) represented by binary into *.txt

import numpy as np
import struct
import sys
import numpy

def convert_kitti_bin_to_pcd(ifile,ofile):
    size_float = 4
    # read from ifile
    list_points = []
    with open(ifile, "rb") as f:
        byte = f.read(size_float * 4)
        while byte:
            x, y, z, intensity = struct.unpack("ffff", byte)
            list_points.append([x, y, z, intensity])
            byte = f.read(size_float * 4)
    print("point size =",len(list_points))
    # write into ofile
    with open(ofile, 'w') as f:
        for points in list_points:
            for item in points:
                f.write(str(item)+' ')
            f.write('\n')

if __name__ == "__main__":
    if len(sys.argv) < 2: 
        print("please use: python converter.py [filename] like `python converter.py 000000.bin`\noutput file(*.txt) will be named after filename from input.")
        exit()
    bin_filename = sys.argv[1]
    txt_filename = bin_filename[:bin_filename.find('.')]+".txt"
    print("Reading:",bin_filename)
    print("Writing:",txt_filename)
    convert_kitti_bin_to_pcd(bin_filename,txt_filename)
    print("Finished")
