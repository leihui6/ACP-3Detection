# evaluate the trained result with standard label marked manually
# before running, please make sure
# 'trained_label' and 'standard_label' folder
# is existed in current work path

import numpy as np
import copy
import os
import sys
from scipy.spatial import distance
from interest_area import calculate_overlapping

# required before use
label_list = \
    ['cutting']
#     ['PrintingMachine', 'Human']
#    ['Socket', 'Plug']

standard_volume = \
    {
#        'PrintingMachine': 0,
#        'Human': 0
        'cutting':0
        # 'Socket': 0,
        # 'Plug': 0
    }

trained_path = 'D:/DataSets/JEF/cutting_500_300_result/evaluation_'

log = open("log.txt", 'w')


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
    # print(KITTI_label)
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


def get_the_right_one(res_standard, res_trained):
    tar_item = None
    have_one = False
    for t_item in res_trained:
        if res_standard[0] == t_item[0]:
            tar_item = copy.deepcopy(t_item)
            tar_item.remove(tar_item[0])
            have_one = True
            break
    if have_one:
        return True, tar_item
    else:
        return False, res_trained[0]


def get_trained_data_list():
    folder_name = trained_path
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
        #if res:
        standard_data.append(res)
    return standard_data


def get_trained_data(filename):
    with open(filename, 'r') as f:
        labels = []
        for label in f:
            values = []
            for number in label.strip().split(' '):
                if number not in label_list:
                    values.append(float(number))
                else:
                    values.append(number)
            # print(values)
            # label_number = [float(number) if number != 'Socket' else number for number in label.strip().split(' ')]
            labels.append(values)
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


def get_delta_angle(angle_0, angle_1):
    return abs(angle_0 - angle_1)


def get_delta_distance(position_0, position_1):
    # print(position_0[0] - position_1[0],' ',position_0[1] - position_1[1],' ',position_0[2] - position_1[2])
    return distance.euclidean(position_0, position_1)


if __name__ == '__main__':
    trained_path = trained_path + str(sys.argv[1]) + '/'
    # get filename list
    trained_data_list = get_trained_data_list()
    standard_data_list = get_standard_data_list()

    print(len(trained_data_list))
    print(len(standard_data_list))

    skip_count = {key: 0 for key in label_list}
    sum_volume, volume_count = {key: 0 for key in label_list}, {key: 0 for key in label_list}

    delta_angle_list, delta_distance_list, delta_volume_list = [], [], []

    for idx, item in enumerate(standard_data_list):
        # print('{}->{}'.format(len(item), len(trained_data_list[idx])))
        # process invalid data
        # print(len(trained_data_list[idx]), len(standard_data_list[idx]))
        if len(trained_data_list[idx]) == 0:
            # print('len(trained_data_list[idx]) == 0')
            # skip_count[curr_label_name] = skip_count[curr_label_name] + 1
            # volume_count[curr_label_name] = volume_count[curr_label_name] + 1
            delta_volume_list.append(0)
            continue

        if not item:
            delta_volume_list.append(0)

        for specific_label in item:
            # print(specific_label)
            label = np.array(position_dimension_rotation(specific_label)).round(8)
            curr_label_name = specific_label[0]

            # in practice, there will be only one label in trained label file
            shot_result = get_the_right_one(specific_label, trained_data_list[idx])
            # print(shot_result)
            # process none label
            if shot_result[0] is False:
                print('No {} in {}_trained'.format(curr_label_name, idx))
                # skip_count[curr_label_name] = skip_count[curr_label_name] + 1
                # volume_count[curr_label_name] = volume_count[curr_label_name] + 1
                delta_volume_list.append(0)
                break

            tar_label = shot_result[1]
            tar_label = np.array(tar_label).round(8)
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
            delta_distance = get_delta_distance(
                (label[0], label[1], label[2]), (tar_label[0], tar_label[1], tar_label[2])
            )
            delta_angle = get_delta_angle(
                np.rad2deg(label[6]), np.rad2deg(tar_label[6])
            )

            # interest_area rect1_area rect2_area
            # print('Now compare between\n', standard_rectangle_2d, '\nand\n', detected_rectangle_2d)
            overlap = calculate_overlapping(standard_rectangle_2d, detected_rectangle_2d, False)
            sum_volume[curr_label_name] = sum_volume[curr_label_name] + overlap[0] * height
            volume_count[curr_label_name] = volume_count[curr_label_name] + 1
            # original volume is based on m^3
            # print('[{:03n}]\toverlap_volume({} cm^3)\toverlap({} m^3)\theight({} m)'.format(idx, round(overlap[0] * height * 1e6, 6), round(overlap[0], 6), round(height, 6)))

            # print current information
            # log.write("{}\t{}\t{}\n".format(overlap[0] * height*1e6, delta_distance, delta_angle))
            # print(overlap[0] * height)
            delta_volume_list.append(abs(overlap[0] * height))
            delta_distance_list.append(delta_distance)
            delta_angle_list.append(delta_angle)

    try:
        for l in label_list:
            print('[{}] average volume:{} cm^3, skip count:{}'.format(l, np.fabs(
                sum_volume[l] / volume_count[l] * 1e6 - standard_volume[l]), skip_count[l]))
    except ZeroDivisionError as e:
        pass

    print(len(delta_volume_list))
    output_file = open("result.txt", 'a+')
    for i in delta_volume_list:
        output_file.write(str(i) + ' ')
    output_file.write('\n')
    # output all delta information
    # for i in delta_volume_list:
    #     print(i, end=' ')
    # print('\n')
    # for i in delta_distance_list:
    #     print(i, end=' ')
    # print('\n')
    # for i in delta_angle_list:
    #     print(i, end=' ')
    # print('\n')

    log.close()
