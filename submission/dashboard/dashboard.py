import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# LOAD DAN SIAPKAN DATA
day_df = pd.read_csv("day_clean.csv")
hour_df = pd.read_csv("hour_clean.csv")

# Ubah kolom tanggal ke format datetime
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

# Tambahkan kolom tahun dan bulan
day_df["year"] = day_df["dteday"].dt.year
day_df["month"] = day_df["dteday"].dt.month

hour_df["year"] = hour_df["dteday"].dt.year
hour_df["month"] = hour_df["dteday"].dt.month

# SIDEBAR FILTER (bagian menu samping kiri dashboard)
st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/2972/2972185.png",
    width=80
)
st.sidebar.title("🚲 Filter Dashboard")

selected_year = st.sidebar.multiselect(
    "Pilih Tahun",
    options=sorted(day_df["year"].unique()),
    default=sorted(day_df["year"].unique())
)

selected_weather = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca",
    options=sorted(day_df["weathersit"].unique()),
    default=sorted(day_df["weathersit"].unique())
)

# Filter data day
filtered_day = day_df[
    (day_df["year"].isin(selected_year)) &
    (day_df["weathersit"].isin(selected_weather))
].copy()

# Filter data hour
filtered_hour = hour_df[
    (hour_df["year"].isin(selected_year)) &
    (hour_df["weathersit"].isin(selected_weather))
].copy()

# Menyederhakan Kode
def show_metric_card(title, subtitle, value):
    st.markdown(
        f"""
        <div style="
            background-color:#FFF0F5;
            padding:20px;
            border-radius:12px;
            text-align:center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        ">
            <h5 style="margin:0; color:#7A4E63;">{title}</h5>
            <p style="margin:8px 0; color:#A67C8B; font-size:14px;">{subtitle}</p>
            <h2 style="color:#D16D9E;">{value}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_section_title(title):
    st.markdown(
        f"""
        <div style="
            background-color:#F4A6C1;
            padding:10px;
            border-radius:8px;
            margin-bottom:10px;
        ">
            <h3 style="color:white; margin:0;">{title}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_conclusion_box(text, min_height="250px"):
    st.markdown(
        f"""
        <div style="
            background-color:#FFF0F5;
            padding:15px;
            border-radius:12px;
            min-height:{min_height};
        ">
            <h4 style="color:#B85C8A;">Kesimpulan</h4>
            <p style="color:#6E4B5B; text-align:justify;">
                {text}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def categorize_hour(hr):
    if 6 <= hr <= 9:
        return "Morning Peak"
    elif 10 <= hr <= 15:
        return "Afternoon"
    elif 16 <= hr <= 19:
        return "Evening Peak"
    else:
        return "Off Hours"


# HEADER DASHBOARD
st.markdown(
    """
    <div style="
        background-color:#E78FB3;
        padding:18px;
        border-radius:12px;
        margin-bottom:20px;
    ">
        <h1 style="
            color:white;
            text-align:left;
            margin:0;
            font-size:34px;
        ">🚲 Bike Sharing Dashboard</h1>
        <p style="
            color:#FFF5F7;
            margin-top:8px;
            font-size:16px;
        ">
            Dashboard ini menampilkan analisis penyewaan sepeda berdasarkan waktu, cuaca, dan pola pengguna.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# CEK DATA HASIL FILTER
if filtered_day.empty or filtered_hour.empty:
    st.warning("Data tidak ditemukan untuk kombinasi filter yang dipilih. Silakan ubah filter tahun atau cuaca.")
    st.stop()

# RINGKASAN DATA
st.markdown("### Ringkasan Data")

# Statistik jumlah data
st.markdown("#### Jumlah Data")
col1, col2 = st.columns(2)

with col1:
    show_metric_card("Total Data Day", "Data harian", len(filtered_day))

with col2:
    show_metric_card("Total Data Hour", "Data per jam", len(filtered_hour))

# Statistik data day
avg_day = round(filtered_day["cnt"].mean(), 2)
max_day = int(filtered_day["cnt"].max())
min_day = int(filtered_day["cnt"].min())

st.markdown("#### Statistik Penyewaan dari Data Day")
col3, col4, col5 = st.columns(3)

with col3:
    show_metric_card("Rata-rata Penyewaan", "Berdasarkan data day", avg_day)

with col4:
    show_metric_card("Penyewaan Tertinggi", "Berdasarkan data day", max_day)

with col5:
    show_metric_card("Penyewaan Terendah", "Berdasarkan data day", min_day)

# Statistik data hour
avg_hour = round(filtered_hour["cnt"].mean(), 2)
max_hour = int(filtered_hour["cnt"].max())
min_hour = int(filtered_hour["cnt"].min())

st.markdown("#### Statistik Penyewaan dari Data Hour")
col6, col7, col8 = st.columns(3)

with col6:
    show_metric_card("Rata-rata per Jam", "Berdasarkan data hour", avg_hour)

with col7:
    show_metric_card("Penyewaan Tertinggi", "Berdasarkan data hour", max_hour)

with col8:
    show_metric_card("Penyewaan Terendah", "Berdasarkan data hour", min_hour)

st.markdown("##")

# ANALISIS TREN PENYEWAAN DARI 2011 SAMPAI 2012
show_section_title("Analisis Tren Penyewaan dari Tahun 2011 sampai 2012")

col_a1, col_a2 = st.columns([3, 1])

with col_a1:
    monthly_trend = (
        filtered_day.groupby(["year", "month"])["cnt"]
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    year_colors = {
        2011: "#D16D9E",
        2012: "#7A86B6"
    }

    for year in sorted(monthly_trend["year"].unique()):
        trend_data = monthly_trend[monthly_trend["year"] == year]

        ax.plot(
            trend_data["month"],
            trend_data["cnt"],
            marker="o",
            linewidth=2,
            label=str(year),
            color=year_colors.get(year, None)
        )

        max_point = trend_data.loc[trend_data["cnt"].idxmax()]
        min_point = trend_data.loc[trend_data["cnt"].idxmin()]

        ax.scatter(max_point["month"], max_point["cnt"], color="red", s=80, zorder=5)
        ax.scatter(min_point["month"], min_point["cnt"], color="orange", s=80, zorder=5)

    ax.set_title("Perbandingan Tren Penyewaan Sepeda per Tahun", fontsize=14)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.set_xticks(range(1, 13))
    ax.legend(title="Tahun")
    ax.grid(True, linestyle="--", alpha=0.7)

    plt.tight_layout()
    st.pyplot(fig)

with col_a2:
    show_conclusion_box(
        "Dari grafik terlihat bahwa jumlah penyewaan pada tahun 2012 cenderung lebih tinggi dibandingkan "
        "tahun 2011. Secara umum, penyewaan meningkat pada pertengahan hingga akhir tahun, sedangkan pada "
        "awal tahun jumlahnya masih relatif lebih rendah.",
        min_height="320px"
    )

st.markdown("##")

# ANALISIS KONDISI CUACA
show_section_title("Analisis Kondisi Cuaca")

col_b1, col_b2 = st.columns([2, 1])

with col_b1:
    weather_trend = filtered_day.groupby("weathersit")["cnt"].mean()

    highlight_value = weather_trend.max()
    colors = ["#EC86B5" if val == highlight_value else "#FADADD" for val in weather_trend]

    fig, ax = plt.subplots(figsize=(6, 3.5))
    weather_trend.plot(kind="bar", color=colors, ax=ax)

    ax.set_title("Penyewaan Berdasarkan Kondisi Cuaca", fontsize=10)
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.tick_params(axis="x", rotation=0)

    plt.tight_layout()
    st.pyplot(fig)

with col_b2:
    show_conclusion_box(
        "Cuaca yang lebih baik cenderung diikuti oleh jumlah penyewaan yang lebih tinggi. "
        "Sebaliknya, ketika kondisi cuaca kurang mendukung, jumlah penyewaan sepeda juga ikut menurun."
    )

st.markdown("##")

# ANALISIS HARI KERJA DAN HARI LIBUR
show_section_title("Analisis Hari Kerja dan Hari Libur")

col_c1, col_c2 = st.columns([2, 1])

with col_c1:
    workingday_trend = filtered_day.groupby("workingday")["cnt"].mean()

    fig, ax = plt.subplots(figsize=(6, 3.5))
    workingday_trend.plot(kind="bar", color=["#F8C8DC", "#EC86B5"], ax=ax)

    ax.set_title("Perbandingan Hari Kerja dan Hari Libur", fontsize=10)
    ax.set_xlabel("Kategori Hari")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Libur", "Hari Kerja"], rotation=0)

    plt.tight_layout()
    st.pyplot(fig)

with col_c2:
    show_conclusion_box(
        "Rata-rata penyewaan pada hari kerja terlihat sedikit lebih tinggi dibandingkan hari libur. "
        "Hal ini menunjukkan bahwa sepeda cukup sering digunakan untuk kegiatan rutin sehari-hari."
    )

st.markdown("##")

# ANALISIS POLA PENGGUNA BERDASARKAN WAKTU
show_section_title("Analisis Pola Pengguna Casual Vs Registered")

col_d1, col_d2 = st.columns([2, 1])

with col_d1:
    hour_trend = filtered_hour.groupby("hr")[["casual", "registered"]].mean()

    fig, ax = plt.subplots(figsize=(6, 3.5))
    hour_trend.plot(ax=ax, color=["#F4A6C1", "#C76D9C"])

    ax.set_title("Pola Penyewaan Casual dan Registered per Jam", fontsize=10)
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Penyewaan")

    plt.tight_layout()
    st.pyplot(fig)

with col_d2:
    show_conclusion_box(
        "Pengguna registered lebih aktif pada jam-jam sibuk, terutama pada pagi dan sore hari. "
        "Sementara itu, pengguna casual cenderung lebih banyak menyewa pada siang hingga sore."
    )

st.markdown("##")


# ANALISIS BERDASARKAN KELOMPOK WAKTU
show_section_title("Analisis Penyewaan Berdasarkan Kelompok Waktu/ Clustering")

filtered_hour["time_group"] = filtered_hour["hr"].apply(categorize_hour)

col_e1, col_e2 = st.columns([2, 1])

with col_e1:
    time_group_trend = (
        filtered_hour.groupby("time_group")["cnt"]
        .mean()
        .reindex(["Off Hours", "Morning Peak", "Afternoon", "Evening Peak"])
    )

    fig, ax = plt.subplots(figsize=(6, 3.5))
    time_group_trend.plot(
        kind="bar",
        color=["#F6BD60", "#84A59D", "#90BE6D", "#F28482"],
        ax=ax
    )

    ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Kelompok Waktu", fontsize=10)
    ax.set_xlabel("Kelompok Waktu")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    ax.tick_params(axis="x", rotation=0)

    plt.tight_layout()
    st.pyplot(fig)

with col_e2:
    show_conclusion_box(
        "Kelompok waktu dengan rata-rata penyewaan tertinggi berada pada evening peak. "
        "Sementara itu, off hours menunjukkan aktivitas penyewaan yang paling rendah."
    )

# FOOTER
st.markdown("---")
st.caption("🚲 by Sabrina Ganeshswara Putri")