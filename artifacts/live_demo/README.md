# Chạy thử lại ngày 13/10/2026

Gazebo Fortress chạy ở chế độ server (`gui:=false`), RViz dùng `rviz/demo.rviz`
với frame rate 15 FPS. Chỉ có một simulator và một nguồn `/clock`.

Đã restart cùng world maze, load map, đặt initial pose tại spawn, undock SUCCEEDED
và chạy ba action NavigateToPose. Không phát lệnh vận tốc thủ công trong các goal.

| Goal | Trạng thái | Sai số vị trí (m) | Thời gian thực (s) |
| --- | --- | --- | --- |
| (-2, -3, 0) | SUCCEEDED | 0.18968 | 52.355 |
| (2, -3, 0) | SUCCEEDED | 0.23182 | 45.022 |
| (-2, 4, π/2) | SUCCEEDED | 0.23936 | 90.693 |

Sai số vị trí và hướng nằm trong tolerance 0.25 m / 0.25 rad. Không có BUMP, CLIFF,
STALL hoặc WHEEL_DROP trong các goal. BACKUP_LIMIT xuất hiện sau undock.
Ground truth chỉ dùng đọc và đối chiếu AMCL.

`navigation_results.json`, `validation.json`, `navigation_probe.txt` và `undock.txt`
ghi kết quả thực tế. Các goal được gửi bằng action; đây không phải bằng chứng thao tác
chuột Nav2 Goal hay xác nhận đã quay được video. Cửa sổ RViz bị dừng trong lần chạy
và được mở lại riêng sau đó; simulator vẫn chạy nền.

Bản đồ, báo cáo và số liệu lần kiểm thử trước được giữ nguyên. Video nộp bài cần
ghi đủ mapping bằng teleop, load map/localization và ba goal qua RViz.
