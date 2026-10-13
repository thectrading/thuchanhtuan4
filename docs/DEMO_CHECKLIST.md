# Kịch bản quay và điều kiện nghiệm thu

1. Hiện world maze trong Gazebo, TurtleBot 4, RViz có RobotModel/scan; kiểm tra `/scan`,
   `/odom`, `/cmd_vel`; undock và chạy teleop ngắn để thấy chuyển động.
2. Hiện node SLAM Toolbox; quay quá trình khảo sát bằng teleop qua nhiều nhánh hành lang.
   Hiện map đang mở rộng trên RViz và cuối cùng phóng toàn map, kiểm tra tường không kép.
3. Dừng robot, lưu `map.yaml` + `map.pgm`; hiện hai file và YAML với đúng đường dẫn ảnh.
4. Dừng SLAM/Gazebo; chạy lại cùng world. Hiện map đã load, AMCL active, 2D Pose Estimate,
   laser trùng tường, particles hội tụ, vị trí RViz khớp Gazebo.
5. Tắt teleop. Dùng Nav2 Goal trong RViz: goal 1, chờ SUCCEEDED; goal 2 tại vùng khác;
   goal 3 tại vùng khác nữa. Quay đường đi và robot tự tránh vật cản, dừng ở mỗi đích.
6. Hiện README, map, cấu hình và báo cáo; upload Drive và kiểm tra quyền public.

Đối với từng goal ghi: tọa độ map (x, y, yaw), vùng, status, thời gian, khoảng sai lệch
cuối, có/không va chạm và tên đoạn video làm bằng chứng. Không tự điền SUCCESS.

| Hạng mục | Bằng chứng cần có |
| --- | --- |
| Simulator/sensor/teleop | Video Gazebo+RViz, output kiểm tra topic |
| Mapping | Video teleop, toàn map RViz, map thật |
| Restart/localization | Video dừng SLAM, restart, AMCL/laser |
| Goal 1/2/3 | RViz Goal, chuyển động tự động, status SUCCEEDED |
| Nộp bài | Drive public, GitHub public, PDF chứa link thật |

Lệnh gợi ý ghi rosbag phục vụ kiểm tra (không thay video):

```bash
ros2 bag record -o artifacts/rosbag_navigation /scan /odom /tf /tf_static /map \
  /amcl_pose /plan /cmd_vel /cmd_vel_nav /navigate_to_pose/_action/status
```

Khuyến nghị dùng OBS hoặc công cụ screen recorder sẵn có để quay Gazebo và RViz song
song. Nếu cắt đoạn chờ dài, ghi rõ tốc độ phát; giữ đoạn gửi goal, di chuyển và kết quả.

Ba pose đã đạt trong kiểm thử action của map kèm package: (-2,-3,0), (2,-3,0),
(-2,4,π/2). Có thể đặt các vị trí tương ứng bằng Nav2 Goal khi quay; kiểm tra lại nếu
thay map. Nếu đặt initial pose sau undock, chú ý robot đã quay khoảng 180°.
