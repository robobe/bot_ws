import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, AppendEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from pathlib import Path


def generate_launch_description():
    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name = "bot_description"  # <--- CHANGE ME
    pkg_description = get_package_share_directory(package_name)
    pkg_gazebo = get_package_share_directory("gazebo_ros")
    rsp_launch_path = (
        Path(pkg_description).joinpath("launch", "rsp.launch.py").as_posix()
    )

    rsp_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([rsp_launch_path]),
        launch_arguments={"use_sim_time": "true"}.items(),
    )

    resources = [os.path.join(pkg_description, "worlds")]
    resource_env = AppendEnvironmentVariable(
        name="GAZEBO_RESOURCE_PATH", value=":".join(resources)
    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gz_server_launch = (
        Path(pkg_gazebo).joinpath("launch", "gzserver.launch.py").as_posix()
    )
    gz_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([gz_server_launch]),
        launch_arguments={
            "pause": "false",
            "verbose": "true",
            "world": "playground.sdf"
        }.items(),
    )

    gz_client_launch = (
        Path(pkg_gazebo).joinpath("launch", "gzclient.launch.py").as_posix()
    )
    gz_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([gz_client_launch])
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

    # Launch them all!
    return LaunchDescription(
        [
            resource_env,
            rsp_launch,
            gz_server,
            gz_client,
            spawn_entity,
        ]
    )
