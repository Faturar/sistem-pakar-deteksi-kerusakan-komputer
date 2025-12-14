# 🧠 Sistem Pakar Diagnosa Penyakit

Metode **Certainty Factor (CF)** Berbasis Web

## 📌 Deskripsi Proyek

Aplikasi ini merupakan **Sistem Pakar berbasis web** yang digunakan untuk membantu pengguna dalam **mendiagnosa penyakit berdasarkan gejala** yang dipilih.
Sistem ini menerapkan metode **Certainty Factor (CF)** untuk menghitung tingkat keyakinan terhadap kemungkinan penyakit yang dialami pengguna.

Aplikasi dirancang dengan **antarmuka interaktif**, **responsif**, serta dilengkapi animasi dan fitur pendukung agar mudah digunakan oleh pengguna awam.

## 🖼️ Tampilan Aplikasi

### Halaman Utama
![Halaman Utama](images/image1.png)

### Proses Diagnosa
![Proses Diagnosa Forward Chaining](images/image4.png)

### Hasil Diagnosa
![Hasil Diagnosa Forward Chaining](images/image5.png)

### Proses Diagnosa
![Proses Diagnosa Backward Chaining](images/image2.png)

### Hasil Diagnosa
![Hasil Diagnosa Backward Chaining](images/image3.png)

---

## 🎯 Tujuan

- Membantu pengguna mendapatkan **diagnosa awal penyakit**
- Mengimplementasikan **metode Certainty Factor (CF)** dalam sistem pakar
- Menjadi media pembelajaran penerapan **AI sederhana di bidang kesehatan**
- Memenuhi kebutuhan tugas akademik / penelitian

---

## 🧩 Fitur Utama

- ✅ Pemilihan gejala menggunakan checkbox
- 📊 Progress bar indikator jumlah gejala dipilih
- 🔍 Fitur pencarian gejala
- 🧮 Perhitungan nilai **Certainty Factor**
- 📋 Hasil diagnosa dengan tingkat keyakinan (tinggi, sedang, rendah)
- 🎨 Animasi hasil & UI responsif
- ⬆️ Tombol _Back to Top_ (Floating Action Button)
- ⏳ Loading overlay saat proses diagnosa

---

## 🛠️ Teknologi yang Digunakan

- **Frontend**

  - HTML5
  - CSS3
  - JavaScript (Vanilla JS)
  - Bootstrap 5

- **Backend**

  - Python
  - Flask Framework

---

## 📂 Struktur Folder

```
project/
│── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│
│── templates/
│   ├── layout.html
│   ├── index.html
│   └── forward.html
│
│── app.py
│── README.md
```

---

## ⚙️ Cara Menjalankan Aplikasi

### 1️⃣ Clone Repository

```bash
git clone https://github.com/username/nama-repo.git
cd nama-repo
```

### 2️⃣ Install Dependensi

Pastikan Python sudah terpasang, lalu jalankan:

```bash
pip install flask
```

### 3️⃣ Jalankan Aplikasi

```bash
python app.py
```

### 4️⃣ Akses di Browser

Buka browser dan akses:

```
http://127.0.0.1:5000
```

---

## 📐 Metode Certainty Factor (CF)

Certainty Factor digunakan untuk menyatakan **tingkat keyakinan pakar** terhadap suatu hipotesis berdasarkan gejala yang dipilih.

Rumus dasar:

```
CF = MB - MD
```

Kombinasi CF:

```
CFkombinasi = CF1 + CF2 × (1 − CF1)
```

Hasil akhir ditampilkan dalam bentuk **persentase keyakinan**.

---

## 📄 Lisensi

Proyek ini dibuat untuk **keperluan akademik dan pembelajaran**.
Bebas digunakan dan dikembangkan lebih lanjut dengan mencantumkan sumber.

---
