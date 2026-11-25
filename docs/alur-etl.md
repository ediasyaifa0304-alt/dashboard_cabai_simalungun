# DOKUMENTASI PROSES ETL
## Sistem Informasi Produksi Cabai Kabupaten Simalungun 2021–2025

### 1. Pendahuluan

ETL (Extract, Transform, Load) merupakan proses pengolahan data untuk memastikan data yang berasal dari file sumber dapat dibersihkan, disesuaikan, dan disimpan ke dalam database PostgreSQL Neon.

Proses ETL pada sistem ini dilakukan menggunakan Python, Pandas, dan Psycopg2 melalui Google Colab.

### 2. Arsitektur Proses ETL

```text
DATA SUMBER (CSV / EXCEL)
          |
          v
       EXTRACT
   Upload data ke Colab
          |
          v
      TRANSFORM
  - Pemeriksaan kolom
  - Konversi satuan
  - Perhitungan produktivitas
  - Validasi data
  - Pemeriksaan duplikasi
          |
          v
         LOAD
  - Koneksi PostgreSQL Neon
  - Pembuatan tabel
  - Insert / Update (UPSERT)
          |
          v
     DATABASE NEON
 produksi_cabai_bulanan
          |
          v
    STREAMLIT DASHBOARD
  Visualisasi dan analisis
```

### 3. Tahapan Extract

Pengambilan data dilakukan melalui file CSV yang diunggah ke Google Colab.

Proses meliputi:
- Membaca file CSV menggunakan Pandas.
- Memeriksa struktur kolom.
- Memastikan format data sesuai template.
- Menampilkan preview data sebelum diproses.

### 4. Tahapan Transform

Transformasi dilakukan untuk menyesuaikan data agar memiliki format dan satuan yang konsisten.

**A. Konversi satuan produksi**

| Satuan sumber | Konversi |
|---|---|
| Ton | 1 |
| Kuintal | 0,1 |
| Kg | 0,001 |

Seluruh nilai produksi dinormalisasi menjadi ton.

**B. Konversi produktivitas**

| Satuan sumber | Konversi |
|---|---|
| Ton/ha | 1 |
| Kuintal/ha | 0,1 |

Seluruh nilai produktivitas dinormalisasi menjadi ton/ha.

**C. Perhitungan produktivitas**

Produktivitas dapat dihitung menggunakan rumus:

Produktivitas = Produksi (ton) / Luas Panen (ha)

Perhitungan otomatis hanya dilakukan apabila:
- Jenis luas merupakan luas panen.
- Data produksi tersedia.
- Data luas panen tersedia dan lebih besar dari nol.

**D. Validasi data**

Pemeriksaan meliputi:
- Tahun berada pada rentang 2021–2025.
- Bulan berada pada rentang 1–12.
- Tidak terdapat nilai negatif.
- Sumber data dicantumkan.
- Tidak terdapat duplikasi kombinasi tahun, bulan, kabupaten, dan komoditas.
- Kelengkapan periode bulanan diperiksa tanpa membuat angka pengganti.

### 5. Tahapan Load

Data yang telah lolos transformasi dimasukkan ke database PostgreSQL Neon.

Tabel tujuan:

`produksi_cabai_bulanan`

Metode penyimpanan menggunakan UPSERT.

UPSERT memiliki dua fungsi:
1. INSERT: menambahkan data baru.
2. UPDATE: memperbarui data apabila kombinasi tahun, bulan, kabupaten, dan komoditas sudah tersedia.

Dengan demikian, proses impor ulang tidak menghasilkan duplikasi untuk kombinasi periode yang sama.

### 6. Verifikasi Hasil ETL

Setelah proses impor, dilakukan pemeriksaan terhadap:
- Jumlah baris yang berhasil diproses.
- Jumlah data berdasarkan tahun dan komoditas.
- Jumlah indikator luas lahan yang terisi.
- Jumlah indikator produksi yang terisi.
- Jumlah indikator produktivitas yang terisi.

Data kemudian dibaca kembali dari Neon dan diekspor sebagai file CSV untuk pemeriksaan hasil.

### 7. Integrasi dengan Streamlit

Aplikasi Streamlit membaca data secara langsung dari database Neon.

Fungsi integrasi meliputi:
- Mengambil data produksi bulanan.
- Menampilkan indikator statistik.
- Menampilkan grafik perkembangan produksi.
- Membandingkan produksi tahunan.
- Menampilkan tabel data.
- Menyediakan fitur ekspor laporan.

Aplikasi menggunakan cache data selama 300 detik untuk mengurangi pengambilan data berulang.

### 8. Kesimpulan

Proses ETL memungkinkan data produksi cabai dari berbagai periode diolah secara terstruktur sebelum digunakan untuk analisis.

Integrasi Google Colab, PostgreSQL Neon, GitHub, dan Streamlit membentuk alur pengolahan data yang mendukung pembaruan, penyimpanan, verifikasi, dan visualisasi informasi produksi cabai Kabupaten Simalungun.
