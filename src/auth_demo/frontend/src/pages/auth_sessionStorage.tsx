import axios from "axios";
import { LoginForm } from "../components/common/login_form";
import { API_BASE_URL } from "../utils/env";
import { UserList } from "../components/common/user_list";

export default function AuthSessionStorage() {
    const onLogin = async ({ email, password } : {
        email: string, password: string,
    }) => {
        const res = await axios.post(`${API_BASE_URL}/by-header/auth/login`, {
            email, password,
        });

        const token = res.data.token;
        if (!token) {
            throw new Error(`No token returned from data: ${res.data}`);
        }

        sessionStorage.setItem('auth', token);
    };

    const fetchEmailList = async () => {
        const token = sessionStorage.getItem('auth');
        let authHeader: string;
        if (token) {
            authHeader = `Bearer ${token}`;
        } else {
            authHeader = "";
        }

        const res = await axios.get(`${API_BASE_URL}/by-header/users`, {
            headers: {
                Authorization: authHeader,
            },
        });
        const list = res.data.content;
        if (!list) {
            throw new Error(`No list returned from data: ${res.data}`);
        }
        return list;
    }

    return <>
        <h1>Auth :: sessionStorage</h1>

        <div>
            <LoginForm onLogin={onLogin} />
        </div>

        <div>
            <UserList fetchEmailList={fetchEmailList} />
        </div>
    </>;
}
