import { Thread, Message } from "./interface"

export class ChatApi{

    static async createThread(): Promise<Thread> {
        const url = `/threads/`;
        const response = await fetch(process.env.NEXT_PUBLIC_BASE_API + url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        });
        const result = await response.json();
        if (response.ok) {
            return result as Thread;
        } else {
            throw new Error("Failed to fetch thread");
        }
    }

    static async callChatApi({
        thread,
        messages,
        headers,
        onResponse,
        onError
    }: {
        thread: Thread
        messages: Message[]
        headers: HeadersInit | undefined
        onResponse: ((message: Message) => void) | undefined;
        onError: (error: any) => void
    }): Promise<void> {
        const url = `/threads/${thread.id}/chat/`;
        
        try{
            const response = await fetch(process.env.NEXT_PUBLIC_BASE_API + url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    ...headers
                },
                body: JSON.stringify({messages: messages})
            })
            const result = await response.json();
            if (onResponse) {
                try {
                    await onResponse(result);
                } catch (err) {
                    throw err;
                }
            }
        } catch (err) {
            if (onError) {
                onError(err);
            }
        }
    }
}