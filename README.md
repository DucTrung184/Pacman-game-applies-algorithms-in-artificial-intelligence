# 🟡 Pacman AI – A* and BFS Based Ghost Chasing Game

Trò chơi Pacman được phát triển bằng Python, sử dụng thư viện Pygame và tích hợp các thuật toán trí tuệ nhân tạo như A* và BFS để điều khiển hành vi của các ghost.  
Dự án được tổ chức rõ ràng, toàn bộ game chạy trong môi trường Pygame, có hệ thống menu, tutorial, hunt mode, và nhạc nền.

---

## 📌 **Mục tiêu dự án**

- Xây dựng một tựa game Pacman đơn giản nhưng có chiều sâu AI:
  - Sử dụng hình ảnh và âm thanh để tạo trải nghiệm sinh động.
  - Thêm hệ thống menu và hướng dẫn chơi trực quan.
  
- Áp dụng các thuật toán AI:
  - **A\*** để điều khiển ghost đỏ truy đuổi chính xác Pacman.
  - **BFS** cho ghost hồng đuổi Pacman theo chiến lược breadth-first.
  - **BFS + Random** cho ghost cam di chuyển tới điểm ngẫu nhiên và thay đổi mục tiêu định kỳ.

- Tích hợp logic gameplay đặc trưng:
  - **Hunt Mode**: Pacman ăn điểm năng lượng lớn sẽ có thể ăn ngược ghost.
  - Kết hợp nhạc nền riêng cho menu và trong game.

---

## 🗂 Cấu trúc thư mục

<pre> ```
  ├── Pacman-Astar/
  │ ├── Ghost (picture)
  │ ├── Pacman (picture)
  │ ├── Menu (picture, sound)
  │ ├── picture
  │ ├── map.txt
  │ ├── map_loader.py
  │ ├── pacman.py
  │ ├── ghost.py
  │ ├── menu.py
  │ ├── pathfinding.py
  │ └── main.py
  ├── Tutorial.txt
  ├── README.md
  └── requirements.txt 
  ``` </pre>

## 🎮 Giới thiệu

Trò chơi Pac-Man này có 3 màn hình chính:
1. **Menu**: hiển thị hình nền + nhạc nền chào mừng
2. **Hướng dẫn chơi (Tutorial)**: giải thích điều khiển và quy tắc
3. **Trò chơi chính**: người chơi điều khiển Pac-Man bằng các phím mũi tên

## ⚡ Hunt Mode

- Trên bản đồ có các **điểm năng lượng lớn**.
- Khi Pac-Man ăn một điểm lớn, game sẽ chuyển sang **hunt mode** trong **8 giây**:
  - Các ghost sẽ **chạy trốn** thay vì đuổi theo.
  - Pac-Man có thể **ăn ghost**.
- Ghost bị ăn sẽ trở về vị trí hồi sinh.

## ☠️ Kết thúc trò chơi

- Pac-Man **thắng** khi ăn hết các điểm năng lượng.
- Pac-Man **thua** khi bị ghost bắt **3 lần** (mất hết mạng).

## 🎵 Âm thanh & Đồ họa

- Game sử dụng hình ảnh PNG cho Pac-Man, ghost và bản đồ.
- Có nhạc nền `.mp3` khác nhau cho menu và trong game.

## 🕹️ Cách điều khiển

| Phím | Hành động |
|------|-----------|
| `→ ↑ ↓ ←` | Di chuyển Pac-Man |
| `Enter` | Vào màn hình hướng dẫn |
| `S`     | Bắt đầu trò chơi |

## Tác giả

Mai Đình Đức Trung
DucTrung184
