

export type MesasgeSource = {

    id: number;
    message_id: number;
    document_title: string;
    page_start: number;
    page_end: number;
    similarity: number;
    chunk_text: string;
    created_at: Date;
}