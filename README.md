# Prerequisites
* Tested on ROS NOETIC
* Required Packages:
```
sudo apt-get install ros-kinetic-gazebo-ros-pkg    
sudo apt-get install ros-kinetic-gazebo-ros-control
sudo apt-get install ros-kinetic-moveit
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

# Moveit + Gazebo
Using ros_control package with Position controllers
```
roslaunch kr10_moveit gazebo.launch
roslaunch kr10_moveit start_moveit_connected_with_gz.launch 
```

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

## Retrieve the artwork
Robots follwes a path passing by 4 predefine locations, saves pictures at each location to kr10_scan/images
We use then these images to stitch them and extract the artwork from background

Start scanner to take the four images
```
rosrun kr10_scan scan.py
```

```
roscd kr10_scan/scripts/
python3 crop.py
```
![alt text](https://github.com/Aridani3/Kuka_kr10/kr10_scan/images/Result.jpg?raw=true)


