import streamlit as st
import pandas as pd
import os
from pathlib import Path

# File paths
file_path = '2017xlsx'
file_path = '2018.xlsx'
file_path = '2020.xlsx' 
file_path = '2021.xlsx' 
file_path = '2022.xlsx' 
file_path = '2023.xlsx' 


# Load data
df = pd.read_excel(file_path)

# Sidebar
st.sidebar.title("Kelompok")
st.sidebar.write("1. Anggota 1\n2. Anggota 2\n3. Anggota 3")

# Header
st.title("Dashboard Wisatawan Masuk ke Indonesia (2017-2023)")
st.subheader("Analisis Jalur Masuk: Darat, Laut, Udara")

# Data Loading
data = load_data()

# Pilihan Widget
st.sidebar.header("Pilih Filter")
year = st.sidebar.selectbox("Pilih Tahun", options=list(data.keys()))
month = st.sidebar.selectbox("Pilih Bulan", options=range(1, 13))
route = st.sidebar.selectbox("Pilih Jalur", options=["Darat", "Laut", "Udara"])
show_total = st.sidebar.checkbox("Tampilkan Total Semua Jalur")
show_distribution = st.sidebar.checkbox("Distribusi Kunjungan Perbulan")
show_trend = st.sidebar.checkbox("Trend Kunjungan Per Jalur")

# Filter Data
df_selected = data[year]
if 'Bulan' in df_selected.columns:
    df_selected = df_selected[df_selected['Bulan'] == month]

# Main Container
with st.container():
    # Bar chart untuk jalur tertentu
    st.subheader(f"Kunjungan Melalui Jalur {route} di Tahun {year}, Bulan {month}")
    chart_data = df_selected[[route]].sum()
    st.bar_chart(chart_data)

    # Total semua jalur
    if show_total:
        st.subheader(f"Total Kunjungan Semua Jalur di Tahun {year}, Bulan {month}")
        total_data = df_selected.sum()
        st.bar_chart(total_data)

    # Distribusi per bulan
    if show_distribution:
        st.subheader(f"Distribusi Kunjungan per Bulan di Tahun {year}")
        monthly_data = df_selected.groupby("Bulan").sum()
        st.bar_chart(monthly_data)

    # Trend per jalur
    if show_trend:
        st.subheader(f"Trend Kunjungan per Jalur (2017-2023)")
        trend_data = pd.DataFrame({
            year: data[year][route].sum() for year in data.keys()
        }, index=[route])
        st.bar_chart(trend_data)
