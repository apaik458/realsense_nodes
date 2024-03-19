# realsense_nodes

## Install
Clone repo
```bash
mkdir -p ~/catkin_ws/src && cd ~/catkin_ws/src
git clone https://github.com/apaik458/realsense_nodes.git
cd ~/catkin_ws && catkin_make
```
Install realsense-ros package
```bash
sudo apt-get install ros-noetic-realsense2-camera
```
Install Python dependencies
```bash
pip install -r requirements.txt
```

## Usage
Start realsense nodes
```bash
roslaunch realsense2_camera rs_camera.launch
```
Run repo package nodes
```bash
rosrun realsense_nodes realsense_nodes.py
```
