# INT3505E 2 Demo: Hệ thống thư viện đơn giản

- [INT3505E 2 Demo: Hệ thống thư viện đơn giản](#int3505e-2-demo-hệ-thống-thư-viện-đơn-giản)
  - [Thông tin chung](#thông-tin-chung)
  - [Tài liệu thiết kế](#tài-liệu-thiết-kế)
  - [Setup](#setup)
    - [Backend](#backend)
    - [Frontend](#frontend)
  - [Run](#run)
    - [Backend](#backend-1)
    - [Frontend](#frontend-1)
  - [Testing](#testing)
    - [Backend API Testing with Postman](#backend-api-testing-with-postman)
    - [Backend API Testing with Newman](#backend-api-testing-with-newman)
    - [CI/CD](#cicd)

![demo image](docs/images/frontend_demo_1.png)

![demo image](docs/images/backend_demo_1.png)

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

## Testing

### Backend API Testing with Postman

Import the JSON file `<project_root>/src/backend/tests/postman/Test_Library_API_VuTungLam.postman_collection.json`
into Postman as a Collection, then run it.

![Backend API Testing with Postman](docs/images/backend_api_testing_postman.png)

### Backend API Testing with Newman

First, install Newman

```sh
npm install -g newman
```

Run the tests:

```sh
cd <project_root>
cd src/backend

newman run ./tests/postman/Test_Library_API_VuTungLam.postman_collection.json
```

Result:

![Backend API Testing with Newman](docs/images/backend_api_testing_newman.png)

### CI/CD

Backend API Testing with Newman has been added to this
project's GitHub Actions workflow.

To run the workflow locally for debugging purpose, install
[`nektos act`](https://nektosact.com/installation/index.html),
then run:

```sh
cd <project_root>

act
```
