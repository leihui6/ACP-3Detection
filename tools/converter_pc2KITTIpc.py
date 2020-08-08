# convert point cloud captured using PMD camera into the format of KITTI, as followings:
# transform the coordinate

import sys
import argparse
import os
import struct
import numpy as np

arg = argparse.ArgumentParser("pc2KITTIpc")

transform_matrix = np.array([
            [0, 0, 1, 0],
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1]]).reshape(4, 4)


def get_pc(ifile):
    size_float = 4
    # read from ifile
    list_points = []
    with open(ifile, "rb") as f:
        byte = f.read(size_float * 4)
        while byte:
            x, y, z, intensity = struct.unpack("ffff", byte)
            list_points.append([x, y, z, intensity])
            byte = f.read(size_float * 4)
    return list_points


if __name__ == "__main__":
    arg.add_argument("--folder", "-f", default="", type=str, help="folder containing many point cloud captured locally")
    args = arg.parse_args()

    input_folder = args.folder
    print('input folder:\t', input_folder)
    outout_folder = "KITTI_"+input_folder

    if not os.path.exists(outout_folder):
        os.mkdir(outout_folder)

    print('output folder:\t', outout_folder)
    bin_list = [bin_file for bin_file in os.listdir(input_folder) if ".bin" in bin_file]
    print('detect %d files in %s/' %(len(bin_list), input_folder))

    for idx, bin_file in enumerate(bin_list):
        pc = get_pc(input_folder+'/'+bin_file)
        pc_numpy = np.array(pc)
        # print(pc_numpy.shape)
        # print("transform matrix is:\n", transform_matrix)
        pc_numpy = np.mat(pc_numpy).transpose()
        t_pc = transform_matrix*pc_numpy
        t_pc = np.mat(t_pc).transpose()
        save_filename = outout_folder+'/'+bin_file[:bin_file.find('.')] + "_KITTI.bin"
        fh = open(save_filename, "bw")
        t_pc.astype(np.float32).tofile(fh)
        print('write into %s(%d/%d)'% (save_filename, idx+1, len(bin_list)))
