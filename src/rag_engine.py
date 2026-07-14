import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

def setup_rag_chain():
    """
    Versi Lightweight tanpa ChromaDB.
    Membaca file TXT langsung ke dalam memori (In-Context Learning).
    Sangat ringan untuk Cloud Deployment.
    """
    # 1. Baca semua file TXT
    DOCS_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'it_manuals')
    konteks_dokumen = ""
    
    if os.path.exists(DOCS_DIR):
        for filename in os.listdir(DOCS_DIR):
            if filename.endswith(".txt"):
                with open(os.path.join(DOCS_DIR, filename), 'r', encoding='utf-8') as f:
                    konteks_dokumen += f"\n\n--- DOKUMEN: {filename} ---\n"
                    konteks_dokumen += f.read()

    # 2. Injeksi teks langsung ke dalam prompt (Bypass Vector DB)
    system_prompt = f"""
    Anda adalah AI IT Support Helpdesk yang profesional. 
    Tugas Anda membantu menyelesaikan masalah teknis hardware/jaringan.
    Gunakan HANYA panduan berikut untuk menjawab, berikan step-by-step:
    
    {konteks_dokumen}
    
    Jika jawabannya tidak ada di dokumen atas, katakan dengan jujur Anda tidak tahu 
    dan sarankan hubungi Tim IT Pusat. Jangan mengarang jawaban.
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    # 3. Gunakan Llama 3.3 via Groq
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)
    
    # Gabungkan Prompt dan LLM
    chain = prompt | llm
    
    # 4. Wrapper class agar format outputnya tetap cocok dengan app.py lama Anda
    class SimpleChain:
        def invoke(self, inputs):
            # Eksekusi LLM dan ambil teks jawabannya
            response = chain.invoke(inputs)
            return {"answer": response.content}
            
    return SimpleChain()