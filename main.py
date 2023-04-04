import os
from random import randint
import sys


red = '\033[91m'
reset = '\033[0m'


def install_pip():
    os.system('sudo apt -y install python3-pip')


def install_pip_libs():
    print(red + "//////////////////" + reset)
    print(red + "INITIALISING LIBS" + reset)
    print(red + "//////////////////" + reset)

    os.system('pip install psutil')
    os.system('pip install pygit2')
    os.system('sudo pip install -U vcstool')


def clone_repo():
    print(red + "//////////////////" + reset)
    print(red + "INITIALISING REPOSITORIES" + reset)
    print(red + "//////////////////" + reset)

    if os.system('python3 pmexec/vcs_p.py --init') != 0:
        print(red + "//////////////////" + reset)
        print(red + f"Failed to clone repos" + reset)
        print(red + "//////////////////" + reset)
        exit()


def install_ros():
    print(red + "//////////////////" + reset)
    print(red + "INSTALLING ROS2" + reset)
    print(red + "//////////////////" + reset)

    commands = [
        'sudo apt install software-properties-common',
        'sudo add-apt-repository universe',
        'sudo apt update && sudo apt install curl',
        'sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg',
        'echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null',
        'sudo apt update',
        'sudo apt upgrade',
        'sudo apt install ros-humble-desktop',
        'sudo apt install ros-humble-ros-base',
        'sudo apt install ros-dev-tools',
        'source /opt/ros/humble/setup.bash'
    ]

    for cmd in commands:
        if os.system(cmd) != 0:
            print(red + "//////////////////" + reset)
            print(red + f"Failed to execute command: {cmd}" + reset)
            print(red + "//////////////////" + reset)
            exit()


def configure_env():
    print(red + "//////////////////" + reset)
    print(red + "CONFIGURING ENVIROMENT" + reset)
    print(red + "//////////////////" + reset)

    ros_domain_id = randint(0, 101)

    commands = [
        'echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc',
        'echo "export ROS_DOMAIN_ID={ros_domain_id}" >> ~/.bashrc',
        'sudo apt install ros-humble-rmw-cyclonedds-cpp',
        'echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> ~/.bashrc'
    ]

    for cmd in commands:
        if os.system(cmd) != 0:
            print(red + "//////////////////" + reset)
            print(red  + f"Failed to execute command: {cmd}" + reset)
            print(red + "//////////////////" + reset)
            exit()


def build_repo():
    print(red + "//////////////////" + reset)
    print(red + "BUILDING PROJECT" + reset)
    print(red + "//////////////////" + reset)

    commands = [
        'rosdep install -i --from-path src --rosdistro humble -y',
        'sudo rosdep init',
        'rosdep update',
        'sudo apt install python3-colcon-common-extensions',
        'colcon build'
    ]

    for cmd in commands:
        if os.system(cmd) != 0:
            print(red + "//////////////////" + reset)
            print(red + f"Failed to execute command: {cmd}" + reset)
            print(red + "//////////////////" + reset)
            exit()


def build():
    install_pip()
    install_pip_libs()
    clone_repo()
    install_ros()
    configure_env()
    build_repo()


build()
