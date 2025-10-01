# SRS: Các trang/màn/page của ứng dụng

- [SRS: Các trang/màn/page của ứng dụng](#srs-các-trangmànpage-của-ứng-dụng)
  - [Thông tin chung](#thông-tin-chung)
  - [1. Nhóm PATRONS](#1-nhóm-patrons)
    - [R-PATRONS](#r-patrons)
    - [C-PATRON](#c-patron)
    - [U-PATRON(id)](#u-patronid)
  - [2. Nhóm TITLES \& COPIES](#2-nhóm-titles--copies)
    - [R-TITLES](#r-titles)
    - [C-TITLE](#c-title)
    - [U-TITLE(id)](#u-titleid)
    - [R-TITLES(titleId)-COPIES](#r-titlestitleid-copies)
    - [C-TITLES(titleId)-COPIES](#c-titlestitleid-copies)
    - [U-TITLES(titleId)-COPIES(copyId)](#u-titlestitleid-copiescopyid)
  - [3. Nhóm BORROWS](#3-nhóm-borrows)
    - [R-BORROWS(patronIds?)](#r-borrowspatronids)
    - [C-BORROW(titleId?, copyId?)](#c-borrowtitleid-copyid)
    - [U-BORROW(borrowId)](#u-borrowborrowid)
  - [Future Improvements](#future-improvements)

## Thông tin chung

- Đây là tài liệu mô tả các màn giao diện tại frontend.
    KHÔNG mô tả API endpoint, do đó method truy cập luôn là `GET`.
    Tuy vậy, cách đặt URI vẫn nên tuân thủ REST.
- Mỗi màn được ký hiệu/định danh bởi một mã. Quy ước:
  - Các màn xem thông tin (danh sách) có mã bắt đầu bằng `R-` (viết tắt Read)
  - Các màn thêm mới có mã bắt đầu bằng `C-` (viết tắt Create)
  - Các màn xem thông tin và cập nhật (đơn lẻ) có mã bắt đầu bằng `U-` (viết tắt Update) và thường yêu cầu đối số `id`.
  - Mã có tham số bắt buộc thì nên cho làm path param, ví dụ `U-TITLE(id)` nên có URI là `/titles/xxx` với `xxx` là ID của title (đầu sách) tương ứng.
  - Mã có tham số tùy chọn thì nên cho làm query param, ví dụ `C-BORROW(titleId?, copyId?)` nên có URI là `/borrows?titleId=xxx&copyId=yyy`, với `xxx` là ID của đầu sách (title), `yyy` là ID của cuốn sách (copy), và chúng đều là optional (có thể bỏ một trong hai hoặc cả hai).
  - Một số mã có nhiều level tham chiếu đến tài nguyên, thì cũng cần phản ánh chúng đầy đủ trong URI. Chẳng hạn, `U-TITLES(titleId)-COPIES(copyId)` nên có URI là `/titles/xxx/copies/yyy`.

## 1. Nhóm PATRONS

Đây là những màn có nghiệp vụ liên quan đến
quản lý người sử dụng dịch vụ thư viện (patrons).
Phân biệt patrons với "người dùng" là quản trị viên,
thủ thư... - người trực tiếp sử dụng ứng dụng
này.

### R-PATRONS

- Summary: Xem danh sách tất cả các patrons
    đã được ghi lại trên hệ thống.
- Input: Không.
- Output: Danh sách patrons.
  - Có pagination.
  - Mỗi hàng trong danh sách bao gồm:
    - Thông tin patron tương ứng.
    - Nút `Xem tình trạng mượn sách`. onClick: redirect tới trang
        [R-BORROWS(patronIds?)](#r-borrowspatronids) với tham số
        `patronIds` là ID của patron được chọn, ví dụ `patronIds=1`.
    - Nút `Chỉnh sửa`. onClick: redirect tới trang [U-PATRON(id)](#u-patronid) tương ứng.
    - Nút `Xóa`. onClick: hỏi lại, nếu người dùng confirm thì xóa patron tương ứng.

### C-PATRON

- Summary: Thêm patron mới.
- Input:
  - Tên patron
- Output:
  - Patron được thêm mới vào hệ thống.
  - Người dùng được redirect về trang [R-PATRONS](#r-patrons)

### U-PATRON(id)

- Summary: Cập nhật thông tin patron.
- Input:
  - Các thông tin như trong màn [C-PATRON](#c-patron)
- Output:
  - Thông tin patron được cập nhật.
  - Người dùng được redirect về trang [R-PATRONS](#r-patrons)













## 2. Nhóm TITLES & COPIES

Nhóm này bao gồm:

- Những màn có nghiệp vụ liên quan đến
    quản lý đầu sách/tựa sách (titles). Phân biệt
    với từ "sách" hoặc "bản sao" (copies).

- Những màn có nghiệp vụ liên quan đến quản lý các
    bản sao của cùng một tựa sách (title). Tài liệu này
    gọi chúng là "copies", hoặc "bản sao", hoặc "cuốn sách",
    hoặc "sách".

### R-TITLES

- Summary: Xem danh sách tất cả các đầu sách của thư viện, có phân trang (pagination).
- Input: Không.
- Output: Danh sách các đầu sách.
  - Có pagination.
  - Mỗi hàng trong danh sách bao gồm:
    - Thông tin đầu sách tương ứng.
    - Tổng số lượng bản sao (copies) của đầu sách đó.
    - Số copies đang được mượn.
    - Số copies đang được lưu tại thư viện.
    - Số copies đã bị mất.
    - Nếu số copies đang được lưu tại thư viện là 0, làm mờ tên tựa sách (chọn màu xám chẳng hạn). Tuy nhiên không làm mờ những thông tin khác.
    - Nút `Chỉnh sửa`. onClick: redirect tới trang [U-TITLE(id)](#u-titleid) tương ứng.
    - Nút `Xóa`. onClick: hỏi lại, nếu người dùng confirm thì xóa đầu sách tương ứng.
- Yêu cầu khác:
  - Có nút `Thêm mới` để thêm đầu sách mới vào thư viện.
- Chú ý:
  - Xóa đầu sách là xóa bản thân đầu sách đó, và xóa tất cả các copies của đầu sách đó trong thư viện.

### C-TITLE

- Summary: Thêm đầu sách mới.
- Input:
  - Tên tựa sách
  - Tái bản (edition), kiểu số nguyên, ví dụ 1, 2, 3 cho 1st, 2nd, 3rd edition...
  - Các tác giả
  - Năm xuất bản
  - Phân loại (tags)
- Output:
  - Đầu sách được thêm mới vào danh sách.
  - Người dùng được redirect về trang [R-TITLES](#r-titles).

### U-TITLE(id)

- Summary: Cập nhật thông tin đầu sách.
- Input:
  - Các thông tin như trong màn [C-TITLE](#c-title).
- Output:
  - Đầu sách được cập nhật.
  - Người dùng được redirect về trang [R-TITLES](#r-titles).

### R-TITLES(titleId)-COPIES

- Summary: Xem danh sách các sách thuộc cùng tựa sách được
    xác định bởi `titleId`.
- Input:
  - Danh sách các tựa sách.
  - Có pagination.
  - Mỗi hàng trong danh sách bao gồm:
    - Thông tin bản sao tương ứng.
    - Tình trạng: có sẵn/đang được mượn/đã mất, hỏng.
    - Nếu tình trạng là có sẵn:
      - Có nút `Cho mượn`. onClick: redirect tới trang [C-BORROW(titleId?, copyId?)](#c-borrowtitleid-copyid), với tham số titleId, copyId tương ứng với copy của hàng.
    - Nếu tình trạng là đang được mượn, hoặc đã mất/hỏng:
      - Có nút `Xem lượt mượn`. onClick: redirect tới trang [U-BORROW(borrowId)](#u-borrowborrowid), với tham số borrowId tương ứng với copy của hàng.
    - Nút `Sửa`. onClick: redirect tới [U-TITLES(titleId)-COPIES(copyId)](#u-titlestitleid-copiescopyid), truyền vào titleId và copyId tương ứng.
    - Nút `Xóa`. onClick: hỏi lại người dùng, nếu confirm thì xóa bản sao tương ứng.

### C-TITLES(titleId)-COPIES

- Summary: Thêm thông tin một bản sao của một tựa sách.
- Input:
  - titleId: ID của tựa sách, có thể cho chọn dropdown...
  - Mã tựa sách, string.
- Output:
  - Thông tin cuốn sách/bản sao được thêm vào hệ thống.
  - Người dùng được redirect về trang [R-TITLES(titleId)-COPIES](#r-titlestitleid-copies).

### U-TITLES(titleId)-COPIES(copyId)

- Summary: Xem và sửa thông tin một bản sao.
- Input:
  - Các thông tin như trong màn [C-TITLES(titleId)-COPIES](#c-titlestitleid-copies).
- Output:
  - Thông tin cuốn sách được cập nhật.
  - Người dùng được redirect về trang [R-TITLES(titleId)-COPIES](#r-titlestitleid-copies).









## 3. Nhóm BORROWS

Đây là những màn có nghiệp vụ liên quan đến các
lượt mượn sách.

Mỗi lượt mượn sách (Borrow) bao gồm các thông tin sau:

- ID của người mượn - Patron
- ID của cuốn sách - Copy
- Trạng thái - `status` - có thể là đang mượn (`"BORROWING"`), đã trả (`"RETURNED"`), hoặc đã làm mất/hỏng không thể sử dụng được nữa (`"LOST"`).
- Ngày giờ mượn - `createdAt`.
- Ngày giờ cập nhật trạng thái mới nhất (có thể chính là thời điểm mượn, hoặc trả, hoặc thời điểm làm mất/hỏng.) - `statusLastUpdatedAt`.

Như vậy, có thể suy ra logic nghiệp vụ phía backend
như sau (**nếu chỉ vẽ frontend thì không cần quan tâm**):

- Để xác định trạng thái HIỆN TẠI một cuốn sách (copy) là
    có sẵn không/có cho mượn được hay không, ta tìm
    borrow gần nhất (tức `statusLastUpdatedAt` là mới nhất)
    thỏa mãn điều kiện khớp copy ID với cuốn sách đang xét. Có
    thể suy từ trạng thái của borrow tìm được ra trạng thái
    của cuốn sách đó:

    - `borrow.status == "BORROWING"` => sách đang được mượn, không thể cho mượn tiếp.
    - `borrow.status == "RETURNED"` => sách đang có sẵn trong thư viện, có thể cho mượn tiếp.
    - `borrow.status == "LOST"` => sách đã mất, không thể cho mượn tiếp.

    Nếu không tìm được borrow thỏa mãn, tức là sách chưa được
    mượn một lần nào cả. Sách đang có sẵn trong thư viện,
    và có thể cho mượn.

- Để xác định số copies của một đầu sách đang có sẵn/đang được mượn/
    bị mất:
    - Lập danh sách các copies tương ứng với đầu sách (title) đang xét.
    - Với mỗi copy, xác định trạng thái của nó dựa trên borrow gần nhất,
        theo phương pháp đã trình bày ở trên.
    - Tổng hợp, đếm số lượng copy theo từng trạng thái.

Chú ý, thông tin duy nhất
về một lượt mượn mà người dùng có thể thay đổi (sau khi
nó được tạo) là *trạng thái* của nó. Việc sửa đổi trạng
thái được thực hiện qua các nút trên giao diện của trang
[R-BORROWS(patronIds?)](#r-borrowspatronids).

### R-BORROWS(patronIds?)

- Summary: Xem lịch sử mượn sách/danh sách các borrows.
- Input:
  - Trạng thái: Chọn trạng thái của các borrow sẽ hiển thị (tức lọc chúng theo trạng thái).
  - Patrons: Dropdown cho phép chọn nhiều patrons - nếu
    không chọn sẽ không lọc borrows theo patrons, nhưng
    nếu chọn, borrows sẽ được lọc theo các patrons được
    chọn. Dropdown đồng thời cập nhật patronIds tương
    ứng với giá trị đang có trong dropdown. Như vậy,
    nếu khi trang mới tải (on page load) mà query param
    `patronIds?` tồn tại giá trị, thì dropdown cũng có
    giá trị mặc định tương ứng, và áp dụng lọc borrows
    ngay. Định dạng của tham số này là danh sách các
    patron IDs được chọn, phân cách nhau bởi một dấu
    phẩy. Nếu không chọn gì thì để trống. Ví dụ
    `patronIds=`, `patronIds=1`, `patronIds=4,500,78,12`.
- Output: Danh sách các lượt mượn sách (borrows)
  - Xếp theo thứ tự gần nhất trước (`statusLastUpdatedAt DESC`)
  - Có pagination.
  - Mỗi hàng trong danh sách bao gồm:
    - Thông tin lượt mượn tương ứng.
    - Nút `Xem chi tiết`. onClick: redirect đến [U-BORROW(borrowId)](#u-borrowborrowid), với tham số `borrowId` tương ứng với lượt mượn cùng hàng.
    - Nếu trạng thái là `"BORROWING"`, có nút `Trả sách` và nút `Báo mất/hỏng sách`.
    - Nếu trạng thái là `"RETURNED"`, có nút `Cho mượn lại` và nút `Báo mất/hỏng sách`.
    - Nếu trạng thái là `"LOST"`, có nút `Trả/đền sách`.
- Yêu cầu khác:
  - Có nút `Cho mượn sách` để thêm lượt mượn mới. onClick: redirect tới trang [C-BORROW(titleId?, copyId?)](#c-borrowtitleid-copyid), không truyền tham số.
  - Nút `Cho mượn lại` phía trên sẽ redirect tới trang [C-BORROW(titleId?, copyId?)](#c-borrowtitleid-copyid), truyền sẵn `copyId` tương ứng với lượt mượn cũ đó.

### C-BORROW(titleId?, copyId?)

- Summary: Cho mượn sách/Thêm lượt mượn sách mới.
- Giao diện:
  - Có 2 dropdown cho phép người dùng chọn đầu sách (title) trước rồi mới chọn sách (copy) của đầu sách đó.
  - Thực tế, input chỉ yêu cầu copyId, vì từ copyId đã suy ra được titleId.
  - Tuy nhiên, giao diện hiển thị 2 dropdown cho người dùng dễ sử dụng.
  - Nếu query parameter `titleId?` được set, thì dropdown đầu tiên sẽ được chọn mặc định là đầu sách tương ứng.
  - Tương tự, nếu query parameter `copyId?` được set, thì dropdown thứ hai sẽ được chọn mặc định là cuốn sách (copy) tương ứng. Đồng thời, title ID tương ứng với copy này sẽ được set vào dropdown đầu tiên - có thể ghi đè giá trị cũ của dropdown đó nếu trước đó nó đã được set bởi query parameter `titleId?`.
  - Việc chọn "mặc định" này giúp tạo thuận tiện cho người dùng khi click các nút cho mượn (lại) sách ở màn [R-BORROWS(patronIds?)](#r-borrowspatronids), vừa giúp đảm bảo giao diện thống nhất - việc cho mượn sách chỉ cần diễn ra trên cùng một màn.

- Input:
  - ID của copy cho mượn.
  - ID của patron đi mượn.

- Output:
  - Borrow mới được tạo ra với đầy đủ thông tin và được thêm vào hệ thống.
  - Người dùng được redirect về trang [R-BORROWS(patronIds?)](#r-borrowspatronids).

### U-BORROW(borrowId)

- Summary: Xem thông tin và cập nhật trạng thái của lượt mượn sách.
- Giao diện:
  - Hiển thị các thông tin của lượt mượn.
  - Các nút `Trả sách`, `Báo mất/hỏng sách`, `Cho mượn lại`, `Trả/đền sách`
    được hiển thị và có chức năng tương tự như đã trình bày ở mô tả trang [R-BORROWS(patronIds?)](#r-borrowspatronids).
- Input:
  - Hành dộng bấm các nút kể trên.
- Output:
  - Trạng thái của borrow được cập nhật.
  - Người dùng được redirect về [R-BORROWS(patronIds?)](#r-borrowspatronids).







## Future Improvements

**Hiện tại, chưa implement các tính năng/ý tưởng/cải tiến**
**dưới đây.**

Có thể đánh dấu một copy là đã dán nhãn (labelled)
và chưa dán nhãn (unlabelled). Một copy được coi là đã
dán nhãn khi bản cứng của cuốn sách đó đã được dán nhãn
ghi mã copy tương ứng, đóng dấu của thư viện .v.v. Nếu
sách là bản mềm thì có thể coi labelled nghĩa là file PDF
đã được ký số với mã copy tương ứng .v.v. Điều này
giúp thủ thư dễ dàng tạo copies trên hệ thông với số
lượng lớn, sau đó dần dần label các copies, thay vì
phải tạo từng copy một trên hệ thống, label bản vật lý/
bản ký số của nó, rồi tạo thủ công copy tiếp theo...
