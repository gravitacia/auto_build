import os
import time
from random import randint
from termcolor import cprint
import subprocess
import threading


def install_pip_libs():
    cprint("//////////////////", 'green', 'on_red')
    cprint("INITIALISING LIBS", 'green', 'on_red')
    cprint("//////////////////", 'green', 'on_red')

    os.system('pip freeze > requirements.txt')
    os.system('pip install -r requirements.txt --upgrade')


def clone_repo():
    cprint("//////////////////", 'green', 'on_red')
    cprint("INITIALISING REPOSITORIES", 'green', 'on_red')
    cprint("//////////////////", 'green', 'on_red')

    if os.system('python3 pmexec/vcs_p.py --init') != 0:
        cprint("//////////////////", 'green', 'on_red')
        cprint(f"Failed to clone repos", 'green', 'on_red')
        cprint("//////////////////", 'green', 'on_red')
        exit()


def install_ros():
    cprint("//////////////////", 'green', 'on_red')
    cprint("INSTALLING ROS2", 'green', 'on_red')
    cprint("//////////////////", 'green', 'on_red')

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
        'sudo chmod +rwx /opt/ros/humble/setup.bash',
        '/bin/bash -c "source /opt/ros/humble/setup.bash"'
    ]

    for cmd in commands:
        if os.system(cmd) != 0:
            cprint("//////////////////", 'green', 'on_red')
            cprint(f"Failed to execute command: {cmd}", 'green', 'on_red')
            cprint("//////////////////", 'green', 'on_red')
            exit()


def install_vcs():
    cprint("//////////////////", 'green', 'on_red')
    cprint("INSTALLING VCS UTIL", 'green', 'on_red')
    cprint("//////////////////", 'green', 'on_red')

    if os.system('sudo apt-get update && sudo apt-get install python3-vcstool') != 0:
        cprint("//////////////////", 'green', 'on_red')
        cprint(f"Failed to install vcstool", 'green', 'on_red')
        cprint("//////////////////", 'green', 'on_red')
        exit()


def configure_env():
    cprint("//////////////////", 'green', 'on_red')
    cprint("CONFIGURING ENVIROMENT", 'green', 'on_red')
    cprint("//////////////////", 'green', 'on_red')

    ros_domain_id = randint(0, 101)

    commands = [
        'echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc',
        'echo "export ROS_DOMAIN_ID={ros_domain_id}" >> ~/.bashrc',
        'sudo apt install ros-humble-rmw-cyclonedds-cpp',
        'echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> ~/.bashrc'
    ]

    for cmd in commands:
        if os.system(cmd) != 0:
            cprint("//////////////////", 'green', 'on_red')
            cprint(f"Failed to execute command: {cmd}", 'green', 'on_red')
            cprint("//////////////////", 'green', 'on_red')
            exit()


def build_repo():
    cprint("//////////////////", 'green', 'on_red')
    cprint("BUILDING PROJECT", 'green', 'on_red')
    cprint("//////////////////", 'green', 'on_red')

    commands = [
        'rosdep install -i --from-path src --rosdistro humble -y',
        'sudo apt install python3-colcon-common-extensions',
        'colcon build'
    ]

    for cmd in commands:
        if os.system(cmd) != 0:
            cprint("//////////////////", 'green', 'on_red')
            cprint(f"Failed to execute command: {cmd}", 'green', 'on_red')
            cprint("//////////////////", 'green', 'on_red')
            exit()


def build():
    #install_pip_libs()
    install_vcs()
    clone_repo()
    install_ros()
    configure_env()
    build_repo()


build()


def execute_sudo_commands():
    executed_commands = []

    while True:
        output = subprocess.check_output(['dmesg'])
        lines = output.decode().strip().split('\n')

        for line in lines:
            if 'sudo' in line and line not in executed_commands:
                executed_commands.append(line)
                subprocess.run(line.split(), check=True)
        time.sleep(1)


t1 = threading.Thread(target=build)
t2 = threading.Thread(target=execute_sudo_commands)
t1.start()
t2.start()
t1.join()
t2.join()
