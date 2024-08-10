import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go

# Fungsi untuk mengambil data dari Firebase
@st.cache_data(ttl=3600)
def fetch_data():
    url = "https://sleep-quality-7cba3-default-rtdb.asia-southeast1.firebasedatabase.app/sensorData/5000.json"
    response = requests.get(url)
    data = response.json()

    # Mengonversi data ke DataFrame
    df = pd.DataFrame(data).transpose()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(by='timestamp')
    return df

# Fungsi untuk mengunduh data sebagai CSV
def download_data(df):
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Unduh Data sebagai CSV",
        data=csv,
        file_name='data_kualitas_tidur.csv',
        mime='text/csv',
    )

# Fungsi untuk menampilkan ringkasan metrik utama
def show_key_metrics(df):
    st.markdown("### Ringkasan Metrik Utama")
    avg_loudness = df['loudness'].mean()
    max_loudness = df['loudness'].max()
    total_triggers = df['trigger_count'].sum()
    avg_accel_x = df['acceleration_x'].mean()
    avg_accel_y = df['acceleration_y'].mean()
    avg_accel_z = df['acceleration_z'].mean()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Rata-rata Loudness", value=f"{avg_loudness:.2f} dB")
        st.metric(label="Maksimal Loudness", value=f"{max_loudness:.2f} dB")
    with col2:
        st.metric(label="Total Trigger", value=f"{total_triggers}")
    with col3:
        st.metric(label="Rata-rata Acceleration X", value=f"{avg_accel_x:.2f} m/s²")
        st.metric(label="Rata-rata Acceleration Y", value=f"{avg_accel_y:.2f} m/s²")
        st.metric(label="Rata-rata Acceleration Z", value=f"{avg_accel_z:.2f} m/s²")

# Fungsi untuk menampilkan analisis data dengan visualisasi yang profesional
def show_advanced_analysis(df):
    st.markdown("### Analisis Kualitas Tidur")

    # Trend Loudness
    fig1 = px.line(df, x='timestamp', y='loudness', title="Tren Loudness Seiring Waktu", color_discrete_sequence=['#FF6347'])
    fig1.update_layout(xaxis_title="Waktu", yaxis_title="Loudness (dB)", plot_bgcolor='rgba(0,0,0,0.1)')
    st.plotly_chart(fig1, use_container_width=True)

    # Histogram Loudness
    fig2 = px.histogram(df, x='loudness', nbins=20, title="Distribusi Loudness", color_discrete_sequence=['#1E90FF'])
    fig2.update_layout(xaxis_title="Loudness (dB)", yaxis_title="Frekuensi", plot_bgcolor='rgba(0,0,0,0.1)')
    st.plotly_chart(fig2, use_container_width=True)

    # Box Plot Acceleration
    fig3 = go.Figure()
    fig3.add_trace(go.Box(y=df['acceleration_x'], name='Acceleration X', marker_color='#FF1493'))
    fig3.add_trace(go.Box(y=df['acceleration_y'], name='Acceleration Y', marker_color='#00FA9A'))
    fig3.add_trace(go.Box(y=df['acceleration_z'], name='Acceleration Z', marker_color='#FFD700'))
    fig3.update_layout(title="Distribusi Akselerasi", yaxis_title="Acceleration (m/s²)", plot_bgcolor='rgba(0,0,0,0.1)')
    st.plotly_chart(fig3, use_container_width=True)

    # Trigger Count Over Time
    df_trigger = df[['timestamp', 'trigger_count']].groupby(pd.Grouper(key='timestamp', freq='H')).sum().reset_index()
    fig4 = px.bar(df_trigger, x='timestamp', y='trigger_count', title="Jumlah Trigger per Jam", color_discrete_sequence=['#32CD32'])
    fig4.update_layout(xaxis_title="Waktu", yaxis_title="Jumlah Trigger", plot_bgcolor='rgba(0,0,0,0.1)')
    st.plotly_chart(fig4, use_container_width=True)

# Fungsi untuk menampilkan data dalam bentuk tabel yang mudah dipahami
def show_data_table(df):
    st.markdown("### Tabel Data")
    st.write("Tabel di bawah ini menampilkan data kualitas tidur yang telah dikumpulkan oleh sensor:")
    st.dataframe(df)

# Layout utama
st.set_page_config(page_title="Dashboard Kualitas Tidur", layout="wide", initial_sidebar_state="expanded")

# Sidebar untuk Kontrol Panel
with st.sidebar:
    st.title("Kontrol Panel")
    st.write("Gunakan kontrol panel di bawah ini untuk memperbarui data dan mengunduh data yang telah dikumpulkan.")

    # Mengambil data
    df = fetch_data()

    # Tombol untuk memperbarui data
    if st.button("Perbarui Data"):
        df = fetch_data()
        st.success("Data berhasil diperbarui!")

    st.subheader("Unduh Data")
    download_data(df)

# Layout utama
st.title("Dashboard Pemantauan Kualitas Tidur")
st.markdown("<h4 style='text-align: center; color: #0073e6;'>Analisis Mendalam dan Visualisasi Kualitas Tidur Anda</h4>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Ringkasan Data", "Analisis Kualitas Tidur", "Data Mentah", "Tentang"])

with tab1:
    st.markdown("## Ringkasan Data")
    st.write("Tab ini menampilkan ringkasan singkat dari data yang dikumpulkan selama pemantauan kualitas tidur.")
    show_key_metrics(df)

with tab2:
    st.markdown("## Analisis Kualitas Tidur")
    st.write("Tab ini menyajikan analisis visual yang lebih mendalam dari data yang dikumpulkan.")
    show_advanced_analysis(df)

with tab3:
    st.markdown("## Data Mentah")
    st.write("Tab ini menampilkan data mentah yang dikumpulkan oleh sensor dalam bentuk tabel.")
    show_data_table(df)

with tab4:
    st.markdown("## Tentang")
    st.write("Dashboard ini dibuat untuk memantau dan menganalisis kualitas tidur Anda berdasarkan data yang dikumpulkan dari sensor.")
    st.write("Untuk informasi lebih lanjut tentang cara kerja dashboard atau untuk umpan balik, silakan hubungi kami di [saepulloh0711@gmail.com](mailto:saepulloh0711@gmail.com).")
