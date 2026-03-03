# ROS 환경 정보
- OS : Ubuntu 20.04 (VMware)
- ROS Version : ROS noetic Desktop Full
- Workspace : '~/catkin_ws'

# ROS 설치과정
1. source list
```bash
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
```
2. Set up your keys
```bash
sudo apt install curl
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
```
3. Installation
```bash
sudo apt update
```
```bash
sudo apt install ros-noetic-desktop-full
```
4. Environment setup
```bash
source /opt/ros/noetic/setup.bash
```
```bash
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
source ~/.bashrc
```
5. Create a ROS Workspace
```bash
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/
catkin_make
```
```bash
source devel/setup.bash
```
```bash
echo $ROS_PACKAGE_PATH
```

# rosdep(의존성 도구 설치)
```bash
sudo apt install python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential
sudo rosdep init
rosdep update
```

# 설치 확인(Verification)
- ```rosversion -d``` (출력결과:```noetic```)