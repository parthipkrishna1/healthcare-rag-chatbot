# 🩺 Healthcare RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers medical questions using the MedQuAD dataset, Pinecone vector database, and a local LLM (Llama3 via Ollama).

---

## 🚀 Quick Start

```bash
pip install -r requirements.txt
```

Create `.env`:

```bash
PINECONE_API_KEY=your_key
```

Run:

```bash
python ingest.py
streamlit run app.py
```

## 🚀 Features

* Medical question answering using real dataset
* Semantic search with embeddings
* Pinecone vector database
* Reranking for better accuracy
* Local LLM (Llama3 via Ollama)
* Streamlit chat interface
* Answers with sources (reduces hallucination)

---

## 🧠 System Architecture

MedQuAD Dataset
→ XML Loader
→ Chunking
→ Embeddings
→ Pinecone Vector DB
→ User Query
→ Embedding
→ Vector Search
→ Reranking
→ Llama3 (Ollama)
→ Answer + Sources
→ Streamlit UI

---

## 🛠️ Tech Stack

* Python
* LangChain
* HuggingFace (Sentence Transformers)
* Pinecone (Vector Database)
* Sentence Transformers (Reranker)
* Ollama (Llama3)
* Streamlit

---

## 📂 Project Structure

app.py → Streamlit UI
ingest.py → data ingestion and vector upload
rag_chatbot.py → retrieval + reranking + LLM
medquad_loader.py → XML dataset parser
requirements.txt → dependencies

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/parthipkrishna1/healthcare-rag-chatbot.git
cd healthcare-rag-chatbot
```

---

### 2. Create virtual environment (recommended)

```
python -m venv .venv
source .venv/bin/activate (Linux/Mac)
.venv\Scripts\activate (Windows)
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```
---

## 🔑 Environment Variables (.env)

Create a file named `.env` in the root directory:

```bash
PINECONE_API_KEY=your_pinecone_api_key_here
```

Important:

* Do NOT upload `.env` to GitHub
* It is ignored using `.gitignore`

---

## 📊 Dataset Setup (MedQuAD)

### Step 1: Download dataset

Download from:
[https://github.com/abachaa/MedQuAD](https://github.com/abachaa/MedQuAD)

---

### Step 2: Place dataset

Create folders:

```
datasets/
└── medquad/
```

Now extract the dataset so the structure looks like this:

```
datasets/medquad/
├── 1_CancerGov_QA/
├── 2_GARD_QA/
├── 3_GHR_QA/
├── 4_MPlus_Health_Topics_QA/
├── 5_NIDDK_QA/
├── 6_NINDS_QA/
├── 7_SeniorHealth_QA/
├── 8_NHLBI_QA_XML/
├── 9_CDC_QA/
├── 10_MPlus_ADAM_QA/
├── 11_MPlusDrugs_QA/
├── 12_MPlusHerbsSupplements_QA/
├── LICENSE.txt
├── readme.txt
```

---

### ⚠️ Important

* Each folder contains multiple `.xml` files
* Your loader (`medquad_loader.py`) automatically scans **all subfolders recursively**, so no changes are needed

This line in your code handles it:

```python
for root_dir, dirs, files in os.walk(folder_path):
```

---

### ✅ What this means

You DO NOT need to:

* merge files
* flatten folders
* manually move XML files

Your system already supports this structure.

---

### Step 3: Verify

Run:

```
python test_medquad.py
```

Expected:

```
Total documents: ~47,000
```

---

## 🤖 Setup Ollama (LLM)

Install Ollama:

[https://ollama.com/download](https://ollama.com/download)

Pull the model:

```
ollama pull llama3
```

Run Ollama:

```
ollama serve
```

## 🧪 Run the Project

### Step 1: Ingest data into Pinecone

python ingest.py

This step will:

* Load MedQuAD dataset
* Split into chunks (~115k)
* Generate embeddings
* Store vectors in Pinecone

Note: First run may take 20–30 minutes

---

### Step 2: Run chatbot UI
```
streamlit run app.py
```
Open in browser:
[http://localhost:8501](http://localhost:8501)

---

## 💬 Example Queries

* What is malaria?
* What are symptoms of leukemia?
* What causes Parkinson disease?
* How is dengue treated?

---

## 🔍 How It Works

1. XML dataset is parsed into documents
2. Documents are split into chunks
3. Chunks are converted into embeddings
4. Stored in Pinecone vector database
5. User query is embedded
6. Similar chunks are retrieved
7. Reranker selects best results
8. LLM generates final answer using context

---

## ⚠️ Important Notes

* This chatbot is for educational purposes only
* Not a replacement for medical advice
* Always consult a healthcare professional

---

## 🚧 Limitations

* Depends on dataset quality
* No real-time medical updates
* No hybrid search (yet)

---

## 🔮 Future Improvements

* Hybrid retrieval (BM25 + vector search)
* Better medical-specific models
* API deployment (FastAPI)
* Docker support
* UI improvements

---

## 👨‍💻 Author

Parthip Krishna

---

## ⭐ If you like this project

Give it a star on GitHub ⭐

---