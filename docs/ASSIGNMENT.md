# Đề bài: TurtleBot 4 — SLAM Toolbox, localization và Nav2

Sử dụng TurtleBot 4 trong môi trường mô phỏng để xây dựng bản đồ bằng SLAM Toolbox,
lưu bản đồ và sử dụng bản đồ đã tạo để thực hiện localization và autonomous navigation
với Nav2. Có thể sử dụng một trong các môi trường mô phỏng có sẵn của TurtleBot 4.

## Phần 1 — TurtleBot 4 Simulation

Khởi chạy TurtleBot 4 trong Gazebo. Kiểm tra:

- Robot xuất hiện và hoạt động bình thường.
- LiDAR được publish trên `/scan`.
- Odometry được publish trên `/odom`.
- Robot nhận được lệnh vận tốc.
- Robot và dữ liệu sensor được hiển thị trên RViz2.

Được phép sử dụng launch/configuration có sẵn trong các package TurtleBot 4,
không cần tự xây dựng simulator hoặc controller.

## Phần 2 — Xây dựng bản đồ bằng SLAM Toolbox

Khởi chạy SLAM Toolbox. Điều khiển robot bằng teleoperation để khảo sát và xây dựng map.

- Khảo sát phần lớn khu vực có thể di chuyển.
- Bản đồ thể hiện các tường, hành lang và vật cản chính.
- Không có lỗi nghiêm trọng như tường bị nhân đôi hoặc các khu vực lệch rõ rệt.
- Theo dõi quá trình xây dựng map trên RViz2.
- Lưu bản đồ tối thiểu gồm `map.yaml` và `map.pgm`.

## Phần 3 — Localization

- Dừng SLAM sau khi hoàn thành mapping.
- Khởi động lại robot trong cùng môi trường.
- Load bản đồ vừa tạo và khởi chạy localization.
- Kiểm tra vị trí robot trên bản đồ tương ứng với vị trí thực tế trong Gazebo.

## Phần 4 — Navigation với Nav2

Khởi chạy Nav2 với bản đồ đã tạo. Sử dụng công cụ Nav2 Goal trên RViz2:

- Thực hiện thành công navigation goal tại các khu vực khác nhau.
- Không điều khiển robot thủ công sau khi đặt goal.
- Robot tự lập kế hoạch, di chuyển đến goal mà không va chạm.

## Nội dung nộp

1. Video demo quá trình mapping, bản đồ hoàn chỉnh trên RViz2, load lại bản đồ,
   localization và hoàn thành ít nhất 03 navigation goal. Upload Google Drive và
   chia sẻ công khai.
2. GitHub repository Public chứa source, launch, `map.yaml`, `map.pgm`, configuration
   nếu có và README hướng dẫn cài đặt/chạy.
3. Một PDF ngắn mô tả cấu trúc chương trình; node/package/topic chính; quá trình mapping,
   localization; cách Nav2 lập kế hoạch và điều khiển; trả lời phần “Nội dung cần hiểu”;
   hình minh họa; link video và GitHub.

Được phép dùng tài liệu, Internet và AI hỗ trợ, nhưng sinh viên phải hiểu và giải thích
được chương trình, node, topic và pipeline nộp.

**Thông tin còn thiếu trong đề được cung cấp:** danh sách câu hỏi cụ thể của phần
“Nội dung cần hiểu”. Báo cáo hiện có các câu hỏi ôn tập, cần bổ sung câu hỏi chính thức.
