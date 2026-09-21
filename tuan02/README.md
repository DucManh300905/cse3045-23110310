# Bài 1: So sánh hiệu năng: tìm phần tử chung giữa hai list

## 1. Giới thiệu

Báo cáo này so sánh hai cách tìm các phần tử chung của hai list trong Python: dùng vòng lặp lồng nhau (độ phức tạp O(n²)) và dùng `set` (độ phức tạp O(n) trung bình). Mục tiêu là cài đặt hai thuật toán, kiểm tra chúng cho kết quả giống nhau, rồi đo thời gian chạy bằng `timeit`.

## 2. Bài toán

Cho hai list số nguyên `list_a` và `list_b`, cần trả về các phần tử của `list_a` cũng xuất hiện trong `list_b`, giữ nguyên thứ tự xuất hiện trong `list_a`.

## 3. Phương pháp thực hiện

**Phương pháp 1: vòng lặp lồng nhau (`find_common_nested`).** Với mỗi phần tử của `list_a`, chương trình duyệt lần lượt `list_b` để tìm phần tử bằng nó. Nếu tìm thấy thì thêm vào kết quả và dừng bằng `break`. Độ phức tạp thời gian là O(n²). Vì dữ liệu có rất ít phần tử trùng, hầu hết phần tử của `list_a` không có trong `list_b` nên phải quét hết `list_b`, do đó `break` gần như không giúp giảm chi phí.

**Phương pháp 2: dùng `set` (`find_common_set`).** Chương trình chuyển `list_b` thành `set`, sau đó duyệt `list_a` và kiểm tra từng phần tử có nằm trong `set` hay không. Việc tra cứu trong `set` mất O(1) trung bình nên tổng thời gian là O(n). Đổi lại, phương pháp này tốn thêm O(n) bộ nhớ cho `set`, và các phần tử phải hashable. Thứ tự kết quả vẫn theo `list_a`, giống phương pháp 1.

## 4. Thiết lập thí nghiệm

Dữ liệu được sinh bằng `random.sample(range(SIZE * 2), SIZE)` với `SIZE = 100_000` và seed cố định là 42 để kết quả tái lập được. Tuy nhiên, ở 100.000 phần tử, phương pháp lồng nhau cần khoảng 10¹⁰ phép so sánh nên không thể chạy thực tế trên máy thông thường. Vì vậy phần benchmark chỉ dùng 1.000 phần tử đầu của mỗi list.

Thời gian được đo bằng `timeit.Timer` với `number=1`. Trước khi đo, chương trình kiểm tra tính đúng đắn bằng cách chạy cả hai hàm trên 1.000 phần tử và dùng `assert` để xác nhận hai kết quả bằng nhau.

## 5. Kết quả

```
=== KẾT QUẢ TIMEIT ===
Kích thước dữ liệu thực tế: 100,000 phần tử/list
Kích thước benchmark: 1,000 phần tử/list
Nested loops O(n²): 0.035948 giây
Set O(n):           0.000177 giây
Speedup:             203.56 lần
```

Bài kiểm tra tính đúng đắn đã qua: hai phương pháp cho kết quả giống nhau. Ở n = 1.000, phương pháp lồng nhau mất khoảng 35,9 ms, trong khi phương pháp dùng `set` chỉ mất khoảng 0,177 ms. Như vậy `set` nhanh hơn khoảng 203,56 lần.

## 6. Phân tích

Kết quả phù hợp với lý thuyết. Vòng lặp lồng nhau có thời gian tăng theo bình phương kích thước dữ liệu, còn `set` chỉ tăng tuyến tính, nên khoảng cách giữa hai phương pháp càng lớn khi dữ liệu càng nhiều.

Nếu n tăng từ 1.000 lên 100.000 (gấp 100 lần), phương pháp lồng nhau sẽ chậm đi khoảng 10.000 lần, còn phương pháp `set` chỉ chậm đi khoảng 100 lần. Ngoại suy từ kết quả trên, thời gian ước tính ở 100.000 phần tử là khoảng 6 phút cho phương pháp lồng nhau và khoảng 0,018 giây cho phương pháp `set`, tức chênh lệch cỡ 20.000 lần. Lưu ý đây chỉ là ước tính, chưa được đo thực tế.

## 7. Hạn chế

- Mỗi phương pháp chỉ được đo một lần (`number=1`). Hàm dùng `set` chạy dưới 1 ms nên số đo dễ bị nhiễu, vì vậy con số speedup 203,56 chỉ nên xem là tham khảo về bậc độ lớn.
- Kết quả chỉ được đo ở một kích thước (n = 1.000), chưa đủ để xác nhận bằng thực nghiệm rằng thời gian tăng theo n² và n.
- Bài kiểm tra tính đúng đắn còn yếu. Hai mẫu 1.000 phần tử lấy từ khoảng `range(200_000)` chỉ có khoảng 5 phần tử chung, nên `assert` kiểm tra được rất ít trường hợp.
- Các số liệu cho n = 100.000 là ước tính, không phải kết quả đo trực tiếp.
- Chưa ghi lại môi trường chạy (phiên bản Python, CPU, hệ điều hành). Thời gian tuyệt đối sẽ khác giữa các máy, nhưng tỉ lệ giữa hai phương pháp thì ổn định hơn.

## 8. Hướng cải thiện

- Dùng `timeit.repeat` và lấy giá trị nhỏ nhất, hoặc tăng `number` cho hàm chạy nhanh.
- Đo ở nhiều kích thước (ví dụ 500, 1.000, 2.000, 4.000) và vẽ biểu đồ thời gian theo n.
- Lấy mẫu kiểm thử từ khoảng giá trị nhỏ hơn để có nhiều phần tử chung hơn.
- Thêm các phương pháp khác để so sánh, ví dụ giao hai `set` (`set(a) & set(b)`), lưu ý cách này không giữ thứ tự.


## 9. Kết luận

Với cùng một bài toán, dùng `set` thay cho vòng lặp lồng nhau giúp nhanh hơn khoảng 200 lần ở n = 1.000, và khoảng cách còn tăng khi dữ liệu lớn hơn, đổi lại tốn thêm bộ nhớ. Khi cần kiểm tra sự tồn tại của phần tử nhiều lần trên dữ liệu lớn, nên ưu tiên cấu trúc dùng bảng băm như `set` hoặc `dict`.