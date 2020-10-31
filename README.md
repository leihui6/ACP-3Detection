- [](#)
  - [3D Detection Techniques](#3d-detection-techniques)
    - [Data Acquisition](#data-acquisition)
    - [3D Point Cloud Labeling Tools](#3d-point-cloud-labeling-tools)
    - [Dataset](#dataset)
      - [**Charging Station Dataset**](#charging-station-dataset)
      - [**Socket/Plug dataset**](#socketplug-dataset)
  - [3D construction and Pin detection](#3d-construction-and-pin-detection)
  - [Contribution](#contribution)
  - [Thanks](#thanks)
---

# loading

> Challenging of Automatic Charging and Plug-in (ACP)

This repository mainly aims to introduce data prerequisites used in our project.

## 3D Detection Techniques

### Data Acquisition

In this project, all point cloud was retrieved by [PMD Camera](https://pmdtec.com/picofamily/monstar/) with [development kits](https://github.com/Gltina/PMD_Camera).

### 3D Point Cloud Labeling Tools

There are many tools (online or off-line) providing labeling on a bunch of points, such as: [basicfinder](https://www.basicfinder.com/en/), [supervise](https://supervise.ly/lidar-3d-cloud/) and [3D BAT](https://github.com/walzimmer/3d-bat).
We are using an online tool, [supervise](https://supervise.ly/lidar-3d-cloud/) for labeling 3D point cloud.

![supervise](./images/supervise.gif)

Check [here](https://supervise.ly/lidar-3d-cloud) to know more detail about SUPERVISE.

### Dataset

For detection of charging station and socket/plug, two datasets for training and a dataset for evaluation need to be formed respectively. To keep the coordinate as same as [KITTI](http://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d), and other requirements that make sure point cloud data we acquired can be fed into the target deep network, [a set of tools](./tools) were developed.

Since *PV-RCNN* is a state-of-the-art deep network framework that has high-performance on many autonomous driving benchmarks, such as KITTI. We employ and practice this learning-based technique to do a challenging of **Automatic Charging and Plug-in(ACP)**. Moreover, Point Cloud, as the data-structure of input in our project, is the fundamental data source of 3D detection in *PV-RCNN*. It was implemented in [OpenPCDet](https://github.com/open-mmlab/OpenPCDet) and modified in [OpenPCDet](https://github.com/Gltina/OpenPCDet). We hope the challenging of ACP can be benefitted by Learning-based methods.

#### **Charging Station Dataset**

For training:

A [dataset of Charging Station](https://drive.google.com/drive/folders/1Mts3K7f51GTvJlAWqqSl5bIP3-BD1Ghh?usp=sharing), which consists of Training(number: *~1000*, size: *480MB*) and Evaluation (number: *~100*, size: *53MB*) data.

#### **Socket/Plug dataset**

For evaluation:

A [dataset of Socket/Plug](https://drive.google.com/drive/folders/1rzPJ6BZGA8h2TIgAkqdqAQC_bGNGD6z7?usp=sharing), which consists of Training(number: *~1000*, size: *254MB*) and Evaluation (number: *~100*, size: *48MB*) data.

## 3D construction and Pin detection

Thanks to the UR robot, multiple data acquisition poses could be obtained and integrated to rebuild a complete 3D environment. Followed by feature-based strategies to identify position and orientation of pin. For more details about this, please refer to this paper.

## Contribution

This project so far is maintained by @[Leihui Li](https://github.com/Gltina) and @[Zhengxue Zhou](mailto:zhouzx@eng.au.dk), please be free to contact us if you have any problems.

## Thanks

Aarhus univeristy, Denmark

Tianjin Unversity of Technology, China
