# API Endpoints (v1)

Dưới đây liệt kê các API endpoints
nhằm phục vụ đầy đủ các màn frontend,
như đã được nêu tại [tài liệu SRS](../SRS/pages.md).
Frontend có những yêu cầu đặc biệt nào
về tham số, thì các API endpoints tương
ứng ở backend phải hỗ trợ những tham
số đó. Đồng thời, các API endpoints có
sự tương ứng với [thiết kế database](./database_design.md),
cả về tên các resource và các trường dữ
liệu cần/có thể xuất hiện.

Định dạng dữ liệu để trao đổi (trong
request và response body) là JSON.

Các endpoints đều RESTful, tuân thủ
RMM level 3, có HATEOAS.

Có thể thêm các API endpoints khác
nếu thấy cần thiết (not recommended).

## 1. Nhóm PATRONS

### GET /api/v1/patrons

### GET /api/v1/patrons/:patronId

### POST /api/v1/patrons

### PATCH /api/v1/patrons/:patronId

### DELETE /api/v1/patrons/:patronId

## 2. Nhóm TITLES & COPIES

### GET /api/v1/titles

### GET /api/v1/titles/:titleId

### POST /api/v1/titles

### PATCH /api/v1/titles/:titleId

### DELETE /api/v1/titles/:titleId

### GET /api/v1/titles/:titleId/copies

### GET /api/v1/titles/:titleId/copies/:copyId

### POST /api/v1/titles/:titleId/copies

### PATCH /api/v1/titles/:titleId/copies/:copyId

### DELETE /api/v1/titles/:titleId/copies/:copyId

## 3. Nhóm BORROWS

### GET /api/v1/borrows?patronId

patronId is optional.

### GET /api/v1/borrows/:borrowId

### POST /api/v1/borrows

### PATCH /api/v1/borrows/:borrowId

### DELETE /api/v1/borrows/:borrowId
