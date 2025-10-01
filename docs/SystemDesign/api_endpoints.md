# API Endpoints

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

### GET /api/patrons

### GET /api/patrons/:patronId

### POST /api/patrons

### PATCH /api/patrons/:patronId

### DELETE /api/patrons/:patronId

## 2. Nhóm TITLES & COPIES

### GET /api/titles

### GET /api/titles/:titleId

### POST /api/titles

### PATCH /api/titles/:titleId

### DELETE /api/titles/:titleId

### GET /api/titles/:titleId/copies

### GET /api/titles/:titleId/copies/:copyId

### POST /api/titles/:titleId/copies

### PATCH /api/titles/:titleId/copies/:copyId

### DELETE /api/titles/:titleId/copies/:copyId

## 3. Nhóm BORROWS

### GET /api/borrows?patronId

patronId is optional.

### GET /api/borrows/:borrowId

### POST /api/borrows

### PATCH /api/borrows/:borrowId

### DELETE /api/borrows/:borrowId
