import { useState } from "react"

export function LoginForm({
    onLogin,
} : {
    onLogin: (arg: { email: string, password: string }) => Promise<any>,
}) {
    const [email, setEmail] = useState('...@legit.com');
    const [password, setPassword] = useState('');
    const [status, setStatus] = useState('');

    const onSubmit = async () => {
        setStatus("LOGGING IN");

        try {
            await onLogin({ email, password });
            setStatus(`SUCCEEDED at ${new Date().toLocaleTimeString()}`);
        } catch (e: any) {
            setStatus(`ERROR: ${e}. ${e?.response?.data?.error || ""}`);
        }
    };

    return <div>
        <h2>Login</h2>
        <div>
            <label>Email:</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} />
        </div>

        <div>
            <label>Password:</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
        </div>

        <div>
            <button onClick={onSubmit}>
                Login
            </button>
        </div>

        <div>
            <p>{`${status}`}</p>
        </div>
    </div>
}
