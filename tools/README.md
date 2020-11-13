# Tools

> Note that for more details on scripts, please use `$(command) -h` to see directly.

## Convert point cloud in binary into ascii point cloud

Point cloud in binary is caputred and saved by this [repo](https://github.com/Gltina/PMD_Camera), the way of writing to file(*.bin) is the same as KITTI.

 `converter_bin2txt.py`

## Convert coordinates to the coordinate system used by KITTI

This program will convert all files in a `$(input_folder)` contains many *.bin captured by [repo](https://github.com/Gltina/PMD_Camera). The default output folder is `'KITTI_'+$(input_folder)`.

`converter_pc2KITTIpc.py`

## Convert json file generated from [supervise]("https://3d.supervise.ly/projects/) into label files

`converter_mylabel2KITTIlabel.py` 

``` python
usage: mylabel2KITTIlabel [-h] --input INPUT --output_folder OUTPUT_FOLDER
mylabel2KITTIlabel: error: the following arguments are required: --input/-i, --output_folder/-o

# sample
python converter_mylabel2KITTIlabel.py -i rough_detection.json -o KITTI_label_rough
```
