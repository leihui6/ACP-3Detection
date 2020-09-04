# evaluate the trained result with standard label marked manually
# before running, please make sure
# 'trained_label' and 'standard_label' folder
# is existing in current work path

import numpy as np
import copy
import os
from interest_area import calculate_overlapping


def get_rotation_matrix_z(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.mat([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1.0, 0],
        [0, 0, 0, 1]
    ])


# return drawable_corners, rectangle_2d
# drawable_corners  : can be draw a 3D box directly
# rectangle_2d      : can be evaluated in plane of XOY
def read_from_label(res):
    # position, dimension, rotation
    x, y, z = 0, 0, 0
    dx, dy, dz = res[3] / 2, res[4] / 2, res[5] / 2
    corners = [
        [-dx, dy, -dz, 1],
        [-dx, -dy, -dz, 1],
        [dx, -dy, -dz, 1],
        [dx, dy, -dz, 1],
        [-dx, dy, dz, 1],
        [-dx, -dy, dz, 1],
        [dx, dy, dz, 1],
        [dx, -dy, dz, 1]
    ]
    # print(corners)
    corners = np.mat(corners).T

    # obtain rotation matrix
    m_r = get_rotation_matrix_z(res[6])
    # print(m_r)
    m_r[:, 3] = np.mat([res[0], res[1], res[2], 1]).reshape((4, 1))
    # print(m_r)

    # apply matrix
    corners_t = m_r * corners
    # print(corners_t.T)
    rectangle_2d = [res[1], res[0], dy * 2, dx * 2, np.rad2deg(res[6])]
    return corners_t.T, rectangle_2d


def position_dimension_rotation(KITTI_label):
    # position dimension rotation
    """
    the number in label order is different from trained label files
    label  8dz  9dx 10dy  11y 12z 13x
    x: [13]+0.27
    y: -[11]
    z: -[12]+[d8]/2
    dx: [9]
    dy: [10]
    dz: [8]
    """
    return [KITTI_label[13] + 0.27, -KITTI_label[11], -KITTI_label[12] + (KITTI_label[8] / 2),
            KITTI_label[9], KITTI_label[10], KITTI_label[8], -KITTI_label[14]]


def get_closest_one(p, res):
    min_dis = np.linalg.norm(p - np.array([res[0][0], res[0][1], res[0][2]]))
    tar_idx = 0
    for idx, item in enumerate(res):
        t_p = np.array([item[0], item[1], item[2]])
        dis = np.linalg.norm(p - t_p)
        if dis < min_dis:
            min_dis = dis
            tar_idx = idx
    return res[tar_idx]


def get_trained_data_list():
    folder_name = 'C:/Users/Lei Li/OneDrive/point cloud data/PMD_datasets/Socket_3Detection/to_KITTI_evaluation/for rough detection/evaluation_result/100/evaluation_250'
    trained_filename_list = [folder_name + '/' + filename for filename in os.listdir(folder_name)]
    train_data = []
    for filename in trained_filename_list:
        res = get_trained_data(filename)
        if res:
            train_data.append(res)
        else:
            train_data.append(res)
    return train_data


def get_standard_data_list():
    folder_name = 'standard_label'
    standard_filename_list = [folder_name + '/' + filename for filename in os.listdir(folder_name)]
    standard_data = []
    for filename in standard_filename_list:
        res = get_trained_data(filename)
        if res:
            standard_data.append(res)
    return standard_data


def get_trained_data(filename):
    with open(filename, 'r') as f:
        labels = []
        for label in f:
            label_number = [float(number) if number != 'Car' else number for number in label.strip().split(' ')]
            labels.append(label_number)
        return labels


def get_delta_between_two_labels(standard_label, trained_label):
    position_delta_x = np.fabs(standard_label[0] - trained_label[0])
    position_delta_y = np.fabs(standard_label[1] - trained_label[1])
    position_delta_z = np.fabs(standard_label[2] - trained_label[2])

    dimension_delta_x = np.fabs(standard_label[3] - trained_label[3])
    dimension_delta_y = np.fabs(standard_label[4] - trained_label[4])
    dimension_delta_z = np.fabs(standard_label[5] - trained_label[5])

    rotation_delta = np.fabs(standard_label[6] - trained_label[6])

    return [position_delta_x, position_delta_y, position_delta_z,
            dimension_delta_x, dimension_delta_y, dimension_delta_z,
            rotation_delta]


if __name__ == '__main__':
    # get filename list
    trained_data_list = get_trained_data_list()
    standard_data_list = get_standard_data_list()

    # print(trained_data_list)
    # print(standard_data_list)

    standard_volume = 0
    skip_count = 0
    sum_volume, volume_count = 0, 0
    for idx, item in enumerate(standard_data_list):
        # print('{}->{}'.format(len(item), len(trained_data_list[idx])))
        for specific_label in item:
            # print(specific_label)
            label = np.array(position_dimension_rotation(specific_label)).round(8)
            p = np.array([label[0], label[1], label[2]])

            # invalid data
            if len(trained_data_list[idx]) == 0:
                skip_count = skip_count + 1
                volume_count = volume_count + 1
                continue

            # in practice, there will be only one label in trained label file
            tar_label = np.array(get_closest_one(p, trained_data_list[idx])).round(8)
            # print('Now compare between\n', label, '\nand\n', tar_label)
            height = np.fabs(tar_label[5]) if np.fabs(label[5]) > np.fabs(tar_label[5]) else np.fabs(label[5])
            # print(label, tar_label)

            # standard data(marked manually)
            standard_draw_corners, standard_rectangle_2d \
                = read_from_label(label)
            # trained data
            detected_draw_corners, detected_rectangle_2d \
                = read_from_label(tar_label)
            # delta between every items
            delta_items = get_delta_between_two_labels(label, tar_label)

            # interest_area rect1_area rect2_area
            # print('Now compare between\n', standard_rectangle_2d, '\nand\n', detected_rectangle_2d)
            overlap = calculate_overlapping(standard_rectangle_2d, detected_rectangle_2d, False)
            sum_volume = sum_volume + overlap[0] * height
            volume_count = volume_count + 1
            # original volume is based on m^3
            print('[{:03n}]\toverlap_volume({} cm^3)\toverlap({} m^3)\theight({} m)'.format(idx, round(overlap[0] * height * 1e6, 6), round(overlap[0], 6), round(height, 6)))
    print('average volume:{} cm^3, skip count:{}'.format(np.fabs(sum_volume / volume_count * 1e6 - standard_volume), skip_count))
