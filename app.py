import streamlit as st
import os
import time
import pandas as pd
from dotenv import load_dotenv
from src.rag_engine import setup_rag_chain
from src.inventory_agent import get_inventory_agent

st.set_page_config(
    page_title="Pharmacy IT & Data Portal",
    page_icon="💊",
    layout="wide", 
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stChatMessage { border-radius: 12px; padding: 10px; border: 1px solid #f0f2f6; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    /* Kustomisasi tombol rekomendasi agar terlihat seperti tag/pill */
    .stButton>button { border-radius: 15px; border: 1px solid #e0e0e0; background-color: #f8f9fa; color: #333; transition: all 0.2s; }
    .stButton>button:hover { border-color: #0066cc; background-color: #e6f2ff; color: #0066cc; }
</style>
""", unsafe_allow_html=True)

load_dotenv()

@st.cache_data
def load_inventory_data():
    """Memuat data CSV untuk ditampilkan di grafik dan tabel secara efisien"""
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'inventory', 'stok_obat.csv')
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return pd.DataFrame()

df_stok = load_inventory_data()

def initialize_systems():
    if "systems_ready" not in st.session_state:
        with st.status("🔗 Memuat Infrastruktur AI...", expanded=True) as status:
            st.write("Menghubungkan ke Node ChromaDB (Lokal)...")
            st.session_state.it_chain = setup_rag_chain()
            time.sleep(0.5)
            st.write("Memuat Engine Analitik Pandas & Model Groq LPU...")
            st.session_state.stock_agent = get_inventory_agent()
            status.update(label="Sistem Operasional. Semua layanan aktif.", state="complete", expanded=False)
        st.session_state.systems_ready = True

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Saya siap membantu Anda menganalisis data stok obat atau menyelesaikan masalah IT (Hardware, POS, Jaringan). Apa yang ingin Anda ketahui?"}
    ]

if "quick_prompt" not in st.session_state:
    st.session_state.quick_prompt = None

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/128/8778/8778084.png", width=60)
    st.title("Admin Console")
    st.caption("AI-Powered Pharmacy Assistant v3.0")
    st.divider()
    
    st.subheader("📊 System Status")
    st.markdown("🟢 **RAG Node:** Online")
    st.markdown("🟢 **Data Agent:** Online")
    st.markdown("🟢 **Network:** Stable")
    
    st.divider()
    if st.button("🔄 Kosongkan Percakapan", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "Sesi direset. Ada yang bisa saya bantu?"}]
        st.rerun()

st.title("🖥️ Pharmacy IT Helpdesk & Data Analytics")
st.markdown("Platform terintegrasi untuk penyelesaian masalah teknis dan pemantauan inventaris pintar.")

tab1, tab2, tab3 = st.tabs(["💬 AI Assistant", "📊 Dashboard Stok", "📁 Data Master Obat"])

with tab1:
    initialize_systems()
    
    st.markdown("#### 💡 Rekomendasi Pertanyaan IT Support:")
    colA, colB, colC = st.columns(3)
    
    def set_prompt(text):
        st.session_state.quick_prompt = text

    with colA:
        st.button("🖨️ Printer kasir berkedip merah & macet", on_click=set_prompt, args=("Printer kasir saya berkedip merah dan kertasnya macet, apa yang harus dilakukan?",), use_container_width=True)
        st.button("🌐 Lampu LOS router berkedip merah", on_click=set_prompt, args=("Lampu indikator LOS pada router internet berkedip merah dan koneksi putus, solusinya?",), use_container_width=True)
    with colB:
        st.button("💻 Aplikasi POS muncul ERR-500", on_click=set_prompt, args=("Aplikasi POS menampilkan ERR-500 Server Timeout saat transaksi, bagaimana mengatasinya?",), use_container_width=True)
        st.button("🔌 Beralih ke Mode Offline jaringan", on_click=set_prompt, args=("Jaringan internet dari pusat sedang gangguan, bagaimana cara menggunakan Mode Offline di POS?",), use_container_width=True)
    with colC:
        st.button("📷 Scanner barcode tidak membaca angka", on_click=set_prompt, args=("Scanner barcode saya tidak bisa merespon.",), use_container_width=True)
        st.button("📉 Cek total aset obat keras (Inventaris)", on_click=set_prompt, args=("Tolong hitung total nilai aset (stok dikali harga) untuk semua obat di kategori Keras.",), use_container_width=True)

    st.divider()

    for message in st.session_state.messages:
        avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    user_input = st.chat_input("Ketik masalah IT atau kueri stok di sini...")
    
    if st.session_state.quick_prompt:
        user_input = st.session_state.quick_prompt
        st.session_state.quick_prompt = None

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(user_input)

        inventory_keywords = ['stok', 'obat', 'sisa', 'kadaluarsa', 'expired', 'harga', 'rak', 'kategori', 'bebas', 'keras', 'aset', 'total', 'hitung']
        is_inventory_query = any(word in user_input.lower() for word in inventory_keywords)

        with st.chat_message("assistant", avatar="🤖"):
            loading_msg = "Menganalisis basis data inventaris..." if is_inventory_query else "Menganalisis topologi jaringan dan manual IT..."
            with st.spinner(loading_msg):
                try:
                    if is_inventory_query:
                        result = st.session_state.stock_agent.invoke({"input": user_input})
                        response = result.get("output", "Gagal memproses data.")
                    else:
                        result = st.session_state.it_chain.invoke({"input": user_input})
                        response = result.get("answer", "Konteks tidak ditemukan.")
                    
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"⚠️ **Error Internal:** `{str(e)}`"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
with tab2:
    st.header("📈 Analitik Visual Stok Obat")
    if not df_stok.empty:

        total_item = len(df_stok)
        total_stok_fisik = df_stok['Stok'].sum()
        obat_kritis = len(df_stok[df_stok['Stok'] < 30])
        
        m1, m2, m3 = st.columns(3)
        m1.metric(label="Total Varian Obat", value=f"{total_item} Item")
        m2.metric(label="Total Stok Fisik", value=f"{total_stok_fisik} Pcs")
        m3.metric(label="Obat Stok Kritis (<30)", value=f"{obat_kritis} Item", delta="- Segera Restock", delta_color="inverse")
        
        st.divider()
        
        st.subheader("Top 10 Obat (Stok Tertinggi)")
        df_top10 = df_stok.nlargest(10, 'Stok').set_index('Nama_Obat')
        st.bar_chart(df_top10['Stok'], color="#1f77b4")
        
        st.subheader("Distribusi Kategori Obat")
        kategori_count = df_stok['Kategori'].value_counts()
        st.bar_chart(kategori_count, color="#ff7f0e")
    else:
        st.warning("Data stok tidak ditemukan. Pastikan file CSV tersedia di folder data/inventory/")
with tab3:
    st.header("📁 Database Master Inventaris")
    st.markdown("Gunakan fitur filter dan pencarian bawaan tabel di bawah ini untuk inspeksi data manual.")
    if not df_stok.empty:
        st.dataframe(
            df_stok,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Harga_Satuan": st.column_config.NumberColumn("Harga Satuan (Rp)", format="Rp %d"),
                "Stok": st.column_config.ProgressColumn("Ketersediaan Stok", min_value=0, max_value=500),
            }
        )
    else:
        st.error("Gagal memuat tabel data.")