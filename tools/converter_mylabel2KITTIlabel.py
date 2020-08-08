import json
import copy
import argparse
import collections

arg = argparse.ArgumentParser("mylabel2KITTIlabel")

target_label = collections.OrderedDict()
target_label['type'] = 'Dontcare'
target_label['truncated'] = 0.0
target_label['occluded'] = 0 # used in image
target_label['alpha'] = 0
target_label['bbox'] = [1, 2, 3, 4] # used in image
target_label['dimensions'] = []
target_label['location'] = []
target_label['rotation_y'] = 0
# target_label['score'] = 'Dontcare'

if __name__ == '__main__':
    arg.add_argument("--input", "-i", default="", type=str, help="input file obtained from https://3d.supervise.ly/projects")
    args = arg.parse_args()

    input_filename = args.input
    output_filename = input_filename[:input_filename.find('.')]+".txt"

    print('input filename:\t', input_filename)
    print('output filename:\t', output_filename)

    with open(input_filename) as f:
        data = json.load(f)

    my_annotations = data[0]['annotations']
    KITTI_annotations = []

    for annotation in my_annotations:
        tmp_target_label = copy.deepcopy(target_label)
        tmp_target_label['type'] = annotation['className']
        tmp_target_label['dimensions'] = list(annotation['geometry']['dimensions'].values())
        tmp_target_label['location'] = list(annotation['geometry']['position'].values())
        tmp_target_label['rotation_y'] = annotation['geometry']['rotation']["z"]
        KITTI_annotations.append(tmp_target_label)

    with open(output_filename, 'w') as f:
        for item in KITTI_annotations:
            value_list = list(item.values())
            for value in value_list:
                if isinstance(value, list):
                    for v in value:
                        f.write(str(round(v, 2))+' ')
                else:
                    if isinstance(value, str):
                        f.write(value+' ')
                    else:
                        f.write(str(round(value, 2)) + ' ')
            f.write('\n')
