---
name: ros2
description: >-
  ROS 2 (Robot Operating System 2) development, colcon build, rosdep, launch,
  debugging, and GUI visualization workflow for this container environment
  (ROS 2 Lyrical, RViz2, rqt, Gazebo). Use when creating, building, running,
  testing, debugging, or visualizing ROS 2 packages, nodes, topics, services,
  actions, parameters, TF2 trees, URDF/Xacro models, launch files, or rosbags.
---

# ROS 2 Development Workflow

This desktop container runs **ROS 2 (`$ROS_DISTRO`, default `lyrical`)** with full desktop GUI and simulation tools (`desktop-full`).

## Environment Conventions

* **ROS 2 Setup**: Interactive bash shells source ROS 2 automatically. In non-interactive `bash -c` invocations, always source both base ROS 2 and the overlay workspace first:
  ```bash
  source /opt/ros/${ROS_DISTRO:-lyrical}/setup.bash
  [ -f /workspace/dev_ws/install/setup.bash ] && source /workspace/dev_ws/install/setup.bash
  ```
* **Workspace**: `/workspace/dev_ws` (symlinked at `~/workspace/dev_ws`). Place new packages under `/workspace/dev_ws/src`.
* **Domain ID**: `ROS_DOMAIN_ID=50` is set globally; keep consistent across nodes unless testing isolation.
* **GUI Display**: Desktop runs on `DISPLAY=:9` (accessible via noVNC on port `6901`). Prefix GUI commands with `DISPLAY=:9` when running from headless/SSH shells.

## Creating & Building Packages

1. **Create a package** in `/workspace/dev_ws/src`:
   - Python (`ament_python`):
     ```bash
     cd /workspace/dev_ws/src
     ros2 pkg create --build-type ament_python <pkg_name> --dependencies rclpy std_msgs
     ```
   - C++ (`ament_cmake`):
     ```bash
     cd /workspace/dev_ws/src
     ros2 pkg create --build-type ament_cmake <pkg_name> --dependencies rclcpp std_msgs
     ```
2. **Ensure package manifests & build files are complete**:
   - Python: register executables under `entry_points['console_scripts']` and launch/config files under `data_files` in `setup.py`; declare runtime deps in `package.xml`.
   - C++: add `install(TARGETS ... DESTINATION lib/${PROJECT_NAME})` and `install(DIRECTORY launch config ... DESTINATION share/${PROJECT_NAME})` in `CMakeLists.txt`.
3. **Resolve dependencies** before building if new dependencies were added:
   ```bash
   cd /workspace/dev_ws && rosdep install --from-paths src --ignore-src -r -y
   ```
4. **Build & Test**:
   ```bash
   cd /workspace/dev_ws
   colcon build --symlink-install --packages-select <pkg_name>
   colcon test --packages-select <pkg_name> && colcon test-result --verbose
   ```
   Always `source /workspace/dev_ws/install/setup.bash` after building a new package or adding new interfaces/launch files.

## Runtime Inspection & Debugging

* **Nodes & Topics**:
  - `ros2 node list` / `ros2 node info /<node>`
  - `ros2 topic list -t`
  - `ros2 topic echo <topic>` / `ros2 topic hz <topic>` / `ros2 topic bw <topic>`
  - `ros2 topic pub --once <topic> <msg_type> "<yaml_payload>"`
* **Services, Actions & Parameters**:
  - `ros2 service list -t` / `ros2 service call <srv> <type> "<yaml>"`
  - `ros2 action list -t` / `ros2 action send_goal <action> <type> "<yaml>"`
  - `ros2 param list` / `ros2 param get <node> <param>` / `ros2 param set <node> <param> <value>`
* **Interfaces & Launch**:
  - `ros2 interface show <pkg>/<msg_or_srv_or_action>`
  - `ros2 launch <pkg> <launch_file>` / `ros2 run <pkg> <executable>`
* **TF2 & URDF**:
  - `ros2 run tf2_ros tf2_echo <source_frame> <target_frame>`
  - `ros2 run tf2_tools view_frames` (outputs PDF/GV in CWD)
  - `check_urdf <(xacro model.urdf.xacro)` (or `urdf_to_graphviz`)
* **Bags & Health**:
  - `ros2 bag record -o <dir> <topics...>` / `ros2 bag info <dir>` / `ros2 bag play <dir>`
  - `ros2 doctor --report` (verify DDS discovery, middleware, and environment)

## GUI & Visualization (`DISPLAY=:9`)

* **RViz2**: `DISPLAY=:9 rviz2` (sample IMU config available via `~/view_imu.sh` / `~/test_imu.rviz`)
* **rqt Tools**: `DISPLAY=:9 rqt`, `rqt_graph`, `rqt_console`, `rqt_plot`, `rqt_tf_tree`
* **Gazebo Sim**: `DISPLAY=:9 gz sim` (also available via `ros2 launch ros_gz_sim gz_sim.launch.py`)

## Verification Checklist

Before finishing any ROS 2 task:
1. Run `colcon build --symlink-install` and confirm exit code `0`.
2. Run `colcon test` / `pytest` / `ament_lint` if tests exist.
3. Verify runtime execution (`ros2 run` / `ros2 launch` with a short timeout or background check + `ros2 node list` / `ros2 topic echo --once`) rather than assuming a build alone means the node runs cleanly.

