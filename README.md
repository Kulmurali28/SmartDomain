# SmartDomain

An AI-powered multi-tenant RAG chatbot platform for intelligent domain assistance.

## What it does

SmartDomain lets you create AI chatbots trained on your own documents and websites.
Users can upload PDFs, web pages, plain text, CSV, and Excel files to build a
knowledge base. The system retrieves relevant information using semantic search
and generates accurate answers using large language models.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js, TypeScript, Tailwind CSS, ShadCN UI |
| Backend | FastAPI, Python 3.11 |
| Vector Database | Pinecone |
| Database | Supabase (PostgreSQL) |
| Embeddings | Voyage AI (primary), OpenAI (fallback) |
| Reranking | FlashRank (ms-marco-MiniLM-L-12-v2) |
| LLM Providers | Google Gemini, Anthropic Claude, OpenRouter |
| Knowledge Graph | SQLite, NetworkX, Matplotlib, Vis.js |
| Web Scraping | Crawl4AI, HTTPX |
| PDF Extraction | PyMuPDF, Tesseract OCR |
| Auth | Supabase Auth + JWT |

---

## Key Features

- **Multi-source ingestion** — PDF, URL, plain text, CSV, Excel
- **5-stage RAG pipeline** — embed → search → rerank → prompt → generate
- **Knowledge graph** — LLM extracts subject-relation-object triplets, visualized with Vis.js
- **Multi-tenant architecture** — each bot has isolated vector namespace and row-level security
- **Embeddable chat widget** — paste 2 lines of HTML on any website
- **Multiple LLM providers** — Gemini, Claude, OpenRouter with automatic failover
- **Analytics dashboard** — conversation volume, answer rates, knowledge gaps

---

## Project Structure

## 📁 Project Structure


SmartDomain/
├── backend/
│   ├── main.py                  # FastAPI app entrypoint
│   ├── config.py                # Environment variable settings
│   ├── database.py              # Supabase database layer
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile               # Backend Docker configuration
│   ├── railway.toml             # Railway deployment configuration
│   │
│   ├── routers/                 # API route handlers
│   │   ├── tenants.py           # Bot management endpoints
│   │   ├── sources.py           # Document ingestion endpoints
│   │   ├── chat.py              # Chat and RAG endpoints
│   │   ├── analytics.py         # Analytics endpoints
│   │   ├── graph.py             # Knowledge graph endpoints
│   │   ├── settings.py          # User settings endpoints
│   │   └── widget.py            # Widget initialization endpoint
│   │
│   ├── services/                # Core business logic
│   │   ├── rag.py               # Five-stage RAG pipeline
│   │   ├── ingestion.py         # Document ingestion pipeline
│   │   ├── embeddings.py        # Voyage AI / OpenAI embeddings
│   │   ├── vector_store.py      # Pinecone vector operations
│   │   ├── graph_service.py     # Knowledge graph extraction
│   │   ├── llm_provider.py      # Multi-provider LLM integration
│   │   └── widget_security.py   # Widget JWT security
│   │
│   ├── schemas/                 # Pydantic data models
│   │
│   └── middleware/
│       └── auth.py              # Supabase JWT verification
│
├── frontend/
│   ├── app/
│   │   ├── dashboard/           # Main dashboard pages
│   │   │   ├── bots/            # Bot management
│   │   │   ├── sources/         # Knowledge source management
│   │   │   ├── analytics/       # Analytics dashboard
│   │   │   ├── graph/           # Knowledge graph visualization
│   │   │   ├── embed/            # Widget embed code generator
│   │   │   └── settings/        # User settings
│   │   │
│   │   └── login/               # Authentication page
│   │
│   ├── components/
│   │   └── ui/                  # ShadCN UI components
│   │
│   ├── lib/                     # API client and Supabase helpers
│   │
│   └── public/
│       └── widget.js            # Embeddable chat widget
│
└── supabase/
    └── schema.sql               # PostgreSQL database schema
```
 

## Setup Guide

### Prerequisites

- Python 3.11+
- Node.js 18+
- [Supabase](https://supabase.com) account (free tier)
- [Pinecone](https://pinecone.io) account (free tier)
- [Voyage AI](https://dash.voyageai.com) API key (for embeddings)
- At least one LLM API key:
  - [Google Gemini](https://aistudio.google.com) — recommended, free tier available
  - [Anthropic Claude](https://console.anthropic.com)
  - [OpenRouter](https://openrouter.ai)

---

### Step 1 — Supabase Database Setup

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to **SQL Editor** in your Supabase dashboard
3. Copy the contents of `supabase/schema.sql` and run it
4. From **Project Settings → API**, copy:
   - Project URL
   - Anon public key
   - Service role key
   - JWT secret

---

### Step 2 — Pinecone Vector Database Setup

1. Create an account at [pinecone.io](https://pinecone.io)
2. Create a new index with:
   - **Dimensions:** `1024`
   - **Metric:** `cosine`
3. Copy your API key and index name

---

### Step 3 — Backend Setup

```bash
cd backend
