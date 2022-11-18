This is a personal project I've been working on, the objective is to navigate autonomously in known and unknown scenarios with a wheeled differential drive robot using SLAM. In order to run the simulation follow these steps:
1. Clone this repo (use main branch, others are still under development, deprecated, or correspond to past commits of this project)
2. Once cloned, go to the repo folder and enter src/modelo_robot/meshes, copy all the files in that folder (the files have .STL extension), now go to ~/.gazebo/models and create a new folder called "robot_meshes", or any other name you want and paste the meshes there.
3. Source ROS2 (run in a terminal: source /opt/ros/foxy/setup.bash)
4. In that same terminal, got to the repo folder and run the launch.sh linux executable file of the repo, you can run it by first, running this command:
chmod +x launch.sh to give the necessary permissions to execute the program, and then run the command ./launch.sh to launch the simulation.
5. Finally, if you want to activate slam, run ./slam.sh in a new terminal (note: launch.sh should be already running since it is the simulation), now you will be able to see a map in rviz2, move the robot around sending msgs to cmd_vel topic in order to map the Gazebo environment the robot is in.

This project is still under development, so you can expect future commits and updates in the future. Best regards!
