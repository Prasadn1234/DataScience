# AGENTS.md

## Cursor Cloud specific instructions

### Repository overview

This is a **Python Agentic AI / Data Science learning repository** built around Jupyter notebooks, plus a minimal **Flask + Gunicorn** deploy skeleton (`app.py`). There is no monorepo, no `docker-compose`, and no shared test/lint configuration.

### Python environment

- **Python:** 3.11+ (Dockerfile uses 3.11; local dev tested on 3.12).
- **Virtualenv:** Use `.venv` at the repo root. On fresh Ubuntu VMs, `python3.12-venv` must be installed once before creating the venv (`sudo apt-get install -y python3.12-venv`).
- **Activate:** `source .venv/bin/activate`
- **Dependencies:** `pip install -r requirements.txt` (Flask 3.0.3, Gunicorn 22.0.0 only).

For notebook work, also install Jupyter locally (not in `requirements.txt`):

```bash
pip install jupyter ipykernel
python -m ipykernel install --user --name=datascience --display-name="Python (datascience)"
```

### Running the web service (deploy skeleton)

The only standalone runnable service in the repo is the empty Flask app.

**Gunicorn (production-style):**

```bash
source .venv/bin/activate
PORT=8000 gunicorn --bind 0.0.0.0:8000 --workers 1 --threads 8 --timeout 0 app:app
```

**Flask dev server:**

```bash
source .venv/bin/activate
python app.py   # binds 0.0.0.0:8000 by default
```

`app.py` defines no routes, so `GET /` returns **404** — that is expected and confirms the server is up.

**Docker (optional):** `docker build -t datascience .` then `docker run -p 8000:8000 -e PORT=8000 datascience`

### Notebooks

Primary workflow is Jupyter/Colab. Notebook dependencies are installed **per notebook** via `pip install` cells (OpenAI, LangChain, ChromaDB, Gradio, etc.).

Capstone notebooks clone datasets at runtime from:

`https://github.com/AI-Project-Lab/IK-pwc-agenticai-datasets.git`

### Required secrets for notebook E2E

Most notebooks need cloud API keys (not required for the Flask skeleton):

| Key | Used by |
|-----|---------|
| `OPENAI_API_KEY` | Most assignments, vector store, CRM, support bot |
| `LANGFUSE_SECRET_KEY`, `LANGFUSE_PUBLIC_KEY` | Contract/healthcare capstones |
| `LANGSMITH_API_KEY` | Support bot evaluation |
| `GOOGLE_API_KEY` | Gemini tutorials |

### Lint / tests

There is **no** configured linter or automated test suite. Basic validation:

```bash
python -m py_compile app.py
python -c "from app import app"
```

Notebook execution requires API keys and per-notebook dependency installs.
