# Hướng dẫn viết code

## API Versioning

Các API version được định nghĩa và nằm trong
thư mục `<project_root>/app/controllers`. Chỉ
cần tạo thư mục mới có định dạng và code tương
tự các thư mục API version đang có là được.

Lưu ý, các API version khác nhau có thể **dùng**
**chung services**. Xem bên dưới.

## Tách biệt Controller (API) và Service

Các services chứa code thực thi tương ứng
với nghiệp vụ thực sự, nằm trong thư mục
`<project_root>/services`.

Cần phân biệt rõ Controller (API) - giao
diện bên ngoài cho người sử dụng, với
Services - phần code nghiệp vụ. Ví dụ,
nhiều API versions cùng dùng chung
hàm `BookService.get_books` khi cần
lấy danh sách các đầu sách.

Như vậy:

1. KHÔNG viết code xử lý nghiệp vụ trực tiếp
    vào các controllers/API versions. Phải
    viết chúng vào các Services.
2. Các API versions/controllers có thể dùng
    chung Services. Các Services không nhất
    thiết tuân theo số phiên bản của controllers
    hay API versions.
