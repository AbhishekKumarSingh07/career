## Solution Document: CricketGPT - Intelligent Cricket Analysis Engine

### 1. Vision & Goals

**Project Vision:** To create an intelligent, conversational AI assistant that provides deep, nuanced analysis of cricket matches by combining structured statistical data with unstructured narrative context.

**Core Goals:**
*   **G-1:** Ingest and process ball-by-ball cricket data from sources like Cricsheet.
*   **G-2:** Allow users to ask complex, natural language questions about players, matches, and scenarios.
*   **G-3:** Provide answers that are more than just stats, incorporating context and analytical insight.
*   **G-4:** Create a scalable backend architecture that can handle a growing dataset and user queries.

---

### 2. High-Level Design (HLD)

The system is designed as a set of microservices communicating via APIs and a shared data layer. This promotes separation of concerns and scalability.

#### 2.1. Architectural Diagram

```
+-----------------+      +-----------------+      +--------------------+
|                 |----->|                 |----->|                    |
|  Cricsheet Data |      |  Data Ingestion |      |  PostgreSQL DB     |
| (YAML/JSON Files)|      | (Python/Celery) |      | (Structured Data,  |
|                 |----->|                 |----->|  Metadata)         |
+-----------------+      +-------+---------+      +----------+---------+
                                 |                           ^
                                 | (Generate Summaries       | (For context)
                                 |  & Embeddings)           |
                                 v                           |
                         +-------+---------+                 |
                         |                 |                 |
                         |  Vector DB      |                 |
                         | (ChromaDB /     |                 |
                         |  Pinecone)      |                 |
                         +-----------------+                 |
                                 ^                           |
                                 | (Semantic Search)         | (Structured Search)
                                 |                           |
+-----------------+      +-------+---------------------------+---------+
|                 |----->|                                             |
|  Frontend       |      |             Core Analytics API              |
| (Streamlit/     |<-----|              (Python/FastAPI)               |
|  Gradio)        |      |                                             |
|                 |      |  [Implements RAG & Hybrid Search Logic]     |
+-----------------+      +---------------------------------------------+
                                 |
                                 | (Prompt + Context)
                                 v
                         +-----------------+
                         |                 |
                         |  LLM Provider   |
                         | (OpenAI/Claude) |
                         +-----------------+
```

#### 2.2. Component Responsibilities

*   **Data Ingestion Service:**
    *   An asynchronous background worker (Celery).
    *   Fetches raw data files from Cricsheet.
    *   Parses the data into a structured format.
    *   Populates the PostgreSQL database with ball-by-ball data and match metadata.
    *   Generates textual summaries for key events (matches, innings).
    *   Creates vector embeddings for these summaries and stores them in the Vector DB.

*   **Core Analytics API:**
    *   A synchronous web service (FastAPI).
    *   Exposes a primary endpoint for user queries.
    *   Orchestrates the Retrieval-Augmented Generation (RAG) pipeline.
    *   Performs hybrid search: filters data using the SQL DB and finds context using the Vector DB.
    *   Constructs prompts and communicates with the external LLM provider.
    *   Formats the final answer and returns it to the user.

*   **Databases:**
    *   **PostgreSQL DB:** The source of truth for structured data. Stores ball-by-ball details, player information, match schedules, etc.
    *   **Vector DB:** Stores text summaries and their corresponding vector embeddings. Enables fast semantic search to find relevant context.

*   **Frontend:**
    *   A simple, lightweight web application (Streamlit is ideal for rapid development).
    *   Provides a user-friendly chat interface to interact with the Analytics API.

#### 2.3. Technology Stack

*   **Backend:** Python 3.10+
*   **API Framework:** FastAPI
*   **Async Worker:** Celery with Redis as a message broker.
*   **Databases:** PostgreSQL, ChromaDB (for local development) / Pinecone (for production).
*   **Data Handling:** Pandas
*   **Gen AI Libraries:** `langchain` or `llama-index`, `openai`
*   **Frontend:** Streamlit

---

### 3. Low-Level Design (LLD)

#### 3.1. Database Schema

**A) PostgreSQL Schema (Simplified)**

```sql
-- Table to store match information
CREATE TABLE matches (
    match_id INT PRIMARY KEY,
    cricsheet_id VARCHAR(20) UNIQUE NOT NULL,
    match_date DATE,
    venue VARCHAR(255),
    team1 VARCHAR(100),
    team2 VARCHAR(100),
    winner VARCHAR(100),
    result_summary TEXT
);

-- Table to store ball-by-ball data
CREATE TABLE deliveries (
    delivery_id SERIAL PRIMARY KEY,
    match_id INT REFERENCES matches(match_id),
    inning INT NOT NULL,
    over INT NOT NULL,
    ball INT NOT NULL,
    batsman VARCHAR(100),
    bowler VARCHAR(100),
    runs_scored INT,
    wicket_type VARCHAR(50),
    is_wicket BOOLEAN DEFAULT FALSE
);
```

**B) Vector Database Document Structure (ChromaDB Collection)**

Each document in the `match_summaries` collection will have:

*   **Content (`page_content`):** A text summary.
    *   *Example:* "In a thrilling encounter at Wankhede, MI chased down 215 against CSK. Suryakumar Yadav's blistering 83 off 35 balls was the highlight, overshadowing Ruturaj Gaikwad's century."
*   **Metadata (`metadata`):** A dictionary linking back to the SQL DB.
    *   *Example:* `{ "match_id": 12345, "source_type": "match_summary", "date": "2023-05-12" }`

#### 3.2. API Endpoint Specification

**Endpoint:** `POST /api/v1/query`

**Request Body (Pydantic Model):**

```python
from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str
    session_id: str | None = None # For conversation history later
```

**Response Body (Pydantic Model):**

```python
from pydantic import BaseModel

class Source(BaseModel):
    match_id: int
    summary: str

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list[Source]
```

#### 3.3. Core RAG Pipeline Logic (in Analytics API)

1.  **Receive Request:** Get the `QueryRequest` object.
2.  **Entity Extraction (Optional but recommended):** Make a preliminary, simple LLM call to extract key entities from the `question`.
    *   *Input Question:* "How did Virat Kohli play against spin in the 2016 IPL?"
    *   *Extracted Entities:* `{ "player": "Virat Kohli", "bowling_type": "spin", "tournament": "IPL", "year": "2016" }`
3.  **Structured Data Retrieval (SQL Query):** Use the extracted entities to query the PostgreSQL `deliveries` table.
    *   `SELECT * FROM deliveries WHERE batsman = 'Virat Kohli' AND ...`
    *   Aggregate this data using Pandas to get key stats (runs, balls, strike rate, dismissals).
4.  **Semantic Context Retrieval (Vector Search):**
    *   Generate an embedding for the user's original `question`.
    *   Query the Vector DB with this embedding to find the top 3-5 most semantically similar match summaries.
5.  **Prompt Construction:** Combine all retrieved information into a single, comprehensive prompt for the main LLM.
    ```
    [System Prompt] You are an expert cricket analyst...

    [User Question] {question}

    [Context from Vector Search]
    - Source 1: {summary_text_1}
    - Source 2: {summary_text_2}

    [Structured Data from SQL]
    Here is the statistical data for the query:
    {pandas_dataframe.to_string()}

    [Instruction] Based on all the above information, provide a nuanced answer.
    ```
6.  **LLM Call:** Send the constructed prompt to the LLM provider (e.g., OpenAI GPT-4).
7.  **Format Response:** Parse the LLM's answer and construct the `QueryResponse` object, including the sources used.

---

### 4. Phased Implementation Plan (Jira Task Breakdown)

This plan is structured into Epics, which can contain multiple user stories or tasks in Jira.

#### **EPIC 1: Project Foundation & Data Ingestion**

*   **TASK-101:** Setup project repository with `pyproject.toml`, virtual environment, and `git`.
*   **TASK-102:** Setup Docker environment with `docker-compose.yml` for PostgreSQL and Redis.
*   **TASK-103:** [DB] Design and implement the PostgreSQL schema (`matches`, `deliveries` tables) using Alembic for migrations.
*   **TASK-104:** [Data] Write a Python script (`scripts/parse_cricsheet.py`) to parse a single Cricsheet YAML file into Pandas DataFrames.
*   **TASK-105:** [Data] Implement the logic to load the parsed DataFrames into the PostgreSQL database.
*   **TASK-106:** [Backend] Setup Celery worker and connect it to the Redis broker.
*   **TASK-107:** [Backend] Create a Celery task `process_match_file(file_path)` that encapsulates the logic from TASK-104 and TASK-105.

#### **EPIC 2: Basic Generative API (No RAG yet)**

*   **TASK-201:** [Backend] Setup a basic FastAPI application with a health check endpoint (`/health`).
*   **TASK-202:** [Backend] Create a simple endpoint `POST /api/v1/summarize_match` that takes a `match_id`.
*   **TASK-203:** [Backend] Implement the logic for this endpoint: fetch match data from PostgreSQL, format it as text, and call an LLM to generate a summary.
*   **TASK-204:** [Infra] Securely manage the `OPENAI_API_KEY` using environment variables and a `.env` file.

#### **EPIC 3: Full RAG Pipeline Implementation**

*   **TASK-301:** [Infra] Add ChromaDB to the `docker-compose.yml` setup.
*   **TASK-302:** [Backend] Modify the Celery ingestion task (TASK-107) to, after saving to SQL, generate a match summary and store it with its embedding in ChromaDB.
*   **TASK-303:** [Backend] Create the `POST /api/v1/query` endpoint in FastAPI with the defined request/response models.
*   **TASK-304:** [Backend] Implement the **Structured Data Retrieval** step (Step 3 in LLD 3.3) within the query endpoint.
*   **TASK-305:** [Backend] Implement the **Semantic Context Retrieval** step (Step 4 in LLD 3.3).
*   **TASK-306:** [Backend] Implement the **Prompt Construction** and **LLM Call** steps (Steps 5 & 6 in LLD 3.3).
*   **TASK-307:** [Testing] Write integration tests for the full RAG pipeline using a sample question.

#### **EPIC 4: Frontend User Interface**

*   **TASK-401:** [Frontend] Setup a new Streamlit application in a separate directory.
*   **TASK-402:** [Frontend] Build the UI: a title, a text input box for the question, and a "Submit" button.
*   **TASK-403:** [Frontend] Implement the logic to call the backend's `/api/v1/query` endpoint when the user submits a question.
*   **TASK-404:** [Frontend] Display the returned `answer` in the UI.
*   **TASK-405:** [Frontend] Prettify the output: display the `sources` used for the answer in an expander or a separate section.

#### **EPIC 5: Enhancements & Scalability (Future Work)**

*   **TASK-501:** [Backend] Implement caching for LLM responses in Redis to reduce costs and latency for repeated questions.
*   **TASK-502:** [Backend] Add basic logging and monitoring to the FastAPI application.
*   **TASK-503:** [Data] Scale the data ingestion to cover all available T20 matches from Cricsheet.
*   **TASK-504:** [AI] Refine the prompt engineering based on test results to improve answer quality.
*   **TASK-505:** [AI] Implement the optional "Entity Extraction" step (LLD 3.3, Step 2) to improve the accuracy of the SQL query.