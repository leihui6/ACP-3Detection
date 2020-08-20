import numpy as np
from scipy.spatial.transform import Rotation as R
import struct
import argparse

arg = argparse.ArgumentParser("apply_URtransformation")

data_list_filename = 'data_list.txt'
transformation_list_filename = 'transformation_list.txt'


def get_rotate(theta, axis):
    """
    Rotate `theta` degrees around axis `axis`
    """
    c, s = np.cos(np.deg2rad(theta)), np.sin(np.deg2rad(theta))
    if axis == 'x':
        return np.mat([
            [1., 0, 0],
            [0, c, -s],
            [0, s, c]
        ])
    elif axis == 'y':
        return np.mat([
            [c, 0, -s],
            [0, 1, 0],
            [s, 0, c]
        ])
    elif axis == 'z':
        return np.mat([
            [c, -s, 0],
            [s, c, 0],
            [0, 0, 1.],
        ])


def get_data_list(filename):
    _data_list = []

    # load data from data_list to get filename
    values_list = []
    with open(filename, 'r') as f:
        for item in f:
            values_list.append(item.strip())

    # read file
    for i, item in enumerate(values_list):
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
            print('done')
    return _data_list


def get_transformation(filename):
    _transformation_list = []

    value_list = []
    with open(filename, 'r') as f:
        for item in f:
            value_list.append(item.strip())
    np.set_printoptions(suppress=True)
    '''
    test_0 = get_rotate(-2.85, 'x')
    test_1 = get_rotate(90.03, 'y')
    test1 = get_rotate(2.85, 'x')
    test2 = get_rotate(-90.03, 'y')
    test3 = get_rotate(2.85, 'z')
    print(test1 * (test2 * test3))
    print(test_0 * test_1 * test3 * (test2 * test1))
    # print(test1, '\n', test2)
    '''
    return _transformation_list


if __name__ == '__main__':
    data_list = get_data_list(data_list_filename)

    transformation_list = get_transformation(transformation_list_filename)

    print(data_list, transformation_list)

    np.savetxt('resdata/' + 'test.out', data_list[0], fmt='%.8f')
