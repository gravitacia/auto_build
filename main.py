import os


def install_ros():
    os.system('sudo apt update && sudo apt install curl gnupg2 lsb-release')
    os.system('curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -')
    os.system(
        'sudo sh -c "echo \'deb [arch=amd64,arm64] http://packages.ros.org/ros2/ubuntu/ `lsb_release -cs` main\' > '
        '/etc/apt/sources.list.d/ros2-latest.list"')

    os.system('sudo apt update')
    os.system('sudo apt install ros-humble-desktop')
    os.system('sudo apt install ros-dev-tools')

    os.system('source /opt/ros/humble/setup.bash')


def install_vcs():
    os.system('sudo apt-get update && sudo apt-get install python3-vcstool')


def configure_env():
    os.system('echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc')
    os.system('echo "export ROS_DOMAIN_ID=1" >> ~/.bashrc')
    os.system('sudo apt install ros-humble-rmw-cyclonedds-cpp')
    os.system('echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> ~/.bashrc')


def build_repo():
    os.system('vcs import src < pm.repos')
    os.system('rosdep install -i --from-path src --rosdistro humble -y')
    os.system('sudo apt install python3-colcon-common-extensions')
    os.system('colcon build')


def build():
    install_ros()
    install_vcs()
    configure_env()
    build_repo()


build()
