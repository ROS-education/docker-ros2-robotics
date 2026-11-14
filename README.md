# Docker ROS 2 Robotics Development Environment

[![ROS 2 Distro](https://img.shields.io/badge/ROS%202-Lyrical%20%2F%20Jazzy-orange.svg)](https://docs.ros.org/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-26.04%20Resolute-E95420.svg)](https://ubuntu.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)
[![Desktop](https://img.shields.io/badge/Desktop-Openbox%20%2B%20Tint2-green.svg)](http://openbox.org/)

สภาพแวดล้อมสำหรับการพัฒนาหุ่นยนต์ด้วย **ROS 2 (Lyrical Luth / Jazzy Jalisco)** บนคอนเทนเนอร์ Docker แบบเบาเร็ว (Lightweight), ปรับแต่งมาเพื่อความคล่องตัว มีหน้าจอ Desktop ผ่าน Web noVNC, TigerVNC, Web VS Code (code-server), และ Antigravity CLI พร้อมสำหรับการเชื่อมต่อฮาร์ดแวร์จริง

---

## 🌟 จุดเด่น (Key Features)

- **Lightweight Modern Desktop (Openbox + Tint2):**
  - ใช้ **Openbox Window Manager** ร่วมกับแถบงาน **Tint2 Taskbar** แทน Desktop Environment ขนาดใหญ่ กินทรัพยากรต่ำ ตอบสนองรวดเร็ว
  - รองรับ Virtual Desktops 4 หน้าจอ พร้อมปุ่มลัดสลับหน้าจอ `[ 1 ] [ 2 ] [ 3 ] [ 4 ]` บนแถบ Taskbar ด้านล่าง
  - **ป้องกันการเผลอสลับหน้าจอ:** ปิดการเปลี่ยนหน้าจอด้วยลูกกลิ้งเมาส์ (Scroll Wheel) บนพื้นหลัง เพื่อให้การซูมมุมมองใน RViz2 หรือโปรแกรมกราฟิกทำงานได้อย่างราบรื่น
- **Web Desktop ผ่าน noVNC (1080p Standard):**
  - เข้าใช้งานหน้าเดสก์ท็อปผ่านเบราว์เซอร์ได้ทันทีที่พอร์ต `6901`
  - ล็อคความละเอียดมาตรฐาน **1920x1080 (Full HD)** พร้อมวอลเปเปอร์มาสคอตทางการของ ROS 2 จัดกึ่งกลางสวยงาม
- **Web IDE (code-server):**
  - พัฒนาโค้ดผ่านเบราว์เซอร์ด้วย VS Code (code-server v4.23.1) ที่พอร์ต `8008`
- **Antigravity CLI (`agy`):**
  - ติดตั้ง Antigravity CLI พร้อมแมป Volume `~/.gemini` เพื่อแชร์คอนฟิก, ประวัติ, ทักษะ (Skills) และข้อมูลการยืนยันตัวตนร่วมกับเครื่องโฮสต์โดยตรง
- **เครื่องมือพัฒนาและหุ่นยนต์ครบครัน:**
  - **Terminator** (Multiplexing Terminal ปรับปรุง Bubblewrap sandbox permissions แล้ว)
  - **Xfe** (File Manager น้ำหนักเบา)
  - **X File Editor (`xfwrite`)** (ตัวแก้ไขโค้ดและข้อความ)
  - **rqt** และ **RViz2** พร้อมโหลด ROS 2 Environment อัตโนมัติ
- **เมนูคลิกขวา (Right-Click Menu):**
  - รวมชอร์ตคัตเปิดโปรแกรมสำคัญและสลับ Desktop ได้สะดวก
- **Robotics Hardware Passthrough:**
  - ตั้งค่าสิทธิ์ `privileged: true` และส่งผ่าน `/dev`, สิทธิ์กลุ่ม `dialout`, `video`, `i2c` สำหรับเชื่อมต่อเซ็นเซอร์ LiDAR, กล้อง, ไมโครคอนโทรลเลอร์ (Arduino/ESP32), หรือหุ่นยนต์ Kobuki / TurtleBot

---

## 🚀 การติดตั้งและเริ่มต้นใช้งาน (Quick Start)

### 1. ความต้องการของระบบ (Prerequisites)
- ติดตั้ง **Docker** และ **Docker Compose**

### 2. ดาวน์โหลดและสร้าง Image
```bash
git clone https://github.com/wn1980/docker-ros2-jazzy.git
cd docker-ros2-jazzy/desktop
```

สร้าง Docker Image:
```bash
docker compose build
```

### 3. รันคอนเทนเนอร์
```bash
docker compose up -d
```

ตรวจสอบสถานะการทำงาน:
```bash
docker compose ps
```

---

## 🌐 พอร์ตและการเข้าใช้งาน (Access & Services)

| บริการ (Service) | URL / ที่อยู่เชื่อมต่อ | บัญชี / รหัสผ่าน | คำอธิบาย |
| :--- | :--- | :--- | :--- |
| **noVNC Web Desktop** | [http://localhost:6901](http://localhost:6901) | *ไม่ต้องใส่รหัสผ่าน* | หน้าจอเดสก์ท็อปผ่านเบราว์เซอร์ (1080p) |
| **code-server (VS Code)** | [http://localhost:8008](http://localhost:8008) | *ไม่ต้องใส่รหัสผ่าน* | Web IDE สำหรับเขียนโค้ดและเปิดเทอร์มินัล |
| **Native TigerVNC** | `localhost:5901` (Display `:9`) | *ไม่ต้องใส่รหัสผ่าน* | สำหรับโปรแกรม VNC Viewer ภายนอก |
| **SSH Server** | `ssh ubuntu@localhost -p 3333` | `ubuntu` / `ubuntu` | Remote Terminal พร้อมสิทธิ์ Sudo (NOPASSWD) |

---

## 🖥️ การใช้งานเดสก์ท็อป (Desktop Usage)

### การสลับหน้าจอเสมือน (Virtual Desktops)
- **แถบ Taskbar ด้านล่าง:** คลิกปุ่มตัวเลข `[ 1 ] [ 2 ] [ 3 ] [ 4 ]`
- **เมนูคลิกขวา:** คลิกขวาบนพื้นที่ว่างบนเดสก์ท็อป -> เลือก **Switch Desktop**
- **คีย์ลัด (Keyboard Shortcuts):**
  - `Super + F1` ถึง `Super + F4`: สลับไปยัง Desktop 1, 2, 3, 4 โดยตรง
  - `Ctrl + Alt + Left / Right`: เลื่อนสลับ Desktop ซ้าย-ขวา

### เมนูคลิกขวา (Right-Click Context Menu)
คลิกขวาที่ใดก็ได้บนหน้าจอว่างเพื่อเปิดเมนู:
1. **Terminator** — เทอร์มินัลแยกหน้าต่างได้หลายจอ
2. **File Manager (Xfe)** — ตัวจัดการไฟล์
3. **X File Editor** (`xfwrite`) — ตัวแก้ไขเท็กซ์ไฟล์/โค้ดอย่างเร็ว
4. **rqt** — เครื่องมือ GUI วิเคราะห์ระบบของ ROS 2
5. **RViz2** — ตัวแสดงผล 3D เซ็นเซอร์และโมเดลหุ่นยนต์
6. **Switch Desktop** — สลับ Desktop 1-4

---

## 📁 โครงสร้างโปรเจกต์ (Project Structure)

```text
docker-ros2-jazzy/
├── desktop/
│   ├── docker-compose.yml          # Compose service configuration (host network, privileged)
│   └── image/
│       ├── Dockerfile              # Dockerfile (Ubuntu 26.04 Resolute / ROS 2 Lyrical, Openbox, code-server)
│       ├── index.html              # noVNC entrypoint with scale-fit viewing
│       └── app/
│           ├── bg.png              # ROS 2 Lyrical mascot artwork (1920x1080)
│           ├── supervisord.conf    # Supervisor process manager config
│           ├── bin/
│           │   ├── xsession.sh     # Desktop session launcher (Openbox, Tint2, RandR watcher)
│           │   └── xvnc.sh         # Xvnc TigerVNC server launcher (1080p, display :9)
│           ├── conf.d/             # Supervisor program definitions (sshd, vnc, novnc, code-server)
│           ├── openbox/
│           │   ├── menu.xml        # Custom Openbox right-click application menu
│           │   └── rc.xml          # Openbox window manager configuration & keybindings
│           ├── tint2/
│           │   └── tint2rc         # Tint2 taskbar theme with [1][2][3][4] desktop buttons
│           └── install/            # Robot driver installation scripts (YDLIDAR, TurtleBot2, Kobuki)
└── README.md
```

---

## 🤖 สคริปต์ติดตั้งฮาร์ดแวร์หุ่นยนต์เพิ่มเติม (Optional Robot Scripts)

ภายในคอนเทนเนอร์มีสคริปต์เสริมสำหรับติดตั้งไดรเวอร์และแพ็กเกจหุ่นยนต์ยอดนิยม อยู่ในโฟลเดอร์ `/app/install/`:
- **YDLIDAR Driver:** `/app/install/ydlidar.sh`
- **TurtleBot 2:** `/app/install/turtlebot2.sh`
- **Kobuki Base:** `/app/install/kobuki-ros-jazzy.sh`

---

## 🤝 การเปิดเผยการพัฒนาด้วย AI (AI Development & Human Verification Disclosure)

โปรเจกต์นี้ได้รับการพัฒนาและปรับปรุงระบบ (Modernization & Re-engineering) โดยใช้ **AI Assistant (Google DeepMind Antigravity)** เป็นผู้ช่วยในการวิเคราะห์, ออกแบบโครงสร้างระบบ, ปรับเปลี่ยน Window Manager มาเป็น Openbox + Tint2, ติดตั้งเครื่องมือพัฒนา, และเขียนสคริปต์คอนฟิกกูเรชันอัตโนมัติ

> **การทดสอบและตรวจสอบโดยมนุษย์ (Human-in-the-Loop Verification):**
> 
> ซอร์สโค้ด, Dockerfile, สคริปต์รันระบบ, การเชื่อมต่อพอร์ต ตลอดจนฟังก์ชันการทำงานทั้งหมดบน GUI และคอนเทนเนอร์จริง **ได้รับการทดสอบ ใช้งานจริง และตรวจสอบความถูกต้องซ้ำอีกครั้งโดยผู้พัฒนาที่เป็นมนุษย์ (Human Maintainer)** เพื่อให้มั่นใจในความเสถียร ประสิทธิภาพ และความปลอดภัยในการใช้งานจริง

---

## 📄 ใบอนุญาต (License)

โปรเจกต์นี้เผยแพร่ภายใต้ใบอนุญาต [Apache License 2.0](LICENSE) หรือตามใบอนุญาตของต้นฉบับซอฟต์แวร์ที่เกี่ยวข้อง
