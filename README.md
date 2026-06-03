# ✨ VisionStudio Pro

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

**VisionStudio Pro** adalah aplikasi web interaktif untuk pemrosesan dan analisis citra digital (*Digital Image Processing*). Dibangun dengan pendekatan desain *Split Screen Studio* yang modern dan *clean*, aplikasi ini memungkinkan pengguna untuk mengeksplorasi berbagai algoritma Computer Vision secara *real-time* tanpa perlu menulis kode.

Proyek ini dikembangkan sebagai tugas akhir / laporan praktikum mata kuliah Pengolahan Citra Digital.

---

## 🚀 Fitur Utama

Aplikasi ini mengemas 6 modul pemrosesan citra ke dalam antarmuka yang sangat responsif:

1. **🎨 Core Vision:** Konversi citra dasar (RGB to Grayscale) dan Thresholding dinamis untuk menghasilkan citra biner.
2. **✦ Arithmetic:** Manipulasi intensitas cahaya pada piksel (Penjumlahan, Pengurangan, Perkalian, Pembagian) dengan *clipping* presisi.
3. **⊕ Logic Ops:** Operasi gerbang logika bitwise (AND, OR, XOR, NOT) yang dilengkapi dengan sistem *Auto-Masking* internal sehingga tidak memerlukan dua input gambar secara manual.
4. **📊 Histogram:** *Visualizer* interaktif untuk mengekstrak dan menganalisis frekuensi penyebaran intensitas piksel warna (Red, Green, Blue) pada gambar.
5. **🌀 Convolution:** Pemfilteran spasial berbasis *kernel matrix* untuk memberikan efek *Gaussian Blur*, *Sharpening*, hingga pendeteksian tepi (*Sobel Edge*).
6. **⬡ Math Morphology:** Mesin operasi morfologi matematis (Erosi, Dilasi, Opening, Closing) yang dilengkapi pilihan bentuk *Structuring Element (SE)*: Persegi, Silang, dan Elips dengan ukuran kernel dinamis.

---

## 🛠️ Teknologi yang Digunakan

* **Bahasa Pemrograman:** Python 3.x
* **UI/UX Framework:** Streamlit
* **Computer Vision Engine:** OpenCV (`opencv-python`)
* **Data & Matrix Processing:** NumPy & Pandas

---

## 📁 Struktur Repositori

Proyek ini menggunakan arsitektur modular (MVC) untuk memisahkan antara *logic*, antarmuka (UI), dan *file* utama agar mudah dikembangkan.

```text
Project pcd/
│

├── app.py                    # File utama eksekusi aplikasi
├──  images/                  # Folder berisi gambar original & hasil screenshot pengujian
└── README.md                 # Dokumentasi proyek
├── requirements.txt          # Daftar dependensi library
