import os
from random import randint
import sys

red = '\033[91m'
reset = '\033[0m'


def execute(commands_list, title):
    separator = '-' * 25
    print(f"{red}{separator} {title} {separator}{reset}")

    for cmd_input in commands_list:
        cmd = cmd_input.split()
        print(f"{red}>>> {' '.join(cmd)}{reset}")

        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.returncode != 0:
            print(f"{red}Command execution failed: {' '.join(cmd)}{reset}")
            print(f"{red}{process.stderr.decode('utf-8')}{reset}")
            exit()

        print(f"{red}{process.stdout.decode('utf-8')}{reset}")

    print(f"{red}{separator}{' ' * len(title)}{separator}{reset}")


def install_pip():
    cmd = ['sudo apt -y install python3-pip']
    execute(cmd, 'INSTALLING PIP')


def install_pip_libs():
    cmd = [
        'pip install psutil',
        'pip install pygit2',
        'sudo pip install -U vcstool'
    ]
    execute(cmd, 'INSTALLING PIP LIBS')


def clone_repo():
    cmd = ['python3 pmexec/vcs_p.py --init']
    execute(cmd, 'CLONE REPOS')


def install_ros():
    cmd = [
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
        'bash /opt/ros/humble/setup.bash'
    ]

    execute(cmd, 'INSTALLING ROS2')


def configure_env():
    ros_domain_id = randint(0, 101)
    print(f"{red}{'-' * 25} {ros_domain_id} {'-' * 25}{reset}")
    cmd = [
        'echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc',
        'echo "export ROS_DOMAIN_ID={ros_domain_id}" >> ~/.bashrc',
        'sudo apt install ros-humble-rmw-cyclonedds-cpp',
        'echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> ~/.bashrc',
        'gedit -s ~/.bashrc'
    ]

    execute(cmd, 'CONFIGURING ENVIROMENT')


def build_repo():
    cmd = [
        'sudo rosdep init',
        'rosdep update',
        'rosdep install -i --from-path src --rosdistro humble -y',
        'sudo apt install python3-colcon-common-extensions',
        'colcon build'
    ]

    execute(cmd, 'BUILDING PROJECT')


def build():
    install_pip()
    install_pip_libs()
    clone_repo()
    install_ros()
    configure_env()
    build_repo()


build()
