import type { Question, Answer } from "../type/question"

export async function fetchOutput(question: Question): Promise<Answer> {
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

    const res = await fetch(`${API_BASE_URL}/answer`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(question)
    });

    if (!res.ok) {
        throw new Error("Failed to retrieve AI output");
    }

    return res.json();
}