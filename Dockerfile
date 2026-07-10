# Sử dụng môi trường Python có sẵn siêu nhẹ
FROM python:3.9-slim

# Chuyển vào thư mục /app bên trong container
WORKDIR /app

# Copy 2 file từ máy tính của Dũng vào trong container
COPY requirements.txt requirements.txt
COPY app.py app.py

# Cài đặt Flask từ file requirements
RUN pip install -r requirements.txt

# Mở cổng số 5000 để giao tiếp với bên ngoài
EXPOSE 5000

# Lệnh để chạy app khi container khởi động
CMD ["python", "app_web.py"]