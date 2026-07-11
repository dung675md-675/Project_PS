# DevOps Intern Project: Automated Server Info Dashboard

Dự án mô phỏng luồng triển khai ứng dụng thực tế (Deployment Pipeline) dành cho vị trí **DevOps Intern**. Dự án bao gồm việc đóng gói ứng dụng Python/Flask bằng Docker, quản trị máy chủ ảo hóa Ubuntu Server trên VMware và thiết lập luồng đồng bộ mã nguồn qua Git/GitHub.

---

## 📌 1. Tổng quan kiến trúc hệ thống

- **Môi trường Local (Windows):** Lập trình ứng dụng `app_web.py` và thiết lập `Dockerfile`.
- **Kho chứa trung tâm (GitHub):** Quản lý phiên bản và đồng bộ mã nguồn.
- **Môi trường Production (Ubuntu Server trên VMware):** Kéo code từ GitHub, đóng gói thành Docker Container và chạy ứng dụng trên cổng web 80.

---

## 🛠️ 2. Công nghệ sử dụng

- **Hệ điều hành:** Ubuntu Server 24.04/26.04 LTS (ảo hóa qua VMware).
- **Công cụ DevOps:** Docker, Git, GitHub.
- **Ngôn ngữ & Framework:** Python 3.9+, Flask.
- **Môi trường tương tác:** VS Code (Remote SSH), PowerShell, Google Chrome.

---

## 🚀 3. Hướng dẫn triển khai chi tiết

### Bước 1: Khởi tạo và kết nối máy chủ

1. Cài đặt Ubuntu Server trên VMware với tùy chọn Network Adapter là **NAT**.
2. Đăng nhập vào Ubuntu và mở cổng kết nối từ xa:
   `sudo apt update && sudo apt install openssh-server -y`
3. Trên máy tính Windows, dùng VS Code Terminal kết nối SSH vào máy chủ:
   `ssh dung@192.168.204.131`

### Bước 2: Chuẩn bị mã nguồn

- **app_web.py:** Ứng dụng Flask hiển thị bảng điều khiển thông tin máy chủ (Server Info Dashboard), tự động trích xuất ID của Container và thời gian hệ thống. (Lưu ý: Lưu file chuẩn UTF-8).
- **Dockerfile:** Cấu hình sử dụng image `python:3.9-slim`, cài đặt thư viện từ `requirements.txt` và thiết lập lệnh khởi chạy `app_web.py`.

### Bước 3: Đồng bộ mã nguồn (Local lên GitHub)

Tại Terminal của máy tính Windows (thư mục chứa dự án), chạy các lệnh sau để đẩy code:

- `git add .`
- `git commit -m "Cập nhật mã nguồn dự án"`
- `git push origin main`

### Bước 4: Triển khai ứng dụng (GitHub về Ubuntu Server)

Tại Terminal đang kết nối SSH với máy chủ Ubuntu, thực hiện lần lượt các lệnh:

1. Kéo mã nguồn mới nhất:
   `git pull origin main`
2. Dọn dẹp các container cũ để giải phóng cổng mạng:
   `sudo docker rm -f $(sudo docker ps -qa)`
3. Đóng gói lại Image mới (không dùng cache):
   `sudo docker build --no-cache -t devops-demo-app .`
4. Khởi chạy ứng dụng:
   `sudo docker run -d -p 80:5000 devops-demo-app`

### Bước 5: Kiểm tra kết quả

Mở trình duyệt web (khuyên dùng chế độ Ẩn danh), truy cập vào địa chỉ IP của máy chủ: `http://192.168.204.131` để xem giao diện Dashboard đã được triển khai thành công.
