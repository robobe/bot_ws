from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, AppendEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from pathlib import Path
import xacro


def generate_launch_description():
    package_name = "bot_description"
    pkg_description = get_package_share_directory(package_name)
    xacro_file = Path(pkg_description).joinpath("urdf", "robot.urdf.xacro").as_posix()
    urdf = xacro.process_file(xacro_file).toxml()

    params = {"robot_description": urdf, "use_sim_time": True}
    node_robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[params],
    )

    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-topic",
            "robot_description",
            "-entity",
            "my_bot"
        ],
        output="screen",
    )

    return LaunchDescription(
        [
            node_robot_state_publisher,
            spawn_entity,
        ]
    )
