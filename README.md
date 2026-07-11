# DevOps Intern Project: Automated Server Info Dashboard

Dự án mô phỏng luồng CI/CD thực tế cho ứng dụng Python/Flask: đóng gói bằng Docker, kiểm thử tự động, và triển khai tự động lên Ubuntu Server (VMware) mỗi khi có thay đổi code, thông qua GitHub Actions self-hosted runner.

---

## 📌 1. Tổng quan kiến trúc hệ thống

- **Môi trường Local (Windows):** Lập trình ứng dụng `app_web.py`, viết test, cập nhật `Dockerfile`.
- **Kho chứa trung tâm (GitHub):** Quản lý phiên bản mã nguồn, chứa workflow CI/CD.
- **Self-hosted Runner (chạy trên chính Ubuntu Server):** Lắng nghe sự kiện push lên nhánh `main`, tự động: chạy test → build Docker image → deploy container mới.
- **Ubuntu Server (VMware, mạng NAT, môi trường lab nội bộ):** Nơi ứng dụng thực sự chạy, phục vụ trên cổng 80.

> Lưu ý: Vì VM chạy ở chế độ NAT (không có IP public), pipeline dùng **self-hosted runner** cài đặt ngay trên VM này, thay vì GitHub-hosted runner (vốn không thể SSH ngược vào máy sau NAT).

---

## 🛠️ 2. Công nghệ sử dụng

- **Hệ điều hành:** Ubuntu Server (ảo hóa qua VMware).
- **Công cụ DevOps:** Docker, Git, GitHub Actions (CI/CD), self-hosted runner.
- **Ngôn ngữ & Framework:** Python 3.9, Flask, Pytest.
- **Môi trường tương tác:** VS Code (Remote SSH), PowerShell.

---

## 🚀 3. Pipeline CI/CD hoạt động như thế nào

File cấu hình: [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)

Mỗi khi có lệnh `git push origin main`, pipeline tự động thực hiện:

1. **Checkout code** mới nhất về workspace của runner.
2. **Cài dependencies** từ `requirements.txt`.
3. **Chạy test** (`tests/test_app.py`) — nếu test fail, pipeline dừng lại ngay, **không deploy bản lỗi**.
4. **Build Docker image**, gắn 2 tag: `devops-demo-app:<commit-sha>` (để rollback khi cần) và `devops-demo-app:latest`.
5. **Gỡ container cũ** (chỉ container tên `devops-demo-app`, không ảnh hưởng container khác trên server).
6. **Chạy container mới** trên cổng 80.
7. **Dọn dẹp** các Docker image cũ không dùng nữa.

Toàn bộ 7 bước trên chạy tự động — không cần SSH thủ công vào server nữa.

---

## ⚙️ 4. Cài đặt self-hosted runner (thực hiện 1 lần)

```bash
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64.tar.gz -L <link_từ_GitHub>
tar xzf ./actions-runner-linux-x64.tar.gz
./config.sh --url https://github.com/<user>/<repo> --token <token>
sudo ./svc.sh install
sudo ./svc.sh start
```

Runner chạy dưới user thường (không phải root), nên cần thêm user vào group `docker` để gọi được lệnh Docker mà không cần `sudo`:

```bash
sudo usermod -aG docker $USER
```

---

## ↩️ 5. Rollback khi bản mới bị lỗi

Vì mỗi image được build đều gắn tag theo mã commit, có thể quay lại bản trước đó bằng cách chạy lại image cũ:

```bash
docker rm -f devops-demo-app
docker run -d --name devops-demo-app -p 80:5000 devops-demo-app:<commit-sha-cũ>
```

---

## 🧪 6. Chạy test thủ công (không qua CI/CD)

```bash
pip install -r requirements.txt pytest
pytest -v
```

---

## 📂 7. Cấu trúc thư mục

```
.
├── .github/workflows/deploy.yml   # Cấu hình CI/CD
├── app_web.py                     # Flask app
├── Dockerfile
├── requirements.txt
└── tests/
    └── test_app.py                # Test tự động
```
