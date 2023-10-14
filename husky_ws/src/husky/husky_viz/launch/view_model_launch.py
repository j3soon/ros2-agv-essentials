import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # The path of .rviz file.
    rviz_config_file = PathJoinSubstitution(
        [FindPackageShare("husky_viz"), "rviz", "test.rviz"]
    )

    # Launch joint state publisher.
    node_joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui"
    )

    # Launch rviz2.
    node_rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz",
        arguments=["-d", rviz_config_file],
        output="screen"
    )

    # Launch Husky's description. ( Use the launch file in "husky_description" )
    # It retrieves Husky's URDF via xacro and publishes the robot state.
    launch_husky_description = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("husky_description"), "launch/description_launch.py")
        )
    )

    return LaunchDescription(
        [
            node_joint_state_publisher_gui,
            node_rviz,
            launch_husky_description,
        ]
    )
