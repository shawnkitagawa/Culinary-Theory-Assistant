
export type Question = {
    question: string;
    top_k: number;
    strictness: "strict" | "balanced" | "creative" | "recipe"
    response_language: "auto" | "english" | "japanese",
}


export type Answer = {

    answer: string;
    sources: [
        {
            chunk_id: string;
            document_title: string;
            page_start: number;
            page_end: number;
            distance: number;
            similarity: number
        }
    ]

}

export type ChatMessage = {
    role: "user" | "assistant";
    content: string;
    source?: string;
};


export type Chat = {
    id: number;
    title: string;
    created_at: number;
    messages: ChatMessage[];
}
