import numpy as np
from scipy.spatial.transform import Rotation as R
import struct
import math
import os
import argparse
import copy

arg = argparse.ArgumentParser("apply_URtransformation")

data_list_filename = 'data_list.txt'
transformation_list_filename = 'transformation_list.txt'


def get_rotate(theta):
    """
    Rotate `theta` degrees around axis `axis`
    """
    rotaion_vector = R.from_rotvec([
        [np.deg2rad(theta[0]), 0, 0],
        [0, np.deg2rad(theta[1]), 0],
        [0, 0, np.deg2rad(theta[2])]])
    rotation_matrix = rotaion_vector.as_rotvec()
    # print(type(rotation_matrix))

    rx, ry, rz = rotation_matrix[0][0], rotation_matrix[1][1], rotation_matrix[2][2]
    # print(rx, ry, rz)
    angle = math.sqrt(rx*rx + ry*ry + rz*rz)
    # print(angle)
    ux, uy, uz = rx/angle, ry/angle, rz/angle
    # print(ux, uy, uz)
    c, s = np.cos(angle), np.sin(angle)
    C = 1-c
    r_m = np.mat([
            [ux * ux * C + c,       ux * uy * C - uz * s,   ux * uz * C + uy * s, 0],
            [uy * ux * C + uz * s,  uy * uy * C + c,        uy * uz * C - ux * s, 0],
            [uz * ux * C - uy * s,  uz * uy * C + ux * s,   uz * uz * C + c, 0],
            [0, 0, 0, 1]
        ])
    return r_m


def get_translation(t_list):
    return np.mat([
        [1, 0, 0, t_list[0]/1000],
        [0, 1, 0, t_list[1]/1000],
        [0, 0, 1, t_list[2]/1000],
        [0, 0, 0, 1]
    ])


def get_data_list(filename):
    _data_list = []

    # load data from data_list to get filename
    files_list = []
    with open(filename, 'r') as f:
        for item in f:
            files_list.append(item.strip())

    # read file
    for i, item in enumerate(files_list):
        if ".bin" in item:
            pass
        elif ".pcd" in item:
            print('loading [{}] from {}'.format(i+1, item))
            point_cloud = []

            with open(item, 'r') as f:
                for line_count, p in enumerate(f):
                    # magic number of '.pcd'
                    if line_count > 10:
                        # print('item', p)
                        x, y, z, intensity = p.strip().split(' ')
                        point_cloud.append([x, y, z, intensity])
            _data_list.append(np.array(point_cloud).astype(float).round(8))
    return _data_list, files_list


def get_transformation(filename):
    _transformation_list = []

    # read data
    value_list = []
    with open(filename, 'r') as f:
        for item in f:
            v = [float(number) for number in item.strip().split(' ')]
            value_list.append(v)

    # obtain transformation
    # (value_list)
    for idx, item in enumerate(value_list):
        r = get_rotate(item[3:6])
        t = get_translation(item[0:3])
        # print(r, '\n', t)
        final_m = r
        final_m[:, 3] = t[:, 3]
        # print(final_m)
        _transformation_list.append(np.mat(final_m))

    return _transformation_list


if __name__ == '__main__':
    np.set_printoptions(suppress=True)

    print('input file: {}, {}'.format(data_list_filename, transformation_list_filename))
    print('output folder: {}, {}'.format('data', 'resdata'))

    data_list, files_list = get_data_list(data_list_filename)
    transformation_list = get_transformation(transformation_list_filename)

    if len(data_list) != len(transformation_list):
        print('size of data doesnt match the transformation')
        exit(-1)

    for idx, data in enumerate(data_list):
        print('[{}] applying ...\n{}'.format(idx+1, transformation_list[idx]))
        data = data.T
        intensity = copy.deepcopy(data[3:])
        data[3:] = 1
        transformed_data = transformation_list[idx] * data
        transformed_data[3:] = intensity
        saved_name = os.path.splitext(files_list[idx])[0].replace('data', 'resdata') + '_t.txt'
        np.savetxt(saved_name, transformed_data.T, fmt='%.8f')
        print('saving ', saved_name)