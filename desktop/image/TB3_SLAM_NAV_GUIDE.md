# คู่มือการติดตั้งและใช้งาน TurtleBot3 Simulation, SLAM และ Auto Nav (ROS 2 Lyrical)

คู่มือฉบับนี้สรุปขั้นตอนตั้งแต่การติดตั้งแพ็กเกจ การรัน Gazebo Simulation การทำแผนที่ด้วย SLAM Toolbox ไปจนถึงการนำทางอัตโนมัติด้วย Nav2 บน **ROS 2 Lyrical**

---

## 1. การติดตั้งแพ็กเกจ (Installation)

ติดตั้งแพ็กเกจสำหรับ TurtleBot3 Simulation, SLAM Toolbox, Teleop และ Navigation2:

```bash
sudo apt update
sudo apt install -y \
  ros-${ROS_DISTRO:-lyrical}-turtlebot3-gazebo \
  ros-${ROS_DISTRO:-lyrical}-slam-toolbox \
  ros-${ROS_DISTRO:-lyrical}-teleop-twist-keyboard \
  ros-${ROS_DISTRO:-lyrical}-navigation2 \
  ros-${ROS_DISTRO:-lyrical}-nav2-bringup \
  ros-${ROS_DISTRO:-lyrical}-nav2-map-server
```

### ตั้งค่า Environment Variables
เพิ่มค่าเริ่มต้นไว้ใน `~/.bashrc` (หรือรันในแต่ละ Terminal):

```bash
source /opt/ros/${ROS_DISTRO:-lyrical}/setup.bash
export ROS_DOMAIN_ID=50
export TURTLEBOT3_MODEL=burger   # เลือกได้: burger, waffle, waffle_pi
```

> **หมายเหตุ:** หากใช้งานผ่าน Desktop Container / noVNC ให้ตั้งค่า `export DISPLAY=:9` ก่อนเปิด GUI (`gz sim`, `rviz2`)

---

## 2. การรัน TurtleBot3 Simulation (Gazebo Sim)

เปิด **Terminal 1** แล้วรันฉากจำลอง:

```bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

ฉากอื่นที่มีให้เลือกใน `turtlebot3_gazebo`:
- `empty_world.launch.py` — พื้นที่โล่ง
- `turtlebot3_world.launch.py` — สนามหกเหลี่ยมพร้อมเสา 9 ต้น
- `turtlebot3_house.launch.py` — จำลองภายในบ้าน

### ตรวจสอบความพร้อมของ Simulation
```bash
ros2 topic list -t
```
ควรพบ Topic สำคัญได้แก่ `/clock`, `/scan`, `/odom`, `/tf`, `/tf_static`, `/robot_description` และ `/cmd_vel` (`geometry_msgs/msg/TwistStamped`)

---

## 3. การทำแผนที่ (SLAM ด้วย SLAM Toolbox)

### 3.1 รัน SLAM Toolbox
เปิด **Terminal 2**:

```bash
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true
```

### 3.2 เปิด RViz2 เพื่อดูแผนที่
เปิด **Terminal 3**:

```bash
rviz2 -d ~/tb3_slam_nav.rviz --ros-args -p use_sim_time:=true
```

หากเปิด RViz2 แบบค่าเริ่มต้น (`rviz2 --ros-args -p use_sim_time:=true`) ให้ตั้งค่าด้วยตนเองดังนี้:
- **Global Options -> Fixed Frame:** `map`
- กด **Add** เพิ่ม Display ที่จำเป็น:
  - `Map` (Topic: `/map`, Durability: `Transient Local`)
  - `LaserScan` (Topic: `/scan`, Reliability: `Reliable`, Filter size: `10`)
  - `RobotModel` (Topic: `/robot_description`, Durability: `Transient Local`)
  - `TF`

### 3.3 บังคับหุ่นยนต์เก็บแผนที่ (Teleop)
เปิด **Terminal 4** แล้วบังคับหุ่นยนต์เดินให้ทั่วพื้นที่ (ต้องใส่ `-p stamped:=true` เนื่องจาก `/cmd_vel` ใช้ชนิด `TwistStamped`):

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=true
```

ปุ่มควบคุมหลัก: `i` (เดินหน้า), `,` (ถอยหลัง), `j` (หมุนซ้าย), `l` (หมุนขวา), `k` (หยุด), `q/z` (เพิ่ม/ลดความเร็ว)

### 3.4 บันทึกแผนที่ (Save Map)
เมื่อเก็บแผนที่ครบแล้ว รันคำสั่งบันทึกแผนที่ (จะได้ไฟล์ `.pgm` และ `.yaml`):

```bash
ros2 run nav2_map_server map_saver_cli -f ~/tb3_map --ros-args -p save_map_timeout:=10.0
```

ผลลัพธ์ที่ได้:
- `~/tb3_map.pgm` (ภาพแผนที่ Occupancy Grid)
- `~/tb3_map.yaml` (Metadata เช่น resolution และ origin)

---

## 4. การรัน Auto Nav (Nav2 Navigation)

> **สำคัญ:** ต้องปิด `slam_toolbox` (**Terminal 2**) ก่อนเริ่มรัน Nav2 เพื่อไม่ให้ชนกับ `amcl` และ `map_server` บน `/map` และ TF `map -> odom` (โดยยังคงเปิด Gazebo Sim ไว้)

### 4.1 เตรียมไฟล์พารามิเตอร์ Nav2 สำหรับ TurtleBot3 Burger
คัดลอกไฟล์ตั้งต้นจาก `nav2_bringup` มาปรับค่าสำหรับ TurtleBot3 Burger:

```bash
cp /opt/ros/${ROS_DISTRO:-lyrical}/share/nav2_bringup/params/nav2_params.yaml ~/tb3_nav2_params.yaml
```

ค่าหลักที่แนะนำให้ปรับใน `~/tb3_nav2_params.yaml`:

| โหนด / หัวข้อ | พารามิเตอร์ | ค่าแนะนำ (TB3 Burger) | เหตุผล |
|---|---|---|---|
| `amcl` | `laser_max_range` | `3.5` | ตรงกับระยะ LiDAR ของ TB3 |
| `amcl` | `set_initial_pose` | `true` (เลือกได้) | ตั้งพิกัดเริ่มต้นอัตโนมัติ (หรือกำหนดผ่าน RViz2) |
| `controller_server` | `controller_frequency` / `model_dt` | `10.0` / `0.1` | ลดภาระ CPU เมื่อรันร่วมกับ Gazebo |
| `controller_server` (MPPI) | `batch_size` / `vx_max` / `vx_min` | `1000` / `0.26` / `-0.22` | เหมาะกับความเร็วสูงสุดของ TB3 Burger |
| `velocity_smoother` | `max_velocity` / `min_velocity` | `[0.26, 0.0, 1.8]` / `[-0.26, 0.0, -1.8]` | จำกัดความเร็วให้เหมาะสมกับตัวหุ่น |
| `local_costmap` / `global_costmap` | `robot_radius` / `inflation_radius` | `0.14` / `0.35` | ให้หุ่นยนต์ผ่านช่องระหว่างเสาในฉากได้สะดวก |
| `bt_navigator` / costmaps / `behavior_server` | `robot_base_frame` | `base_footprint` | ตรงกับโครงสร้าง TF ของ TurtleBot3 |
| `collision_monitor` | `scan.min_height` | `0.05` | รองรับความสูง LiDAR ของ TB3 (~0.17 m) |

*(ดูไฟล์ตัวอย่างที่ปรับแต่งและทดสอบแล้วได้ที่ `~/tb3_nav2_params.yaml`)*

### 4.2 รัน Nav2 Bringup
เปิด **Terminal 2** (หลังจากปิด `slam_toolbox` แล้ว):

```bash
ros2 launch nav2_bringup bringup_launch.py \
  map:=$HOME/tb3_map.yaml \
  params_file:=$HOME/tb3_nav2_params.yaml \
  use_sim_time:=True \
  autostart:=True \
  use_keepout_zones:=False \
  use_speed_zones:=False
```

รอจนหน้าจอแสดงข้อความ:
```text
[lifecycle_manager_nav2]: Managed nodes are active
```

### 4.3 เปิด RViz2 สำหรับ Nav2
```bash
rviz2 -d ~/tb3_slam_nav.rviz --ros-args -p use_sim_time:=true
```

Display ที่ควรมีสำหรับ Nav2 (รวมอยู่ใน `~/tb3_slam_nav.rviz` แล้ว):
- `Map` (`/map`)
- `Global Costmap` (`/global_costmap/costmap`) และ `Local Costmap` (`/local_costmap/costmap`)
- `Global Plan` (`/plan`) และ `Local Plan` (`/local_plan`)
- `LaserScan` (`/scan`), `RobotModel`, `TF`

### 4.4 กำหนดตำแหน่งเริ่มต้นและสั่งนำทาง
1. **กำหนดตำแหน่งเริ่มต้น (หากไม่ได้ตั้ง `set_initial_pose` ใน YAML):**
   - กดปุ่ม **2D Pose Estimate** บน RViz2 แล้วคลิกลากระบุตำแหน่งและทิศทางปัจจุบันของหุ่นยนต์บนแผนที่ (เช็กให้เส้นแดง `LaserScan` ซ้อนทับขอบกำแพงแผนที่พอดี)
2. **สั่งให้หุ่นยนต์วิ่งไปเป้าหมาย (เลือกวิธีใดวิธีหนึ่ง):**
   - **ผ่าน RViz2:** กดปุ่ม **2D Goal Pose** แล้วคลิกลากจุดหมายบนแผนที่
   - **ผ่าน CLI:**
     ```bash
     ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose \
       "{pose: {header: {frame_id: 'map'}, pose: {position: {x: 0.0, y: 0.0, z: 0.0}, orientation: {w: 1.0}}}}"
     ```

---

## 5. ปัญหาที่พบบ่อยและการแก้ไข (Troubleshooting)

1. **Error `KeyError: 'TURTLEBOT3_MODEL'` ตอนเปิด Gazebo**
   - ยังไม่ได้กำหนดตัวแปรรุ่นหุ่นยนต์ ให้รัน `export TURTLEBOT3_MODEL=burger` ก่อน `ros2 launch`
2. **กดคีย์บอร์ดใน `teleop_twist_keyboard` แล้วหุ่นไม่ขยับ**
   - `turtlebot3_gazebo` บน ROS 2 Lyrical รับ `/cmd_vel` เป็น `geometry_msgs/msg/TwistStamped` ต้องรันพร้อม `--ros-args -p stamped:=true`
3. **Nav2 `controller_server` หรือ `planner_server` โหลดไม่ขึ้น (`parameter_value_from failed for parameter 'filters'`)**
   - อย่าเปลี่ยน `filters:` ใน `nav2_params.yaml` เป็นลิสต์ว่าง `[]` ให้คงค่าเริ่มต้นไว้แล้วปิดฟีเจอร์ผ่าน Argument `use_keepout_zones:=False use_speed_zones:=False` แทน
4. **RViz2 แจ้ง `Message Filter dropping message: frame 'base_scan'`**
   - ตรวจสอบว่ารัน RViz2 ด้วย `--ros-args -p use_sim_time:=true` และตั้งค่า Display `LaserScan` ให้มี `Reliability Policy: Reliable` และ `Filter size: 10`
5. **Nav2 วางแผนเส้นทางผ่านช่องแคบไม่ได้**
   - ลด `robot_radius` (เช่น `0.14`) และ `inflation_radius` (เช่น `0.35`) ในทั้ง `local_costmap` และ `global_costmap`
