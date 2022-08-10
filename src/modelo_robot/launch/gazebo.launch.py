import os
  
from ament_index_python.packages import get_package_share_directory
 
from launch_ros.parameter_descriptions import ParameterValue
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.conditions import IfCondition
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
  
def generate_launch_description():
 
 
    model_arg = DeclareLaunchArgument(name='model', description='Absolute path to robot urdf file')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    use_sim_time = LaunchConfiguration('use_sim_time') 
    package_name = 'modelo_robot'
    pkg_share = FindPackageShare(package=package_name).find(package_name)
    pkg_gazebo_ros = FindPackageShare(package='gazebo_ros').find('gazebo_ros') 

    world_file_path = 'museum.world'
    world = LaunchConfiguration('world')
    world_path = os.path.join(pkg_share, 'worlds',  world_file_path)

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
        )
    
    declare_world_cmd = DeclareLaunchArgument(
        name='world',
        default_value=world_path,
        description='Full path to the world model file to load')
    

    robot_name_in_model = 'Seguidor_linea_robot'

    # Get URDF via xacro

    urdf_file_name = 'Seguidor_linea_robot.urdf'
    urdf = os.path.join(
        get_package_share_directory('modelo_robot'),
        'urdf',
        urdf_file_name
        )
    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    robot_description = {"robot_description": robot_desc}
 
 
    #rivz2
    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='log',
        parameters=[{'use_sim_time': use_sim_time}],
    )
 
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters= [{'use_sim_time': use_sim_time, 'robot_description': robot_desc}] #[{'use_sim_time': use_sim_time, "robot_description": robot_description_content}],
    )

    start_joint_state_publisher_cmd = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        parameters=[{'use_sim_time': use_sim_time}],
        name='joint_state_publisher',
    )
 
 
    #spawn the robot 
    spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=["-topic", "/robot_description", 
                    "-entity", robot_name_in_model,
                    "-x", '0.0',
                    "-y", '0.0',
                    "-z", '0.05',
                    "-Y", '0.0']
    )


    '''gazebo = ExecuteProcess(
        cmd=['gazebo', world_path, '--verbose', '-s', 'libgazebo_ros_factory.so', 
        '-s', 'libgazebo_ros_init.so'], output='screen',
        )'''

    # Start Gazebo server
    start_gazebo_server_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')),
        launch_arguments={'world': world}.items())
 
    # Start Gazebo client    
    start_gazebo_client_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')))
    
    robot_localization_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[os.path.join(pkg_share, 'config', 'ekf.yaml'), {'use_sim_time': use_sim_time}]
    )

    map_frame = ExecuteProcess(
        cmd=['ros2', 'run', 'tf2_ros', 'static_transform_publisher', '-1.0', '-1.0', '0', '0', '0', '0', 'map'
        , 'odom_link'], output='screen',
        )

     
    return LaunchDescription([
    declare_use_sim_time_cmd,
    declare_world_cmd, 
    rviz2,
    spawn,
    robot_state_publisher_node,
    robot_localization_node,
    start_gazebo_server_cmd,
    start_gazebo_client_cmd
])
