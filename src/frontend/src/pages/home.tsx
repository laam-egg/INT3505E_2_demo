export default function HomePage() {
    return <>
    <h1>{"Chào mừng đến với Hệ thống quản lý thư viện sách!"}</h1>
    <div>
        <p>{"Hãy xem tùy chọn các mục ở sidebar bên trái."}</p>
        <p><a target="_blank" href={import.meta.env.VITE_API_BASE_URL}>Truy cập backend server</a></p>
    </div>
    </>
}
