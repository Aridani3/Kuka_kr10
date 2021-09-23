# Robot URDF
* Import the CAD of the Kuka kr10 from [grabcad](https://grabcad.com/library/kuka-kr-agilus-1).  
* Used MeshLab to clean the cad (e.g., deleting duplicate faces).  
* Creating the Unified Robotic Description Format (URDF) file using Solidworks' URDF exporter.  
* Followed several steps to get a URDF robot properly working in [Gazebo](http://gazebosim.org/tutorials?tut=ros_urdf).

# Prerequisites
* Tested on ROS NOETIC
* Required Packages:
```
sudo apt-get install ros-noetic-gazebo-ros-pkg    
sudo apt-get install ros-noetic-gazebo-ros-control
sudo apt-get install ros-noetic-moveit
```

# Installation
```
mkdir kuka_kr10
cd kuka_kr10
mkdir src
cd src
git clone https://github.com/Aridani3/Kuka_kr10.git
cd ..
catkin init
catkin build
source devel/setup.bash
```

# Moveit
Launch demo to use moveit with the kuka kr10 
```
roslaunch kr10_moveit demo.launch
```
<img src="https://github.com/Aridani3/Kuka_kr10/blob/main/media/moveit_demo.gif" />

# Moveit + Gazebo
Using ros_control package with Position controllers
```
roslaunch kr10_moveit gazebo.launch
roslaunch kr10_moveit start_moveit_connected_with_gz.launch 
```

<img src="https://github.com/Aridani3/Kuka_kr10/blob/main/media/moveit_gazebo.gif" />

# Artwork retrieval
## Spawn artwork to Gazebo simulation
If you executed the previous steps:
```
rosrun gazebo_ros spawn_model -file `rospack find kuka_kr10_urdf`/urdf/boxe.urdf -urdf -model boxe
```
Or starting from scratch execute the following:
```
roslaunch kr10_moveit gazebo.launch
roslaunch kr10_scan scan.launch
```
<img src="https://github.com/Aridani3/Kuka_kr10/blob/main/media/artwork_gazebo.png" height="300" width="300"/>

## Retrieve the artwork
Robots follwes a path passing by 4 predefine locations, saves pictures at each location to kr10_scan/images
We use then these images to stitch them and extract the artwork from background

Start scanner to take the four images

```
rosrun kr10_scan scan.py
```

<img src="https://github.com/Aridani3/Kuka_kr10/blob/main/media/scan.gif" />

Resulting on these four images:
<p align="center">
  <img src="https://github.com/Aridani3/Kuka_kr10/blob/main/kr10_scan/images/Image_0.jpg" height="200" width="200">
  <img src="https://github.com/Aridani3/Kuka_kr10/blob/main/kr10_scan/images/Image_1.jpg" height="200" width="200">
  <img src="https://github.com/Aridani3/Kuka_kr10/blob/main/kr10_scan/images/Image_2.jpg" height="200" width="200">
  <img src="https://github.com/Aridani3/Kuka_kr10/blob/main/kr10_scan/images/Image_3.jpg" height="200" width="200">
</p>

Running the following stitches the images and extract the artwork from background:

```
roscd kr10_scan/scripts/
python3 crop.py
```

Result:

<p align="center">
  <img src="https://github.com/Aridani3/Kuka_kr10/blob/main/kr10_scan/images/Box_result.jpg" height="300" width="323">
  <img src="https://github.com/Aridani3/Kuka_kr10/blob/main/kr10_scan/images/Result.jpg" height="300" width="183">
</p>
