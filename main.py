import subprocess
from random import randint
import sys


red = '\033[91m'
reset = '\033[0m'


def execute(commands_list, title):
    separator = '-' * 25
    print(f"{red}{separator} {title} {separator}{reset}", flush=True)

    for cmd_input in commands_list:
        cmd = cmd_input.split()
        print(f"{' '.join(cmd)}", flush=True)
        
        if cmd[0] == "source":
            os.system(f"bash -c {' '.join(cmd)}")
        else:
            command_exit_code = os.system(' '.join(cmd))
            if command_exit_code != 0:
                print(f"{red}Command execution failed: {' '.join(cmd)}{reset}", flush=True)
                exit()

    print(f"{red}{separator}{' ' * len(title)}{separator}{reset}", flush=True)


def install_pip():
    commands = ['sudo apt -y install python3-pip']
    execute(commands, 'INSATLLING PIP')


def install_pip_libs():
    commands = [
        'pip install psutil',
        'pip install pygit2',
        'sudo pip install -U vcstool'
    ]
    execute(commands, 'INSTALLING PIP LIBS')


def clone_repo():
    commands = ['python3 pmexec/vcs_p.py --init']
    execute(commands, 'CLONE REPOS')


def install_ros():
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
    execute(commands, 'INSTALLING ROS2')


def configure_env():
    ros_domain_id = randint(0, 101)
    print(f"{red}{'-' * 25} {ros_domain_id} {'-' * 25}{reset}", flush=True)
    commands = [
        f'echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc',
        f'echo "export ROS_DOMAIN_ID={ros_domain_id}" >> ~/.bashrc',
        'sudo apt install ros-humble-rmw-cyclonedds-cpp',
        'echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> ~/.bashrc',
        'gedit -s ~/.bashrc',
    ]
    execute(commands, 'CONFIGURING ENVIRONMENT')


def build_repo():
    commands = [
        'sudo apt install -y python3-colcon-common-extensions',
        'sudo rosdep init',
        'rosdep update',
        'rosdep install -i --from-path src --rosdistro humble -y',
        'colcon build'
    ]
    execute(commands, 'BUILDING PROJECT')


def build():
    install_pip()
    install_pip_libs()
    clone_repo()
    install_ros()
    configure_env()
    build_repo()


build()
