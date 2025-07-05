# 🟡 Pac-Man AI Game

Một phiên bản Pac-Man đơn giản được viết hoàn toàn bằng Python với thư viện Pygame, áp dụng các thuật toán trí tuệ nhân tạo để điều khiển ghost.

## 🎮 Giới thiệu

Trò chơi Pac-Man này có 3 màn hình chính:
1. **Menu**: hiển thị hình nền + nhạc nền chào mừng
2. **Hướng dẫn chơi (Tutorial)**: giải thích điều khiển và quy tắc
3. **Trò chơi chính**: người chơi điều khiển Pac-Man bằng các phím mũi tên

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
  ├── .gitignore
  ├── Tutorial.txt
  ├── README.md
  └── requirements.txt 
  ``` </pre>

## 🧠 AI Ghost Behavior

Trong màn chơi chính, có 3 ghost:
- 👻 **Ghost đỏ** sử dụng thuật toán **A\*** để truy đuổi Pac-Man.
- 👻 **Ghost hồng** sử dụng thuật toán **BFS** để truy đuổi.
- 👻 **Ghost cam** sử dụng BFS nhưng **đi tới một vị trí ngẫu nhiên trên bản đồ**, và thay đổi mục tiêu sau mỗi vài giây.

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

## 🚀 Cài đặt & Chạy

### 1. Cài đặt thư viện

```bash
pip install pygame
