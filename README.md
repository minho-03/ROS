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

## 과제 2: /turtle1/pose 관찰 및 필드 분석

`rostopic echo /turtle1/pose` 명령어를 통해 거북이의 실시간 상태를 확인

- **x**: 거북이의 가로 위치. 오른쪽으로 갈수록 값이 커진다. (0 ~ 11.0 사이)
- **y**: 거북이의 세로 위치. 위쪽으로 갈수록 값이 커진다. (0 ~ 11.0 사이)
- **theta**: 거북이가 바라보는 방향 (라디안 단위). 
  - 0은 오른쪽, $\pi/2$(약 1.57)는 위쪽, $\pi$(약 3.14)는 왼쪽을 의미한다.
- **linear_velocity**: 거북이의 현재 전진/후진 속도. (방향키 위/아래 입력 시 변함)
- **angular_velocity**: 거북이의 현재 회전 속도. (방향키 좌/우 입력 시 변함)

### /turtle1/pose 데이터 특징
1. **좌표계 범위**: 원점(0,0)은 왼쪽 하단이며, 전체 맵은 약 11.0 x 11.0의 크기를 가짐을 확인.
2. **방향(theta) 데이터**: 
- 단위는 라디안(radian)을 사용함.
- 반시계 방향으로 회전 시 값이 증가함.
3. **업데이트 주기**: 거북이가 이동하지 않는 정지 상태에서도 약 60Hz(초당 60번)의 주기로 위치 데이터가 계속해서 발행(publish)됨을 확인.

## 과제 3: turtlesim 토픽 및 메시지 구조 분석

실행 중인 `turtlesim_node`에서 발행/구독되는 주요 토픽들의 구조를 분석.

### 1. /turtle1/cmd_vel
- **Type**: `geometry_msgs/Twist`
- **Description**: 거북이에게 이동 명령을 내리는 토픽 (구독자: turtlesim_node)
- **Structure**:
  - `linear` (Vector3): 직진 속도 ($x, y, z$) - 주로 $x$축 사용
  - `angular` (Vector3): 회전 속도 ($x, y, z$) - 주로 $z$축 사용

### 2. /turtle1/pose
- **Type**: `turtlesim/Pose`
- **Description**: 거북이의 현재 상태 정보를 발행하는 토픽 (발행자: turtlesim_node)
- **Structure**:
  - `x`, `y`: 위치 좌표 (`float32`)
  - `theta`: 방향 (`float32`, radian)
  - `linear_velocity`, `angular_velocity`: 현재 속도 (`float32`)

### 3. /turtle1/color_sensor
- **Type**: `turtlesim/Color`
- **Description**: 거북이 위치의 배경 색상 정보를 전달함
- **Structure**: `r`, `g`, `b` (uint8, 0~255 범위)