# SmartDomain

An AI-powered multi-tenant RAG chatbot platform for intelligent domain assistance.

---

## What it does

SmartDomain lets you create AI chatbots trained on your own documents and websites.
Users can upload PDFs, web pages, plain text, CSV, and Excel files to build a
knowledge base. The system retrieves relevant information using semantic search
and generates accurate answers using large language models.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 16, React 19, TypeScript |
| Styling | Tailwind CSS 4, ShadCN UI |
| Charts | Recharts |
| Graph Visualization | Vis.js, React Force Graph |
| Backend | FastAPI, Python 3.11, Uvicorn |
| Vector Database | Pinecone |
| Database | Supabase (PostgreSQL) |
| Embeddings | Voyage AI (primary), OpenAI (fallback) |
| Reranking | FlashRank (ms-marco-MiniLM-L-12-v2) |
| LLM Providers | Google Gemini, Anthropic Claude, OpenRouter |
| Knowledge Graph | SQLite, NetworkX, Matplotlib |
| Web Scraping | Crawl4AI, Playwright, HTTPX |
| PDF Extraction | PyMuPDF, Tesseract OCR, Pillow |
| Auth | Supabase Auth + JWT (python-jose) |
| Text Chunking | LlamaIndex SentenceSplitter |
| Rate Limiting | SlowAPI |
| Data Processing | Pandas, OpenPyXL |

---

## Key Features

- **Multi-source ingestion** — PDF, URL, plain text, CSV, Excel
- **5-stage RAG pipeline** — embed → search → rerank → prompt → generate
- **Knowledge graph** — LLM extracts subject-relation-object triplets, visualized interactively
- **Multi-tenant architecture** — each bot has isolated Pinecone namespace and Supabase RLS
- **Embeddable chat widget** — paste 2 lines of HTML on any website
- **Multiple LLM providers** — Gemini, Claude, OpenRouter with automatic failover
- **Analytics dashboard** — conversation volume, answer rates, knowledge gaps
- **Widget security** — 2-layer JWT + domain whitelisting system

---

## Project Structure

```
SmartDomain/
├── backend/
│   ├── main.py                 # FastAPI app entrypoint
│   ├── config.py               # Environment variable settings
│   ├── database.py             # Supabase database layer
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # Backend Docker configuration
│   ├── railway.toml            # Railway deployment configuration
│   ├── routers/
│   │   ├── tenants.py          # Bot management endpoints
│   │   ├── sources.py          # Document ingestion endpoints
│   │   ├── chat.py             # Chat and RAG endpoints
│   │   ├── analytics.py        # Analytics endpoints
│   │   ├── graph.py            # Knowledge graph endpoints
│   │   ├── settings.py         # User settings endpoints
│   │   └── widget.py           # Widget initialization endpoint
│   ├── services/
│   │   ├── rag.py              # 5-stage RAG pipeline
│   │   ├── ingestion.py        # Document ingestion pipeline
│   │   ├── embeddings.py       # Voyage AI / OpenAI embeddings
│   │   ├── vector_store.py     # Pinecone vector operations
│   │   ├── graph_service.py    # Knowledge graph extraction
│   │   ├── llm_provider.py     # Multi-provider LLM integration
│   │   └── widget_security.py  # Widget JWT security
│   ├── schemas/                # Pydantic data models
│   └── middleware/
│       └── auth.py             # Supabase JWT verification
├── frontend/
│   ├── app/
│   │   ├── dashboard/
│   │   │   ├── bots/           # Bot management
│   │   │   ├── sources/        # Knowledge source management
│   │   │   ├── analytics/      # Analytics dashboard
│   │   │   ├── graph/          # Knowledge graph visualization
│   │   │   ├── embed/          # Widget embed code generator
│   │   │   └── settings/       # User settings
│   │   └── login/              # Authentication page
│   ├── components/ui/          # ShadCN UI components
│   ├── lib/                    # API client and Supabase helpers
│   └── public/
│       └── widget.js           # Embeddable chat widget script
└── supabase/
    └── schema.sql              # Full PostgreSQL database schema
```

---

## How the RAG Pipeline Works

```
User Query
    ↓
1. Embed Query       — Voyage AI converts query to 1024-dim vector
    ↓
2. Vector Search     — Pinecone retrieves top 10 similar chunks
    ↓
3. Rerank            — FlashRank reorders by relevance, keeps top 5
    ↓
4. Build Prompt      — Context + conversation history + system prompt
    ↓
5. LLM Generate      — Gemini / Claude generates structured JSON response
    ↓
Answer + Sources + Confidence Score
```

---

## How the Ingestion Pipeline Works

```
Source Input (URL / PDF / Text / CSV / Excel)
    ↓
Text Extraction
    ├── URL       — Crawl4AI browser scraper → HTTPX fallback
    ├── PDF       — PyMuPDF text layer → Tesseract OCR fallback
    └── CSV/Excel — Pandas
    ↓
Chunking          — LlamaIndex SentenceSplitter (512 tokens, 50 overlap)
    ↓
Embedding         — Voyage AI voyage-02 → 1024-dimensional vectors
    ↓
Storage
    ├── Pinecone  — Vector embeddings (namespace per bot)
    ├── Supabase  — Source metadata and indexing status
    └── SQLite    — Knowledge graph triplets (subject-relation-object)
```

---

## Setup Guide

### Prerequisites

- Python 3.11+
- Node.js 18+
- [Supabase](https://supabase.com) account (free tier works)
- [Pinecone](https://pinecone.io) account (free tier works)
- [Voyage AI](https://dash.voyageai.com) API key
- At least one LLM API key:
  - [Google Gemini](https://aistudio.google.com) — recommended, free tier available
  - [Anthropic Claude](https://console.anthropic.com)
  - [OpenRouter](https://openrouter.ai)

---

### Step 1 — Supabase Database Setup

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to **SQL Editor** in your Supabase dashboard
3. Copy the full contents of `supabase/schema.sql` and run it
4. Go to **Project Settings → API** and copy:
   - Project URL
   - Anon public key
   - Service role key
   - JWT secret

---

### Step 2 — Pinecone Vector Database Setup

1. Create an account at [pinecone.io](https://pinecone.io)
2. Create a new index:
   - **Dimensions:** `1024`
   - **Metric:** `cosine`
3. Copy your API key and index name

---

### Step 3 — Backend Setup

```bash
cd backend
cp .env.example .env
```

Fill in your `.env` file:

```env
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_role_key
SUPABASE_JWT_SECRET=your_jwt_secret

# LLM Providers (at least one required)
GEMINI_API_KEY=your_gemini_key
ANTHROPIC_API_KEY=your_anthropic_key
OPENROUTER_API_KEY=your_openrouter_key

# Embeddings
VOYAGE_API_KEY=your_voyage_key

# Vector Database
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=your_index_name

# Widget Security
WIDGET_JWT_SECRET=any_random_secret_string

# App
ENVIRONMENT=development
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright browsers (needed for web scraping):

```bash
playwright install chromium
```

Run the backend:

```bash
uvicorn main:app --reload
```

Backend runs at **http://localhost:8000**  
API docs available at **http://localhost:8000/docs**

---

### Step 4 — Frontend Setup

```bash
cd frontend
```

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
```

Install dependencies:

```bash
npm install
```

Run the frontend:

```bash
npm run dev
```

Frontend runs at **http://localhost:3000**

---

## Backend Dependencies

Key Python packages from `requirements.txt`:

| Package | Version | Purpose |
|---|---|---|
| fastapi | latest | REST API framework |
| uvicorn | latest | ASGI server |
| supabase | 2.9.0 | Database and auth client |
| pinecone | 6.0.0+ | Vector database client |
| anthropic | 0.28.x | Claude LLM client |
| google-generativeai | 0.5.x | Gemini LLM client |
| voyageai | 0.3.0+ | Embedding generation |
| flashrank | latest | Cross-encoder reranking |
| llama-index | 0.11.0+ | Text chunking (SentenceSplitter) |
| pymupdf | latest | PDF text extraction |
| crawl4ai | latest | Browser-based web scraping |
| playwright | latest | Browser automation for scraping |
| pytesseract | latest | OCR for scanned PDFs |
| python-jose | 3.3.0 | JWT creation and verification |
| slowapi | 0.1.9 | API rate limiting |
| networkx | latest | Knowledge graph construction |
| pandas | latest | CSV and Excel processing |
| httpx | latest | HTTP client for URL fallback |

---

## Frontend Dependencies

Key packages from `package.json`:

| Package | Version | Purpose |
|---|---|---|
| next | 16.2.0 | React framework |
| react | 19.2.4 | UI library |
| @supabase/supabase-js | 2.48.1 | Supabase client |
| @supabase/ssr | 0.5.2 | Supabase SSR helpers |
| react-hook-form | 7.71.2 | Form handling |
| zod | 4.3.6 | Schema validation |
| recharts | 3.8.0 | Analytics charts |
| react-force-graph-2d | 1.29.1 | Knowledge graph visualization |
| lucide-react | 0.577.0 | Icons |
| sonner | 2.0.7 | Toast notifications |
| tailwindcss | 4.x | Utility CSS framework |

---

## Environment Variables Reference

| Variable | Required | Description |
|---|---|---|
| `SUPABASE_URL` | Yes | Supabase project URL |
| `SUPABASE_ANON_KEY` | Yes | Supabase anonymous public key |
| `SUPABASE_SERVICE_KEY` | Yes | Supabase service role key |
| `SUPABASE_JWT_SECRET` | Yes | Supabase JWT secret |
| `PINECONE_API_KEY` | Yes | Pinecone API key |
| `PINECONE_INDEX_NAME` | Yes | Pinecone index name |
| `VOYAGE_API_KEY` | Yes | Voyage AI embeddings key |
| `GEMINI_API_KEY` | Recommended | Google Gemini API key |
| `ANTHROPIC_API_KEY` | Optional | Anthropic Claude API key |
| `OPENROUTER_API_KEY` | Optional | OpenRouter API key |
| `WIDGET_JWT_SECRET` | Yes | Secret for widget session JWTs |
| `ENVIRONMENT` | Yes | development or production |
| `BACKEND_URL` | Yes | Backend server URL |
| `FRONTEND_URL` | Yes | Frontend server URL |

---

## Authors

Developed by students of Computer Science & Engineering (AI),
Vishwakarma Institute of Technology, Pune.

- Dhananjay Bhagat
- Murali Kulkarni
- Rahul Kuwar
- Kunal Patil
- Tanmay Kawal

---

## License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.
