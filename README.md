# TelepatIA – AI-Powered Medical Assistant

TelepatIA is a web application developed as a technical challenge for the AI Engineer role. The solution processes either audio or text input, transcribes it, and analyzes it using Firebase serverless functions, returning structured medical information and a contextual diagnosis. Additionally, an enhanced agentic version was delivered using intelligent agents.

---

## 🚀 Main Technologies

* **Frontend:** Gradio (Python UI)
* **Backend:** Firebase Cloud Functions (Python with Functions Framework)
* **AI:** OpenAI GPT-4o-mini for text processing and structuring
* **STT:** OpenAI GPT-4o-transcribe Speech-to-Text API

---

## 🏙️ Project Architecture

```
TELEPATIA/
├── frontend/
│   ├── app.py                # Starts the Gradio UI
│   ├── api.py                # Connects to Firebase Cloud Functions
│   └── models/               # Shared Pydantic schemas
├── functions/
│   ├── main.py               # Entry point for Firebase Functions
│   ├── func/                 # Functional modules (transcription, extraction, diagnosis)
│   └── shared/               # Shared logic (services, models, clients, prompts)
├── firebase.json            # Firebase deployment configuration
├── .firebaserc              # Project alias setup
```

---

## 🧰 Combined Approach: Traditional Functions + Intelligent Agents

The required **three cloud functions** were delivered and deployed independently, integrated into the frontend:

1. `transcribe_audio`: receives a URL and transcribes the audio.
2. `extract_info`: extracts structured medical data from a given text.
3. `generate_diagnosis`: generates a diagnosis, treatment, and recommendations from structured input.

As an added value, an **autonomous agent-based system** was developed:

### Agents implemented in the additional system:

* **Manager Agent:** orchestrates the entire decision flow.
* **Data Extractor Agent:** extracts symptoms, patient info, and reason for consultation.
* **Diagnostic Agent:** generates diagnosis, treatment, and follow-up suggestions.
* **Content Guardrail Agent:** ensures safety and relevance of the conversation.

This system has contextual memory, acts autonomously, and intelligently decides the workflow without manually chaining functions. It aims to extract the most information possible for a more precise and human-like medical result.

---

## 🚪 Step-by-Step Guide to Run the Project

### 🚀 Prerequisites

* Python 3.10+
* Node.js 18+
* Firebase CLI
* OpenAI account with API Key

### 1. Clone the repository

```bash
git clone https://github.com/your_user/telepatIA.git
cd telepatIA
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=Your Openai API KEY
OPENAI_MODEL=Your Model (gpt-4o-mini Recomended)
```

---

### 🚀 Start the Frontend (Gradio)

```bash
cd frontend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```

The app will open at `http://localhost:7860` where you can upload audio url or type text.

---

### 🚀 Start the Backend (Cloud Functions locally)

First, prepare the Python environment inside the `functions/` directory:

```bash
cd functions
python -m venv venv # or venv\Scripts\activate on Windows
source venv/bin/activate
pip install -r requirements.txt
cd ..
firebase emulators:start
```

This will start the local Firebase emulator and load the cloud functions correctly.

> **Important:** Running `firebase emulators:start` without installing dependencies first **will not work**. You must set up the virtual environment and install all requirements beforehand.

---

## 📊 Implemented Features

| Module                         | Description                                              |
| ------------------------------ | -------------------------------------------------------- |
| Audio Transcription            | Downloads and transcribes audio using Whisper/OpenAI     |
| Medical Information Extraction | Extracts `symptoms`, `patient_info`, `reason` from text  |
| Diagnosis Generation           | Produces `diagnosis`, `treatment`, and `recommendations` |
| Guardrails                     | Blocks unsafe or irrelevant medical content              |
| Logging & Metrics              | Tracks latency, timestamp, and logs errors               |

---

## 📂 Backend Structure Overview

* `/func/`: Each cloud function is modularized independently.
* `/shared/assets/`: Prompts and example audio files.
* `/shared/models/`: Reusable Pydantic schemas.
* `/shared/clients/`: OpenAI client wrapper.
* `/shared/services/`: Core logic for agent-based flows and functions.
* `/shared/tools/`: Utilities used by the agents such as audio processing and intelligent extractors.

---

## 📊 Final Output

* Accepts audio url or free text
* Transcribes audio (if provided)
* Extracts structured medical info
* Returns human-readable diagnosis
* Agentic version supports memory and intelligent flow orchestration

---

## 📄 License

MIT License

---

## 🚀 Author

**Jaider Cardona. (Grey)** – Technical Challenge for AI Engineer Role – June 2025

---

> "Built with Firebase Cloud Functions and an optional agentic architecture for intelligent, contextual medical diagnosis."
