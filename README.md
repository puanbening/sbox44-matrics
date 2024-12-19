# Kriptografi S-box<sub>44</sub>

## Deskripsi
Aplikasi ini merupakan tool berbasis Streamlit yang digunakan untuk menghitung berbagai parameter (matrics) kriptografi pada S-box, seperti:
- **Nonlinearity (NL)**
- **Strict Avalanche Criterion (SAC)**
- **Bit Independence Criterion - Nonlinearity (BIC-NL)**
- **Bit Independence Criterion - SAC (BIC-SAC)**
- **Linear Approximation Probability (LAP)**
- **Differential Approximation Probability (DAP)**

## Fitur 
1. **Mengunggah File Excel**: User dapat melakukan input file excel berisi S-box.
2. **Menampilkan hasil import S-box**: Hasil import S-box akan muncul dalam bentuk dataframe.
3. **Memilih Parameter**: User dapat memilih satu parameter untuk dihitung.
4. **Hitung Nilai**: Hasil perhitungan akan ditampilkan setelah User memilih tombol Hitung.

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
