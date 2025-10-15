const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default function HomePage() {
    if (!API_BASE_URL) {
        return "Bạn chưa gán đầy đủ biến môi trường!";
    }

    return <>
        <h1>{"Chào mừng đến với Hệ thống quản lý thư viện sách!"}</h1>
        <div>
            <p>{"Hãy xem tùy chọn các mục ở sidebar bên trái."}</p>
            <p><a target="_blank" href={API_BASE_URL}>Truy cập backend server</a></p>
        </div>
    </>
}
