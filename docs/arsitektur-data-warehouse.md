# ARSITEKTUR DATA WAREHOUSE
## Sistem Informasi Produksi Cabai Kabupaten Simalungun 2021–2025

### 1. Pendahuluan

Data Warehouse dikembangkan untuk mengintegrasikan dan mengelola data produksi cabai Kabupaten Simalungun periode 2021–2025.

Arsitektur yang digunakan adalah Star Schema dengan PostgreSQL pada Neon sebagai pusat penyimpanan data.

### 2. Arsitektur Database

Database menggunakan schema `dw` yang terdiri dari satu tabel fakta dan tiga tabel dimensi.

**Fact Table:**
- `dw.fact_produksi_bulanan`

**Dimension Tables:**
- `dw.dim_tanggal`
- `dw.dim_komoditas`
- `dw.dim_wilayah`

### 3. Diagram Star Schema

```mermaid
erDiagram
    DIM_TANGGAL ||--o{ FACT_PRODUKSI_BULANAN : memiliki
    DIM_KOMODITAS ||--o{ FACT_PRODUKSI_BULANAN : memiliki
    DIM_WILAYAH ||--o{ FACT_PRODUKSI_BULANAN : memiliki

    DIM_TANGGAL {
        id_tanggal PK
        tanggal
        hari
        bulan
        nama_bulan
        tahun
        kuartal
    }

    DIM_KOMODITAS {
        id_komoditas PK
        nama_komoditas
    }

    DIM_WILAYAH {
        id_wilayah PK
        nama_kabupaten
    }

    FACT_PRODUKSI_BULANAN {
        id_fakta PK
        id_tanggal FK
        id_komoditas FK
        id_wilayah FK
        luas_panen_ha
        produksi_ton
        produktivitas_ton_ha
        project_sumber
        updated_at
    }
```

### 4. Penjelasan Tabel

**A. Fact Produksi Bulanan**

Tabel fakta menyimpan nilai pengukuran produksi cabai berdasarkan periode, komoditas, dan wilayah.

Atribut utama:
- id_fakta
- id_tanggal
- id_komoditas
- id_wilayah
- luas_panen_ha
- produksi_ton
- produktivitas_ton_ha
- project_sumber
- updated_at

**B. Dimension Tanggal**

Menyimpan informasi waktu untuk mendukung analisis berdasarkan bulan, tahun, dan kuartal.

**C. Dimension Komoditas**

Menyimpan identitas jenis komoditas cabai yang dianalisis.

**D. Dimension Wilayah**

Menyimpan identitas wilayah kabupaten yang menjadi objek analisis.

### 5. Grain Data

Grain atau tingkat detail data pada tabel fakta adalah:

Satu baris mewakili satu kombinasi:
- Satu periode bulan.
- Satu jenis komoditas.
- Satu wilayah.

Terdapat unique constraint pada kombinasi `id_tanggal`, `id_komoditas`, dan `id_wilayah` untuk mencegah duplikasi pada grain tersebut.

### 6. Relasi Antar Tabel

Hubungan tabel menggunakan foreign key:

- `fact_produksi_bulanan.id_tanggal` → `dim_tanggal.id_tanggal`
- `fact_produksi_bulanan.id_komoditas` → `dim_komoditas.id_komoditas`
- `fact_produksi_bulanan.id_wilayah` → `dim_wilayah.id_wilayah`

Setiap tabel dimensi dapat memiliki banyak catatan pada tabel fakta.

### 7. Hasil Implementasi

Berdasarkan hasil pengujian database:

| Komponen | Jumlah |
|---|---:|
| Fact produksi bulanan | 180 baris |
| Dimension tanggal | 60 baris |
| Dimension komoditas | 3 baris |
| Dimension wilayah | 1 baris |
| Periode pengamatan | 2021–2025 |

### 8. Kesimpulan

Penerapan Star Schema memungkinkan data produksi cabai dianalisis berdasarkan dimensi waktu, komoditas, dan wilayah.

Struktur ini menjadi dasar pengembangan visualisasi, analisis tren, perbandingan tahunan, dan pengukuran produktivitas pada dashboard Streamlit.

**Catatan:** Data yang digunakan dalam pengujian dashboard merupakan data uji coba dan belum boleh dianggap sebagai statistik produksi resmi sebelum diverifikasi dengan sumber data pemerintah.
