import textwrap
import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import io
import html
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

st.set_page_config(
    page_title="Dashboard Cabai Simalungun",
    page_icon="🌶️",
    layout="wide"
)
st.markdown(
    """
        <style>

    /* =========================================
       1. BACKGROUND UTAMA
    ========================================= */

    :root {
        color-scheme: light;
    }

    .stApp {
        background: linear-gradient(
            135deg,
            #F3F7F2 0%,
            #EAF2EC 52%,
            #F8FAF7 100%
        );
        color: #24372C;
    }

    [data-testid="stAppViewContainer"] {
        background: transparent;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.7rem;
        padding-bottom: 3rem;
    }


    /* =========================================
       2. WARNA TEKS UTAMA
    ========================================= */

    .main,
    .main p,
    .main li,
    .main label,
    .main [data-testid="stMarkdownContainer"],
    .main [data-testid="stCaptionContainer"] {
        color: #26392E !important;
    }

    .main h1 {
        color: #17452D !important;
        font-weight: 800 !important;
        letter-spacing: -0.8px;
    }

    .main h2,
    .main h3 {
        color: #24583A !important;
        font-weight: 750 !important;
    }


    /* =========================================
       3. SIDEBAR HIJAU TUA
    ========================================= */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #123B2B 0%,
            #1D563B 100%
        );
        border-right: 1px solid #24583A;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p {
        color: #F4F8F4 !important;
    }

    section[data-testid="stSidebar"]
    [data-testid="stCaptionContainer"] {
        color: #D1E3D5 !important;
    }

    section[data-testid="stSidebar"]
    [data-testid="stWidgetLabel"] p {
        color: #F4F8F4 !important;
        font-weight: 600;
    }

    section[data-testid="stSidebar"]
    [data-baseweb="select"] > div {
        background: #FFFFFF !important;
        border: 1px solid #CFE0D2 !important;
        border-radius: 9px;
    }

    section[data-testid="stSidebar"]
    [data-baseweb="select"] input {
        color: #193D2B !important;
    }

    section[data-testid="stSidebar"]
    [data-baseweb="tag"] {
        background: #E1F0E5 !important;
    }

    section[data-testid="stSidebar"]
    [data-baseweb="tag"] span {
        color: #1B4A32 !important;
    }

    section[data-testid="stSidebar"]
    .stButton > button {
        background: #F2F7F2;
        color: #17452D !important;
        border: 1px solid #D5E4D8;
        font-weight: 700;
    }


/* =========================================
   KARTU STATISTIK - PREMIUM DESIGN
========================================= */

[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        #FFFFFF 0%,
        #F0F8F2 100%
    ) !important;

    border: 1px solid #D6E7DA !important;
    border-left: 5px solid #238653 !important;

    border-radius: 18px !important;
    padding: 24px 22px !important;

    min-height: 145px;

    box-shadow: 0 6px 20px
        rgba(25, 75, 45, 0.07) !important;

    transition: all 0.25s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-4px);

    box-shadow: 0 12px 26px
        rgba(25, 75, 45, 0.13) !important;

    border-color: #91BDA0 !important;
}

[data-testid="stMetricLabel"] {
    color: #587462 !important;
    font-size: 13px !important;
    font-weight: 750 !important;
    letter-spacing: 0.4px;
}

[data-testid="stMetricValue"] {
    color: #16472E !important;
    font-size: 30px !important;
    font-weight: 850 !important;
    letter-spacing: -0.5px;
}

[data-testid="stMetricDelta"] {
    font-weight: 700 !important;
}

    /* =========================================
       5. TOMBOL
    ========================================= */

    .stButton > button,
    .stDownloadButton > button {
        background: #FFFFFF;
        color: #1E5B3A !important;
        border-radius: 11px;
        border: 1px solid #BFD5C4;
        font-weight: 700;
        min-height: 43px;
        transition: all 0.2s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: #EAF4EC;
        border-color: #287A48;
        color: #17452D !important;
    }


    /* =========================================
       6. TAB NAVIGASI
    ========================================= */

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #D9E6DC;
    }

    .stTabs [data-baseweb="tab"] {
        background: #E8F1EA;
        color: #315C42 !important;
        border-radius: 10px 10px 0 0;
        padding: 11px 17px;
        font-weight: 700;
    }

    .stTabs [aria-selected="true"] {
        background: #1D6A43 !important;
        color: #FFFFFF !important;
    }

    .stTabs [aria-selected="true"] * {
        color: #FFFFFF !important;
    }


    /* =========================================
       7. KARTU GRAFIK
    ========================================= */

    div[data-testid="stPlotlyChart"] {
        background: #FFFFFF;
        border: 1px solid #DFEAE1;
        border-radius: 17px;
        padding: 12px;
        box-shadow: 0 4px 15px rgba(30, 70, 45, 0.05);
    }


    /* =========================================
       8. TABEL DATA
    ========================================= */

    div[data-testid="stDataFrame"] {
        background: #FFFFFF;
        border: 1px solid #DCE8DE;
        border-radius: 13px;
        overflow: hidden;
    }


    /* =========================================
       9. EXPANDER
    ========================================= */

    div[data-testid="stExpander"] {
        background: #FFFFFF;
        border: 1px solid #DCE8DE;
        border-radius: 13px;
    }


    /* =========================================
       10. PEMBATAS
    ========================================= */

    hr {
        border-color: #D6E4D9;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }


    /* =========================================
       11. RESPONSIVE MOBILE
    ========================================= */

    @media screen and (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1rem;
        }

        [data-testid="stMetric"] {
            padding: 12px;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.3rem !important;
        }

        .main h1 {
            font-size: 1.7rem !important;
        }

        .main h2 {
            font-size: 1.35rem !important;
        }
    }

/* SIDEBAR MENU - FORCE LIGHT TEXT */

section[data-testid="stSidebar"]
[data-testid="stMarkdownContainer"] a,
section[data-testid="stSidebar"]
[data-testid="stMarkdownContainer"] a:link,
section[data-testid="stSidebar"]
[data-testid="stMarkdownContainer"] a:visited {

    color: #FFFFFF !important;

    text-decoration: none !important;

    background: rgba(255,255,255,0.09) !important;

    border: 1px solid rgba(255,255,255,0.13) !important;

    border-radius: 10px !important;

    display: block !important;

    padding: 11px 13px !important;

    margin: 7px 0 !important;

    font-weight: 600 !important;
}

section[data-testid="stSidebar"]
[data-testid="stMarkdownContainer"] a:hover {

    color: #FFFFFF !important;

    background: rgba(255,255,255,0.22) !important;

    border-color: rgba(255,255,255,0.35) !important;

    text-decoration: none !important;
}

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================
# MENU NAVIGASI DASHBOARD - STABIL
# =========================================

st.sidebar.markdown("### 🌶️ SIMALUNGUN DASHBOARD")

st.sidebar.caption(
    "Pusat Informasi Produksi Cabai"
)

st.sidebar.markdown("---")

st.sidebar.markdown("**MENU UTAMA**")

st.sidebar.markdown(
    "[🏠 Ringkasan Dashboard](#ringkasan-dashboard)"
)

st.sidebar.markdown(
    "[📈 Tren Produksi Bulanan](#grafik-bulanan)"
)

st.sidebar.markdown(
    "[📊 Perbandingan Tahunan](#perbandingan-tahunan)"
)

st.sidebar.markdown(
    "[📉 Analisis Tren Komoditas](#analisis-tren-komoditas)"
)

st.sidebar.markdown(
    "[🥧 Kontribusi Komoditas](#kontribusi-komoditas)"
)

st.sidebar.markdown(
    "[🌱 Produktivitas dan Luas Panen](#produktivitas-lahan)"
)

st.sidebar.markdown(
    "[📋 Data Produksi Bulanan](#data-bulanan)"
)

st.sidebar.divider()

# =========================================
# HERO SECTION - PREMIUM DASHBOARD
# =========================================

st.components.v1.html(
    """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    background: transparent;
    font-family: Arial, sans-serif;
}

.hero {
    position: relative;
    overflow: hidden;
    min-height: 310px;
    padding: 36px 42px;
    border-radius: 23px;
    background: linear-gradient(
        120deg,
        #103D2C 0%,
        #176342 55%,
        #39885C 100%
    );
    box-shadow: 0 12px 30px rgba(18,59,43,0.14);
    border: 1px solid rgba(255,255,255,0.12);
}

.hero-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 25px;
    position: relative;
    z-index: 2;
}

.hero-copy {
    flex: 1;
    min-width: 0;
}

.eyebrow {
    display: inline-block;
    background: rgba(255,255,255,0.14);
    color: #E4F4E8;
    padding: 9px 15px;
    border-radius: 30px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.4px;
}

.hero h1 {
    color: #FFFFFF;
    font-size: clamp(27px, 3.4vw, 43px);
    font-weight: 800;
    line-height: 1.2;
    margin: 22px 0 12px;
}

.hero h2 {
    color: #E5F3E9;
    font-size: 21px;
    font-weight: 600;
    margin: 0 0 14px;
}

.hero-description {
    color: #D5E9DB;
    font-size: 15px;
    line-height: 1.8;
    max-width: 680px;
}

.period {
    display: inline-block;
    margin-top: 22px;
    padding: 10px 17px;
    border-radius: 9px;
    background: #E6F3E9;
    color: #17452D;
    font-size: 13px;
    font-weight: 750;
}

.hero-icon {
    width: 145px;
    height: 145px;
    flex-shrink: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.22);
    border-radius: 30px;
    font-size: 82px;
}

.circle {
    position: absolute;
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 50%;
}

.circle-one {
    width: 250px;
    height: 250px;
    right: -80px;
    bottom: -145px;
}

.circle-two {
    width: 160px;
    height: 160px;
    right: 90px;
    top: -115px;
}

@media(max-width:650px) {
    .hero {
        padding: 27px 23px;
        min-height: 290px;
    }

    .hero-icon {
        display: none;
    }

    .hero h1 {
        font-size: 27px;
    }

    .hero h2 {
        font-size: 18px;
    }
}
</style>
</head>

<body>
<div class="hero">

    <div class="hero-content">

        <div class="hero-copy">

            <div class="eyebrow">
                PUSAT INFORMASI PERTANIAN
            </div>

            <h1>
                DASHBOARD PRODUKSI CABAI
            </h1>

            <h2>
                Kabupaten Simalungun
            </h2>

            <div class="hero-description">
                Platform informasi dan analisis data produksi,
                luas panen, serta produktivitas cabai
                untuk periode 2021–2025.
            </div>

            <div class="period">
                📊 PERIODE DATA 2021 - 2025
            </div>

        </div>

        <div class="hero-icon">
            🌶️
        </div>

    </div>

    <div class="circle circle-one"></div>
    <div class="circle circle-two"></div>

</div>
</body>
</html>
    """,
    height=340,
    scrolling=False
)

# KONEKSI DATABASE NEON
@st.cache_data(ttl=300)
def ambil_data():

    conn = psycopg2.connect(
        st.secrets["DATABASE_URL"]
    )

    try:
        df = pd.read_sql_query("""
    SELECT *
    FROM dw.vw_produksi_bulanan
    ORDER BY tahun, bulan, komoditas
""", conn)

        return df

    finally:
        conn.close()


# MEMUAT DATA
try:
    df = ambil_data()

except Exception as e:
    st.error("Gagal menghubungkan database Neon.")
    st.error(str(e))
    st.stop()
# =========================================
# FILTER DATA
# =========================================

st.sidebar.markdown("### 🎛️ FILTER DATA")

st.sidebar.caption(
    "Atur periode dan komoditas untuk menyesuaikan analisis."
)

tahun = st.sidebar.multiselect(
    "Pilih Tahun",
    sorted(df["tahun"].unique()),
    default=sorted(df["tahun"].unique())
)

komoditas = st.sidebar.multiselect(
    "Pilih Komoditas",
    sorted(df["komoditas"].unique()),
    default=sorted(df["komoditas"].unique())
)

data = df[
    (df["tahun"].isin(tahun)) &
    (df["komoditas"].isin(komoditas))
].copy()

if data.empty:
    st.warning("Tidak ada data untuk pilihan tersebut.")
    st.stop()


# RINGKASAN DATA
total_produksi = data["produksi_ton"].sum()
total_luas = data["luas_panen_ha"].sum()

produktivitas = (
    total_produksi / total_luas
    if total_luas > 0 else 0
)

# =========================================
# RINGKASAN DATA - PREMIUM KPI DASHBOARD
# =========================================

st.divider()

st.header("Ringkasan Data")

st.caption(
    "Indikator utama produksi cabai berdasarkan "
    "periode dan komoditas yang dipilih."
)

# MEMBUAT TIGA KOLOM STATISTIK
kpi1, kpi2, kpi3 = st.columns(
    3,
    gap="large"
)

# -----------------------------------------
# KARTU 1: TOTAL PRODUKSI
# -----------------------------------------

with kpi1:

    st.metric(
        label="🌶️ TOTAL PRODUKSI",
        value=f"{total_produksi:,.0f} Ton",
        help="Akumulasi seluruh produksi cabai berdasarkan filter."
    )

    st.caption(
        "Total hasil produksi seluruh komoditas terpilih."
    )


# -----------------------------------------
# KARTU 2: TOTAL LUAS PANEN
# -----------------------------------------

with kpi2:

    st.metric(
        label="🌾 TOTAL LUAS PANEN",
        value=f"{total_luas:,.0f} Ha",
        help="Akumulasi luas panen berdasarkan filter."
    )

    st.caption(
        "Total luas panen seluruh komoditas terpilih."
    )


# -----------------------------------------
# KARTU 3: PRODUKTIVITAS
# -----------------------------------------

with kpi3:

    st.metric(
        label="📊 PRODUKTIVITAS TERTIMBANG",
        value=f"{produktivitas:,.2f} Ton/Ha",
        help="Total produksi dibagi total luas panen."
    )

    st.caption(
        "Rasio produksi terhadap luas panen."
    )

st.divider()

# NAMA BULAN
bulan_nama = {
    1: "Januari", 2: "Februari",
    3: "Maret", 4: "April",
    5: "Mei", 6: "Juni",
    7: "Juli", 8: "Agustus",
    9: "September", 10: "Oktober",
    11: "November", 12: "Desember"
}

urutan_bulan = list(bulan_nama.values())

data["nama_bulan"] = data["bulan"].map(bulan_nama)
st.markdown(
    '<div id="grafik-bulanan"></div>',
    unsafe_allow_html=True
)
# GRAFIK PRODUKSI BULANAN
st.divider()
st.header("Grafik Produksi Cabai Bulanan")

produksi = (
    data.groupby(
        ["tahun", "bulan"],
        as_index=False
    )["produksi_ton"].sum()
)

produksi["nama_bulan"] = produksi["bulan"].map(bulan_nama)

# =========================================
# GRAFIK PRODUKSI BULANAN - PREMIUM
# =========================================

fig1 = px.line(
    produksi,
    x="nama_bulan",
    y="produksi_ton",
    color="tahun",
    markers=True,

    category_orders={
        "nama_bulan": urutan_bulan
    },

    color_discrete_sequence=[
        "#176B4D",
        "#3D9970",
        "#E0B04C",
        "#4E79A7",
        "#9B6B9E"
    ],

    labels={
        "nama_bulan": "Bulan",
        "produksi_ton": "Produksi (Ton)",
        "tahun": "Tahun"
    }
)

# PENGATURAN GARIS DAN TITIK DATA
fig1.update_traces(
    line=dict(width=3),

    marker=dict(
        size=8,
        line=dict(
            width=1.5,
            color="#FFFFFF"
        )
    ),

    hovertemplate=(
        "Produksi: %{y:,.2f} Ton"
        "<extra></extra>"
    )
)

# PENGATURAN TAMPILAN GRAFIK
fig1.update_layout(

    template="plotly_white",

    height=480,

    autosize=True,

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="#FFFFFF",

    font=dict(
        family="Arial, sans-serif",
        size=12,
        color="#365344"
    ),

    hovermode="x unified",

    margin=dict(
        l=35,
        r=25,
        t=65,
        b=45
    ),

    legend=dict(
        title="Tahun Produksi",
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),

    xaxis=dict(
        title="Bulan",
        categoryorder="array",
        categoryarray=urutan_bulan,
        showgrid=False,
        linecolor="#DCE8DF"
    ),

    yaxis=dict(
        title="Produksi (Ton)",
        rangemode="tozero",
        gridcolor="#E7EEE9",
        zeroline=False,
        tickformat=",.0f"
    )
)

# TAMPILKAN GRAFIK
st.plotly_chart(
    fig1,
    use_container_width=True,
    config={
        "displayModeBar": True,
        "displaylogo": False,
        "responsive": True
    }
)

# GRAFIK PRODUKSI TAHUNAN
st.header("Perbandingan Produksi Tahunan")

tahunan = (
    data.groupby("tahun", as_index=False)
    ["produksi_ton"].sum()
)
tahunan["tahun_label"] = (
    tahunan["tahun"].astype(int).astype(str)
)

# =========================================
# PERBANDINGAN PRODUKSI TAHUNAN - PREMIUM
# =========================================

fig2 = px.bar(
    tahunan,

    x="tahun_label",
    y="produksi_ton",

    color="tahun_label",

    text="produksi_ton",

    color_discrete_map={
        "2021": "#176B4D",
        "2022": "#3D9970",
        "2023": "#E0B04C",
        "2024": "#4E79A7",
        "2025": "#9B6B9E"
    },

    labels={
        "tahun_label": "Tahun",
        "produksi_ton": "Produksi (Ton)"
    }
)

# LABEL ANGKA DI ATAS BATANG
fig2.update_traces(

    texttemplate="%{y:,.0f}",

    textposition="outside",

    cliponaxis=False,

    marker_line_color="#FFFFFF",

    marker_line_width=1.5,

    hovertemplate=(
        "Tahun: %{x}<br>"
        "Produksi: %{y:,.2f} Ton"
        "<extra></extra>"
    )
)

# TAMPILAN GRAFIK
fig2.update_layout(

    template="plotly_white",

    height=450,

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="#FFFFFF",

    font=dict(
        family="Arial, sans-serif",
        size=12,
        color="#365344"
    ),

    showlegend=False,

    margin=dict(
        l=35,
        r=30,
        t=65,
        b=50
    ),

    bargap=0.42,

    xaxis=dict(
        title="Tahun Produksi",
        type="category",
        showgrid=False,
        linecolor="#DCE8DF"
    ),

    yaxis=dict(
        title="Produksi (Ton)",
        rangemode="tozero",
        gridcolor="#E7EEE9",
        zeroline=False,
        tickformat=",.0f"
    )
)

# TAMPILKAN GRAFIK
st.plotly_chart(
    fig2,
    use_container_width=True,
    config={
        "displayModeBar": True,
        "displaylogo": False,
        "responsive": True
    }
)

st.markdown(
    '<div id="kontribusi-komoditas"></div>',
    unsafe_allow_html=True
)
# GRAFIK KOMODITAS
st.header("Produksi Berdasarkan Komoditas")

komoditas_data = (
    data.groupby(
        ["tahun", "komoditas"],
        as_index=False
    )["produksi_ton"].sum()
)


# =========================================
# PRODUKSI BERDASARKAN KOMODITAS - PREMIUM
# =========================================

fig3 = px.bar(
    komoditas_data,

    x="tahun",
    y="produksi_ton",

    color="komoditas",

    barmode="group",

    category_orders={
        "komoditas": [
            "Cabai Besar",
            "Cabai Keriting",
            "Cabai Rawit"
        ]
    },

    color_discrete_map={
        "Cabai Besar": "#176B4D",
        "Cabai Keriting": "#E0B04C",
        "Cabai Rawit": "#4E79A7"
    },

    labels={
        "tahun": "Tahun Produksi",
        "produksi_ton": "Produksi (Ton)",
        "komoditas": "Jenis Cabai"
    }
)

# PENGATURAN BATANG DAN TOOLTIP
fig3.update_traces(

    marker_line_color="#FFFFFF",

    marker_line_width=1.2,

    hovertemplate=(
        "Tahun: %{x}<br>"
        "Produksi: %{y:,.2f} Ton"
        "<extra>%{fullData.name}</extra>"
    )
)

# PENGATURAN LAYOUT
fig3.update_layout(

    template="plotly_white",

    height=480,

    autosize=True,

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="#FFFFFF",

    font=dict(
        family="Arial, sans-serif",
        size=12,
        color="#365344"
    ),

    hovermode="closest",

    bargap=0.22,

    bargroupgap=0.08,

    margin=dict(
        l=40,
        r=30,
        t=80,
        b=50
    ),

    legend=dict(
        title="Jenis Komoditas",
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),

    xaxis=dict(
        title="Tahun Produksi",
        type="category",
        showgrid=False,
        linecolor="#DCE8DF"
    ),

    yaxis=dict(
        title="Produksi (Ton)",
        rangemode="tozero",
        gridcolor="#E7EEE9",
        zeroline=False,
        tickformat=",.0f"
    )
)

# TAMPILKAN GRAFIK
st.plotly_chart(
    fig3,
    use_container_width=True,
    config={
        "displayModeBar": True,
        "displaylogo": False,
        "responsive": True
    }
)

st.markdown(
    '<div id="produktivitas-lahan"></div>',
    unsafe_allow_html=True
)
# GRAFIK LUAS PANEN
st.header("Perkembangan Luas Panen")

luas = (
    data.groupby(
        ["tahun", "bulan"],
        as_index=False
    )["luas_panen_ha"].sum()
)

luas["nama_bulan"] = luas["bulan"].map(bulan_nama)


# =========================================
# GRAFIK LUAS PANEN - PREMIUM DESIGN
# =========================================

fig4 = px.line(
    luas,

    x="nama_bulan",
    y="luas_panen_ha",

    color="tahun",

    markers=True,

    category_orders={
        "nama_bulan": urutan_bulan
    },

    color_discrete_sequence=[
        "#176B4D",
        "#3D9970",
        "#E0B04C",
        "#4E79A7",
        "#9B6B9E"
    ],

    labels={
        "nama_bulan": "Bulan",
        "luas_panen_ha": "Luas Panen (Ha)",
        "tahun": "Tahun"
    }
)

# PENGATURAN GARIS DAN TITIK
fig4.update_traces(

    line=dict(
        width=3
    ),

    marker=dict(
        size=8,
        line=dict(
            width=1.5,
            color="#FFFFFF"
        )
    ),

    hovertemplate=(
        "Luas Panen: %{y:,.2f} Ha"
        "<extra></extra>"
    )
)

# PENGATURAN TAMPILAN
fig4.update_layout(

    template="plotly_white",

    height=460,

    autosize=True,

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="#FFFFFF",

    font=dict(
        family="Arial, sans-serif",
        size=12,
        color="#365344"
    ),

    hovermode="x unified",

    margin=dict(
        l=45,
        r=25,
        t=65,
        b=45
    ),

    legend=dict(
        title="Tahun",
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),

    xaxis=dict(
        title="Bulan",
        categoryorder="array",
        categoryarray=urutan_bulan,
        showgrid=False,
        linecolor="#DCE8DF"
    ),

    yaxis=dict(
        title="Luas Panen (Ha)",
        rangemode="tozero",
        gridcolor="#E7EEE9",
        zeroline=False,
        tickformat=",.0f"
    )
)

# TAMPILKAN GRAFIK
st.plotly_chart(
    fig4,
    use_container_width=True,
    config={
        "displayModeBar": True,
        "displaylogo": False,
        "responsive": True
    }
)

st.markdown(
    '<div id="data-bulanan"></div>',
    unsafe_allow_html=True
)
# TABEL DATA
st.divider()
st.header("Tabel Data Produksi Cabai")

kolom = [
    "tahun",
    "bulan",
    "kabupaten",
    "komoditas",
    "luas_panen_ha",
    "produksi_ton",
    "produktivitas_ton_ha"
]

# =========================================
# TABEL DATA PRODUKSI CABAI - PREMIUM
# =========================================

st.dataframe(
    data[kolom],

    use_container_width=True,

    hide_index=True,

    height=520,

    column_config={

        "tahun": st.column_config.NumberColumn(
            "Tahun",
            format="%.0f"
        ),

        "bulan": st.column_config.TextColumn(
            "Bulan"
        ),

        "kabupaten": st.column_config.TextColumn(
            "Kabupaten"
        ),

        "komoditas": st.column_config.TextColumn(
            "Jenis Komoditas"
        ),

        "luas_panen_ha": st.column_config.NumberColumn(
            "Luas Panen (Ha)",
            format="%.2f"
        ),

        "produksi_ton": st.column_config.NumberColumn(
            "Produksi (Ton)",
            format="%.2f"
        ),

        "produktivitas_ton_ha": st.column_config.NumberColumn(
            "Produktivitas (Ton/Ha)",
            format="%.2f"
        )
    }
)

# DOWNLOAD DATA
st.download_button(
    "Download Data CSV",
    data=data[kolom].to_csv(
        index=False
    ).encode("utf-8-sig"),
    file_name="data_cabai_simalungun.csv",
    mime="text/csv"
)

st.divider()
st.caption(
    "Sumber data: Badan Pusat Statistik (BPS) Kabupaten Simalungun "
    "dan data SPH-SBS. "
    "Data mencakup periode 2021–2025, terdiri atas data bulanan "
    "dan tahunan yang telah melalui proses pengolahan dan penyesuaian. "
    "Data tahunan digunakan sebagai pembanding dan rekapitulasi, "
    "sedangkan data bulanan digunakan untuk analisis perkembangan "
    "produksi, luas panen, dan produktivitas. "
    "Data yang merupakan hasil estimasi atau pengolahan dari data "
    "tahunan tidak dikategorikan sebagai observasi bulanan resmi. "
    "Database Neon PostgreSQL digunakan sebagai media penyimpanan data."
)
with st.expander("Sumber Data dan Metodologi Pengolahan"):
    st.markdown("""
    **Sumber Data**
    - Badan Pusat Statistik (BPS) Kabupaten Simalungun.
    - Publikasi Statistik Pertanian Tanaman Hortikultura Sayuran.
    - Data bulanan SPH-SBS.

    **Metodologi Pengolahan**
    1. Pengumpulan data produksi cabai periode 2021–2025.
    2. Penggabungan data bulanan dan tahunan sesuai ketersediaan sumber.
    3. Penyesuaian satuan produksi ke dalam ton.
    4. Pengelompokan komoditas Cabai Besar,
       Cabai Keriting, dan Cabai Rawit.
    5. Pengolahan data untuk analisis produksi,
       luas panen, dan produktivitas.
    6. Penyimpanan data menggunakan Neon PostgreSQL.
    7. Visualisasi dan analisis melalui Streamlit.

    **Catatan:** Data hasil estimasi dibedakan dari
    data observasi resmi.
    """)
st.markdown(
    '<div id="analisis-tren-komoditas"></div>',
    unsafe_allow_html=True
)
st.divider()
st.header("Analisis Otomatis Produksi Cabai")

if data.empty:
    st.info("Tidak ada data untuk filter yang dipilih.")

else:
    # PRODUKSI BERDASARKAN TAHUN
    produksi_tahunan = (
        data.groupby("tahun")["produksi_ton"]
        .sum()
        .sort_index()
    )

    tahun_tertinggi = produksi_tahunan.idxmax()
    tahun_terendah = produksi_tahunan.idxmin()

    nilai_tertinggi = produksi_tahunan.max()
    nilai_terendah = produksi_tahunan.min()

    # PRODUKSI BERDASARKAN KOMODITAS
    produksi_komoditas = (
        data.groupby("komoditas")["produksi_ton"]
        .sum()
        .sort_values(ascending=False)
    )

    komoditas_tertinggi = produksi_komoditas.idxmax()
    nilai_komoditas = produksi_komoditas.max()

    # TAMPILAN METRIK
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Tahun Produksi Tertinggi",
        str(int(tahun_tertinggi)),
        f"{nilai_tertinggi:,.0f} Ton"
    )

    col2.metric(
        "Tahun Produksi Terendah",
        str(int(tahun_terendah)),
        f"{nilai_terendah:,.0f} Ton"
    )

    col3.metric(
        "Komoditas Terbesar",
        str(komoditas_tertinggi),
        f"{nilai_komoditas:,.0f} Ton"
    )

    # NARASI ANALISIS
    st.subheader("Ringkasan Temuan")

    st.write(
        f"Berdasarkan filter yang dipilih, "
        f"produksi cabai tertinggi tercatat pada tahun "
        f"**{tahun_tertinggi}** sebesar "
        f"**{nilai_tertinggi:,.0f} ton**."
    )

    st.write(
        f"Produksi terendah tercatat pada tahun "
        f"**{tahun_terendah}** sebesar "
        f"**{nilai_terendah:,.0f} ton**."
    )

    st.write(
        f"Komoditas dengan kontribusi produksi terbesar "
        f"adalah **{komoditas_tertinggi}**, "
        f"dengan total produksi "
        f"**{nilai_komoditas:,.0f} ton**."
    )

    # PERUBAHAN PRODUKSI TAHUN AWAL DAN AKHIR
    if len(produksi_tahunan) >= 2:

        produksi_awal = produksi_tahunan.iloc[0]
        produksi_akhir = produksi_tahunan.iloc[-1]

        tahun_awal = produksi_tahunan.index[0]
        tahun_akhir = produksi_tahunan.index[-1]

        if produksi_awal != 0:

            perubahan = (
                (produksi_akhir - produksi_awal)
                / produksi_awal
            ) * 100

            if perubahan > 0:
                keterangan = "meningkat"
            elif perubahan < 0:
                keterangan = "menurun"
            else:
                keterangan = "tidak berubah"

            st.info(
                f"Dari tahun **{tahun_awal}** ke "
                f"**{tahun_akhir}**, produksi "
                f"{keterangan} sebesar "
                f"**{abs(perubahan):.2f}%**."
            )

st.divider()
st.header("Analisis Tren dan Insight Komoditas")

if data.empty:
    st.info("Belum tersedia data untuk dianalisis.")

else:
    tahun_tersedia = sorted(
        data["tahun"].dropna().unique().tolist()
    )

    # MEMBANDINGKAN PRODUKSI AWAL DAN AKHIR
    if len(tahun_tersedia) < 2:
        st.info(
            "Pilih minimal dua tahun untuk melihat "
            "perubahan tren produksi komoditas."
        )

    else:
        tahun_awal = tahun_tersedia[0]
        tahun_akhir = tahun_tersedia[-1]

        produksi_awal = (
            data[data["tahun"] == tahun_awal]
            .groupby("komoditas")["produksi_ton"]
            .sum(min_count=1)
            .rename("Produksi awal (ton)")
        )

        produksi_akhir = (
            data[data["tahun"] == tahun_akhir]
            .groupby("komoditas")["produksi_ton"]
            .sum(min_count=1)
            .rename("Produksi akhir (ton)")
        )

        tren = (
            produksi_awal.to_frame()
            .join(produksi_akhir, how="inner")
            .reset_index()
        )

        if tren.empty:
            st.info(
                "Belum ada data pembanding yang lengkap "
                "untuk komoditas yang dipilih."
            )

        else:
            tren["Perubahan (%)"] = tren.apply(
                lambda row: (
                    (
                        row["Produksi akhir (ton)"]
                        - row["Produksi awal (ton)"]
                    ) / row["Produksi awal (ton)"] * 100
                )
                if row["Produksi awal (ton)"] != 0
                else float("nan"),
                axis=1
            )

            tren = tren.dropna(
                subset=["Perubahan (%)"]
            ).copy()

            if not tren.empty:

                tren["Status tren"] = tren[
                    "Perubahan (%)"
                ].apply(
                    lambda x: (
                        "Meningkat" if x > 0
                        else "Menurun" if x < 0
                        else "Stabil"
                    )
                )

                tren["Label"] = tren[
                    "Perubahan (%)"
                ].map(lambda x: f"{x:+.2f}%")

                st.subheader(
                    f"Perubahan Produksi {tahun_awal}–{tahun_akhir}"
                )

                fig_tren = px.bar(
                    tren.sort_values("Perubahan (%)"),
                    x="Perubahan (%)",
                    y="komoditas",
                    color="Status tren",
                    text="Label",
                    orientation="h",
                    labels={
                        "komoditas": "Jenis Cabai",
                        "Perubahan (%)": "Perubahan Produksi (%)",
                        "Status tren": "Status Tren",
                    },
                )

                fig_tren.update_layout(
                    height=380,
                    margin=dict(
                        l=10, r=10, t=30, b=10
                    ),
                    legend_title_text="Status Tren",
                )

                fig_tren.update_xaxes(
                    ticksuffix="%"
                )

                st.plotly_chart(
                    fig_tren,
                    use_container_width=True
                )

                st.dataframe(
                    tren[
                        [
                            "komoditas",
                            "Produksi awal (ton)",
                            "Produksi akhir (ton)",
                            "Perubahan (%)",
                            "Status tren",
                        ]
                    ].rename(
                        columns={
                            "komoditas": "Komoditas",
                        }
                    ),
                    use_container_width=True,
                    hide_index=True,
                )

                # INSIGHT PRODUKSI
                tertinggi = tren.loc[
                    tren["Perubahan (%)"].idxmax()
                ]

                terendah = tren.loc[
                    tren["Perubahan (%)"].idxmin()
                ]

                st.subheader("Insight Perubahan Produksi")

                c1, c2 = st.columns(2)

                c1.metric(
                    "Perubahan Produksi Tertinggi",
                    tertinggi["komoditas"],
                    f'{tertinggi["Perubahan (%)"]:+.2f}%'
                )

                c2.metric(
                    "Perubahan Produksi Terendah",
                    terendah["komoditas"],
                    f'{terendah["Perubahan (%)"]:+.2f}%'
                )

    st.divider()

    st.subheader(
        "Perbandingan Produktivitas Komoditas"
    )

    produktivitas_komoditas = (
        data.groupby("komoditas", as_index=False)
        .agg(
            rata_rata_produktivitas=(
                "produktivitas_ton_ha", "mean"
            )
        )
        .dropna(
            subset=["rata_rata_produktivitas"]
        )
        .sort_values(
            "rata_rata_produktivitas",
            ascending=True
        )
    )

    if not produktivitas_komoditas.empty:

        produktivitas_komoditas["Label"] = (
            produktivitas_komoditas[
                "rata_rata_produktivitas"
            ].map(lambda x: f"{x:.2f} ton/ha")
        )

        fig_produktivitas = px.bar(
            produktivitas_komoditas,
            x="rata_rata_produktivitas",
            y="komoditas",
            orientation="h",
            text="Label",
            labels={
                "komoditas": "Jenis Cabai",
                "rata_rata_produktivitas":
                    "Produktivitas (Ton/Ha)",
            },
        )

        fig_produktivitas.update_layout(
            height=350,
            margin=dict(
                l=10, r=10, t=30, b=10
            ),
        )

        st.plotly_chart(
            fig_produktivitas,
            use_container_width=True
        )

        terbaik = produktivitas_komoditas.loc[
            produktivitas_komoditas[
                "rata_rata_produktivitas"
            ].idxmax()
        ]

        st.info(
            f"Komoditas dengan rata-rata produktivitas "
            f"tertinggi adalah **{terbaik['komoditas']}**, "
            f"dengan produktivitas sebesar "
            f"**{terbaik['rata_rata_produktivitas']:.2f} ton/ha**."
        )

    else:
        st.info(
            "Data produktivitas belum tersedia."
        )

    st.caption(
        "Analisis mengikuti filter tahun, bulan, dan komoditas "
        "yang dipilih. Insight ini menggambarkan tren produksi "
        "dan produktivitas, bukan keuntungan ekonomi atau "
        "rekomendasi tanam."
    )

# =====================================================
# ANALISIS KONTRIBUSI PRODUKSI KOMODITAS
# =====================================================

st.divider()

st.header("Analisis Kontribusi Produksi Komoditas")

if data.empty:
    st.info("Data produksi belum tersedia.")

else:
    kontribusi = (
        data.groupby("komoditas", as_index=False)
        .agg(
            total_produksi=(
                "produksi_ton",
                lambda x: x.sum(min_count=1)
            )
        )
        .dropna(subset=["total_produksi"])
    )

    total_produksi_semua = (
        kontribusi["total_produksi"].sum()
    )

    if kontribusi.empty or total_produksi_semua <= 0:

        st.warning(
            "Belum tersedia data produksi yang valid "
            "untuk menghitung kontribusi."
        )

    else:

        kontribusi["persentase"] = (
            kontribusi["total_produksi"]
            / total_produksi_semua
        ) * 100

        kontribusi = kontribusi.sort_values(
            "total_produksi",
            ascending=False
        )

        # GRAFIK KONTRIBUSI
        st.subheader("Persentase Kontribusi Produksi")

        fig_kontribusi = px.pie(
            kontribusi,
            names="komoditas",
            values="total_produksi",
            hole=0.55,
            title="Distribusi Produksi Berdasarkan Komoditas"
        )

        fig_kontribusi.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate=(
                "%{label}<br>"
                "Produksi: %{value:,.2f} ton<br>"
                "Kontribusi: %{percent}"
                "<extra></extra>"
            )
        )

        fig_kontribusi.update_layout(
            height=430,
            margin=dict(
                l=10, r=10, t=60, b=10
            ),
            legend_title_text="Komoditas"
        )

        st.plotly_chart(
            fig_kontribusi,
            use_container_width=True
        )

        # METRIK UTAMA
        tertinggi_kontribusi = kontribusi.iloc[0]

        col1, col2 = st.columns(2)

        col1.metric(
            "Total Produksi Seluruh Komoditas",
            f"{total_produksi_semua:,.2f} Ton"
        )

        col2.metric(
            "Kontributor Produksi Terbesar",
            tertinggi_kontribusi["komoditas"],
            f'{tertinggi_kontribusi["persentase"]:.2f}%'
        )

        # TABEL KONTRIBUSI
        st.subheader("Rincian Kontribusi Komoditas")

        tabel_kontribusi = kontribusi[
            [
                "komoditas",
                "total_produksi",
                "persentase"
            ]
        ].rename(
            columns={
                "komoditas": "Komoditas",
                "total_produksi": "Total Produksi (Ton)",
                "persentase": "Kontribusi (%)"
            }
        )

        st.dataframe(
            tabel_kontribusi,
            use_container_width=True,
            hide_index=True
        )

        # NARASI OTOMATIS
        st.subheader("Ringkasan Kontribusi")

        st.write(
            f"Berdasarkan filter yang dipilih, "
            f"komoditas **{tertinggi_kontribusi['komoditas']}** "
            f"merupakan penyumbang produksi terbesar "
            f"dengan total produksi sebesar "
            f"**{tertinggi_kontribusi['total_produksi']:,.2f} ton**, "
            f"atau setara dengan "
            f"**{tertinggi_kontribusi['persentase']:.2f}%** "
            f"dari total produksi seluruh komoditas."
        )

        st.caption(
            "Kontribusi dihitung berdasarkan total produksi "
            "dalam periode dan komoditas yang dipilih."
        )

# =====================================================
# ANALISIS PRODUKTIVITAS DAN LUAS PANEN
# =====================================================

st.divider()

st.header("Analisis Produktivitas dan Efisiensi Luas Panen")

if data.empty:
    st.info("Belum tersedia data untuk dianalisis.")

else:
    analisis_lahan = data.copy()

    # MENYESUAIKAN NAMA KOLOM LUAS PANEN
    if "luas_panen_ha" in analisis_lahan.columns:
        kolom_luas = "luas_panen_ha"
    elif "luas_lahan_ha" in analisis_lahan.columns:
        kolom_luas = "luas_lahan_ha"
    else:
        st.error("Kolom luas panen tidak ditemukan.")
        st.stop()

    # KONVERSI NUMERIK
    analisis_lahan["luas_analisis"] = pd.to_numeric(
        analisis_lahan[kolom_luas],
        errors="coerce"
    )

    analisis_lahan["produksi_analisis"] = pd.to_numeric(
        analisis_lahan["produksi_ton"],
        errors="coerce"
    )

    analisis_lahan = analisis_lahan.dropna(
        subset=["luas_analisis", "produksi_analisis"]
    )

    analisis_lahan = analisis_lahan[
        (analisis_lahan["luas_analisis"] > 0) &
        (analisis_lahan["produksi_analisis"] >= 0)
    ]

    if analisis_lahan.empty:
        st.warning(
            "Tidak tersedia data luas panen dan produksi "
            "yang valid untuk menghitung produktivitas."
        )

    else:

        # =============================================
        # RINGKASAN PRODUKTIVITAS
        # =============================================

        total_luas_analisis = (
            analisis_lahan["luas_analisis"].sum()
        )

        total_produksi_analisis = (
            analisis_lahan["produksi_analisis"].sum()
        )

        produktivitas_tertimbang = (
            total_produksi_analisis /
            total_luas_analisis
        )

        st.subheader("Ringkasan Produktivitas")

        p1, p2, p3 = st.columns(3)

        p1.metric(
            "Total Luas Panen",
            f"{total_luas_analisis:,.2f} Ha"
        )

        p2.metric(
            "Total Produksi",
            f"{total_produksi_analisis:,.2f} Ton"
        )

        p3.metric(
            "Produktivitas Tertimbang",
            f"{produktivitas_tertimbang:,.2f} Ton/Ha"
        )

        # =============================================
        # PRODUKTIVITAS BERDASARKAN KOMODITAS
        # =============================================

        st.subheader(
            "Produktivitas Berdasarkan Komoditas"
        )

        produktivitas_lahan = (
            analisis_lahan.groupby(
                "komoditas",
                as_index=False
            )
            .agg(
                total_luas=(
                    "luas_analisis", "sum"
                ),
                total_produksi=(
                    "produksi_analisis", "sum"
                )
            )
        )

        produktivitas_lahan = produktivitas_lahan[
            produktivitas_lahan["total_luas"] > 0
        ].copy()

        produktivitas_lahan[
            "produktivitas_tertimbang"
        ] = (
            produktivitas_lahan["total_produksi"] /
            produktivitas_lahan["total_luas"]
        )

        produktivitas_lahan = (
            produktivitas_lahan.sort_values(
                "produktivitas_tertimbang",
                ascending=False
            )
        )

        fig_lahan = px.bar(
            produktivitas_lahan,
            x="komoditas",
            y="produktivitas_tertimbang",
            color="komoditas",
            text="produktivitas_tertimbang",
            labels={
                "komoditas": "Jenis Cabai",
                "produktivitas_tertimbang": "Ton/Ha"
            },
            title="Produktivitas Tertimbang Setiap Komoditas"
        )

        fig_lahan.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside"
        )

        fig_lahan.update_layout(
            height=400,
            margin=dict(
                l=10, r=10, t=60, b=10
            ),
            showlegend=False
        )

        st.plotly_chart(
            fig_lahan,
            use_container_width=True
        )

        # =============================================
        # PERINGKAT PRODUKTIVITAS
        # =============================================

        st.subheader("Peringkat Produktivitas")

        tabel_produktivitas = (
            produktivitas_lahan[
                [
                    "komoditas",
                    "total_luas",
                    "total_produksi",
                    "produktivitas_tertimbang"
                ]
            ]
            .rename(
                columns={
                    "komoditas": "Komoditas",
                    "total_luas": "Total Luas Panen (Ha)",
                    "total_produksi": "Total Produksi (Ton)",
                    "produktivitas_tertimbang":
                        "Produktivitas (Ton/Ha)"
                }
            )
            .reset_index(drop=True)
        )

        tabel_produktivitas.index += 1

        st.dataframe(
            tabel_produktivitas,
            use_container_width=True
        )

        # =============================================
        # PRODUKTIVITAS TAHUNAN
        # =============================================

        st.subheader(
            "Perkembangan Produktivitas Tahunan"
        )

        tahunan_lahan = (
            analisis_lahan.groupby(
                ["tahun", "komoditas"],
                as_index=False
            )
            .agg(
                total_luas=(
                    "luas_analisis", "sum"
                ),
                total_produksi=(
                    "produksi_analisis", "sum"
                )
            )
        )

        tahunan_lahan = tahunan_lahan[
            tahunan_lahan["total_luas"] > 0
        ].copy()

        tahunan_lahan[
            "produktivitas_tertimbang"
        ] = (
            tahunan_lahan["total_produksi"] /
            tahunan_lahan["total_luas"]
        )

        fig_tahunan_lahan = px.line(
            tahunan_lahan,
            x="tahun",
            y="produktivitas_tertimbang",
            color="komoditas",
            markers=True,
            labels={
                "tahun": "Tahun",
                "produktivitas_tertimbang": "Ton/Ha",
                "komoditas": "Jenis Cabai"
            },
            title="Tren Produktivitas Cabai Tahun ke Tahun"
        )

        fig_tahunan_lahan.update_layout(
            height=400,
            hovermode="x unified",
            margin=dict(
                l=10, r=10, t=60, b=10
            )
        )

        st.plotly_chart(
            fig_tahunan_lahan,
            use_container_width=True
        )

        # =============================================
        # INSIGHT OTOMATIS
        # =============================================

        st.subheader(
            "Insight Produktivitas Lahan"
        )

        komoditas_terbaik = produktivitas_lahan.iloc[0]

        komoditas_terendah = produktivitas_lahan.iloc[-1]

        i1, i2 = st.columns(2)

        i1.metric(
            "Produktivitas Tertinggi",
            komoditas_terbaik["komoditas"],
            f'{komoditas_terbaik["produktivitas_tertimbang"]:.2f} Ton/Ha'
        )

        i2.metric(
            "Produktivitas Terendah",
            komoditas_terendah["komoditas"],
            f'{komoditas_terendah["produktivitas_tertimbang"]:.2f} Ton/Ha'
        )

        st.write(
            f"Berdasarkan data dan filter yang dipilih, "
            f"**{komoditas_terbaik['komoditas']}** memiliki "
            f"produktivitas tertimbang tertinggi sebesar "
            f"**{komoditas_terbaik['produktivitas_tertimbang']:.2f} ton/ha**."
        )

        st.write(
            f"Sementara itu, **{komoditas_terendah['komoditas']}** "
            f"memiliki produktivitas tertimbang terendah sebesar "
            f"**{komoditas_terendah['produktivitas_tertimbang']:.2f} ton/ha**."
        )

        st.caption(
            "Produktivitas tertimbang dihitung dari total produksi "
            "dibagi total luas panen. Nilai ini menunjukkan hasil "
            "produksi per hektare, bukan efisiensi biaya atau keuntungan."
        )

# =====================================================
# TAHAP 5 - EXPORT LAPORAN PDF DAN EXCEL
# =====================================================

st.divider()

st.header("Export Laporan Profesional PDF dan Excel")

# Menggunakan data yang sudah mengikuti filter dashboard
if "filtered" in globals():
    export_df = filtered.copy()
elif "data" in globals():
    export_df = data.copy()
else:
    st.error("Data dashboard tidak ditemukan.")
    st.stop()

# Memastikan kolom utama tersedia
required_columns = [
    "tahun",
    "komoditas",
    "produksi_ton"
]

missing_columns = [
    col for col in required_columns
    if col not in export_df.columns
]

if missing_columns:
    st.error(
        f"Kolom berikut tidak ditemukan: {missing_columns}"
    )
    st.stop()

if export_df.empty:
    st.warning("Tidak ada data untuk diekspor.")
    st.stop()

# Mencari kolom luas lahan
area_col = next(
    (
        col for col in [
            "luas_panen_ha",
            "luas_lahan_ha"
        ]
        if col in export_df.columns
    ),
    None
)

# Konversi numerik
export_df["produksi_ton"] = pd.to_numeric(
    export_df["produksi_ton"],
    errors="coerce"
)

if area_col:
    export_df[area_col] = pd.to_numeric(
        export_df[area_col],
        errors="coerce"
    )

# =====================================================
# RINGKASAN TAHUNAN
# =====================================================

ringkasan_tahunan = (
    export_df.groupby("tahun", as_index=False)
    .agg(
        total_produksi_ton=(
            "produksi_ton",
            lambda x: x.sum(min_count=1)
        )
    )
)

if area_col:
    luas_tahunan = (
        export_df.groupby("tahun", as_index=False)
        .agg(
            total_luas_ha=(
                area_col,
                lambda x: x.sum(min_count=1)
            )
        )
    )

    ringkasan_tahunan = ringkasan_tahunan.merge(
        luas_tahunan,
        on="tahun",
        how="left"
    )

    ringkasan_tahunan["produktivitas_ton_ha"] = (
        ringkasan_tahunan["total_produksi_ton"] /
        ringkasan_tahunan["total_luas_ha"].where(
            ringkasan_tahunan["total_luas_ha"] > 0
        )
    )

# =====================================================
# RINGKASAN KOMODITAS
# =====================================================

ringkasan_komoditas = (
    export_df.groupby("komoditas", as_index=False)
    .agg(
        total_produksi_ton=(
            "produksi_ton",
            lambda x: x.sum(min_count=1)
        )
    )
    .sort_values(
        "total_produksi_ton",
        ascending=False
    )
)

if area_col:
    luas_komoditas = (
        export_df.groupby("komoditas", as_index=False)
        .agg(
            total_luas_ha=(
                area_col,
                lambda x: x.sum(min_count=1)
            )
        )
    )

    ringkasan_komoditas = ringkasan_komoditas.merge(
        luas_komoditas,
        on="komoditas",
        how="left"
    )

    ringkasan_komoditas["produktivitas_ton_ha"] = (
        ringkasan_komoditas["total_produksi_ton"] /
        ringkasan_komoditas["total_luas_ha"].where(
            ringkasan_komoditas["total_luas_ha"] > 0
        )
    )

# =====================================================
# EXPORT EXCEL
# =====================================================

excel_buffer = io.BytesIO()

excel_data = export_df.copy()

# Menghilangkan informasi timezone agar Excel kompatibel
for col in excel_data.columns:
    try:
        if excel_data[col].dt.tz is not None:
            excel_data[col] = (
                excel_data[col].dt.tz_localize(None)
            )
    except (AttributeError, TypeError):
        pass

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    excel_data.to_excel(
        writer,
        sheet_name="Data Produksi",
        index=False
    )

    ringkasan_tahunan.to_excel(
        writer,
        sheet_name="Ringkasan Tahunan",
        index=False
    )

    ringkasan_komoditas.to_excel(
        writer,
        sheet_name="Ringkasan Komoditas",
        index=False
    )

    # Format setiap worksheet
    for sheet in writer.sheets.values():

        sheet.freeze_panes = "A2"
        sheet.auto_filter.ref = sheet.dimensions

        for column_cells in sheet.columns:

            max_length = max(
                len(str(cell.value or ""))
                for cell in column_cells
            )

            letter = column_cells[0].column_letter

            sheet.column_dimensions[letter].width = min(
                max_length + 3,
                35
            )

excel_buffer.seek(0)

# =====================================================
# EXPORT PDF
# =====================================================

pdf_buffer = io.BytesIO()

doc = SimpleDocTemplate(
    pdf_buffer,
    pagesize=landscape(A4),
    rightMargin=1.5 * cm,
    leftMargin=1.5 * cm,
    topMargin=1.5 * cm,
    bottomMargin=1.5 * cm
)

styles = getSampleStyleSheet()
story = []

# Judul laporan
story.append(
    Paragraph(
        "LAPORAN PRODUKSI CABAI",
        styles["Title"]
    )
)

story.append(
    Paragraph(
        "Kabupaten Simalungun",
        styles["Heading2"]
    )
)

story.append(Spacer(1, 10))

story.append(
    Paragraph(
        "Tanggal laporan: " +
        datetime.now().strftime("%d-%m-%Y %H:%M"),
        styles["Normal"]
    )
)

tahun_dipilih = sorted(
    export_df["tahun"].dropna().unique().tolist()
)

komoditas_dipilih = sorted(
    export_df["komoditas"].dropna().unique().tolist()
)

story.append(
    Paragraph(
        "Tahun: " + html.escape(
            ", ".join(map(str, tahun_dipilih))
        ),
        styles["Normal"]
    )
)

story.append(
    Paragraph(
        "Komoditas: " + html.escape(
            ", ".join(map(str, komoditas_dipilih))
        ),
        styles["Normal"]
    )
)

story.append(Spacer(1, 18))

# Ringkasan utama
total_produksi = export_df[
    "produksi_ton"
].sum(min_count=1)

total_luas = (
    export_df[area_col].sum(min_count=1)
    if area_col else None
)

story.append(
    Paragraph(
        "RINGKASAN DATA PRODUKSI",
        styles["Heading2"]
    )
)

summary_data = [
    ["Indikator", "Nilai"],
    [
        "Total produksi",
        f"{total_produksi:,.2f} ton"
    ],
    [
        "Total luas lahan",
        f"{total_luas:,.2f} ha"
        if pd.notna(total_luas) else "Tidak tersedia"
    ],
    [
        "Jumlah tahun",
        str(len(tahun_dipilih))
    ],
    [
        "Jumlah komoditas",
        str(len(komoditas_dipilih))
    ]
]

summary_table = Table(
    summary_data,
    colWidths=[6 * cm, 9 * cm]
)

summary_table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#174A7E")),
        ("TEXTCOLOR", (0, 0), (-1, 0),
         colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5,
         colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("FONTNAME", (0, 0), (-1, 0),
         "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1),
         "MIDDLE")
    ])
)

story.append(summary_table)
story.append(Spacer(1, 20))

# Fungsi tabel PDF
def buat_tabel_pdf(frame):

    rows = [list(frame.columns)]

    for row in frame.itertuples(index=False, name=None):

        values = []

        for value in row:

            if pd.isna(value):
                values.append("-")

            elif isinstance(value, (int, float)):
                values.append(f"{value:,.2f}")

            else:
                values.append(str(value))

        rows.append(values)

    usable_width = landscape(A4)[0] - 3 * cm

    widths = [
        usable_width / len(frame.columns)
    ] * len(frame.columns)

    table = Table(
        rows,
        colWidths=widths,
        repeatRows=1
    )

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0),
             colors.HexColor("#174A7E")),
            ("TEXTCOLOR", (0, 0), (-1, 0),
             colors.white),
            ("GRID", (0, 0), (-1, -1),
             0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 7),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1),
             "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, 0),
             "Helvetica-Bold")
        ])
    )

    return table

# Tabel produksi tahunan
story.append(
    Paragraph(
        "RINGKASAN PRODUKSI TAHUNAN",
        styles["Heading2"]
    )
)

story.append(
    buat_tabel_pdf(ringkasan_tahunan)
)

story.append(Spacer(1, 20))

# Tabel produksi komoditas
story.append(
    Paragraph(
        "PRODUKSI BERDASARKAN KOMODITAS",
        styles["Heading2"]
    )
)

story.append(
    buat_tabel_pdf(ringkasan_komoditas)
)

story.append(Spacer(1, 20))

story.append(
    Paragraph(
        "Sumber: Database Neon Pusat. "
        "Laporan dibuat berdasarkan filter dashboard "
        "yang dipilih pengguna.",
        styles["Italic"]
    )
)

doc.build(story)

pdf_buffer.seek(0)

# =====================================================
# TOMBOL DOWNLOAD
# =====================================================

st.subheader("Download Laporan")

col_pdf, col_excel = st.columns(2)

with col_pdf:

    st.download_button(
        label="Download Laporan PDF",
        data=pdf_buffer.getvalue(),
        file_name="laporan_produksi_cabai.pdf",
        mime="application/pdf",
        use_container_width=True,
        key="download_laporan_pdf"
    )

with col_excel:

    st.download_button(
        label="Download Data Excel",
        data=excel_buffer.getvalue(),
        file_name="laporan_produksi_cabai.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        use_container_width=True,
        key="download_laporan_excel"
    )
# REFRESH DATA NEON
if st.sidebar.button("🔄 Muat Ulang Data", use_container_width=True):
    st.cache_data.clear()
    st.rerun()
