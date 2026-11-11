# ðŸ–¥ï¸ AI IT Helpdesk Agent

An enterprise-grade, 100% local, zero-cost **Agentic AI IT Helpdesk Agent** built with **LangGraph**, **LangChain**, **ChromaDB**, **SQLite**, and **Streamlit**.

This project provides an end-to-end automated IT support solution featuring explicit workflow routing, Retrieval-Augmented Generation (RAG) over corporate knowledge bases, tool calling for ticket management, long-term memory persistence across app restarts, and Human-in-the-Loop (HITL) confirmation for support ticket submissions.

---

## ðŸ“Œ Problem Statement

IT helpdesks face overwhelming volumes of repetitive user queries ranging from basic Wi-Fi and printer troubleshooting to account lockouts and hardware failures. Manual ticketing systems often result in delayed response times, poor prioritization, and repetitive data entry. 

## ðŸ’¡ Solution

The **AI IT Helpdesk Agent** acts as an autonomous virtual IT specialist. It uses a **LangGraph StateGraph** classifier to route requests dynamically:
- **Technical Queries** are grounded with RAG over indexed knowledge base docs.
- **Ticket Requests** undergo rule-based priority analysis and trigger Human-in-the-Loop confirmation before recording tickets in SQLite.
- **General Queries & Facts** update and retrieve long-term user memory profiles.

---

## ðŸ—ï¸ System Architecture & Workflow

### LangGraph Workflow Topology

```
                  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                  â”‚    User Query        â”‚
                  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                             â”‚
                             â–¼
                   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                   â”‚  classifier_node  â”‚
                   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                             â”‚
             â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
             â–¼               â–¼               â–¼
    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
    â”‚technical_agent â”‚ â”‚ticket_agentâ”‚ â”‚general_agent â”‚
    â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
             â”‚               â”‚              â”‚
             â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                             â”‚
                             â–¼
                          [ END ]
```

### RAG Pipeline Flow
1. **Document Loading**: Text loaders scan `knowledge_base/` (`wifi.txt`, `slow_laptop.txt`, `vpn.txt`, etc.).
2. **Chunking**: `RecursiveCharacterTextSplitter` creates 500-character overlapping chunks.
3. **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` produces dense vector representations.
4. **Vector Store**: `ChromaDB` stores embeddings locally in `data/chroma_db/`.
5. **Contextual Generation**: `ChatOllama` (`llama3.2`) generates grounded answers referencing retrieved context.

---

## ðŸš€ Features

- **100% Free & Local Stack**: Zero API key dependencies. Runs via Ollama, ChromaDB, HuggingFace embeddings, SQLite, and Streamlit.
- **Live Ollama Health Monitoring**: Real-time status banner indicating if Ollama and `llama3.2` are online/offline.
- **Human-in-the-Loop (HITL) Safeguards**: Confirms ticket creation with `YES - Create Ticket` or `NO - Cancel` before performing SQLite writes.
- **Color-Coded Priority Detection**: Automatically classifies issues into `HIGH` (Red), `MEDIUM` (Orange), and `LOW` (Green) priority badges.
- **Long-Term SQLite Memory**: Persists user facts (such as names and past context) in `data/helpdesk.db` across sessions.
- **Tool Calling**: Native callable tools for ticket insertion (`create_ticket`), ticket status lookup (`check_ticket_status`), and time retrieval (`get_current_time`).

---

## ðŸ› ï¸ Technology Stack

- **Frontend**: Streamlit (Glassmorphic dark dashboard)
- **Agent Orchestration**: LangGraph (`StateGraph`), LangChain
- **LLM Engine**: Ollama (`llama3.2`)
- **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)
- **Vector Database**: ChromaDB (Persisted locally)
- **Relational DB & Memory**: SQLite (`data/helpdesk.db`)
- **Language**: Python 3.10+

---

## ðŸ“‚ Project Structure

```
ai-it-helpdesk-agent/
â”œâ”€â”€ app.py                  # Streamlit dashboard UI & HITL interface
â”œâ”€â”€ requirements.txt        # Python dependency specifications
â”œâ”€â”€ README.md               # Documentation & architecture guide
â”œâ”€â”€ .gitignore              # Data and cache ignores
â”œâ”€â”€ src/                    # Core AI Helpdesk implementation package
â”‚   â”œâ”€â”€ __init__.py         # Package init
â”‚   â”œâ”€â”€ config.py           # Ollama health check & host settings
â”‚   â”œâ”€â”€ database.py         # SQLite connection & CRUD operations
â”‚   â”œâ”€â”€ memory.py           # Short-term and long-term user memory
â”‚   â”œâ”€â”€ tools.py            # Ticket tools & priority detection
â”‚   â”œâ”€â”€ rag.py              # ChromaDB vector index & retrieval
â”‚   â”œâ”€â”€ agents.py           # LangGraph node execution functions
â”‚   â””â”€â”€ graph.py            # LangGraph StateGraph & conditional routing
â”œâ”€â”€ knowledge_base/         # IT troubleshooting guides
â”‚   â”œâ”€â”€ wifi.txt
â”‚   â”œâ”€â”€ internet.txt
â”‚   â”œâ”€â”€ printer.txt
â”‚   â”œâ”€â”€ software.txt
â”‚   â”œâ”€â”€ password.txt
â”‚   â”œâ”€â”€ vpn.txt
â”‚   â”œâ”€â”€ email.txt
â”‚   â””â”€â”€ slow_laptop.txt
â”œâ”€â”€ tests/                  # Verification & test suite
â”‚   â”œâ”€â”€ test_helpdesk.py               # Core 6-step test suite
â”‚   â”œâ”€â”€ full_checklist_verification.py # Complete 23-point verification
â”‚   â””â”€â”€ run_and_check_all_features.py  # 31-feature capability suite
â””â”€â”€ data/
    â””â”€â”€ .gitkeep            # Storage directory for helpdesk.db and ChromaDB
```

---

## âš¡ Installation & Setup

### 1. Clone & Install Dependencies
```bash
cd ai-it-helpdesk-agent
pip install -r requirements.txt
```

### 2. Ollama Setup (Local LLM Engine)
Install [Ollama](https://ollama.com) and pull the model:
```bash
ollama pull llama3.2
```

---

## ðŸ–¥ï¸ Running the Application

Launch the Streamlit dashboard:
```bash
streamlit run app.py
```

Run the end-to-end test suite:
```bash
python test_helpdesk.py
```

---

## ðŸŽ¬ Verified Demo Scenarios

| Scenario | Input Query | Agent Route | Outcome |
| :--- | :--- | :--- | :--- |
| **1. Wi-Fi Issue** | `"My WiFi is not connecting"` | `technical_agent` | RAG retrieves `wifi.txt` context; presents step-by-step fix. |
| **2. Slow Laptop** | `"My laptop is very slow"` | `technical_agent` | RAG retrieves `slow_laptop.txt` context; presents CPU/RAM cleanup guide. |
| **3. High Priority Ticket** | `"Create a ticket because my laptop keeps restarting"` | `ticket_agent` | Detects `HIGH` priority -> Triggers HITL confirmation -> On `YES` inserts into SQLite. |
| **4. Ticket Lookup** | `"Check ticket status TKT-2026-XXXXX"` | `ticket_agent` | Invokes `check_ticket_status` tool -> Returns status, date, priority from SQLite. |
| **5. Long-Term Memory** | `"My name is Throna"` -> `"What is my name?"` | `general_agent` | Stores fact in `user_memory` SQLite table; retrieves correctly across restarts. |

---

## ðŸš€ Future Improvements

- Integrate active Directory / LDAP single sign-on (SSO).
- Add automated email notification dispatch upon ticket creation.
- Support multi-modal screenshot diagnostics via vision LLMs.

---

## ðŸ“Š Additional Enhancement: IT Support Analytics Dashboard

I extended the original AI IT Helpdesk Agent with a separate ticket analytics dashboard using Streamlit, Pandas, and Plotly.

### Dashboard Features

- **KPI Metrics:** Total tickets, open tickets, closed tickets, and closure rate.
- **Priority Analysis:** Visual breakdown of high, medium, and low priority tickets.
- **Status Analysis:** Open versus closed ticket distribution.
- **Issue Categorization:** Rule-based classification of ticket descriptions into Network, Hardware, Account Access, Software, Printer, and Other categories.
- **Ticket Trends:** Daily ticket creation analysis.
- **Ticket Filtering:** Filter records by priority and status.
- **CSV Export:** Download filtered ticket records for further analysis.

### Implementation Details

- Connected the dashboard to the existing SQLite ticket database.
- Used Pandas for data preparation and analysis.
- Used Plotly for interactive visualizations.
- Integrated the dashboard as a separate Streamlit page.
- Preserved the original AI chatbot and ticket management workflow.

**Note:** Issue categories are inferred from ticket descriptions using keyword-based rules; they are not stored as categories in the original database.

### Manual Testing Performed

| Test | Result |
|---|---|
| SQLite ticket retrieval | Passed |
| KPI calculation | Passed |
| Priority and status charts | Displayed |
| Issue category analysis | Displayed |
| Ticket creation trend | Displayed |
| Ticket record display | Passed |
| CSV report download | Passed |
| Streamlit multipage navigation | Passed |

### Technologies Used for This Enhancement

Python, Streamlit, Pandas, Plotly, SQLite, PowerShell.

### Project Attribution

This is an enhancement to the original open-source AI IT Helpdesk Agent project. The original implementation and its authors retain their respective credit. The analytics dashboard and related integration described above are my contributions.
