
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
# VALIDASI KELENGKAPAN DAN KUALITAS DATA
# =====================================================

st.divider()
st.header("Validasi Kelengkapan dan Kualitas Data")

quality_df = data.copy()

if quality_df.empty:

    st.info("Tidak ada data untuk diperiksa.")

else:

    # MENENTUKAN KOLOM LUAS PANEN
    if "luas_panen_ha" in quality_df.columns:
        area_col = "luas_panen_ha"
    elif "luas_lahan_ha" in quality_df.columns:
        area_col = "luas_lahan_ha"
    else:
        area_col = None

    required_cols = [
        "tahun", "bulan", "komoditas", "produksi_ton"
    ]

    missing_columns = [
        col for col in required_cols
        if col not in quality_df.columns
    ]

    if missing_columns:

        st.error(
            f"Kolom wajib tidak ditemukan: {missing_columns}"
        )

    else:

        total_records = len(quality_df)

        # =============================================
        # PEMERIKSAAN DATA KOSONG
        # =============================================

        missing_summary = (
            quality_df.isna().sum()
            .reset_index()
        )

        missing_summary.columns = [
            "Nama Kolom", "Jumlah Data Kosong"
        ]

        missing_summary = missing_summary[
            missing_summary["Jumlah Data Kosong"] > 0
        ]

        missing_rows = int(
            quality_df.isna().any(axis=1).sum()
        )

        # =============================================
        # PEMERIKSAAN DATA DUPLIKAT
        # =============================================

        key_cols = [
            col for col in [
                "tahun", "bulan", "kabupaten", "komoditas"
            ]
            if col in quality_df.columns
        ]

        duplicate_mask = quality_df.duplicated(
            subset=key_cols,
            keep=False
        )

        duplicate_count = int(duplicate_mask.sum())

        # =============================================
        # PEMERIKSAAN BULAN
        # =============================================

        bulan_num = pd.to_numeric(
            quality_df["bulan"],
            errors="coerce"
        )

        invalid_month_mask = (
            bulan_num.notna() &
            ~bulan_num.between(1, 12)
        )

        # =============================================
        # PEMERIKSAAN LUAS PANEN
        # =============================================

        if area_col:

            area_num = pd.to_numeric(
                quality_df[area_col],
                errors="coerce"
            )

            invalid_area_mask = (
                area_num.notna() &
                (area_num <= 0)
            )

        else:

            area_num = None

            invalid_area_mask = pd.Series(
                False, index=quality_df.index
            )

        # =============================================
        # PEMERIKSAAN PRODUKSI
        # =============================================

        produksi_num = pd.to_numeric(
            quality_df["produksi_ton"],
            errors="coerce"
        )

        negative_production_mask = (
            produksi_num.notna() &
            (produksi_num < 0)
        )

        # =============================================
        # PEMERIKSAAN PRODUKTIVITAS
        # =============================================

        mismatch_mask = pd.Series(
            False, index=quality_df.index
        )

        if (
            area_col
            and "produktivitas_ton_ha" in quality_df.columns
        ):

            produktivitas_num = pd.to_numeric(
                quality_df["produktivitas_ton_ha"],
                errors="coerce"
            )

            expected_productivity = (
                produksi_num /
                area_num.where(area_num > 0)
            )

            mismatch_mask = (
                expected_productivity.notna() &
                produktivitas_num.notna() &
                (
                    (
                        expected_productivity -
                        produktivitas_num
                    ).abs() > 0.51
                )
            )

        # =============================================
        # RINGKASAN HASIL VALIDASI
        # =============================================

        st.subheader("Ringkasan Pemeriksaan")

        q1, q2, q3, q4 = st.columns(4)

        q1.metric(
            "Total Data",
            f"{total_records:,}"
        )

        q2.metric(
            "Baris dengan Data Kosong",
            f"{missing_rows:,}"
        )

        q3.metric(
            "Baris Duplikat",
            f"{duplicate_count:,}"
        )

        q4.metric(
            "Produktivitas Tidak Konsisten",
            f"{int(mismatch_mask.sum()):,}"
        )

        # =============================================
        # TABEL STATUS VALIDASI
        # =============================================

        pemeriksaan = [
            ("Data kosong", missing_rows),
            ("Data duplikat", duplicate_count),
            ("Bulan tidak valid",
             int(invalid_month_mask.sum())),
            ("Luas panen nol/negatif",
             int(invalid_area_mask.sum())),
            ("Produksi negatif",
             int(negative_production_mask.sum())),
            ("Produktivitas tidak konsisten",
             int(mismatch_mask.sum())),
        ]

        hasil_validasi = pd.DataFrame(
            pemeriksaan,
            columns=["Jenis Pemeriksaan", "Jumlah Temuan"]
        )

        hasil_validasi["Status"] = hasil_validasi[
            "Jumlah Temuan"
        ].apply(
            lambda x: "Perlu Diperiksa" if x > 0 else "Lolos"
        )

        st.subheader("Detail Hasil Validasi")

        st.dataframe(
            hasil_validasi,
            use_container_width=True,
            hide_index=True
        )

        # =============================================
        # DETAIL DATA KOSONG
        # =============================================

        with st.expander("Lihat Detail Data Kosong"):

            if missing_summary.empty:

                st.success("Tidak ditemukan data kosong.")

            else:

                st.dataframe(
                    missing_summary,
                    use_container_width=True,
                    hide_index=True
                )

        # =============================================
        # MENGUMPULKAN BARIS YANG BERMASALAH
        # =============================================

        issue_frames = []

        def tambah_temuan(mask, label):

            if mask.any():

                temp = quality_df.loc[mask].copy()

                temp["temuan_validasi"] = label

                issue_frames.append(temp)

        tambah_temuan(
            quality_df.isna().any(axis=1),
            "Terdapat data kosong"
        )

        tambah_temuan(
            duplicate_mask,
            "Data duplikat"
        )

        tambah_temuan(
            invalid_month_mask,
            "Bulan tidak valid"
        )

        tambah_temuan(
            invalid_area_mask,
            "Luas panen nol atau negatif"
        )

        tambah_temuan(
            negative_production_mask,
            "Produksi negatif"
        )

        tambah_temuan(
            mismatch_mask,
            "Produktivitas tidak konsisten"
        )

        # =============================================
        # TAMPILKAN DETAIL TEMUAN
        # =============================================

        st.subheader("Detail Baris yang Perlu Diperiksa")

        if issue_frames:

            issues_df = pd.concat(
                issue_frames,
                ignore_index=True
            )

            st.warning(
                f"Ditemukan {len(issues_df)} catatan "
                "temuan pemeriksaan. Satu baris dapat "
                "memiliki lebih dari satu jenis temuan."
            )

            st.dataframe(
                issues_df,
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "Unduh Hasil Validasi CSV",
                data=issues_df.to_csv(
                    index=False
                ).encode("utf-8-sig"),
                file_name="hasil_validasi_data_cabai.csv",
                mime="text/csv"
            )

        else:

            st.success(
                "Tidak ditemukan masalah berdasarkan "
                "aturan validasi yang digunakan."
            )

        st.caption(
            "Validasi ini hanya mendeteksi potensi masalah. "
            "Tidak ada data asli yang diubah atau dihapus. "
            "Perbedaan produktivitas menggunakan toleransi "
            "0,51 ton/ha untuk mengakomodasi pembulatan."
        )
