# FINALISASI SISTEM
## Dashboard Produksi Cabai Kabupaten Simalungun 2021–2025

### 1. Deskripsi Sistem

Dashboard Produksi Cabai Kabupaten Simalungun merupakan aplikasi berbasis web yang digunakan untuk menyajikan informasi produksi, luas lahan, dan produktivitas cabai dalam periode 2021–2025.

Sistem dikembangkan menggunakan Python, PostgreSQL Neon, GitHub, dan Streamlit.

### 2. Arsitektur Sistem

Alur kerja sistem:

CSV / EXCEL
↓
GOOGLE COLAB
↓
NEON POSTGRESQL
↓
GITHUB
↓
STREAMLIT DASHBOARD

Keterangan:
- CSV/Excel: sumber data.
- Google Colab: pengolahan dan pengiriman data.
- Neon PostgreSQL: penyimpanan data.
- GitHub: penyimpanan kode aplikasi dan dokumentasi.
- Streamlit: penyajian dashboard berbasis web.

### 3. Teknologi yang Digunakan

| Teknologi | Fungsi |
|---|---|
| Python | Bahasa pemrograman |
| Pandas | Pengolahan data |
| Plotly | Visualisasi grafik |
| Streamlit | Framework dashboard |
| PostgreSQL | Database relasional |
| Neon | Cloud database |
| GitHub | Version control dan repository |
| Google Colab | Lingkungan pengolahan data |

### 4. Fitur Utama Sistem

1. Filter data berdasarkan tahun.
2. Filter berdasarkan jenis komoditas cabai.
3. Ringkasan statistik produksi.
4. Grafik produksi cabai bulanan.
5. Perbandingan produksi tahunan.
6. Produksi berdasarkan komoditas.
7. Perkembangan luas lahan.
8. Analisis otomatis produksi cabai.
9. Insight perubahan produksi.
10. Tabel data produksi bulanan.
11. Download data CSV.
12. Export laporan profesional PDF.
13. Export laporan Excel.

### 5. Integrasi Database

Sistem menggunakan Neon PostgreSQL sebagai database pusat.

Tabel utama:

`produksi_cabai_bulanan`

Data diambil menggunakan koneksi database dan query SQL dari aplikasi Streamlit.

Kredensial database disimpan melalui Streamlit Secrets.

### 6. Deployment Aplikasi

Aplikasi disimpan pada GitHub dan dijalankan menggunakan Streamlit Community Cloud.

File utama aplikasi:
- app.py
- requirements.txt
- README.md

Aplikasi dapat diakses melalui alamat URL deployment Streamlit.

### 7. Pengujian Sistem

Pengujian dilakukan terhadap:
- Koneksi database.
- Pembacaan data.
- Filter dashboard.
- Visualisasi grafik.
- Analisis otomatis.
- Tabel data.
- Ekspor PDF dan Excel.
- Akses aplikasi melalui browser.

Status kelulusan setiap pengujian dicatat berdasarkan hasil pengujian aktual.

### 8. Keterbatasan Sistem

Dataset yang digunakan pada tahap pengembangan merupakan dataset latihan dengan estimasi sebaran bulanan, bukan observasi bulanan resmi.

Oleh karena itu, hasil visualisasi dan analisis pada tahap pengembangan tidak dapat digunakan sebagai representasi statistik resmi Kabupaten Simalungun.

Penggunaan untuk analisis kebijakan atau penelitian empiris memerlukan penggantian dataset dengan data terverifikasi.

### 9. Pengembangan Selanjutnya

Beberapa pengembangan yang dapat dilakukan:
- Integrasi data resmi dari instansi terkait.
- Pembaruan data secara berkala.
- Penambahan visualisasi spasial.
- Pengembangan analisis tren lanjutan.
- Peningkatan performa dashboard.
- Pengembangan sistem autentikasi pengguna.

### 10. Kesimpulan

Dashboard Produksi Cabai Kabupaten Simalungun telah dikembangkan sebagai sistem informasi berbasis web yang mengintegrasikan proses pengolahan data, penyimpanan database, visualisasi, analisis, dan pelaporan.

Sistem ini diharapkan dapat menjadi sarana pendukung penyajian informasi produksi cabai secara terstruktur, interaktif, dan mudah diakses.
