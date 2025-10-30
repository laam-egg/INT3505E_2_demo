export default function Home() {
    return <>
        <h1>Demo đăng nhập</h1>

        <p>Các cách lưu token:</p>

        <ol>
            <li><a href="local_storage">localStorage</a></li>
            <li><a href="session_storage">sessionStorage</a></li>
            <li><a href="httponly_cookie">HTTP-Only Cookie</a></li>
        </ol>
    </>
}
