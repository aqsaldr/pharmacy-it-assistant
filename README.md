# 💊 AI-Powered Pharmacy ITSM & Inventory Dashboard

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B)
![LangChain](https://img.shields.io/badge/LangChain-Integration-green)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3-orange)

Sebuah platform *dashboard* cerdas dwifungsi yang dirancang untuk mendukung operasional harian apotek berskala besar. Aplikasi ini mengintegrasikan teknologi *Large Language Models* (LLM) berkecepatan tinggi dengan agen analitik data untuk menyediakan sistem *helpdesk* IT otomatis dan pemantauan ketersediaan inventaris secara *real-time*.

## 🚀 Latar Belakang & Filosofi Arsitektur

Dalam lingkungan operasional apotek yang kritis, stabilitas infrastruktur jaringan (seperti manajemen *bandwidth* atau penanganan *router* yang terputus) dan keandalan perangkat keras mutlak diperlukan. 

**Catatan Arsitektur (Cloud-Optimized):** Versi awal aplikasi ini menggunakan arsitektur Vector RAG (ChromaDB + HuggingFace Embeddings). Namun, untuk keperluan *deployment* pada *environment* cloud dengan sumber daya memori terbatas (RAM < 1GB), arsitektur telah dioptimalkan secara drastis menjadi **Lightweight In-Context Learning**. Sistem kini secara dinamis menyuntikkan dokumen SOP IT langsung ke dalam memori LPU Groq, menghilangkan latensi pembacaan *database* eksternal dan mencegah *bottleneck* memori (*Out of Memory*), sehingga aplikasi berjalan jauh lebih ringan dan stabil di *cloud*.

## ✨ Fitur Utama

1. **IT Support Helpdesk (In-Context AI Node):**
   - Memberikan panduan *troubleshooting step-by-step* terkait *error* jaringan, konfigurasi perangkat keras (printer *thermal* macet), dan *bug software* (sistem POS).
   - Dirancang dengan *guardrails* ketat untuk mencegah halusinasi AI; sistem akan mengarahkan pengguna ke *helpdesk* pusat jika kueri berada di luar SOP jaringan dan infrastruktur yang ditetapkan.

2. **Inventory Analytics (Data Agent):**
   - Menganalisis *dataset* CSV inventaris secara dinamis menggunakan eksekusi kode Python (Pandas) di latar belakang.
   - Menghitung total nilai aset, memfilter daftar obat keras/bebas, dan mendeteksi stok yang mendekati batas kritis.
   - Mengonversi hasil komputasi finansial secara otomatis ke dalam format mata uang Rupiah.

3. **Enterprise-Grade UI Dashboard:**
   - Antarmuka berbasis **Tabs** yang profesional: *Chatbot Assistant*, *Dashboard Metrik Stok* interaktif (dengan grafik visual), dan *Tabel Data Master* yang dapat disortir.
   - Dilengkapi *Quick Prompt Buttons* untuk mempercepat resolusi masalah IT yang paling umum terjadi di lapangan.

## 🛠️ Tech Stack Terkini

* **Frontend:** [Streamlit](https://streamlit.io/) (dengan injeksi CSS kustom)
* **LLM Engine:** [Groq](https://groq.com/) (`llama-3.3-70b-versatile`) memfasilitasi *inference* ultra-cepat.
* **Orkestrasi AI:** LangChain (Core, Experimental).
* **Data Processing:** Pandas & Tabulate (Tool-calling untuk LLM).

## 📁 Struktur Direktori

```text
pharmacy-it-assistant/
│
├── data/
│   ├── it_manuals/         # SOP IT, Panduan Jaringan & Hardware (.txt)
│   └── inventory/          # Database Master Stok Obat (.csv)
│
├── src/
│   ├── __init__.py
│   ├── prompt_templates.py # Kumpulan instruksi persona AI (System Prompts)
│   ├── rag_engine.py       # Logika In-Context Learning (Cloud Optimized)
│   └── inventory_agent.py  # Logika Pandas DataFrame Agent
│
├── app.py                  # File utama aplikasi UI Streamlit
├── requirements.txt        # Daftar dependensi library Python
├── .env.example            # Template konfigurasi environment
└── README.md               # Dokumentasi proyek
```

## ⚙️ Panduan Instalasi (Lokal)
Clone Repository:

```text
git clone [https://github.com/username-anda/pharmacy-it-assistant.git](https://github.com/username-anda/pharmacy-it-assistant.git)
cd pharmacy-it-assistant
```

# Buat Virtual Environment:

```text
python -m venv venv
source venv/bin/activate  # Untuk Windows: venv\Scripts\activate
```

# Install Dependensi:

```text
pip install -r requirements.txt
```

# Konfigurasi API Key:

Salin file .env.example dan ubah namanya menjadi .env.
Buka file .env dan masukkan API Key Groq Anda (Dapatkan secara gratis di Groq Console):

```text
GROQ_API_KEY=gsk_kunci_api_anda_di_sini
```

# Jalankan Aplikasi:

```text
streamlit run app.py
```

Catatan: Saat dijalankan pertama kali, aplikasi akan mengunduh model HuggingFace (sekitar 80MB) dan memproses database vektor.