import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime as dt

# --------------------- Konfigurasi Halaman -------------------------
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

# --------------------- Styling CSS -------------------------
st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
        h1 {
            color: #ff7f0e;
            text-align: center;
        }
        h2 {
            color: #1f77b4;
        }
        .block-container {
            padding-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# --------------------- Sidebar -------------------------
st.sidebar.image('https://raw.githubusercontent.com/bagusangkasawan/data-analysis/refs/heads/main/dashboard/bikes-sharing.png', use_column_width=True)
st.sidebar.header('🚲 Bike Sharing Dashboard')
st.sidebar.write("Gunakan dashboard ini untuk menganalisis data penyewaan sepeda berdasarkan kondisi cuaca, waktu, dan tipe pengguna.")
st.sidebar.markdown("---")
st.sidebar.text('Created by: Ryan Nugroho')

# --------------------- Data Loading -------------------------
@st.cache_data
def load_data():
    day = pd.read_csv("https://raw.githubusercontent.com/ryannugroho/Analisis-Data/refs/heads/main/data/day.csv")
    hour = pd.read_csv("https://raw.githubusercontent.com/ryannugroho/Analisis-Data/refs/heads/main/data/hour.csv")
    day["dteday"] = pd.to_datetime(day["dteday"])
    hour["dteday"] = pd.to_datetime(hour["dteday"])
    return day, hour

day, hour = load_data()

# --------------------- Layout Utama -------------------------
st.title("🚲 Bike Sharing Data Analysis")

# Membagi dashboard menjadi dua kolom
col1, col2 = st.columns([1, 1])

# --------------------- Visualisasi 1: Cuaca -------------------------
weathersit_count = day.groupby("weathersit")[["casual", "registered"]].sum()

with col1:
    st.subheader("Jumlah Penyewaan Berdasarkan Cuaca")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=weathersit_count.index, y=weathersit_count['casual'], color='skyblue', label='Casual')
    sns.barplot(x=weathersit_count.index, y=weathersit_count['registered'], color='orange', label='Registered', bottom=weathersit_count['casual'])
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Jumlah Penyewaan (Juta)')
    ax.set_title('Jumlah Penyewaan Sepeda Berdasarkan Cuaca')
    ax.legend()
    plt.xticks(weathersit_count.index-1, ['Cerah', 'Mendung', 'Hujan Sedang'])
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x/1000000:.1f}Jt'))
    st.pyplot(fig)

# --------------------- Visualisasi 2: Waktu -------------------------
hour["hr_group"] = hour.hr.apply(lambda x: "Dini Hari" if x < 6 else 
                                           "Pagi" if x < 11 else 
                                           "Siang" if x < 15 else 
                                           "Sore" if x < 18 else "Malam")
hr_group_count = hour.groupby("hr_group")[['casual', 'registered']].sum()

with col2:
    st.subheader("Jumlah Penyewaan Berdasarkan Waktu")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=hr_group_count.index, y=hr_group_count['casual'], color='skyblue', label='Casual')
    sns.barplot(x=hr_group_count.index, y=hr_group_count['registered'], color='orange', label='Registered', bottom=hr_group_count['casual'])
    ax.set_xlabel('Waktu')
    ax.set_ylabel('Jumlah Penyewaan (Juta)')
    ax.set_title('Jumlah Penyewaan Sepeda Berdasarkan Waktu')
    ax.legend()
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x/1000000:.1f}Jt'))
    st.pyplot(fig)

# --------------------- Visualisasi 3: Cluster -------------------------
def cluster_group(row):
    if row['weathersit'] == 1:
        return 'Clear_Workday' if row['workingday'] == 1 else 'Clear_Holiday'
    elif row['weathersit'] == 2:
        return 'Cloudy_Workday' if row['workingday'] == 1 else 'Cloudy_Holiday'
    elif row['weathersit'] == 3:
        return 'Light_Rain_Workday' if row['workingday'] == 1 else 'Light_Rain_Holiday'

day['cluster'] = day.apply(cluster_group, axis=1)
cluster_counts = day.groupby('cluster')[['registered', 'casual']].sum()

st.subheader("Total Penyewaan Berdasarkan Cluster")
fig, ax = plt.subplots(figsize=(12, 8))
bar_width = 0.35
ax.barh(cluster_counts.index, cluster_counts['registered'], height=bar_width, label='Registered', color='#1f77b4')
ax.barh(cluster_counts.index, cluster_counts['casual'], height=bar_width, label='Casual', color='#ff7f0e', left=cluster_counts['registered'])
ax.set_xlabel('Jumlah Penyewaan')
ax.set_ylabel('Cluster')
ax.set_title('Total Penyewaan Sepeda Berdasarkan Cluster')
ax.legend(title='Tipe Pengguna')
ax.grid(axis='x', linestyle='--', alpha=0.7)
st.pyplot(fig)