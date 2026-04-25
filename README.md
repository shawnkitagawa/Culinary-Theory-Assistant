# Culinary Technique RAG Assistant

A backend-focused AI knowledge assistant that uses Retrieval-Augmented Generation (RAG) to answer culinary technique questions from a custom document-based knowledge base.

This project demonstrates how business documents, manuals, training materials, PDFs, or specialized knowledge sources can be converted into an AI assistant that answers user questions with grounded context.

Although this project uses culinary technique content, the same architecture can be adapted for many business use cases, including customer support bots, employee training assistants, internal documentation search, restaurant training systems, education tools, and PDF-based AI assistants.

This project is designed primarily as a backend AI engineering showcase.

Its core value is in the API design, document processing workflow, vector search pipeline, database integration, LLM response generation, and cloud deployment.

Any frontend included in the project is intentionally lightweight and serves as a simple interface for demonstrating the backend system in action.

---

## Live Demo
[Try the deployed demo](https://culinary-rag-api-724121259172.asia-northeast1.run.app/)
> Note: This demo is deployed on Google Cloud Run. The first request may take a few seconds if the service is waking up from a cold start.


## Project Goal

The goal of this project is to build a backend-driven AI assistant that can:

- answer culinary technique questions from a stored knowledge base
- process culinary text documents into searchable chunks
- generate embeddings from document chunks
- store embeddings in PostgreSQL using pgvector
- retrieve relevant context based on a user's question
- generate grounded AI answers using retrieved document content
- expose the system through FastAPI endpoints
- provide a simple frontend demo for users
- deploy the backend to Google Cloud Run
- demonstrate a reusable architecture for client-facing AI document assistants

This project emphasizes backend system design, API architecture, RAG implementation, vector search, database modeling, and cloud deployment.

The frontend is not the main focus of the project. It is included to make the backend system easier to test, present, and demonstrate.

---

## Core Idea

Many businesses already have valuable knowledge stored in documents, PDFs, manuals, recipes, SOPs, training guides, FAQs, and internal resources.

The problem is that this information is often difficult to search quickly.

This system solves that problem by turning stored documents into a searchable AI knowledge assistant.

Instead of giving a generic AI answer, the system first retrieves relevant information from the custom knowledge base and then uses that context to generate a grounded response.

In simple terms:

```text
Documents → Chunks → Embeddings → Vector Search → Retrieved Context → AI Answer
