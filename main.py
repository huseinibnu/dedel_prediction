import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Load model
stunting_model = joblib.load('model_stunting.joblib')

st.title('Aplikasi Prediksi Status Gizi')

# Input data
tinggi = st.number_input('Masukkan panjang badan anak anda (cm) : ', min_value=0)
umur = st.number_input('Masukkan umur anak anda (bulan) : ', min_value=0)
jenis_kelamin = st.selectbox('Jenis Kelamin', ['laki-laki', 'perempuan'])

# Ubah jenis kelamin menjadi bentuk numerik
jenis_kelamin_num = 0 if jenis_kelamin == "laki-laki" else 1

# Prediksi model
diab_diagnosis = ''

# Button prediksi
if st.button('Prediksi Stunting'):
    # Buat DataFrame untuk prediksi
    data_baru = np.array([umur, jenis_kelamin_num, tinggi])

    # Prediksi
    diab_prediction = stunting_model.predict(data_baru)

    # Konversi hasil prediksi menjadi label yang sesuai
    if diab_prediction[0] == 0:
        diab_diagnosis = "Severely Stunted"
    elif diab_prediction[0] == 1:
        diab_diagnosis = "Stunted"
    elif diab_prediction[0] == 2:
        diab_diagnosis = "Normal"
    else:
        diab_diagnosis = "Tinggi"

    # Tampilkan hasil prediksi
    st.success(diab_diagnosis)
