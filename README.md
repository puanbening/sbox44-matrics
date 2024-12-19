# Kriptografi S-box<sub>44</sub>

## Deskripsi
Aplikasi ini merupakan tool berbasis Streamlit yang digunakan untuk menghitung nilai dari berbagai parameter (matrics) kriptografi pada S-box, seperti:
- **Nonlinearity (NL)**
- **Strict Avalanche Criterion (SAC)**
- **Bit Independence Criterion - Nonlinearity (BIC-NL)**
- **Bit Independence Criterion - SAC (BIC-SAC)**
- **Linear Approximation Probability (LAP)**
- **Differential Approximation Probability (DAP)**

## Fitur 
1. **Mengunggah file excel**: User dapat melakukan input file excel berisi S-box.
2. **Menampilkan hasil import S-box**: Hasil import S-box akan muncul dalam bentuk dataframe.
3. **Memilih parameter**: User dapat memilih satu parameter untuk dihitung.
4. **Menghitung nilai parameter**: Hasil perhitungan akan ditampilkan setelah User menekan tombol 'Hitung'.

## Setup Environment: Shell/Terminal
```
cd sbox44-matrics
pipenv install
pipenv shell
pip install -r requirements.txt
```
## Run steamlit app
```
streamlit run dashboard.py
```
