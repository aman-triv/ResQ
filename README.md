# 🚨 LifeGrid - Offline Emergency Triage & AI First-Aid System

LifeGrid is an offline-capable AI emergency rescue assistant designed to function during network outages, natural disasters, or critical situations. It processes incoming SOS text messages and voice notes locally to categorize urgency, provide real-time first-aid guidance, and generate priority-weighted rescue paths.

---

## 🚀 Completed Milestones

### **Phase 1: Local NLP & SOS Parsing**
- **Model:** Llama 3.2 (via Ollama)
- **Features:** 
  - Parses raw SOS messages locally into structured JSON.
  - Generates urgency scores (1-10), classifies categories (human/animal), and flags medical emergencies.
- **File:** `test_nlp.py`

---

### **Phase 2: Speech AI & Dynamic First-Aid Guidance**
- **Models:** OpenAI Whisper & Llama 3.2 (via Ollama)
- **Features:**
  - Converts incoming voice notes (`.wav`/`.mp3`) into clean text without internet access (`test_whisper.py`).
  - Generates real-time, situation-specific First-Aid and safety steps offline during medical crises (`test_firstaid.py`).

---

### **Phase 3: Delivery-Style VRP Route Engine**
- **Algorithm/Engine:** Google OR-Tools
- **Features:**
  - Multi-stop route optimization using a custom **Priority-Distance Weighting Matrix**.
  - Balances physical distances with Phase 1 urgency scores to prioritize life-threatening emergencies first.
- **File:** `test_vrp.py`

---

## 🛠️ Tech Stack & Tools

- **Language:** Python 3.14
- **Local LLM Engine:** Ollama (Llama 3.2)
- **Speech-to-Text:** OpenAI Whisper
- **Route Optimization Engine:** Google OR-Tools
- **Deep Learning Framework:** PyTorch
- **Version Control:** Git & GitHub

---

## 💻 How to Run Locally

1. **Install Dependencies:**
   pip install openai-whisper torch ortools

2. **Run Ollama Local Server:**
   Ensure Ollama is installed and running `llama3.2`.

3. **Execute Test Modules:**
   - NLP Triage: `python test_nlp.py`
   - Speech Transcription: `python test_whisper.py`
   - First-Aid Guidance: `python test_firstaid.py`
   - VRP Route Engine: `python test_vrp.py`