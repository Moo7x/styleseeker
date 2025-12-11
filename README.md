# StyleSeeker 🛍️🔍

> **A Full-Stack AI-Powered Visual Search Engine for E-commerce.**

StyleSeeker allows users to upload an image of a fashion item (like a shirt or dress) and instantly finds visually similar products from a catalog of over 40,000 items. It leverages deep learning embeddings and vector search to understand "style" beyond just keywords.

![Project Screenshot](https://via.placeholder.com/800x400?text=Upload+Screenshot+Here+Later)
_(Add a screenshot of your React UI here later!)_

---

## 🚀 Tech Stack

**Core AI & Data:**

- **Vector Database:** Weaviate (running via Docker)
- **ML Model:** OpenAI CLIP (via Hugging Face Transformers)
- **Embeddings:** PyTorch
- **Data Processing:** Pandas, Pillow

**Backend:**

- **Framework:** FastAPI (Python)
- **Server:** Uvicorn
- **Architecture:** Modular Service-Repository pattern

**Frontend:**

- **Framework:** React (Vite)
- **Styling:** CSS3 (Custom responsive grid)

---

## ⚙️ Architecture

1.  **Ingestion Pipeline:** A Python script processes the dataset, generating 512-dimensional vectors using the CLIP model and indexing them into Weaviate.
2.  **Search API:** The FastAPI backend accepts an image upload, processes it in-memory through the same CLIP model, and queries Weaviate for nearest neighbors.
3.  **User Interface:** A React frontend manages file uploads and displays the retrieved product images in a responsive grid.

---

## 🛠️ Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.10+
- Node.js & npm

### 1. Start the Infrastructure

Start the Vector Database:

    ```bash
    docker compose up -d
    ```
    *This command starts all services in detached mode (`-d`).*

2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate
pip install -r requirements.txt
```

# Start the API

```bash
uvicorn app.main:app --reload
```

3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Visit http://localhost:5173 to try the app!
