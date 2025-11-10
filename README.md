# ⚙️ Ramayan 3075 — The Neural Exile
### 🚀 An AI-Powered Narrative Transformation Engine  
*Built by Shiva Sannidh — for the Pratilipi AI Engineer Assignment*

---

> “What if timeless epics could be reborn through artificial intelligence?”

**Ramayan 3075** is a generative AI storytelling system that uses **LLM orchestration**, **prompt chaining**, and **structured emotional logic**  
to reimagine ancient narratives in futuristic worlds.

Unlike typical one-shot prompt systems, this project introduces a **modular story-generation pipeline** that merges:
- 🧠 **LLM Reasoning** — multi-stage generation (world → characters → beats → scenes)
- 💡 **Deterministic fallback** — reproducible creative runs
- 💬 **Prompt templating** — reusable creative instruction sets
- 🛠️ **Generative LT (Language Transformation)** — converts classic literature into coherent, emotionally aligned modern adaptations

---

## 🧬 Quick Summary
| Feature | Description |
|----------|-------------|
| **Architecture Type** | Generative LT (Language Transformation) |
| **Core Engine** | Python + OpenAI LLMs (gpt-4o-mini) |
| **Modes** | Deterministic & Dynamic (LLM) |
| **Innovation** | Multi-prompt chaining for emotionally stable story generation |
| **Output Format** | Auto-assembled Markdown Narrative |
| **Pipeline Steps** | World → Characters → Plot Beats → Scenes → Reflection |
| **AI Controls** | Guardrails for tone, structure, and thematic fidelity |

---

## 🧠 Demo Command
Generate a complete futuristic Ramayan story in one line:

```bash
python src/run_neural_exile.py --use-llm

Output Example:
🤖 Running in LLM mode (using OpenAI API)...
✅ Story generated and saved to: outputs/story_output_llm_2025xxxxTxxxxZ.md


## 🧩 Generative LT Concept

**Generative LT (Language Transformation)** is the core method behind this system.  
It applies structured prompt engineering to translate **classical literature** into **contextually coherent modern narratives** while preserving:
- Emotional integrity
- Narrative structure
- Thematic consistency

Each transformation follows a reproducible chain:

Classic Source → Context Mapping → Prompt Chaining → Emotional Reframing → Output Synthesis
---

## ⚙️ Features
- **Two Generation Modes**
  - Deterministic (Offline, reproducible)
  - LLM-based (OpenAI API, prompt chaining)
- **Modular Pipeline:**  
  World → Characters → Beats → Scenes 
- **Emotionally Grounded Outputs:**  
  Focused on sensory detail and moral choice
- **Clean Markdown Output:**  
  Auto-assembled and timestamped

---

## 🧠 System Architecture

ramayan3075_neural_exile/
├── src/
│   ├── run_neural_exile.py        # orchestrator (main runner)
│   ├── llm_utils.py               # OpenAI wrapper + retries/fallbacks
│   ├── utils.py                   # helper utils (file I/O, parsing)
│
├── prompts/
│   ├── world.txt                  # world prompt template
│   ├── characters.txt             # characters prompt (fixed names)
│   ├── beats.txt                  # beats prompt template
│   └── scenes.txt                 # scenes prompt template
│
├── outputs/                       # generated .md outputs (optionally ignored in git)
│   └── story_output_llm_YYYYMMDDT*.md
│
├── runs/                          # saved prompts/responses for provenance (optional)
│   └── run_YYYYMMDDT*.json
│
├── docs/
│   ├── solution_documentation.md  # Approach diagram, design, challenges, future work
│   └── architecture.mmd           # Mermaid source (optional)
│
├── tests/                         # minimal smoke tests for CI (recommended)
│   └── test_pipeline.py
│
├── .env                           # local secrets (DO NOT commit)
├── .gitignore
├── README.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .github/
    └── workflows/
        └── ci.yml

Input → Template Load → LLM or Deterministic Generation → Post-Processing → Markdown Assembly

Key Files:
| Path | Description |
|------|--------------|
| `src/run_neural_exile.py` | Main orchestration pipeline |
| `src/llm_utils.py` | OpenAI API helper with retries |
| `prompts/` | Structured templates for each stage |
| `outputs/` | Generated markdown outputs |
| `docs/solution_documentation.md` | Full project explanation & diagrams |

---

## 🚀 How to Run

### 1️ Setup Environment
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt

### 2 Add API Key:

create a .env file:
  OPENAI_API_KEY=your_key_here


3️⃣ Run the Pipeline
Deterministic mode:
```bash
python src/run_neural_exile.py
LLM mode:
```bash
python src/run_neural_exile.py --use-llm
4️⃣ View Results
Open your generated story inside outputs/.


