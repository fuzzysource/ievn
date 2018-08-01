# IEVN PSSE

> Chương trình tự động hóa một số thao tác của chương trình PSSE
và thống kê khối lượng xây dựng

## Tính năng
- `step1.py`: Tạo file raw từ file `.dxf`.
- `step2.py`: Tính loadflow với loạt file `.raw` tạo ra từ `step1`.
- `tba.py`: Thống kê khối lượng Trạm biến áp, phục vụ quy hoạch (Khó sử
dụng, không đáng tin cậy)

## Yêu cầu
- Python 3.6
- pyautogui
- DOSBOX
- File chạy `psse.exe` của Viện Năng lượng

## Cài đặt
### Python3
Cài đặt **Python3** với bộ cài tại

https://www.python.org/downloads/

### pyautogui
```
C:\Python34\pip.exe install pyautogui
```
### Dosbox

https://www.dosbox.com/

### Cấu trúc thư mục
Tạo các thư mục và copy các file `psse.exe`,`step1.py` và `step1.py` vào theo cấu
trúc sau.
```
<thư mục gốc>
    |__ DWG-R14
    |     |__ SDO
    |          step2.py
    |          *.raw
    |          *.nod
    |         *.are
    |__*.dxf
    |__psse.exe
    |__step1.py
	
```
Thư mục mẫu được đặt tại `chedo` hoặc tải thư mục được cấu trúc sẵn tại
`chedo.zip`.

## Hướng dẫn sử dụng

### Step 1: Tạo file raw:
* Xóa tất cả các file `*.raw` đang có trong thư mục `SDO`, tắt bộ gõ 
Tiếng Việt hoặc chuyển về gõ tiếng Anh.
* Dùng chuột kéo file `psse.exe` ở trong thư mục gốc vào icon `DOSBOX`
 tại desktop.
* Click đúp vào `step1.py`, ấn `OK`, trong 5s di chuột vào cửa sổ chương
trình `psse.exe`
* `step1.py`sẽ tự động tìm tất cả các file `.dxf` và tạo ra file `raw`.
* File `.raw` được đặt tại thư mục `SDO`

### Step 2: Chạy PSSE để tính loadflow
* Mở **PSSE**
* Click vào biểu tượng `CLI`
* Chọn `Run Script`
* Trỏ vào file `step2.py` và OK
* File `.nod` và `.are` được tạo ra tại thư mục `SDO`

## Giấy phép
* `step1.py` và `step2.py` được Đàm Tiến Long tạo ra đầu tiên.
* `psse.exe` là sản phẩm của Viện Năng lượng, không được phân phối tại dự
án này

Toàn bộ mã nguồn và tài liệu của dự án này thuộc về **Public Domain**. Điều đó có nghĩa là người dùng có mọi quyền sử dụng mã nguồn và tài liệu của dự án này vào mục đích của họ mà không có bất kỳ hạn chế nào. Người dùng chịu trách nhiệm về các sử dụng cách thành phần của dự án và sản phẩm tạo ra bằng các thành phần đó.
