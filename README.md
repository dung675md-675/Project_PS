# DevOps Intern Project — Automated Server Info Dashboard

Ứng dụng Flask hiển thị trạng thái server, được triển khai tự động qua pipeline CI/CD: mỗi lần push code lên GitHub, hệ thống tự chạy test, build Docker image và deploy lên Ubuntu Server — không cần thao tác thủ công.

## Kiến trúc

```
Local (Windows)  →  GitHub (main)  →  Self-hosted Runner (Ubuntu Server, VMware)
   code + test         source control        test → build → deploy tự động
```

VM chạy ở chế độ mạng NAT (không có IP public), nên pipeline dùng **self-hosted runner** cài đặt ngay trên VM, thay vì GitHub-hosted runner.

## Công nghệ

- **Hạ tầng:** Ubuntu Server (VMware), Docker
- **CI/CD:** GitHub Actions (self-hosted runner)
- **Ứng dụng:** Python 3.9, Flask (trong Docker image)
- **Kiểm thử:** Pytest, chạy bằng Python hệ thống trên runner

## Cấu trúc thư mục

```
.
├── .github/workflows/deploy.yml   # Pipeline CI/CD
├── conftest.py                    # Giúp pytest import đúng module app_web
├── app_web.py                     # Flask app
├── Dockerfile
├── requirements.txt
└── tests/
    └── test_app.py
```

## Pipeline hoạt động thế nào

File cấu hình: [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)

Mỗi lần `git push origin main`, runner trên VM tự động:

1. Checkout code mới nhất.
2. Tạo virtual environment (`venv`) bằng Python hệ thống của VM.
3. Cài `requirements.txt` và `pytest` vào venv.
4. Chạy test (`PYTHONPATH=. pytest -v`) — **nếu test fail, pipeline dừng ngay, không deploy bản lỗi.**
5. Build Docker image, gắn 2 tag: `<commit-sha>` (để rollback) và `latest`.
6. Gỡ container cũ tên `devops-demo-app` (không ảnh hưởng container khác trên server).
7. Chạy container mới trên cổng 80.
8. Dọn Docker image cũ không dùng nữa.

## Cài đặt môi trường (thực hiện 1 lần)

**1. Cài self-hosted runner** — lấy đúng lệnh từ GitHub: repo → _Settings → Actions → Runners → New self-hosted runner_.

**2. Cho runner chạy Docker không cần `sudo`:**

```bash
sudo usermod -aG docker $USER
# đăng xuất / đăng nhập lại để có hiệu lực
```

**3. Cài gói tạo virtual environment** (theo đúng phiên bản Python hệ thống, ví dụ):

```bash
sudo apt install python3.14-venv -y
```

## Chạy test thủ công (không qua CI/CD)

```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt pytest
PYTHONPATH=. ./venv/bin/pytest -v
```

## Rollback

Mỗi image build đều có tag theo mã commit, nên có thể quay lại bản trước đó:

```bash
docker rm -f devops-demo-app
docker run -d --name devops-demo-app -p 80:5000 devops-demo-app:<commit-sha-cũ>
```

## Kết quả

Truy cập `http://<IP-VM>` để xem dashboard hiển thị trạng thái, thời gian và Container ID của bản đang chạy — xác nhận pipeline đã deploy thành công.
