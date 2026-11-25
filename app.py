
import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Cabai Simalungun",
    page_icon="🌶️",
    layout="wide"
)

st.title("🌶️ DASHBOARD PRODUKSI CABAI")
st.subheader("Kabupaten Simalungun Tahun 2021–2025")

st.write(
    "Dashboard informasi produksi, luas panen, "
    "dan produktivitas cabai."
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
            FROM produksi_cabai_pusat
            ORDER BY tahun, bulan
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


# FILTER DATA
st.sidebar.header("Filter Data")

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

st.divider()
st.header("Ringkasan Data")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Produksi",
    f"{total_produksi:,.0f} Ton"
)

c2.metric(
    "Total Luas Panen",
    f"{total_luas:,.0f} Ha"
)

c3.metric(
    "Produktivitas Tertimbang",
    f"{produktivitas:,.0f} Ton/Ha"
)

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

fig1 = px.line(
    produksi,
    x="nama_bulan",
    y="produksi_ton",
    color="tahun",
    markers=True,
    category_orders={
        "nama_bulan": urutan_bulan
    },
    labels={
        "nama_bulan": "Bulan",
        "produksi_ton": "Produksi (Ton)",
        "tahun": "Tahun"
    }
)

st.plotly_chart(fig1, use_container_width=True)


# GRAFIK PRODUKSI TAHUNAN
st.header("Perbandingan Produksi Tahunan")

tahunan = (
    data.groupby("tahun", as_index=False)
    ["produksi_ton"].sum()
)

fig2 = px.bar(
    tahunan,
    x="tahun",
    y="produksi_ton",
    text="produksi_ton",
    labels={
        "tahun": "Tahun",
        "produksi_ton": "Produksi (Ton)"
    }
)

st.plotly_chart(fig2, use_container_width=True)


# GRAFIK KOMODITAS
st.header("Produksi Berdasarkan Komoditas")

komoditas_data = (
    data.groupby(
        ["tahun", "komoditas"],
        as_index=False
    )["produksi_ton"].sum()
)

fig3 = px.bar(
    komoditas_data,
    x="tahun",
    y="produksi_ton",
    color="komoditas",
    barmode="group",
    labels={
        "tahun": "Tahun",
        "produksi_ton": "Produksi (Ton)",
        "komoditas": "Jenis Cabai"
    }
)

st.plotly_chart(fig3, use_container_width=True)


# GRAFIK LUAS PANEN
st.header("Perkembangan Luas Panen")

luas = (
    data.groupby(
        ["tahun", "bulan"],
        as_index=False
    )["luas_panen_ha"].sum()
)

luas["nama_bulan"] = luas["bulan"].map(bulan_nama)

fig4 = px.line(
    luas,
    x="nama_bulan",
    y="luas_panen_ha",
    color="tahun",
    markers=True,
    category_orders={
        "nama_bulan": urutan_bulan
    },
    labels={
        "nama_bulan": "Bulan",
        "luas_panen_ha": "Luas Panen (Ha)",
        "tahun": "Tahun"
    }
)

st.plotly_chart(fig4, use_container_width=True)


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

st.dataframe(
    data[kolom],
    use_container_width=True,
    hide_index=True
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
    "Sumber: Database Neon Pusat. "
    "Data bulanan merupakan estimasi sebaran "
    "berdasarkan dataset latihan, bukan observasi "
    "bulanan resmi."
)
