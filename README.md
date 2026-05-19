# 🧩 8-Puzzle Algorithm Visualizer (Bản Tối Ưu Hóa Hệ Thống)

Một ứng dụng mô phỏng trực quan (Visualizer) các thuật toán tìm kiếm không gian trạng thái phổ biến áp dụng vào trò chơi trí tuệ trí tuệ nhân tạo kinh điển: **8-Puzzle (Trò chơi trượt 8 số)**. 

Dự án được xây dựng hoàn toàn bằng ngôn ngữ **Python 3** kết hợp với framework giao diện hiện đại **Flet (Flutter engine cho Python)**. Ứng dụng mang lại một trải nghiệm mượt mà với giao diện Dark Mode, giúp người học dễ dàng quan sát cách các cấu trúc dữ liệu như `Queue`, `Stack` và các tập hợp `Reached (Visited)` vận hành trên thực tế theo từng bước (Step-by-step).

👉 **Link Kho Lưu Trữ GitHub:** [https://github.com/NguyenTrungKien1805/8puzzel_visualizer](https://github.com/NguyenTrungKien1805/8puzzel_visualizer)

---

## 🚀 Các Tính Năng Core Của Ứng Dụng

### 1. Trực Quan Hóa Bàn Cờ Sinh Động (Grid Board Visualizer)
* Hệ thống lưới $3 \times 3$ tự động cập nhật trạng thái các ô số theo thời gian thực.
* Ô trống (`0`) được thiết kế ẩn text và chuyển màu nền sang xám (`grey`) để người dùng dễ dàng định vị tiêu điểm di chuyển, các ô số còn lại mang màu xanh bộ đội/hiện đại (`blue`).

### 2. Tích Hợp 4 Biến Thể Thuật Toán Tìm Kiếm Không Gian
Dự án không chỉ cài đặt thuật toán cơ bản mà chia nhỏ thành các hướng tiếp cận cài đặt thực tế để so sánh:
* **Hàm 1: BFS (Check Đích Lúc POP + Thêm Reached Lúc POP):** Cách tiếp cận lý thuyết cơ bản. Node được kiểm tra xem có phải là Goal hay không chỉ khi nó được đưa ra khỏi hàng đợi `Frontier`.
* **Hàm 2: BFS (Check Đích Lúc PUSH + Thêm Reached NGAY):** Phiên bản tối ưu hóa cực hạn của BFS. Hệ thống kiểm tra điều kiện Goal ngay khi sinh Node con (Push) và đưa thẳng vào tập `Reached`. Giảm thiểu tối đa số lượng Node rác sinh ra trong hàng đợi.
* **Hàm 3: DFS (Tìm Kiếm Theo Chiều Sâu):** Sử dụng cấu trúc `Stack` (`pop` ở cuối danh sách). Khám phá các nhánh trạng thái sâu nhất trước khi quay lui.
* **Hàm 4: IDDFS (Tìm Kiếm Sâu Dần - Iterative Deepening DFS):** Giải pháp tối ưu kết hợp: Vừa đảm bảo tìm ra đường đi ngắn nhất (giống BFS) vừa tiết kiệm bộ nhớ không gian lưu trữ (giống DFS) bằng cách giới hạn độ sâu tịnh tiến liên tục từ tầng $0 \rightarrow 50$.

### 3. Cơ Chế Trộn Hướng Ngẫu Nhiên (`Directions Shuffle`)
* Thay vì cố định thứ tự quét hàng xóm là `[Lên, Xuống, Trái, Phải]`, tại mỗi cấu trúc sinh Node kế tiếp (`next_states`), mảng hướng đi sẽ được xáo trộn bằng hàm `shuffle()`.
* **Ý nghĩa:** Giúp thuật toán DFS không bị "giam cầm" cố định ở một nhánh vô tận, tạo ra sự đột biến ngẫu nhiên về số bước giải qua mỗi lần bấm nút "Giải".

### 4. Bộ Điều Khiển Đa Tiến Trình (Playback Controller)
* **Giải 8 - Puzzle:** Kích hoạt luồng chạy thuật toán, đóng băng trạng thái chờ và kết xuất dữ liệu logs đồng thời.
* **Prev / Next:** Di chuyển thủ công lùi hoặc tiến 1 bước trên cấu trúc cây đường đi đã tìm thấy.
* **Play / Pause:** Sử dụng cơ chế bất đồng bộ `asyncio.sleep(0.5)` để tự động "trình chiếu" bàn cờ mượt mà với tốc độ 500ms/bước.

### 5. Hệ Thống Đồng Hồ Đếm Bước Tối Giản
* Ô hiển thị tiến trình được thiết kế cô đọng theo định dạng phân số: `Hiện tại / Tổng số bước` (Ví dụ: `0 / 14`, `7 / 14`). Giúp người xem nắm bắt ngay lập tức độ dài của chuỗi hành động tối ưu.

### 6. Nhật Ký Kết Xuất Kép (Dual Logs System)
* **Khung Logs Hệ Thống (Phía Trên):** Mô phỏng từng bước lặp `STEP X`. Xuất dữ liệu bảng biểu trực quan gồm 3 cột: `NODE` đang xét, trạng thái toàn bộ `FRONTIER` (Hàng đợi/Ngăn xếp), và tập `REACHED` tại thời điểm đó.
* **Sơ Đồ Dịch Chuyển Ma Trận (Phía Dưới):** In ra toàn bộ chuỗi ma trận tĩnh từ lúc bắt đầu cho tới lúc kết thúc. Đi kèm chỉ dẫn bằng chữ cụ thể như: `Bước 1 (Ô trống dịch chuyển SANG TRÁI)`, `Bước 2 (Ô trống dịch chuyển LÊN (UP))`...

---

## 📊 Bảng So Sánh Đặc Tính Thuật Toán Trong Ứng Dụng

| Thuật toán | Cấu trúc dữ liệu | Thời điểm check Đích | Tính Tối Ưu (Đường đi ngắn nhất) | Sức chịu đựng số lượng Node | Ảnh hưởng bởi `Shuffle` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Hàm 1: BFS (Pop)** | `deque` (Queue - FIFO) | Khi lấy ra khỏi Queue | **Có** | Trung bình (Tốn RAM) | Ít (Chỉ đổi thứ tự Log) |
| **Hàm 2: BFS (Push)**| `deque` (Queue - FIFO) | Khi vừa sinh ra | **Có** | Rất tốt (Tiết kiệm RAM) | Ít (Chỉ đổi thứ tự Log) |
| **Hàm 3: DFS** | `deque` (Stack - LIFO) | Khi lấy ra khỏi Stack | **Không** | Kém (Dễ thám hiểm vô tận)| **Cực kỳ lớn** (Thay đổi số bước đột biến) |
| **Hàm 4: IDDFS** | `deque` lặp tầng depth | Khi lấy ra khỏi Stack | **Có** | Tốt (Tiết kiệm RAM) | Trung bình |

---

## 🛠 Hướng Dẫn Cài Đặt Chi Tiết

### 1. Yêu cầu tiên quyết
Hệ thống máy tính của bạn cần cài đặt sẵn **Python 3.8** hoặc các phiên bản cao hơn. Bạn có thể kiểm tra bằng lệnh:
```bash
python --version

### 2. Cài đặt thư viện Flet
Flet là framework hỗ trợ xây dựng giao diện Flutter bằng mã Python. Mở Terminal / Command Prompt của bạn lên và thực thi lệnh gõ:

Bash
pip install flet==0.22.1
