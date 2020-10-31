# convert point cloud captured using PMD camera into the format of KITTI, as followings:
# transform the coordinate

"""

The point cloud processed in this project are captured above a surface.
So, first we should do is to adjust the height of whole point cloud.

"""

import copy
import argparse
import os
import struct
import numpy as np

arg = argparse.ArgumentParser("pc2_KITTI_pc")

# Height info:
# kitti_camera : 1.73 m
# PMD_camera in this project: 0.796 m
# 1.73 - 0.305 = 1.425

# negative direction
# x + 7m
# transform_matrix = np.mat(np.array([
#    [0, 0, 1, 7],
#    [1, 0, 0, 0],
#    [0, 1, 0, -1.425],
#    [0, 0, 0, 1]]))

start_number = 0

# 2 positive direction
transform_matrix = np.mat(np.array([
    [0, 0, 1, 7],
    [-1, 0, 0, 0],
    [0, -1, 0, -1.425],
    [0, 0, 0, 1]]))

# need to amplified, 10x in paper
scale = 10
amplification_matrix = np.mat(np.array([
    [scale, 0, 0, -67.5],
    [0, scale, 0, 0.09],
    [0, 0, scale, 15.48],
    [0, 0, 0, 1]]))


def get_pc(filename):
    size_float = 4
    # read from filename
    list_points = []
    with open(filename, "rb") as f:
        byte = f.read(size_float * 4)
        # skip = False
        while byte:
            # if skip is True:
            #     byte = f.read(size_float * 4)
            #     skip = False
            #     continue
            x, y, z, intensity = struct.unpack("ffff", byte)
            list_points.append([x, y, z, intensity])
            byte = f.read(size_float * 4)
            # skip = True
    return list_points


if __name__ == "__main__":
    arg.add_argument("--folder", "-f", default="", type=str, help="folder containing many point cloud captured locally",
                     required=True)
    args = arg.parse_args()

    input_folder = args.folder
    print('input folder:\t', input_folder)
    output_folder = "KITTI_" + input_folder

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    print('output folder:\t', output_folder)
    bin_list = [bin_file for bin_file in os.listdir(input_folder) if ".bin" in bin_file]
    print('detect %d files in %s/' % (len(bin_list), input_folder))

    print('transform matrix is:\n', transform_matrix)

    for idx, bin_file in enumerate(bin_list):
        pc = get_pc(input_folder + '/' + bin_file)
        pc_numpy = np.mat(np.array(pc)).T
        intensity = copy.deepcopy(pc_numpy[3:])
        pc_numpy[3:] = 1
        # print(pc_numpy.T)
        t_pc = amplification_matrix * transform_matrix * pc_numpy
        t_pc[3:] = intensity
        # print(t_pc.T)
        save_filename = output_folder + '/' + "{:06n}.bin".format(idx + start_number)
        with open(save_filename, "bw") as f:
            t_pc.T.astype(np.float32).tofile(f)
        num_rows, num_cols = t_pc.shape
        print('[{}/{}]write into {}({})'.format(idx + 1, len(bin_list), save_filename, num_cols))
