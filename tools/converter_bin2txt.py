# convert point cloud containing (x,y,z,intensity) represented by binary into *.txt

import struct
import argparse

arg = argparse.ArgumentParser("bin2txt")


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
    print("point size =", len(list_points))

    with open(ofile, 'w') as f:
        for points in list_points:
            for item in points:
                f.write(str(round(item, 8))+' ')
            f.write('\n')


if __name__ == "__main__":
    arg.add_argument("--input", "-i", default="", type=str, help="input *.bin file", required=True)
    args = arg.parse_args()

    bin_filename = args.input
    txt_filename = bin_filename[:bin_filename.find('.')]+".txt"

    print("Reading:", bin_filename)
    print("Writing:", txt_filename)
    convert_kitti_bin_to_pcd(bin_filename, txt_filename)
    print("Finished")
