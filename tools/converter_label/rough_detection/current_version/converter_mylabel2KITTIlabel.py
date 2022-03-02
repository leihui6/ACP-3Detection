import json
import copy
import argparse
import os
import collections
import numpy as np

arg = argparse.ArgumentParser("mylabel2KITTIlabel")

target_label = collections.OrderedDict()
target_label['type'] = 'Dontcare'
target_label['truncated'] = 0.0
target_label['occluded'] = 0  # used in image
target_label['alpha'] = 0
target_label['bbox'] = [1, 2, 3, 4]  # used in image
target_label['dimensions'] = []
target_label['location'] = []
target_label['rotation_y'] = 0
# target_label['score'] = 'Dontcare'

# the height of velodyne camera
camera_height = -1.73

transform_location = np.mat([
    [0, -1, 0],
    [0, 0, -1],
    [1, 0, 0],
])


def get_transformed_values(_list, m):
    r = m * np.mat(_list).T
    r = r.T
    return r.tolist()[0]


def get_dimensions(_list):
    x = _list[0]
    y = _list[1]
    z = _list[2]
    return list([z, x, y])


start_number = 0

if __name__ == '__main__':
    arg.add_argument("--input_folder", "-i", default="", type=str,
                     help="folder containing JSON file form https://3d.supervise.ly/projects", required=True)
    arg.add_argument("--output_folder", "-o", default="", type=str, help="output folder", required=True)
    args = arg.parse_args()

    input_filename = args.input_folder
    output_folder = args.output_folder
    print('input filename:\t', input_filename)
    print('output folder:\t', output_folder)

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    label_list = [json_file for json_file in os.listdir(input_filename) if ".json" in json_file]

    print(label_list)
    exit()
    for idx, data in enumerate(label_list):
        with open(input_filename + '\\' + data) as f:
            annotation = json.load(f)
        KITTI_annotations = []
        # my_annotations = annotations['figures']
        data_name = data
        print('reading {}'.format(data_name))

        # save current annotation into
        save_filename = "{:06n}.txt".format(idx + start_number)
        save_path = output_folder + '/' + save_filename
        print('saving {}'.format(save_path))
        f = open(save_path, 'w')
        # key -> name
        objects = {}
        for object_name in annotation['objects']:
            objects[object_name['key']] = "PrintingMachine"# object_name['classTitle']

        for label in annotation['figures']:
            # produce new annotations
            tmp_target_label = copy.deepcopy(target_label)
            tmp_target_label['type'] = objects[label['objectKey']]
            # print(list(annotation['geometry']['dimensions'].values()))
            tmp_target_label['dimensions'] = get_dimensions(
                list(label['geometry']['dimensions'].values()))
            # print('dimensions', tmp_target_label['dimensions'])
            position = list(label['geometry']['position'].values())
            position[2] = camera_height  # z
            position[0] = position[0] - 0.27  # x
            tmp_target_label['location'] = get_transformed_values(position, transform_location)
            # print('location', tmp_target_label['location'])
            tmp_target_label['rotation_y'] = -float(label['geometry']['rotation']["z"])
            KITTI_annotations.append(tmp_target_label)
            # exit()

            for item in KITTI_annotations:
                value_list = list(item.values())
                for value in value_list:
                    if isinstance(value, list):
                        for v in value:
                            f.write(str(round(v, 2)) + ' ')
                    else:
                        if isinstance(value, str):
                            f.write(value + ' ')
                        else:
                            f.write(str(round(value, 2)) + ' ')
                f.write('\n')
        f.close()