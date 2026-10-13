# Báo cáo thực hành TurtleBot 4: SLAM, localization và Nav2

Sinh viên: **[điền họ tên, MSSV, lớp]**. Môi trường: Ubuntu 22.04, ROS 2 Humble,
Gazebo Fortress, TurtleBot 4 Lite, world `maze` từ package simulator chính thức.

**Kết quả:** đã tạo map SLAM thật, restart/load map và hoàn thành 3 action Nav2
SUCCEEDED trong Gazebo, có log đối chiếu vị trí AMCL với vị trí simulator. Video
teleop, 3 goal bấm qua RViz và link công khai còn cần bổ sung. PDF hiện là bản nháp.

## 1. Cấu trúc chương trình

Package `turtlebot4_slam_nav` dùng ament_cmake để cài launch/config/map/RViz và hai
script hỗ trợ. Không viết lại robot/controller. `simulation.launch.py` mở Gazebo,
world chính thức, spawn robot/dock bằng launch TurtleBot 4 và chạy bridge `/clock`.
`mapping.launch.py` thêm SLAM Toolbox synchronous. `localization.launch.py` dùng
map_server và AMCL, kiểm tra file map tồn tại trước khi launch. `navigation.launch.py`
thêm Nav2 chính thức. Config local cho phép tái hiện cùng tham số mà không sửa `/opt/ros`.
Trên máy kiểm thử, sensor Ogre 1 bị lỗi minimum-range; overlay sao chép description
chính thức và chỉ đổi renderer thành Ogre 2. Dùng Cyclone DDS để ổn định ROS services.
Không thay đổi geometry, sensor poses, physics hoặc controller của TurtleBot 4.

## 2. Node, package và topic chính

| Node/package | Vai trò |
| --- | --- |
| Gazebo + turtlebot4_ignition_bringup | World, robot, LiDAR, dock, cảm biến và bridge |
| irobot_create_nodes / motion_control | Undock, nhận vận tốc, phản xạ an toàn Create 3 |
| robot_state_publisher | TF từ base tới các link dựa trên URDF/joint_states |
| ros_gz_bridge / parameter_bridge | Chuyển message giữa Gazebo Transport và ROS 2 |
| slam_toolbox | Scan matching, pose graph, loop closure, occupancy map |
| map_server + amcl | Load map cố định và ước lượng pose bằng particle filter |
| planner_server / NavFn | Đường đi toàn cục trên global costmap |
| controller_server / DWB | Chọn vận tốc theo đường đi và local costmap |
| bt_navigator, behavior_server | Điều phối action navigation và recovery |
| velocity_smoother | Làm mượt lệnh vận tốc trước khi gửi robot |
| lifecycle_manager | Configure/activate các node Nav2 và localization |
| rviz2 + nav2_rviz_plugins | Hiển thị sensor/map/path và đặt pose/goal |

| Topic/action | Kiểu | Ý nghĩa |
| --- | --- | --- |
| `/scan` | sensor_msgs/LaserScan | Khoảng cách LiDAR theo góc, m/rad |
| `/odom` | nav_msgs/Odometry | Pose/twist trong odom, có drift |
| `/cmd_vel` | geometry_msgs/Twist | Vận tốc cuối tới Create 3, m/s và rad/s |
| `/cmd_vel_nav` | geometry_msgs/Twist | Lệnh Nav2 trước velocity_smoother |
| `/map` | nav_msgs/OccupancyGrid | Grid: -1 unknown, 0 free, 100 occupied |
| `/tf`, `/tf_static` | tf2_msgs/TFMessage | Biến đổi động và tĩnh giữa các frame |
| `/clock` | rosgraph_msgs/Clock | Thời gian mô phỏng cho use_sim_time |
| `/initialpose` | geometry_msgs/PoseWithCovarianceStamped | Initial pose cho AMCL từ RViz |
| `/amcl_pose` | geometry_msgs/PoseWithCovarianceStamped | Pose AMCL ước lượng trong map |
| `/particle_cloud` | nav2_msgs/ParticleCloud | Phân bố giả thuyết pose của AMCL |
| `/plan`, `/local_plan` | nav_msgs/Path | Đường toàn cục và đường local của DWB |
| `/global_costmap/costmap`, `/local_costmap/costmap` | nav_msgs/OccupancyGrid | Chi phí tránh vật cản |
| `/undock` | irobot_create_msgs/action/Undock | Rời dock trước khi chạy |
| `/navigate_to_pose` | nav2_msgs/action/NavigateToPose | Goal, feedback, kết quả Nav2 |

TF chính: `map → odom → base_link → rplidar_link`. Frame sensor còn có alias Gazebo
`turtlebot4/rplidar_link/rplidar` được nối bằng static TF của package chính thức.
`map → odom` do SLAM phát khi mapping, AMCL phát khi localization. Hai node không chạy
đồng thời. `odom → base_link` từ odometry controller; `base_link → sensor` từ mô hình.

## 3. Quá trình xây dựng bản đồ

Khởi chạy world maze và SLAM Toolbox, undock, dùng teleop để đi chậm qua các hành lang,
quay nhìn các mặt tường và đi vòng về vùng cũ. Odometry cung cấp dự đoán chuyển động;
scan matching hiệu chỉnh pose theo các scan. Mỗi pose và ràng buộc tương đối tạo thành
pose graph; loop closure thêm ràng buộc khi nhận ra vùng đã đi và tối ưu graph để giảm
drift. Từ scan đã gắn pose, hệ thống dựng occupancy grid ở resolution 0.05 m/pixel.

Quan sát map trên RViz trong suốt quá trình: vùng xám là chưa quan sát, trắng là trống,
đen là vật cản. Phải khảo sát phần lớn vùng robot đi được, không chỉ diện tích nhìn
thấy từ một điểm; kiểm tra tường kép, hành lang lệch hoặc đứt gãy. Chỉ chụp toàn map
và ghi hoàn thành sau khi đã kiểm tra thực tế.

`map_saver_cli` lưu `/map` thành `map.pgm` và metadata `map.yaml`. YAML gồm `image`,
`resolution`, `origin`, `negate`, `occupied_thresh`, `free_thresh`, `mode`. Origin
chỉ pose của gốc grid trong frame map; PGM dùng hệ dòng ảnh từ trên xuống. Đây không
phải file SDF và không phải pose graph SLAM đã serialize.
Script dùng free_thresh 0.196 và occupied_thresh 0.65 để pixel xám 205 của PGM trinary
vẫn là unknown sau khi load lại; kiểm tra round trip được ghi cùng bằng chứng.

## 4. Localization sau khi restart

Dừng SLAM và simulator, khởi động lại đúng world/model/spawn, load map vừa lưu.
map_server cung cấp map cố định; AMCL dự đoán phân bố pose từ odometry, so sánh LiDAR
với map để tính trọng số particle, resample và ước lượng pose. Dùng 2D Pose Estimate
đặt pose gần vị trí/hướng thực tế để tránh hội tụ vào vị trí sai trong maze có cấu trúc
lặp lại. Particle cloud thu hẹp và laser khớp tường là dấu hiệu localization tốt;
so sánh robot trên RViz với Gazebo tại nhiều điểm, không chỉ nhìn particles.
Đặc biệt, undock trong bản Create 3 này quay robot khoảng π rad. Nếu đặt initial
pose sau undock thì phải dùng hướng thực tế đó, không dùng lại yaw spawn bằng 0.

Frame odom liên tục nhưng drift; frame map ổn định theo bản đồ và có thể hiệu chỉnh
gián đoạn. AMCL phát map→odom để robot có pose trong map mà không làm odom mất liên tục.
Không dùng tọa độ ground truth Gazebo làm localization thay cho AMCL.

## 5. Nav2 lập kế hoạch và điều khiển

RViz Nav2 Goal gửi action NavigateToPose. bt_navigator dùng behavior tree để yêu cầu
planner_server tìm global path, rồi controller_server bám đường và kiểm tra đích.
Global costmap kết hợp map tĩnh, scan vật cản và inflation; NavFn cấu hình Dijkstra
(`use_astar=false`) tìm đường trên lưới chi phí. `allow_unknown=false` tránh lập đường
qua vùng chưa khảo sát.

Local costmap rolling window dùng frame odom, cập nhật LiDAR gần robot. DWB lấy mẫu
các vận tốc, mô phỏng các trajectory ngắn hạn, chấm điểm theo khoảng cách đường/goal,
vật cản, hướng và dao động, rồi chọn lệnh hợp lệ. velocity_smoother làm mượt lệnh,
phát `/cmd_vel` cho Create 3. Inflation radius 0.45 m tạo chi phí quanh vật cản;
robot radius 0.19 m bảo vệ footprint. Costmap là mô hình tránh vật cản; không bảo đảm
thành công nếu sensor/TF/localization sai.

Behavior tree có thể yêu cầu replan, clear costmap, spin, backup, wait khi lỗi.
Recovery cũng tự động; sinh viên không điều khiển thủ công sau khi gửi goal.
Goal checker dùng tolerance x/y 0.25 m, yaw 0.25 rad, nên thành công không yêu cầu
tâm robot trùng goal tuyệt đối. Action status 4 là SUCCEEDED; 5/6 không phải thành công.

## 6. Nội dung cần hiểu

**Đề được cung cấp chưa có danh sách câu hỏi “Nội dung cần hiểu”.** Các câu dưới đây
là kiến thức ôn tập, cần bổ sung câu hỏi đúng nguyên văn từ giảng viên trước khi nộp.

- **SLAM khác localization thế nào?** SLAM đồng thời ước lượng pose và tạo/cập nhật
  map; localization ước lượng pose trên map đã có, không tạo lại map tĩnh.
- **Vì sao odometry chưa đủ?** Sai số tích lũy từ tích phân chuyển động; LiDAR và
  map/loop closure giúp hiệu chỉnh drift.
- **Vì sao cần TF?** Scan ở frame sensor, odometry ở odom, goal ở map. TF cho phép
  đưa các dữ liệu về cùng hệ tại đúng timestamp. Chỉ có topic mà thiếu TF vẫn lỗi.
- **Vì sao dùng use_sim_time?** Timestamp của scan/TF/Gazebo phải cùng clock; trộn
  thời gian máy và thời gian simulator gây transform extrapolation/timeouts.
- **Global/local planner khác nhau?** Global tìm tuyến đi dài tới goal trên map;
  controller local chọn vận tốc khả thi theo vật cản gần robot và đường toàn cục.
- **Map khác costmap?** Map lưu hình học/occupancy; costmap thêm chi phí, robot size,
  inflation và vật cản quan sát hiện tại để hỗ trợ planning/control.
- **Vật cản mới khi map không đổi?** AMCL vẫn dùng map cố định; obstacle layer cập
  nhật vật cản mới từ LiDAR để Nav2 tránh/replan.
- **PGM/YAML có đủ để tiếp tục SLAM?** Đủ cho map_server/AMCL; tiếp tục tối ưu pose
  graph SLAM cần serialize graph và dữ liệu tương ứng.
- **Thế nào là goal đạt?** Action SUCCEEDED, robot dừng trong tolerance, không va chạm;
  có video/log. Gửi action được chấp nhận chưa chứng minh đã đến đích.

## 7. Kết quả và minh họa

Kết quả thực tế được ghi tại [VALIDATION.md](../artifacts/VALIDATION.md). Bổ sung vào
PDF ảnh Gazebo/RViz khi mapping, toàn map, AMCL sau restart và 3 goal thành công.

Map đã lưu có 401×401 pixel, resolution 0.05 m; vùng sàn trống được quan sát khoảng
76.8% theo đối chiếu gần đúng với world. Save/load giữ nguyên 67.189 ô unknown.
Ba goal action kiểm thử (-2,-3,0), (2,-3,0), (-2,4,π/2) đều SUCCEEDED. Sai số goal
trong map lần lượt 0.216/0.250/0.235 m, trong tolerance 0.25 m; vị trí AMCL lệch
Gazebo 0.067/0.020/0.056 m. Không ghi nhận BUMP/STALL trong các goal.
Ảnh map và đường đi trong PDF được vẽ từ dữ liệu ROS thực tế; không phải screenshot RViz.

| Goal | Khu vực, x/y/yaw trong map | Kết quả | Bằng chứng video |
| --- | --- | --- | --- |
| 1 | Chưa ghi goal RViz thực tế | Chưa nghiệm thu | Chưa có |
| 2 | Chưa ghi goal RViz thực tế | Chưa nghiệm thu | Chưa có |
| 3 | Chưa ghi goal RViz thực tế | Chưa nghiệm thu | Chưa có |

## 8. Link nộp bài và nguồn

- Video Google Drive public: **chưa cung cấp/upload**.
- Repository GitHub Public: **chưa cung cấp/publish**.
- [TurtleBot 4 simulator](https://turtlebot.github.io/turtlebot4-user-manual/software/turtlebot4_simulator.html)
- [TurtleBot 4 navigation](https://turtlebot.github.io/turtlebot4-user-manual/tutorials/navigation.html)
- [SLAM Toolbox](https://github.com/SteveMacenski/slam_toolbox)
- [Nav2 concepts](https://docs.nav2.org/jazzy/getting_started/navigation_concepts/)

Lệnh Humble và tên plugin được đối chiếu source cài trên máy; tài liệu Nav2 mới hơn
có thể dùng cú pháp khác. Video action/script kiểm thử không thay thế demo goal RViz.
