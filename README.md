# Baomoi Crawler

Dự án này giúp bạn lấy dữ liệu từ trang Baomoi.com, bao gồm tiêu đề, mô tả, hình ảnh và nội dung bài viết. Dữ liệu sau khi lấy sẽ được lưu vào file Excel.

## Tính năng

- Lấy đầy đủ dữ liệu từ Baomoi.com:
  - Tiêu đề bài viết
  - Đường dẫn bài viết
  - URL hình ảnh
  - Mô tả (sapo) bài viết
  - Nội dung đầy đủ bài viết
- Hỗ trợ lấy dữ liệu từ nhiều trang
- Tự động lưu dữ liệu vào file Excel
- Lên lịch chạy tự động vào 6h sáng hàng ngày

## Yêu cầu hệ thống

- Python 3.8 trở lên
- Các thư viện Python (được liệt kê trong file requirements.txt)

## Cài đặt

1. Clone repository này về máy của bạn:

```bash
git clone https://github.com/your-username/baomoi-crawler.git
cd baomoi-crawler
```

2. Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

## Cách sử dụng

### Chạy trực tiếp

Để chạy crawler và lấy dữ liệu ngay lập tức:

```bash
python test.py
```

### Tùy chỉnh số trang và số bài viết

```bash
python test.py --pages 3 --articles 10
```

Trong đó:
- `--pages`: Số trang cần lấy (mặc định: 1)
- `--articles`: Số bài viết mỗi trang (mặc định: 10)

### Lên lịch chạy tự động

Để thiết lập crawler chạy tự động vào 6h sáng hàng ngày:

```bash
python test.py --schedule
```

## Cấu trúc thư mục

```
baomoi-crawler/
├── test.py            # Mã nguồn chính
├── requirements.txt   # Danh sách thư viện cần thiết
├── README.md          # Hướng dẫn sử dụng
└── data/              # Thư mục chứa dữ liệu đã lấy
    └── baomoi_data_YYYYMMDD_HHMMSS.xlsx
```

## Cấu trúc dữ liệu

Mỗi bản ghi trong file Excel/CSV bao gồm các thông tin:
- Tiêu đề: Tiêu đề bài viết
- Link: Link đến bài viết gốc
- Ảnh: URL của hình ảnh đại diện
- Mô tả: Tóm tắt nội dung bài viết
- Nội dung: Nội dung đầy đủ của bài viết
- Ngày lấy: Ngày thực hiện lấy dữ liệu

## Tạo Github Repository

1. Đăng nhập vào Github
2. Tạo repository mới với tên "baomoi-crawler"
3. Đặt chế độ Public
4. Push code lên repository:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/baomoi-crawler.git
git push -u origin main
```

## Các lưu ý

- Tôn trọng robots.txt của trang web khi crawl dữ liệu
- Đặt thời gian nghỉ giữa các requests để tránh tạo tải lên máy chủ
- Cập nhật code nếu cấu trúc HTML của trang thay đổi

## Đóng góp

Mọi đóng góp đều được hoan nghênh. Vui lòng tạo issue hoặc pull request để cải thiện dự án.

## Giấy phép

Dự án này được phân phối dưới Giấy phép MIT.
