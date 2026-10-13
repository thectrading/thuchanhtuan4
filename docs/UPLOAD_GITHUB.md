# Tự đăng bài lên GitHub

Bộ file đã chuẩn bị nằm tại:

```text
/home/chuc/workspaces/ur_gz/submission_github/turtlebot4_slam_nav/
```

Mở thư mục bằng:

```bash
xdg-open /home/chuc/workspaces/ur_gz/submission_github/turtlebot4_slam_nav
```

1. Đăng nhập GitHub bằng tài khoản muốn nộp bài.
2. Mở https://github.com/new, kiểm tra **Owner**, đặt tên
   `turtlebot4-slam-nav`, chọn **Public** và tạo repository.
3. Trong repository trống, bấm **uploading an existing file**. Nếu repo đã có
   file, chọn **Add file → Upload files**.
4. Trong cửa sổ thư mục đã mở ở trên, chọn các file và thư mục bên trong
   `turtlebot4_slam_nav` rồi kéo vào trang upload. Giữ nguyên cấu trúc thư mục.
   Dùng Ctrl+H để hiện và chọn thêm `.gitignore`.
5. Kiểm tra danh sách upload có `README.md`, `package.xml`, `CMakeLists.txt`,
   `launch/`, `config/`, `rviz/`, `scripts/`, `tools/`, `maps/`, `docs/` và
   `artifacts/`. Trong `maps/` phải có cả `map.yaml` và `map.pgm`.
6. Điền commit message `Add TurtleBot 4 SLAM and Nav2 assignment`, chọn commit
   vào `main` và xác nhận **Commit changes** theo màn hình.
7. Mở lại repository, kiểm tra nhãn **Public**, README và hai file map. Copy
   link repository để điền vào báo cáo và nơi nộp bài.

File `turtlebot4_slam_nav_submission.zip` là bản nén của cùng bộ file. Nếu dùng
ZIP, giải nén trước rồi upload các file/thư mục bên trong. Chỉ upload ZIP sẽ
không hiển thị source, launch và map riêng để người chấm xem trực tiếp.

Repository chứa một ROS package; khi chạy trên workspace mới, đặt nội dung
repository tại `<workspace>/src/turtlebot4_slam_nav`, rồi làm theo README.
Các lệnh ví dụ trong README dùng workspace của máy hiện tại; đổi đường dẫn
theo máy của người chạy.

## Hoàn thiện báo cáo và video

- Chỉnh `docs/BAO_CAO_TURTLEBOT4.docx` hoặc `.doc`: điền họ tên, MSSV, lớp,
  link GitHub thực tế và link Google Drive video thực tế; xuất lại PDF.
- Upload các bản Word/PDF đã sửa vào cùng đường dẫn trên GitHub để cập nhật.
- Video bài nộp cần đủ mapping bằng teleop, bản đồ hoàn chỉnh, restart/load
  map, localization và ít nhất ba goal thành công qua Nav2 Goal trên RViz.
- `videos/PREVIEW_GOAL1.mp4` ở thư mục source trên máy là clip xem thử một
  goal thành công, chưa đáp ứng video toàn bộ bài. Không nằm trong gói upload.
- Đưa video hoàn chỉnh lên Google Drive, chia sẻ cho **Anyone with the link**
  với quyền **Viewer**, rồi kiểm tra link bằng cửa sổ ẩn danh.
- Báo cáo hiện vẫn có các chỗ điền thông tin và mô tả phần demo cần bổ sung.
  Cập nhật đúng những việc đã thực hiện trước khi nộp; bổ sung các câu hỏi
  “Nội dung cần hiểu” nguyên văn của giảng viên nếu có.

GitHub cho upload tối đa 100 file mỗi lần qua trình duyệt, tối đa 25 MiB mỗi
file. Bộ file đã chuẩn bị nhỏ hơn các giới hạn này.

Tài liệu: [upload file](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository),
[tạo repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository).
