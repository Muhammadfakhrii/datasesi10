import streamlit as st
import pandas as pd
import os

# File paths
file_paths = {
    '2017': '2017.xlsx',
    '2018': '2018.xlsx',
    '2019': '2019.xlsx',
    '2020': '2020.xlsx',
    '2021': '2021.xlsx',
    '2022': '2022.xlsx',
    '2023': '2023.xlsx',
}

# Load data
def load_data():
    all_data = {}
    for year, path in file_paths.items():
        try:
            df = pd.read_excel(path)
            all_data[year] = df
        except Exception as e:
            st.error(f"Error loading {path}: {e}")
    return all_data

# Sidebar
st.sidebar.title("Kelompok")
st.sidebar.write("1. Anggota 1\n2. Anggota 2\n3. Anggota 3")

# Header
st.title("Dashboard Wisatawan Masuk ke Indonesia (2017-2023)")
st.subheader("Analisis Jalur Masuk: Darat, Laut, Udara")

# Load all data
data = load_data()

# Sidebar Filters
st.sidebar.header("Pilih Filter")
year = st.sidebar.selectbox("Pilih Tahun", options=list(data.keys()))
month = st.sidebar.selectbox("Pilih Bulan", options=range(1, 13))
route = st.sidebar.selectbox("Pilih Jalur", options=["Darat", "Laut", "Udara"])
show_total = st.sidebar.checkbox("Tampilkan Total Semua Jalur")
show_distribution = st.sidebar.checkbox("Distribusi Kunjungan Perbulan")
show_trend = st.sidebar.checkbox("Trend Kunjungan Per Jalur")

# Filter Data
if year in data:
    df_selected = data[year]
    if 'Bulan' in df_selected.columns:
        df_selected = df_selected[df_selected['Bulan'] == month]

    # Main Container
    with st.container():
        # Bar chart untuk jalur tertentu
        st.subheader(f"Kunjungan Melalui Jalur {route} di Tahun {year}, Bulan {month}")
        if route in df_selected.columns:
            chart_data = df_selected[[route]].sum()
            st.bar_chart(chart_data)
        else:
            st.error(f"Kolom '{route}' tidak ditemukan dalam data!")

        # Total semua jalur
        if show_total:
            st.subheader(f"Total Kunjungan Semua Jalur di Tahun {year}, Bulan {month}")
            total_data = df_selected.sum()
            st.bar_chart(total_data)

        # Distribusi per bulan
        if show_distribution:
            st.subheader(f"Distribusi Kunjungan per Bulan di Tahun {year}")
            if 'Bulan' in df_selected.columns:
                monthly_data = df_selected.groupby("Bulan").sum()
                st.bar_chart(monthly_data)
            else:
                st.error("Kolom 'Bulan' tidak ditemukan dalam data!")

        # Trend per jalur
        if show_trend:
            st.subheader(f"Trend Kunjungan per Jalur (2017-2023)")
            trend_data = pd.DataFrame({
                year: data[year][route].sum() if route in data[year].columns else 0
                for year in data.keys()
            }, index=[route])
            st.bar_chart(trend_data)
else:
    st.error("Data untuk tahun yang dipilih tidak ditemukan!")
