# Analisis E-Commerce ✨

Panduan ini menjelaskan langkah-langkah untuk menyiapkan environment dan menjalankan aplikasi Streamlit untuk proyek **Analisis Data**.

---

## Setup Env - Anaconda

Langkah-langkah untuk menyiapkan environment menggunakan Anaconda:

```bash
# Membuat environment baru dengan Python 3.9
conda create --name main-ds python=3.9

# Mengaktifkan environment
conda activate main-ds

# Menginstal dependencies dari file requirements.txt
pip install -r requirements.txt
```


## Setup Env - Shell/Terminal

Langkah-langkah untuk menyiapkan environment menggunakan shell atau terminal:

``` bash
# Masuk ke direktori proyek
cd proyek_analisis_data

# Menginstal pipenv dan membuat environment baru
pipenv install

# Mengaktifkan environment pipenv
pipenv shell

# Menginstal dependencies dari file requirements.txt
pip install -r requirements.txt
```


## Menjalankan Streamlit

Setelah environment siap, jalankan aplikasi Streamlit dengan perintah berikut:

``` bash
# Masuk ke folder dashboard
cd dashboard

# Run app.py
streamlit run app.py
```