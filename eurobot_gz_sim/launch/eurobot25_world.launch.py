from os.path import join
import os
from launch.actions import AppendEnvironmentVariable

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    eurobot_gz_sim_dir = get_package_share_directory("eurobot_gz_sim")
    ros_gz_sim_dir = get_package_share_directory("ros_gz_sim")

    set_env_vars_resources_models = AppendEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH',
        os.path.join(eurobot_gz_sim_dir,
                     'models'))

    set_env_vars_resources_media = AppendEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH',
        os.path.join(eurobot_gz_sim_dir,
                     'media'))

    default_world = os.path.join(eurobot_gz_sim_dir, "worlds", "eurobot25.sdf")

    gz_sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("ros_gz_sim"),
                "launch",
                "gz_sim.launch.py"
            ])
        ),
        launch_arguments={
            "gz_args": f"-r {default_world}"
        }.items()
    )

    ld = LaunchDescription()

    ld.add_action(set_env_vars_resources_models)
    ld.add_action(set_env_vars_resources_media)
    ld.add_action(gz_sim_launch)

    return ld
