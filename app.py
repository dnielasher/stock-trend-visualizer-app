import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date, timedelta

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Stock Trend Visualizer",
    page_icon="📈",
    layout="wide"
)

# --- Judul dan Deskripsi ---
st.title("📈 Aplikasi Visualisasi Tren Saham")
st.markdown("""
Aplikasi ini mengambil data historis dari Yahoo Finance dan memvisualisasikan tren harga penutupan (Closing Price) 
beserta indikator Moving Average sederhana.
*Dibuat menggunakan Python & Streamlit.*
""")
st.divider()

# --- Sidebar (Input Pengguna) ---
st.sidebar.header("Konfigurasi Data")

# Input Ticker Saham (Default: BBRI.JK untuk Bank BRI)
ticker_symbol = st.sidebar.text_input("Masukkan Simbol Saham (Yahoo Finance):", value="BBRI.JK")

# Input Rentang Tanggal (Default: 1 tahun terakhir)
start_date = st.sidebar.date_input("Tanggal Mulai", value=date.today() - timedelta(days=365))
end_date = st.sidebar.date_input("Tanggal Akhir", value=date.today())

# Tombol untuk memuat data
load_data = st.sidebar.button("Tampilkan Data")

# --- Fungsi Caching Data (Agar cepat) ---
@st.cache_data
def fetch_stock_data(symbol, start, end):
    try:
        data = yf.download(symbol, start=start, end=end)
        if data.empty:
            return None
        # Hitung Simple Moving Average (SMA 20 hari) sebagai contoh analisis tren
        data['SMA_20'] = data['Close'].rolling(window=20).mean()
        return data
    except Exception as e:
        return None

# --- Logika Utama ---
if load_data:
    with st.spinner(f'Mengambil data untuk {ticker_symbol}...'):
        stock_data = fetch_stock_data(ticker_symbol, start_date, end_date)

    if stock_data is None:
        st.error(f"Gagal mengambil data untuk simbol '{ticker_symbol}'. Pastikan simbol benar atau coba rentang tanggal lain.")
    else:
        # Tampilkan Tabulasi
        tab1, tab2 = st.tabs(["📊 Grafik Harga", "📄 Data Mentah"])

        with tab1:
            st.subheader(f"Pergerakan Harga Penutupan: {ticker_symbol}")
            
            # Siapkan data untuk grafik Streamlit
            chart_data = stock_data[['Close', 'SMA_20']].copy()
            # Rename kolom agar lebih jelas di legenda grafik
            chart_data.columns = ['Harga Penutupan (Close)', 'Trend 20 Hari (SMA)']
            
            # Tampilkan Line Chart Interaktif
            st.line_chart(chart_data, color=["#2980b9", "#e74c3c"]) # Biru untuk harga, Merah untuk tren

            st.caption("Garis Biru: Harga Penutupan Harian. Garis Merah: Rata-rata pergerakan 20 hari (Indikator Tren).")

        with tab2:
            st.subheader("Data Historis Terbaru")
            # Tampilkan dataframe (diurutkan dari yang paling baru)
            st.dataframe(stock_data.sort_index(ascending=False).head(50), use_container_width=True)

else:
    st.info("👈 Silakan masukkan simbol saham (contoh: BBRI.JK, TLKM.JK, atau GOOG) di sidebar dan klik 'Tampilkan Data'.")

# --- Footer ---
st.divider()
st.markdown("Developed by **Daniel Asher** | Mahasiswa Matematika - Data Analytics Portfolio")