# CricketGPT - The Intelligent Cricket Analysis Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

CricketGPT is a powerful, conversational AI assistant that provides deep, nuanced analysis of cricket matches. It goes beyond simple statistics by combining structured ball-by-ball data with narrative context, allowing users to ask complex questions and receive expert-level insights.

## Key Features

-   **Natural Language Queries:** Ask complex questions like *"How does Rohit Sharma perform against left-arm pace in the powerplay?"* instead of writing complex SQL.
-   **Deep Analysis:** Get answers that blend statistics with context, identifying trends, turning points, and player-specific patterns.
-   **Retrieval-Augmented Generation (RAG):** Utilizes a state-of-the-art RAG pipeline to ground LLM responses in factual data, reducing hallucinations.
-   **Automated Summaries:** Can generate concise summaries for entire matches or specific innings.
-   **Scalable Architecture:** Built on a modern Python backend stack designed for scalability and maintainability.

## Demo

Here's an example of the kind of interaction you can have with CricketGPT:

```
👤 You:
What was the turning point in the 2011 World Cup final?

🤖 CricketGPT:
The turning point in the 2011 World Cup final can be identified as the partnership between Gautam Gambhir and MS Dhoni.

After losing Sehwag and Tendulkar early, India was under immense pressure at 31/2. Gambhir anchored the innings with a crucial 97. However, the definitive shift occurred when MS Dhoni promoted himself up the order ahead of Yuvraj Singh to counter the spin of Muralitharan.

His unbeaten 91* and the 109-run partnership with Gambhir stabilized the innings and systematically dismantled the Sri Lankan bowling attack, leading India to a historic victory. The final six by Dhoni is the iconic moment, but the strategic foundation was this partnership.
```

## Architecture

The system uses a microservices-based architecture to separate data processing from the query-serving API.

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
                         | (ChromaDB)      |                 |
                         +-----------------+                 |
                                 ^                           |
                                 | (Semantic Search)         | (Structured Search)
                                 |                           |
+-----------------+      +-------+---------------------------+---------+
|                 |----->|                                             |
|  Frontend       |      |             Core Analytics API              |
| (Streamlit)     |<-----|              (Python/FastAPI)               |
|                 |      |                                             |
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

## Technology Stack

-   **Backend:** Python 3.10+
-   **API Framework:** FastAPI
-   **Async Worker:** Celery
-   **Message Broker:** Redis
-   **Databases:**
    -   **Relational:** PostgreSQL
    -   **Vector:** ChromaDB
-   **Data Handling:** Pandas
-   **Gen AI Libraries:** LangChain, OpenAI
-   **Frontend:** Streamlit
-   **Containerization:** Docker

## Getting Started

Follow these instructions to get a local copy up and running.

### Prerequisites

-   Python 3.10+
-   Docker and Docker Compose
-   Git
-   An OpenAI API Key

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/cricket-gpt.git
    cd cricket-gpt
    ```

2.  **Create a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**
    Create a `.env` file in the project root by copying the example file.
    ```sh
    cp .env.example .env
    ```
    Now, edit the `.env` file and add your OpenAI API key:
    ```env
    OPENAI_API_KEY="sk-..."
    ```

5.  **Launch the infrastructure:**
    This will start PostgreSQL, Redis, and ChromaDB in Docker containers.
    ```sh
    docker-compose up -d
    ```

6.  **Run database migrations:**
    (Assuming you are using Alembic for migrations)
    ```sh
    alembic upgrade head
    ```

## Usage

### 1. Ingest Data

First, you need to populate the databases with cricket data.

-   Download ball-by-ball data from a source like [Cricsheet.org](https://cricsheet.org/downloads/) and place it in a directory (e.g., `data/`).
-   Run the ingestion script (this will trigger the Celery workers):

```sh
# Example command
python scripts/ingest_data.py --path ./data/
```

### 2. Run the Application

You need to run the API backend and the Streamlit frontend.

-   **Start the Celery worker (in a separate terminal):**
    ```sh
    celery -A app.workers.tasks worker --loglevel=info
    ```

-   **Start the FastAPI server (in a separate terminal):**
    ```sh
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

-   **Start the Streamlit frontend (in a separate terminal):**
    ```sh
    streamlit run frontend/app.py
    ```

Now, open your browser and navigate to the Streamlit URL (usually `http://localhost:8501`) to start asking questions!

## Project Roadmap

This project is planned in several phases.

-   [x] **Phase 1: Core Backend & Data Pipeline**
    -   [x] Setup project structure and Docker environment.
    -   [x] Implement PostgreSQL schema.
    -   [x] Develop Celery worker for data ingestion from Cricsheet files.
-   [ ] **Phase 2: Basic Generative API**
    -   [ ] Setup FastAPI application.
    -   [ ] Create a simple endpoint for match summarization.
-   [ ] **Phase 3: Full RAG Pipeline**
    -   [ ] Integrate ChromaDB for vector storage.
    -   [ ] Enhance ingestion worker to create and store embeddings.
    -   [ ] Build the core `/api/v1/query` endpoint with hybrid search.
-   [ ] **Phase 4: Frontend User Interface**
    -   [ ] Develop a Streamlit application for user interaction.
    -   [ ] Connect the frontend to the backend API.
-   [ ] **Phase 5: Enhancements & Scalability**
    -   [ ] Implement Redis caching for LLM responses.
    -   [ ] Add logging and monitoring.
    -   [ ] Refine prompt engineering for better answer quality.

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.