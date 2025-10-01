# INT3505E 2 Demo: Hệ thông thư viện đơn giản

- [INT3505E 2 Demo: Hệ thông thư viện đơn giản](#int3505e-2-demo-hệ-thông-thư-viện-đơn-giản)
  - [Thông tin chung](#thông-tin-chung)
  - [Tài liệu thiết kế](#tài-liệu-thiết-kế)
  - [Setup](#setup)
    - [Backend](#backend)
    - [Frontend](#frontend)
  - [Run](#run)
    - [Backend](#backend-1)
    - [Frontend](#frontend-1)

## Thông tin chung

- **Sinh viên:** Vũ Tùng Lâm 22028235 UET
- **Yêu cầu đề bài:**
  - Topic: hệ thống thư viện đơn giản bao gồm: quản lý sách, mượn - trả sách.
  - Sử dụng Flask
  - Assignment Link: <https://portal.uet.vnu.edu.vn/courses/3181/assignments/31620>

## Tài liệu thiết kế

- [Đặc tả yêu cầu](./docs/SRS/README.md)
- [Thiết kế hệ thống](./docs/SystemDesign/README.md)

## Setup

### Backend

Yêu cầu Python 3.12+,
MongoDB 8.0+ (các phiên
bản cũ hơn có thể vẫn
chạy được, nhưng chưa được
kiểm chứng.)

```sh
cd <project_root>
cd src/backend

virtualenv venv -p $(which python3.12)
source ./venv/bin/activate
pip install -r requirements.txt
```

Đồng thời trong thư mục `src/backend`,
copy file `.env.example` vào file mới
tên là `.env`. Sửa các biến môi trường
trong file đó cho phù hợp.

### Frontend

Yêu cầu Node.js 22+ (các phiên
bản cũ hơn có thể vẫn
chạy được, nhưng chưa được
kiểm chứng.)

```sh
cd <project_root>
cd src/frontend

yarn
```

## Run

### Backend

```sh
cd <project_root>
cd src/backend
source ./venv/bin/activate

flask run --host=0.0.0.0 --port=5000
```

### Frontend

Sau khi chạy backend, cần tạo lại
OpenAPI contracts:

```sh
cd <project_root>
cd src/frontend

yarn api:sync
```

Từ đó về sau, nếu backend không có
thay đổi về API, có thể chạy frontend
như thông thường:

```sh
cd <project_root>
cd src/frontend

yarn dev
# OR:
yarn build
yarn preview
```
