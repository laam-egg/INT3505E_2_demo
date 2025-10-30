import { useState } from "react";

export function UserList({
    fetchEmailList,
}: {
    fetchEmailList: () => Promise<string[]>,
}) {
    const [emailList, setEmailList] = useState<string[]>([]);
    const [status, setStatus] = useState<string>("");

    const onRefresh = async () => {
        setStatus("LOADING...");
        setEmailList([]);
        try {
            const newEmailList = await fetchEmailList();
            setEmailList(newEmailList);
            setStatus(`SUCCESS - Last updated: ${new Date().toLocaleTimeString()}`)
        } catch (e: any) {
            setStatus("ERROR: " + e + ". " + (e?.response?.data?.error || ""));
        }
    };

    return <div>
        <h2>{"User List (only authenticated users can see this)"}</h2>

        <div>
            <p>{status}</p>
        </div>

        <div>
            <button onClick={onRefresh}>Refresh</button>
        </div>

        <div>
            <p>{`Total: ${emailList.length}`}</p>
            <ol>
                {emailList.map((email, index) => {
                    return (
                        <li key={index}>{email}</li>
                    );
                })}
            </ol>
        </div>
    </div>;
}
