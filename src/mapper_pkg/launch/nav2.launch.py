# Author: Addison Sears-Collins
# Date: September 2, 2021
# Description: Launch a basic mobile robot using the ROS 2 Navigation Stack
# https://automaticaddison.com
 
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
 
def generate_launch_description():
    # Set the path to different files and folders. 
    package_name = 'mapper_pkg'
    pkg_share = FindPackageShare(package=package_name).find(package_name)
    nav2_dir = FindPackageShare(package='nav2_bringup').find('nav2_bringup') 
    nav2_launch_dir = os.path.join(nav2_dir, 'launch') 
    static_map_path = os.path.join(pkg_share, 'maps', 'my_map.yaml')
    nav2_params_path = os.path.join(pkg_share, 'config', 'nav2_params.yaml')
    nav2_bt_path = FindPackageShare(package='nav2_bt_navigator').find('nav2_bt_navigator')
    behavior_tree_xml_path = os.path.join(nav2_bt_path, 'behavior_trees', 'navigate_w_replanning_and_recovery.xml')

    # Launch configuration variables specific to simulation
    autostart = LaunchConfiguration('autostart')
    default_bt_xml_filename = LaunchConfiguration('default_bt_xml_filename')
    headless = LaunchConfiguration('headless')
    map_yaml_file = LaunchConfiguration('map')
    model = LaunchConfiguration('model')
    namespace = LaunchConfiguration('namespace')
    params_file = LaunchConfiguration('params_file')
    rviz_config_file = LaunchConfiguration('rviz_config_file')
    slam = LaunchConfiguration('slam')
    use_namespace = LaunchConfiguration('use_namespace')
    use_robot_state_pub = LaunchConfiguration('use_robot_state_pub')
    use_rviz = LaunchConfiguration('use_rviz')
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_simulator = LaunchConfiguration('use_simulator')
    world = LaunchConfiguration('world')

    # Map fully qualified names to relative ones so the node's namespace can be prepended.
    # In case of the transforms (tf), currently, there doesn't seem to be a better alternative
    # https://github.com/ros/geometry2/issues/32
    # https://github.com/ros/robot_state_publisher/pull/30
    # TODO(orduno) Substitute with `PushNodeRemapping`
    #              https://github.com/ros2/launch_ros/issues/56
    #remappings = [('/tf', 'tf'),
    #            ('/tf_static', 'tf_static')]



            
    declare_autostart_cmd = DeclareLaunchArgument(
    name='autostart', 
    default_value='true',
    description='Automatically startup the nav2 stack')

    declare_bt_xml_cmd = DeclareLaunchArgument(
    name='default_bt_xml_filename',
    default_value=behavior_tree_xml_path,
    description='Full path to the behavior tree xml file to use')
            
    declare_map_yaml_cmd = DeclareLaunchArgument(
    name='map',
    default_value=static_map_path,
    description='Full path to map file to load')
            
        
    declare_params_file_cmd = DeclareLaunchArgument(
    name='params_file',
    default_value=nav2_params_path,
    description='Full path to the ROS2 parameters file to use for all launched nodes')

    declare_slam_cmd = DeclareLaunchArgument(
    name='slam',
    default_value='False',
    description='Whether to run SLAM')
        
    declare_use_sim_time_cmd = DeclareLaunchArgument(
    name='use_sim_time',
    default_value='True',
    description='Use simulation (Gazebo) clock if true')

    # Specify the actions

    # Launch the ROS 2 Navigation Stack
    start_ros2_navigation_cmd = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(os.path.join(nav2_launch_dir, 'bringup_launch.py')),
    launch_arguments = {
                        'slam': slam,
                        'map': map_yaml_file,
                        'use_sim_time': use_sim_time,
                        'params_file': params_file,
                        'default_bt_xml_filename': default_bt_xml_filename,
                        'autostart': autostart}.items())

    # Create the launch description and populate
    ld = LaunchDescription()

    # Declare the launch options
    ld.add_action(declare_autostart_cmd)
    ld.add_action(declare_bt_xml_cmd)
    ld.add_action(declare_map_yaml_cmd)
    ld.add_action(declare_params_file_cmd)
    ld.add_action(declare_slam_cmd)
    ld.add_action(declare_use_sim_time_cmd)

    # Add any actions
    ld.add_action(start_ros2_navigation_cmd)

    return ld