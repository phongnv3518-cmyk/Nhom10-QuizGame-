```
  ____    _    _   _____   ______          _____              __  __   ______ 
 / __ \  | |  | | |_   _| |___  /         / ____|     /\     |  \/  | |  ____|
| |  | | | |  | |   | |      / /   ____  | |  __     /  \    | \  / | | |__   
| |  | | | |  | |   | |     / /   |____| | | |_ |   / /\ \   | |\/| | |  __|  
| |__| | | |__| |  _| |_   / /__         | |__| |  / ____ \  | |  | | | |____ 
 \___\_\  \____/  |_____| /_____|         \_____| /_/    \_\ |_|  |_| |______|
                                                                               
```

## Nhóm 10 - Quiz Game Project

### Mô tả dự án
Ứng dụng Quiz Game với kiến trúc client-server, cho phép nhiều người chơi tham gia trả lời câu hỏi trắc nghiệm theo thời gian thực.

### Tính năng
- 🎮 Giao diện đồ họa thân thiện với người dùng
- 🌐 Hỗ trợ nhiều người chơi cùng lúc
- ⏱️ Hệ thống tính điểm theo thời gian
- 📊 Bảng xếp hạng trực tiếp
- 💾 Lưu trữ câu hỏi từ file CSV

### Cấu trúc dự án
```
phong-confi/
├── client/          # Ứng dụng client
├── server/          # Server xử lý game
├── core/            # Logic dùng chung
├── config/          # Cấu hình
└── data/            # Dữ liệu câu hỏi
```

### Cài đặt
```bash
pip install -r requirements.txt
```

### Sử dụng
1. Chạy server:
```bash
python server/server.py
```

2. Chạy client:
```bash
python client/gui_client.py
```