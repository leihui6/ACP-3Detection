# Tools

> Note that for more details on scripts, please use `$(command) -h` to see directly.

## Convert point cloud in binary into ascii point cloud

Point cloud in binary is caputred and saved by this [repo](https://github.com/Gltina/PMD_Camera), the way of writing to file(*.bin) is the same as KITTI.

 `converter_bin2txt.py`

## Convert coordinates to the coordinate system used by KITTI

This program will convert all files in a `$(input_folder)` contains many *.bin captured by [repo](https://github.com/Gltina/PMD_Camera). The default output folder is `'KITTI_'+$(input_folder)`.

`converter_pc2KITTIpc.py`

## Convert json file generated from **supervise** into label files

### Older Version ([SUPERVISE](https://3d.supervise.ly/projects), which will be closed on *Nov 30*)

`converter_mylabel2KITTIlabel.py` 

``` python
usage: mylabel2KITTIlabel [-h] --input INPUT --output_folder OUTPUT_FOLDER
mylabel2KITTIlabel: error: the following arguments are required: --input/-i, --output_folder/-o

# sample
python converter_mylabel2KITTIlabel.py -i rough_detection.json -o KITTI_label_rough
```

### Current Version ([*New version - SUPERVISE*](https://app.supervise.ly/projects/))

``` shell
usage: mylabel2KITTIlabel [-h] --input_folder INPUT_FOLDER --output_folder
                          OUTPUT_FOLDER

optional arguments:
  -h, --help            show this help message and exit
  --input_folder INPUT_FOLDER, -i INPUT_FOLDER
                        folder containing JSON file form
                        https://3d.supervise.ly/projects
  --output_folder OUTPUT_FOLDER, -o OUTPUT_FOLDER
                        output folder
```

