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

## 과제 4: rostopic pub으로 정사각형 그리기

명령줄 인터페이스(CLI)를 통해 거북이에게 직접 속도 명령을 전달하여 정사각형 경로를 주행함.

### 과제 4 실행 결과 화면
![거북이로 정사각형 그리기 실행 화면](./images/과제4.PNG)

### 사용한 명령어 순서
1. **직진**: `rostopic pub -1 /turtle1/cmd_vel geometry_msgs/Twist -- '[2.0, 0.0, 0.0]' '[0.0, 0.0, 0.0]'`
2. **90도 회전**: `rostopic pub -1 /turtle1/cmd_vel geometry_msgs/Twist -- '[0.0, 0.0, 0.0]' '[0.0, 0.0, 1.5708]'`
3. 위 과정을 4회 반복하여 정사각형 궤적 생성 완료.

## 과제 5: turtlesim 2개 동시 실행 관찰

`__name` 파라미터를 사용하여 동일한 노드를 서로 다른 이름으로 실행하는 실습을 진행함.

### 과제 5 실행 결과 화면
![거북이 두 마리 실행 화면](./images/과제5.PNG)

### 관찰 결과
- **노드 목록**: `/turtlesim`과 `/my_turtle` 두 개의 노드가 정상 실행됨을 확인.
- **동작 원리**: `turtle_teleop_key`로 조종 시 두 거북이가 동시에 움직임.
- **원인 분석**: 두 노드 모두 `/turtle1/cmd_vel` 토픽을 구독(Subscribe)하고 있기 때문에, 하나의 발행자(Publisher)가 보내는 메시지를 동시에 수신함.

# Launch 파일을 활용한 노드 관리
### 실습 1: turtlesim 멀티 런치 파일 (`multi_turtle.launch`)
- **목표**: 한 번에 거북이 2마리를 띄우고, 통신 간섭 없이 각각 독립적으로 제어함.
- **핵심 기술**:
  - `name="turtle2"`: 노드 이름을 다르게 지정하여 중복 실행 시 발생하는 충돌을 방지함.
  - `<remap>`: 두 번째 거북이의 구독 토픽을 `/turtle1/cmd_vel`에서 `/turtle2/cmd_vel`로 변경(리맵핑)하여 통신망을 분리함.
- **결과**: 키보드 조작(`teleop`)으로는 첫 번째 거북이만 움직이고, 터미널에서 `rostopic pub`으로 `/turtle2/cmd_vel`에 명령을 보내면 두 번째 거북이만 따로 제어됨을 확인함.

### 실습 2: param을 활용한 런치 파일 (`color_turtle.launch`)
- **목표**: 런치 파일 내부에서 파라미터(Parameter)를 설정하여 turtlesim의 배경색을 변경함.
- **핵심 기술**:
  - `<param>`: 노드 실행 시 파라미터 서버에 초기 설정값(RGB)을 등록함. (실습에서는 모두 0으로 설정하여 검은 배경 생성)
  - `rosparam set`: 노드 실행 도중에 파라미터 값을 동적으로 변경함.
  - `rosservice call /clear`: 변경된 배경색을 화면에 즉시 적용(새로고침)하도록 서비스에 요청함.
- **결과**: 노드 실행 시 검은색 배경이 적용되며, 터미널 명령어를 통해 빨간색, 파란색 등으로 배경색을 실시간으로 바꾸는 데 성공함.

### 실습 3: include로 런치 파일 합치기 (`full_turtle.launch`)
- **목표**: 기존 런치 파일을 모듈처럼 재사용하고, 노드 시각화 도구를 추가로 실행함.
- **핵심 기술**:
  - `<include>`: 다른 런치 파일(`color_turtle.launch`)을 그대로 불러와 코드를 재사용함.
  - `$(find 패키지명)`: ROS 시스템에서 해당 패키지의 절대 경로를 자동으로 찾아 에러를 방지함.
- **결과**: `roslaunch` 명령어 한 번으로 거북이 화면, 조종기, 그리고 현재 통신 상태를 보여주는 `rqt_graph` 창이 동시에 실행됨을 확인함.