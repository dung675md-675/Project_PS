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

    # Giao diện HTML: tách CSS riêng để dễ đọc và dễ chỉnh sửa sau này
    html_content = f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <title>Trạng thái hệ thống</title>
        <style>
            /* ---- Bảng màu: chỉ dùng 3 màu chính ---- */
            :root {{
                --color-bg: #FAFAFA;
                --color-text: #1F2937;
                --color-border: #E5E7EB;
                --color-accent: #15803D; /* xanh lá trầm, dùng cho trạng thái "hoạt động" */
            }}

            body {{
                background-color: var(--color-bg);
                color: var(--color-text);
                font-family: -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
                margin: 0;
                padding: 40px 20px;
                display: flex;
                justify-content: center;
            }}

            .status-card {{
                width: 100%;
                max-width: 480px;
                border: 1px solid var(--color-border);
                border-radius: 6px;
                padding: 24px;
            }}

            .status-header {{
                display: flex;
                align-items: center;
                gap: 8px;
                margin-bottom: 20px;
            }}

            .status-dot {{
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background-color: var(--color-accent);
            }}

            .status-title {{
                font-size: 16px;
                font-weight: 600;
                margin: 0;
            }}

            .status-row {{
                display: flex;
                justify-content: space-between;
                padding: 10px 0;
                border-top: 1px solid var(--color-border);
                font-size: 14px;
            }}

            .status-label {{
                color: #6B7280; /* xám nhạt hơn cho nhãn */
            }}

            .status-value {{
                font-family: "SFMono-Regular", Consolas, "Courier New", monospace;
                text-align: right;
            }}

            .status-footer {{
                margin-top: 20px;
                padding-top: 12px;
                border-top: 1px solid var(--color-border);
                font-size: 12px;
                color: #9CA3AF;
                text-align: right;
            }}
        </style>
    </head>
    <body>
        <div class="status-card">
            <div class="status-header">
                <span class="status-dot"></span>
                <p class="status-title">Hệ thống CI/CD đang hoạt động</p>
            </div>

            <div class="status-row">
                <span class="status-label">Trạng thái</span>
                <span class="status-value">Đang chạy ổn định</span>
            </div>
            <div class="status-row">
                <span class="status-label">Thời gian máy chủ</span>
                <span class="status-value">{current_time}</span>
            </div>
            <div class="status-row">
                <span class="status-label">Container ID</span>
                <span class="status-value">{hostname}</span>
            </div>

            <div class="status-footer">
                Dự án DevOps Intern — Phát triển bởi Dũng
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)