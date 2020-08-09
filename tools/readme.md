# Tools

> Note that for more details about description on scripts, please use `$(command) -h` to see.

## Convert point cloud in binary into ascii point cloud

Point cloud in binary is caputred and saved by this [repo](https://github.com/Gltina/PMD_Camera), the way of writing to file(*.bin) is the same as KITTI.

 `converter_bin2txt.py`

## Convert coordinates to the coordinate system used by KITTI

This program will convert all files in `bin/` that contains many *.bin captured by [repo](https://github.com/Gltina/PMD_Camera). The default output folder is `'KITTI_'+$(input_folder)`, in this sample, the output folder is `KITTI_bin/`.

`converter_pc2KITTIpc.py`

## Conver json file generated from web into label files

`converter_mylabel2KITTIlabel.py`
