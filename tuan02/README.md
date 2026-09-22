# Tuần 02: Big-O và chọn cấu trúc dữ liệu


## Bài 1. Chẩn đoán và sửa Big-O

### 1. Đề bài

Cho script tìm phần tử chung giữa hai danh sách 100.000 phần tử bằng hai vòng lặp lồng nhau (O(n²)). Viết lại bằng `set` để đạt O(n), dùng `timeit` đo cả hai và báo cáo số lần tăng tốc.

### 2. Phương pháp

**`find_common_nested` (O(n²)).** Với mỗi phần tử của `list_a`, duyệt lần lượt `list_b` để tìm phần tử bằng nó, nếu thấy thì thêm vào kết quả và `break`.

**`find_common_set` (O(n)).** Chuyển `list_b` thành `set`, rồi duyệt `list_a` và kiểm tra từng phần tử có nằm trong `set` hay không.

```python
def find_common_set(list_a, list_b):
    set_b = set(list_b)
    return [item for item in list_a if item in set_b]
```

**Vì sao Big-O giảm:** `set` là bảng băm nên kiểm tra một phần tử có mặt hay không chỉ mất O(1) trung bình thay vì phải quét cả list O(n), do đó n lần kiểm tra chỉ tốn O(n) thay vì O(n²).

### 3. Thiết lập thí nghiệm

- Dữ liệu: hai list n phần tử, lấy bằng `random.sample` từ `range(2n)` với seed cố định (42). Cách này cho khoảng n/2 phần tử chung, nên bài kiểm tra tính đúng đắn có ý nghĩa.
- Kiểm tra đúng đắn: dùng `assert` so sánh kết quả hai hàm (kể cả thứ tự) ở n = 100, 1.000 và 3.000.
- Đo thời gian bằng `timeit.repeat` và lấy giá trị nhỏ nhất: nested đo 3 lần (mỗi lần 1 lượt gọi), set đo 5 lần (mỗi lần 20 lượt gọi, lấy trung bình mỗi lượt).
- Nested được đo ở n = 1.000 đến 8.000. Với n = 100.000, bản nested không chạy trực tiếp mà được ước tính bằng cách ngoại suy bậc hai từ n = 8.000. Bản `set` được đo trực tiếp ở n = 100.000.

### 4. Kết quả

Kiểm tra tính đúng đắn:

```
[OK] n=  100: giống nhau, 52 phần tử chung
[OK] n=1,000: giống nhau, 499 phần tử chung
[OK] n=3,000: giống nhau, 1,514 phần tử chung
```

Thời gian đo được:

| n | nested (s) | set (s) | Tăng tốc |
|---|---|---|---|
| 1.000 | 0,035687 | 0,000091 | ×393 |
| 2.000 | 0,150655 | 0,000301 | ×501 |
| 4.000 | 0,588764 | 0,000578 | ×1.019 |
| 8.000 | 2,537183 | 0,001430 | ×1.774 |

Ở n = 100.000:

| Phương pháp | Thời gian | Ghi chú |
|---|---|---|
| set | 0,026926 s | đo trực tiếp, 50.034 phần tử chung |
| nested | khoảng 396,4 s (≈ 6,6 phút) | ước tính, ngoại suy n² từ n = 8.000 |
| Tăng tốc | khoảng ×14.723 | ước tính |

### 5. Phân tích

- Với nested, mỗi lần n tăng gấp đôi thì thời gian tăng khoảng 4 lần (0,0357 → 0,1507 → 0,5888 → 2,5372 s, tỉ lệ lần lượt khoảng 4,2, 3,9 và 4,3). Đây là dấu hiệu thực nghiệm của O(n²).
- Với set, thời gian tăng chậm hơn nhiều theo n (từ 0,000091 s lên 0,001430 s khi n tăng 8 lần), phù hợp với O(n).
- Vì hai tốc độ tăng khác nhau, mức tăng tốc lớn dần theo n: ×393 ở n = 1.000, ×1.774 ở n = 8.000 và khoảng ×14.723 ở n = 100.000.
- Cái giá của `set` là tốn thêm bộ nhớ O(n) và yêu cầu phần tử phải hashable.

### 6. Hạn chế

- Thời gian nested ở n = 100.000 là ước tính, chưa đo trực tiếp. Ngoại suy bậc hai có thể thấp hơn thực tế vì list lớn không còn nằm gọn trong bộ nhớ đệm CPU, nên số đo thật có thể lớn hơn 396,4 s.
- Nested chỉ đo 3 lần ở mỗi kích thước nên vẫn có nhiễu; thời gian tuyệt đối phụ thuộc máy, còn tỉ lệ giữa hai phương pháp ổn định hơn.

## Bài 2. Chọn đúng cấu trúc dữ liệu cho 3 tình huống

### (a) Hàng đợi tác vụ xử lý theo thứ tự đến

**Cấu trúc:** `collections.deque`

```python
from collections import deque

queue = deque()
queue.append("task1")        # enqueue: O(1)
queue.append("task2")
queue.append("task3")
while queue:
    task = queue.popleft()   # dequeue: O(1), vào trước ra trước (FIFO)
    print("xử lý", task)
```

**Big-O thao tác chủ đạo:** `append` và `popleft` đều O(1).

**Vì sao:** cần thêm ở một đầu và lấy ở đầu kia theo thứ tự FIFO nên chọn `deque`, vì `list.pop(0)` phải dịch chuyển toàn bộ phần tử nên mất O(n).

### (b) Đếm 10 từ khóa xuất hiện nhiều nhất trong file log

**Cấu trúc:** `dict` dưới dạng `collections.Counter`

```python
from collections import Counter

def top_keywords(path, k=10):
    counts = Counter()
    with open(path, encoding="utf-8") as f:
        for line in f:                    # đọc từng dòng, không nạp cả file vào RAM
            counts.update(line.split())   # mỗi lần cộng 1: O(1) trung bình
    return counts.most_common(k)          # O(M log k), M = số từ khác nhau
```

**Big-O thao tác chủ đạo:** đếm toàn bộ là O(N) với N là tổng số từ. Bước lấy top k là O(M log k), thường nhỏ hơn nhiều vì M ≤ N và k = 10.

**Vì sao:** bài toán là ánh xạ từ khóa sang số lần xuất hiện nên chọn cấu trúc băm `dict`/`Counter`, vì mỗi lần cập nhật chỉ tốn O(1) thay vì phải tìm trong list mất O(n).

### (c) Kiểm tra "user-id này đã xử lý chưa?" trên luồng dữ liệu lớn

**Cấu trúc:** `set`

```python
processed = set()

def handle(user_id):
    if user_id in processed:      # kiểm tra tồn tại: O(1) trung bình
        return False              # đã xử lý, bỏ qua
    processed.add(user_id)        # thêm: O(1) trung bình
    return True
```

**Big-O thao tác chủ đạo:** `in` và `add` đều O(1) trung bình (trường hợp xấu nhất O(n) khi va chạm băm, hiếm gặp). Bộ nhớ là O(số id đã thấy).

**Vì sao:** chỉ cần trả lời có/không cho câu hỏi tồn tại, không cần thứ tự hay giá trị đi kèm, nên chọn `set`, vì `in` trên list phải quét O(n) mỗi lần và sẽ chậm dần theo luồng dữ liệu.

**Lưu ý mở rộng:** nếu tập id quá lớn để vừa RAM, có thể dùng Bloom filter (chấp nhận một tỉ lệ nhỏ báo nhầm) hoặc kho ngoài như Redis.

### Bảng tóm tắt

| Tình huống | Cấu trúc | Thao tác chủ đạo | Big-O |
|---|---|---|---|
| (a) Hàng đợi FIFO | `deque` | `append` / `popleft` | O(1) |
| (b) Top 10 từ khóa | `Counter` (dict) | đếm từng từ | O(N) tổng, O(1) mỗi lần cập nhật |
| (c) Đã xử lý chưa? | `set` | `in` / `add` | O(1) trung bình |

## Cách chạy

Dự án dùng `uv` để quản lý môi trường. Từ thư mục gốc của dự án:

```bash
uv run python tuan02\src\tuan02\bai2_data_structures.py
```

Chỉ dùng thư viện chuẩn của Python, không cần cài thêm gói.
