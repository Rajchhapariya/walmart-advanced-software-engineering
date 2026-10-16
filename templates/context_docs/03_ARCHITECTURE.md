# System Architecture & Technical Specifications

**Architecture Paradigm:** Decoupled Micro-modular / Modular Monolith  
**Primary Stack:** Python 3.11 (FastAPI) | TypeScript (React) | PostgreSQL 16 | Redis

---

## 1. High-Level System Context

```
+-------------------------------------------------------------+
|                     Client Web Layer                        |
|       (React / Vite / Tailwind / Lucide Icons)              |
+------------------------------+------------------------------+
                               | HTTPS / WSS
                               v
+-------------------------------------------------------------+
|                     API Gateway / Router                    |
|             (FastAPI / Pydantic V2 / CORS / Auth)           |
+------------------------------+------------------------------+
                               |
       +-----------------------+-----------------------+
       |                                               |
       v                                               v
+-----------------------------+         +-----------------------------+
|    Synchronous Domain Core   |         |   Asynchronous Task Worker  |
|  - Auth & User Session      |         |  - Background Ingestion     |
|  - Real-time CRUD Operations|         |  - External API Dispatchers |
+--------------+--------------+         +--------------+--------------+
               |                                       |
               +-------------------+-------------------+
                                   |
                                   v
+-------------------------------------------------------------+
|                     Persistence Layer                       |
|   - PostgreSQL (Relational Data, ACID Transactions, 3NF)    |
|   - Redis (Session Cache, Token Bucket Rate Limiting)       |
+-------------------------------------------------------------+
```

---

## 2. Decoupling & Design Patterns

- **Strategy Pattern:** Isolates vendor-specific logic (e.g. LLM providers, database drivers) behind abstract interfaces.
- **Factory Pattern:** Centralizes dynamic instantiation and dependency injection.
- **Repository Pattern:** Abstracts raw SQL / ORM operations from domain service logic.

---

## 3. Data Flow & Concurrency Controls

- **Connection Management:** Connection pool configured with `pool_size=20, max_overflow=10, pool_timeout=30`.
- **Idempotency:** All mutation endpoints require an `Idempotency-Key` header to prevent duplicate execution.
- **Rate Limiting:** Token-bucket rate limiter enforces 60 requests/minute per authenticated client.
