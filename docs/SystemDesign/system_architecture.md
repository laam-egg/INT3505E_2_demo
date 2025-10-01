# Kiến trúc hệ thống

Hệ thống được tổ chức theo kiến trúc Client-Server.

- Server/Backend được lập trình bằng Python 3.12+, framework Flask. Có sử
    dụng Swagger (`flask-restx`). Có expose một endpoint riêng để hiển
    thị Swagger UI (tại `/api/docs`) và một endpoint riêng
    để trả về OAS JSON (tại `/api/json`). Tất cả các API
    endpoint đều có prefix là `/api/...`. API tuân thủ
    REST chặt chẽ - đạt RMM level 3, có HATEOAS.
    - [Thiết kế database](./database_design.md)
    - [Tài liệu định nghĩa chi tiết các API](./api_endpoints.md)

- Client/Frontend được lập trình bằng TypeScript, React 18
    (không có SWC). Có sử dụng thư viện `antd` để
    vẽ UI, đặc biệt là hiển thị bảng dữ liệu, ví dụ
    danh sách các đầu sách. Client truy cập tới các API
    endpoints của server để query/mutate dữ liệu. Hiện
    chưa có xác thực quản trị viên (đăng nhập/đăng ký), song
    vẫn có trang quản lý người sử dụng thư viện (patrons).
    Chi tiết giao diện, hành vi của các màn ở frontend
    được định nghĩa trong [tài liệu SRS](../SRS/pages.md).
    (Trong tài liệu cũng ghi rõ sự phân biệt người dùng
    hệ thống/quản trị viên/thủ thư với người sử dụng
    dịch vụ thư viện/patrons).
