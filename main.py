import os
from random import randint


def install_pip():
    os.system('sudo apt -y install python3-pip')


def install_pip_libs():
    print("//////////////////", 'green', 'on_red')
    print("INITIALISING LIBS", 'green', 'on_red')
    print("//////////////////", 'green', 'on_red')

    os.system('pip install psutil')
    os.system('pip install pygit2')
    os.system('sudo pip install -U vcstool')


def clone_repo():
    print("//////////////////", 'green', 'on_red')
    print("INITIALISING REPOSITORIES", 'green', 'on_red')
    print("//////////////////", 'green', 'on_red')

    if os.system('python3 pmexec/vcs_p.py --init') != 0:
        print("//////////////////", 'green', 'on_red')
        print(f"Failed to clone repos", 'green', 'on_red')
        print("//////////////////", 'green', 'on_red')
        exit()


def install_ros():
    print("//////////////////", 'green', 'on_red')
    print("INSTALLING ROS2", 'green', 'on_red')
    print("//////////////////", 'green', 'on_red')

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
            print("//////////////////", 'green', 'on_red')
            print(f"Failed to execute command: {cmd}", 'green', 'on_red')
            print("//////////////////", 'green', 'on_red')
            exit()


def configure_env():
    print("//////////////////", 'green', 'on_red')
    print("CONFIGURING ENVIROMENT", 'green', 'on_red')
    print("//////////////////", 'green', 'on_red')

    ros_domain_id = randint(0, 101)

    commands = [
        'echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc',
        'echo "export ROS_DOMAIN_ID={ros_domain_id}" >> ~/.bashrc',
        'sudo apt install ros-humble-rmw-cyclonedds-cpp',
        'echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> ~/.bashrc'
    ]

    for cmd in commands:
        if os.system(cmd) != 0:
            print("//////////////////", 'green', 'on_red')
            print(f"Failed to execute command: {cmd}", 'green', 'on_red')
            print("//////////////////", 'green', 'on_red')
            exit()


def build_repo():
    print("//////////////////", 'green', 'on_red')
    print("BUILDING PROJECT", 'green', 'on_red')
    print("//////////////////", 'green', 'on_red')

    commands = [
        'rosdep install -i --from-path src --rosdistro humble -y',
        'sudo rosdep init',
        'rosdep update',
        'sudo apt install python3-colcon-common-extensions',
        'colcon build'
    ]

    for cmd in commands:
        if os.system(cmd) != 0:
            print("//////////////////", 'green', 'on_red')
            print(f"Failed to execute command: {cmd}", 'green', 'on_red')
            print("//////////////////", 'green', 'on_red')
            exit()


def build():
    install_pip()
    install_pip_libs()
    clone_repo()
    install_ros()
    configure_env()
    build_repo()


build()
