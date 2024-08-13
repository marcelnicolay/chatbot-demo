export interface Message {
    role: "user" | "assistant"
    content: string
}

export interface Thread {
    id: string
}