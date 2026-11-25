# PENGUJIAN INTEGRASI DAN EVALUASI SISTEM

## Sistem Informasi Produksi Cabai Kabupaten Simalungun 2021–2025

### 1. Tujuan Pengujian

Pengujian dilakukan untuk memastikan seluruh komponen sistem dapat bekerja secara terintegrasi, mulai dari penyimpanan data hingga penyajian informasi pada dashboard.

### 2. Pengujian Integrasi Database

| ID | Pengujian | Hasil yang Diharapkan |
|---|---|---|
| T01 | Koneksi Neon | Database berhasil terhubung |
| T02 | Pembacaan data | Data berhasil ditampilkan |
| T03 | Query database | Tidak terdapat error SQL |
| T04 | Pembaruan data | Dashboard dapat membaca data terbaru |

### 3. Pengujian Dashboard

| ID | Pengujian | Hasil yang Diharapkan |
|---|---|---|
| T05 | Filter tahun | Data berubah sesuai tahun |
| T06 | Filter komoditas | Data berubah sesuai komoditas |
| T07 | Kombinasi filter | Hasil sesuai pilihan filter |
| T08 | Kartu indikator | Nilai statistik tampil |
| T09 | Grafik produksi | Grafik tampil sesuai data |
| T10 | Perbandingan tahunan | Perbandingan berhasil ditampilkan |
| T11 | Analisis produktivitas | Informasi produktivitas tampil |
| T12 | Tabel bulanan | Data tampil sesuai filter |

### 4. Pengujian Ekspor Laporan

| ID | Pengujian | Hasil yang Diharapkan |
|---|---|---|
| T13 | Export PDF | File PDF berhasil diunduh |
| T14 | Export Excel | File Excel berhasil diunduh |
| T15 | Isi laporan | Data sesuai dengan filter yang dipilih |
| T16 | Format laporan | Tabel dan angka terbaca dengan baik |

### 5. Pengujian Deployment

| ID | Pengujian | Hasil yang Diharapkan |
|---|---|---|
| T17 | Akses Streamlit | Aplikasi dapat dibuka |
| T18 | GitHub integration | Perubahan kode dapat di-deploy |
| T19 | Database Secrets | Kredensial tersimpan aman |
| T20 | Responsivitas | Dashboard dapat digunakan melalui browser |

### 6. Evaluasi Sistem

Evaluasi dilakukan berdasarkan beberapa aspek:

1. Fungsionalitas: seluruh fitur berjalan sesuai tujuan.
2. Integrasi: koneksi antara Neon dan Streamlit berjalan baik.
3. Visualisasi: grafik dan tabel mudah dipahami.
4. Pelaporan: hasil ekspor dapat dibuka dan digunakan.
5. Keamanan: kredensial database tidak dipublikasikan.

### 7. Kesimpulan

Pengujian integrasi bertujuan memastikan sistem informasi produksi cabai Kabupaten Simalungun dapat menjalankan proses pengambilan data, pengolahan, penyimpanan, visualisasi, dan pelaporan secara terintegrasi.

Status akhir pengujian ditentukan berdasarkan hasil pengujian aktual setiap komponen.
