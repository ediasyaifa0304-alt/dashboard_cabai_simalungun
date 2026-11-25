# 🌶️ Dashboard Produksi Cabai Kabupaten Simalungun

## 1. Deskripsi Proyek

Dashboard Produksi Cabai Kabupaten Simalungun merupakan aplikasi berbasis web yang digunakan untuk mengelola, memvisualisasikan, dan menganalisis data produksi cabai periode 2021–2025.

Aplikasi ini dikembangkan menggunakan pendekatan Data Warehouse dengan metode Star Schema dan divisualisasikan menggunakan Streamlit.

## 2. Tujuan Proyek

1. Mengintegrasikan data produksi cabai periode 2021–2025.
2. Menerapkan konsep Data Warehouse menggunakan Star Schema.
3. Menampilkan informasi produksi cabai secara interaktif.
4. Menganalisis perkembangan produksi berdasarkan tahun dan komoditas.
5. Menyajikan informasi luas panen dan produktivitas.

## 3. Teknologi yang Digunakan

| Teknologi | Kegunaan |
|---|---|
| Python | Bahasa pemrograman |
| Pandas | Pengolahan data |
| PostgreSQL | Database |
| Neon | Database cloud |
| Streamlit | Pengembangan dashboard |
| Plotly | Visualisasi data |
| Psycopg2 | Koneksi Python dengan PostgreSQL |
| GitHub | Penyimpanan kode dan pengelolaan proyek |

## 4. Arsitektur Sistem

Alur pengolahan data proyek:

1. Data produksi cabai tahun 2021–2025.
2. Proses ETL (Extract, Transform, Load).
3. Penyimpanan data pada Neon PostgreSQL.
4. Pengelolaan Data Warehouse dengan pendekatan Star Schema.
5. Pengambilan data menggunakan Python.
6. Visualisasi dan analisis melalui Streamlit.

## 5. Metode Data Warehouse

Proyek menggunakan pendekatan Star Schema yang terdiri dari:

- Fact Table: menyimpan data dan nilai pengukuran produksi.
- Dimension Tanggal: menyimpan informasi waktu.
- Dimension Komoditas: menyimpan jenis komoditas cabai.
- Dimension Wilayah: menyimpan informasi wilayah jika digunakan dalam model data.

## 6. Fitur Dashboard

- Ringkasan indikator produksi.
- Grafik produksi cabai bulanan.
- Perbandingan produksi tahunan.
- Analisis produksi berdasarkan komoditas.
- Analisis tren produksi komoditas.
- Analisis kontribusi produksi.
- Analisis produktivitas dan luas panen.
- Tabel data produksi.
- Filter tahun dan komoditas.
- Navigasi dashboard.
- Sistem caching dan refresh data.

## 7. Periode Data

Periode pengamatan: 2021–2025.

Objek penelitian: Produksi cabai Kabupaten Simalungun.

Indikator yang digunakan meliputi produksi, luas panen, dan produktivitas.

## 8. Catatan Penggunaan

Data yang masih bersifat uji coba harus diverifikasi terhadap sumber data asli sebelum digunakan sebagai hasil penelitian atau publikasi resmi.

Kredensial database disimpan melalui Streamlit Secrets dan tidak dicantumkan dalam repository publik.
