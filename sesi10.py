import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur gaya visualisasi
sns.set(style='dark')

# Daftar URL file Excel di GitHub
file_urls = [
    "https://github.com/Muhammadfakhrii/datasesi10/blob/main/2017.xlsx",
    "https://github.com/Muhammadfakhrii/datasesi10/blob/main/2018.xlsx",
    "https://github.com/Muhammadfakhrii/datasesi10/blob/main/2019.xlsx",
    "https://github.com/Muhammadfakhrii/datasesi10/blob/main/2020.xlsx",
    "https://github.com/Muhammadfakhrii/datasesi10/blob/main/2021.xlsx",
    "https://github.com/Muhammadfakhrii/datasesi10/blob/main/2022.xlsx",
    "https://github.com/Muhammadfakhrii/datasesi10/blob/main/2023.xlsx",
    
]

# Menggabungkan semua file menjadi satu dataframe
dataframes = []
for url in file_urls:
    year_df = pd.read_excel(url)  # Baca file Excel langsung dari URL
    year_df['Year'] = url.split('/')[-1].split('.')[0]  # Tambahkan kolom tahun
    dataframes.append(year_df)

# Menggabungkan semua dataframe
df = pd.concat(dataframes, ignore_index=True)

# Preprocessing: Mengatur ulang kolom yang relevan
df.columns = df.iloc[0]  # Menggunakan baris pertama sebagai header
df = df[1:]  # Menghapus baris header lama
df = df.reset_index(drop=True)  # Reset indeks

# Konversi kolom numerik
numeric_columns = df.columns[1:-1]  # Asumsi kolom pertama adalah kategori, terakhir adalah 'Year'
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Menampilkan data di Streamlit
st.title("Dashboard Analisis Wisatawan")
st.dataframe(df)

# Menampilkan Total Pengunjung per Lokasi
st.subheader("Total Kunjungan per Pintu Masuk")
df['Total'] = df[numeric_columns].sum(axis=1)
total_visitors = df[['Pintu Masuk', 'Total']].sort_values(by='Total', ascending=False)
st.bar_chart(total_visitors.set_index('Pintu Masuk'))

# Menampilkan data visualisasi lainnya (best & worst performance)
st.subheader("Pintu Masuk dengan Pengunjung Tertinggi & Terendah")
top_performance = total_visitors.head(5)
bottom_performance = total_visitors.tail(5)

col1, col2 = st.columns(2)
with col1:
    st.write("Tertinggi")
    st.dataframe(top_performance)

with col2:
    st.write("Terendah")
    st.dataframe(bottom_performance)
