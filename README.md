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

Yêu cầu Python 3.12+.

```sh
cd <project_root>
cd src/backend

virtualenv venv -p $(which python3.12)
source ./venv/bin/activate
pip install -r requirements.txt
```

### Frontend

Yêu cầu Node.js 22+.

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

```sh
cd <project_root>
cd src/frontend

yarn dev
# OR:
yarn build
yarn preview
```
