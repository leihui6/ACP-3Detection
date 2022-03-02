# Deep Learning on 3D Object Detection for Automatic Plug-in Charging Using a Mobile Manipulator

> Challenging of Automatic Plug-in Charging (APC) & Automatic Charging and Plug-in (ACP)

**This repository aims to introduce data prerequisites used in our project,** focusing on 3D detection on Charging Station and Socket/Plug, which is mainly based on [PV-RCNN](https://github.com/open-mmlab/OpenPCDet).

## 3D Detection Techniques

### Data Acquisition

In this project, all point cloud was retrieved by a [PMD Camera](https://pmdtec.com/picofamily/monstar/) with [development kits](https://github.com/Gltina/PMD_Camera).

### 3D Point Cloud Labeling Tools

There are many tools (online or off-line) providing labeling on a bunch of points, such as, [basicfinder](https://www.basicfinder.com/en/), [supervise](https://supervise.ly/lidar-3d-cloud/) and [3D BAT](https://github.com/walzimmer/3d-bat).
We are using an online tool, [supervise](https://supervise.ly/lidar-3d-cloud/) for labeling 3D point cloud as below.

<p align="center">
  <img width="460" height="300" src="./images/supervise.gif">
</p>

### Dataset

Inspired by [KITTI](http://www.cvlibs.net/datasets/kitti/), for detection of charging station and socket/plug, two datasets for training and a dataset for evaluation need to be established respectively. To keep the coordinate as same as [KITTI](http://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d), and other requirements that make sure point cloud data we acquired can be fed into the target deep network, [a set of tools](./tools) were developed.

Since *[PV-RCNN](https://openaccess.thecvf.com/content_CVPR_2020/html/Shi_PV-RCNN_Point-Voxel_Feature_Set_Abstraction_for_3D_Object_Detection_CVPR_2020_paper.html)* is a state-of-the-art deep network framework that has high-performance on many autonomous driving benchmarks, such as [KITTI](http://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d). We employ and practice this learning-based technique to do a challenging of **Automatic Charging and Plug-in(ACP)**. Moreover, Point Cloud, as the data-structure of input in our project, is the fundamental data source of 3D detection in *PV-RCNN*. PV-RCNN was implemented in [OpenPCDet](https://github.com/open-mmlab/OpenPCDet) and modified in [OpenPCDet](https://github.com/Gltina/OpenPCDet). We hope the challenging of ACP can be benefitted by Learning-based methods.

#### **Charging Station Dataset**

For training:

A [dataset of Charging Station](https://drive.google.com/drive/folders/1Mts3K7f51GTvJlAWqqSl5bIP3-BD1Ghh?usp=sharing), which consists of Training(number: *~1000*, size: *480MB*) and Evaluation (number: *~100*, size: *53MB*) data.

Download [model](https://drive.google.com/file/d/1ic44aMHJlTgST7QMamVc5XcpHJH8JR67/view?usp=sharing) (150 MB), trained with *~1000* dataset and *250* epochs.

Detection Result:

<p align="center">
  <img width="" height="200" src="./images/ChargingStationDetection.gif"> </br>  
</p>

#### **Socket/Plug Dataset**

For evaluation:

A [dataset of Socket/Plug](https://drive.google.com/drive/folders/1rzPJ6BZGA8h2TIgAkqdqAQC_bGNGD6z7?usp=sharing), which consists of Training(number: *~1000*, size: *254MB*) and Evaluation (number: *~100*, size: *48MB*) data.

Download [model](https://drive.google.com/file/d/1freumTO3oX19fejeWbiZZ-qFK2nn3fBN/view?usp=sharing) (150 MB), trained with *~1000* dataset and *250* epochs.

Detection Result:

<p align="center">
<img width="" height="200" src="./images/SocketPlugin.gif">
</p>

## 3D Construction and Pin Detection

Thanks to the **UR robot**, multiple acquisition poses could be obtained and integrated to rebuild a complete 3D environment. Followed by feature-based strategies to identify position and orientation of pin. For more details about this, please refer to these papers(click as below).

## Papers
If you found it is useful, please consider cite us:

```
@article{zhou2022learning,
  title={Learning-based object detection and localization for a mobile robot manipulator in SME production},
  author={Zhou, Zhengxue and Li, Leihui and F{\"u}rsterling, Alexander and Durocher, Hjalte Joshua and Mouridsen, Jesper and Zhang, Xuping},
  journal={Robotics and Computer-Integrated Manufacturing},
  volume={73},
  pages={102229},
  year={2022},
  publisher={Elsevier}
}

@inproceedings{zhou2021deep,
  title={Deep Learning on 3D Object Detection for Automatic Plug-in Charging Using a Mobile Manipulator},
  author={Zhou, Zhengxue and Li, Leihui and Wang, Riwei and Zhang, Xuping},
  booktitle={2021 IEEE International Conference on Robotics and Automation (ICRA)},
  pages={4148--4154},
  year={2021},
  organization={IEEE}
}
```




## Contribution

This project so far is maintained by @[Leihui Li](https://github.com/Gltina) and @[Zhengxue Zhou](https://github.com/Zhengxuez), please be free to contact us if you have any problems.
