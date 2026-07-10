from flask import Flask
import socket
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def server_info():
    # Lấy tên máy chủ (khi chạy trong Docker, đây sẽ là ID của container)
    hostname = socket.gethostname()
    # Lấy thời gian hiện tại của hệ thống
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Thiết kế giao diện HTML đơn giản
    html_content = f"""
    <div style="font-family: Arial, sans-serif; margin: 40px; padding: 20px; border: 2px solid #4CAF50; border-radius: 10px;">
        <h2 style="color: #4CAF50;">🚀 Hệ thống CI/CD đã hoạt động!</h2>
        <p><b>Trạng thái:</b> Ứng dụng đang chạy mượt mà.</p>
        <p><b>Thời gian máy chủ:</b> {current_time}</p>
        <p><b>Tên máy chủ (Container ID):</b> {hostname}</p>
        <hr>
        <p><i>Dự án DevOps Intern - Phát triển bởi Dũng</i></p>
    </div>
    """
    return html_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)