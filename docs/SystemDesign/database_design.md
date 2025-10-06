# Thiết kế database

Ứng dụng sử dụng database là MongoDB 8.x.
Tài liệu này định nghĩa các schema cho các
collections (bảng) mà ứng dụng sẽ sử
dụng. Mỗi đề mục ghi tên collection
(collection name) sẽ được lưu vào
MongoDB.

Để thuận tiện, schema các collection
được viết dưới dạng TypeScript types.
Tuy vậy, tùy công nghệ backend
(Python/Flask hay gì khác...) thì
cần có chuyển đổi cho phù hợp.

Các schema cũng mặc định luôn có
một trường là `_id: ObjectId`. Tuy
nhiên, khi trả ra DTO gửi về client,
server buộc phải chuyển các ID này
về kiểu string hex, ví dụ `673eb1af0c763fdf2244090f`.

Đối với các ràng buộc có tham chiếu
(references) tương tự như foreign keys
trong SQL, các collection schemas sẽ
định nghĩa trường tham chiếu có kiểu
`string`, chứa ID được tham chiếu
dưới dạng string hex như ví dụ trên.
Chẳng hạn `titleId: string`. Trường hợp
tham chiếu nhiều ID thì trường tham
chiếu vẫn có kiểu `string`, song giá
trị là danh sách các string-hex ID
được tham chiếu, phân cách nhau bởi dấu
phẩy. Nếu không có thì để string rỗng
hoặc null. Ví dụ:

    copyIds=
    copyIds=673eb1af0c763fdf2244090f
    copyIds=673eb1af0c763fdf2244090f,673eb1af0c763fdf2244090e,673eb1af0c763fdf2244090d

Các trường tham chiếu sẽ được
chú thích là `/*ref*/`.

Một số trường khác cũng có ngữ nghĩa
là danh sách các thông tin nào đó.
Các trường như vậy thường được đặt
tên là từ tiếng Anh số nhiều, ví dụ
`authors` là danh sách các tác giả.
Thường các danh sách này khi lưu vào
database sẽ lưu dưới dạng `newline-separated list`,
tức là các thông tin được phân cách
nhau bởi ký tự newline `\n`. Nếu
là danh sách trống thì để string
rỗng hoặc null. Ví dụ với code
TypeScript:

```typescript
const authorsToSaveIntoDb = `Arthur\nBob\nCarl\nDavid`;
```

hay code Python:

```typescript
title_tags = "thriller\ncomedy\ndetective"
```

Trên đây là các lưu ý chung. Sau đây là các schema.

## patrons

```typescript
type Patron = {
    name: string,
};
```

## titles

```typescript
type Title = {
    name: string,
    edition: number,
    authors: string, /*newline-separated list*/
    yearOfPublication: number,
    tags: string, /*newline-separated list*/
};
```

## copies

```typescript
type Copy = {
    titleId: string, /*ref*/
    code: string,
};
```

## borrows

```typescript
type Borrow = {
    patronId: string, /*ref*/
    copyId: string, /*ref*/
    status: string, /*"BORROWING", "RETURNED", or "LOST"*/
    createdAt: Date,
    statusLastUpdatedAt: Date,
};
```
