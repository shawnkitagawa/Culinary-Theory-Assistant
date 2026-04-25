create extension if not exists vector;
create extension if not exists pgcrypto;

do $$
begin
    if not exists (select 1 from pg_type where typname = 'documentstatus') then
        create type documentstatus as enum ('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED');
    end if;
end
$$;

create table if not exists public.documents (
    document_id uuid not null default gen_random_uuid(),
    title varchar(255) not null,
    total_page integer not null,
    author varchar(255),
    created_at timestamptz not null default now(),
    published_at timestamptz,
    status documentstatus not null default 'PENDING',
    file_path varchar(255) not null,

    constraint documents_pkey primary key (document_id),
    constraint document_unique unique (title, author, file_path),
    constraint documents_file_path_key unique (file_path)
);

create table if not exists public.chunks (
    chunk_id uuid not null default gen_random_uuid(),
    document_id uuid not null,
    page_start integer not null,
    page_end integer not null,
    chunk_text text not null,
    embedding vector(1536) not null,
    chunk_index integer not null,
    created_at timestamptz not null default now(),

    constraint chunks_pkey primary key (chunk_id),
    constraint document_chunk_index_unique unique (document_id, chunk_index),
    constraint chunks_document_id_fkey foreign key (document_id)
        references public.documents (document_id)
        on delete cascade
);

create index if not exists chunk_embedding_hnsw_idx
on public.chunks
using hnsw (embedding vector_cosine_ops);