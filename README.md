# Data Analisis dengan Python

## Setup  (Opsi 1)
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install numpy pandas scipy matplotlib seaborn jupyter streamlit babel
```

## Setup (Opsi 2 - Menggunakan Terminal/PowerShell Tanpa Conda)
```
pip install numpy pandas scipy matplotlib seaborn jupyter streamlit babel
mkdir main-ds
cd main-ds
pipenv install
pipenv shell
```

## Run steamlit app
```
streamlit run dashboard_ecommerce.py
```
