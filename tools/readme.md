# TOOLS

## Convert point cloud in binary into ascii point cloud

point cloud in binary is caputred and saved by this [repo](https://github.com/Gltina/PMD_Camera), the way of writing to file(*.bin) is the same as KITTI.

``` python
python converter_bin2txt.py xxx.bin
 ```

## Convert coordinates to the coordinate system used by KITTI

This program will convert all files in `bin/` that contains many *.bin captured by [repo](https://github.com/Gltina/PMD_Camera). The default output folder is `'KITTI_'+$(input_folder)`, in this sample, the output folder is `KITTI_bin/`.

``` python
python converter_pc2KITTIpc.py --folder bin
```
> Note that `bin` is a folder instead of a specific file, and dont need to add `/`.
