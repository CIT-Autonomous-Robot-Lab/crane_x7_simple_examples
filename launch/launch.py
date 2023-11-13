# SPDX-FileCopyrightText: 2023 Keitaro Nakamura

import os

from ament_index_python.packages import get_package_share_directory
from crane_x7_description.robot_description_loader import RobotDescriptionLoader
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import SetParameter
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import yaml


def load_file(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)

    try:
        with open(absolute_file_path, 'r') as file:
            return file.read()
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        return None


def load_yaml(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)

    try:
        with open(absolute_file_path, 'r') as file:
            return yaml.safe_load(file)
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        return None


def generate_launch_description():
    description_loader = RobotDescriptionLoader()

    robot_description_semantic_config = load_file(
        'crane_x7_moveit_config', 'config/crane_x7.srdf')
    robot_description_semantic = {
        'robot_description_semantic': robot_description_semantic_config}

    kinematics_yaml = load_yaml('crane_x7_moveit_config', 'config/kinematics.yaml')

    # 複数のコードを用いる時は以下を編集してください
#    declare_example_name = DeclareLaunchArgument(
#        'execution', default_value='exec_dir',
#        description=('Set an example executable name:[pick_and_place]')
#    )

    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='false',
        description=('Set true when using the gazebo simulator.')
    )
    #パッケージ名の変更、実行コマンドの変更は以下を編集してください
    example_node = Node(name=[LaunchConfiguration('exec_dir'), '_node'],
                        package='cit_cranex7_ros2',
                        executable=LaunchConfiguration('execute'),
                        output='screen',
                        parameters=[{'robot_description': description_loader.load()},
                                    robot_description_semantic,
                                    kinematics_yaml])

    return LaunchDescription([
        declare_use_sim_time,
        SetParameter(name='use_sim_time', value=LaunchConfiguration('use_sim_time')),
        declare_example_name,
        example_node
    ])
