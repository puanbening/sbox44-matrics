# Kriptografi S-box<sub>44</sub>

## Deskripsi
Aplikasi ini merupakan tool berbasis Streamlit yang digunakan untuk menghitung berbagai parameter (matrics) kriptografi pada S-box, seperti:
- **Nonlinearity (NL)**
- **Strict Avalanche Criterion (SAC)**
- **Bit Independence Criterion - Nonlinearity (BIC-NL)**
- **Bit Independence Criterion - SAC (BIC-SAC)**
- **Linear Approximation Probability (LAP)**
- **Differential Approximation Probability (DAP)**

---

## Fitur Utama
1. **Unggah File Excel**: Unggah file excel berisi S-box.
2. **Pilih Parameter**: User dapat memilih satu parameter untuk dihitung.
3. **Hitung Nilai**: Hasil perhitungan akan ditampilkan.

---

## Setup Environment: Shell/Terminal
```
mkdir dashboard
cd dashboard
pipenv install
pipenv shell
pip install -r requirements.txt
```
## Run steamlit app
```
streamlit run dashboard.py
```
