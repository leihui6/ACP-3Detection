# convert point cloud captured using PMD camera into the format of KITTI, as followings:
# transform the coordinate

import copy
import argparse
import os
import struct
import numpy as np

arg = argparse.ArgumentParser("pc2KITTIpc")

transform_matrix = np.mat(np.array([
            [0, 0, 1, 5.0],
            [1, 0, 0, 0],
            [0, 1, 0, -0.817],
            [0, 0, 0, 1]]))


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


start_number = 97

if __name__ == "__main__":
    arg.add_argument("--folder", "-f", default="", type=str, help="folder containing many point cloud captured locally", required=True)
    args = arg.parse_args()

    input_folder = args.folder
    print('input folder:\t', input_folder)
    output_folder = "KITTI_"+input_folder

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    print('output folder:\t', output_folder)
    bin_list = [bin_file for bin_file in os.listdir(input_folder) if ".bin" in bin_file]
    print('detect %d files in %s/' % (len(bin_list), input_folder))

    print('transform matrix is:\n', transform_matrix)

    for idx, bin_file in enumerate(bin_list):
        pc = get_pc(input_folder+'/'+bin_file)
        pc_numpy = np.mat(np.array(pc)).T
        intensity = copy.deepcopy(pc_numpy[3:])
        pc_numpy[3:] = 1
        # print(pc_numpy.T)
        t_pc = transform_matrix*pc_numpy
        t_pc[3:] = intensity
        # print(t_pc.T)
        save_filename = output_folder+'/'+"{:06n}.bin".format(idx+start_number)
        with open(save_filename, "bw") as f:
            t_pc.T.astype(np.float32).tofile(f)
        print('write into {}({}/{})'.format(save_filename, idx+1, len(bin_list)))
