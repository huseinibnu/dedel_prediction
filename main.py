import streamlit as st
import joblib
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import zipfile

st.set_page_config(
    page_title="DEDEL",
    page_icon="logo USU.png",
    layout="wide"
)

# Tambahkan CSS untuk mengubah warna background sidebar menjadi #62ea39
st.markdown("""
    <style>
        /* Mengubah warna latar belakang sidebar */
        [data-testid="stSidebar"] {
            background-color: #62ea39;
        }
    </style>
    """, unsafe_allow_html=True)


# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Pengenalan", "Prediksi", "Panduan MPASI"],
        icons=["bar-chart-line", "question-circle", "journal-text"],
        menu_icon="cast",
        default_index=1,
        styles={
            "container": {"padding": "0!important", "background-color": "#62ea39"},  # Background hijau
            "icon": {"color": "#000", "font-size": "22px"},
            "nav-link": {"color": "#000", "font-size": "22px", "text-align": "left", "margin": "0px",
                         "--hover-color": "#62ea39"},  # Warna hover hijau
            "nav-link-selected": {"color": "#62ea39", "background-color": "#f4f6fa"},
        }
    )

if selected == "Pengenalan":
    back_button_html = """
            <style>
                .back-button {
                    background-color: #62ea39;
                    text-decoration:None;
                    padding:8px;
                    color: #fff;
                    font-weight: bold;
                    border-radius: 25px;
                    border: 2px solid #fff;
                }
                .back-button:hover {
                    background-color: white;
                    text-decoration: None;
                    color: #62ea39;
                    border: 2px solid #62ea39;
                }
            </style>
            <a class="back-button" href="https://dedel.pubhe.com/public/dashboard" target="_blank">🔙 Kembali</a>
            """
    st.markdown(back_button_html, unsafe_allow_html=True)

    @st.cache_data
    def get_data():
        df = pd.read_csv("data_balita.csv")
        return df

    df = get_data()

    st.header("Child Growth Dashboard :bar_chart:", divider="green")
    st.markdown("")

    # Top KPI
    total_children = df["Umur (bulan)"].count()  # No need for int() conversion here
    average_height = round(df["Tinggi Badan (cm)"].mean(), 1)
    average_age = round(df["Umur (bulan)"].mean(), 1)

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("Jumlah Anak:")
        st.subheader(f"{total_children:,}")

    with middle_column:
        st.subheader("Rata-rata Tinggi Badan:")
        st.subheader(f"{average_height} cm")

    with right_column:
        st.subheader("Rata-rata Umur:")
        st.subheader(f"{average_age} bulan")

    # Compute the count of each gender
    gender_counts = df["Jenis Kelamin"].value_counts().reset_index()
    gender_counts.columns = ["Jenis Kelamin", "Jumlah"]

    fig_gender_distribution = go.Figure()
    fig_gender_distribution.add_trace(go.Bar(
        x=gender_counts["Jenis Kelamin"],
        y=gender_counts["Jumlah"],
        marker_color=["#87ceeb", "#ffc0cb"],  # Custom colors for the bars
    ))
    fig_gender_distribution.update_layout(
        title="<b>Distribusi Jenis Kelamin</b>",
        template="plotly_white",
        xaxis=dict(fixedrange=True),  # Disable zoom on x-axis
        yaxis=dict(fixedrange=True),  # Disable zoom on y-axis
        dragmode=False,  # Disable panning
        showlegend=False  # Hide legend if not necessary
    )

    # Compute the count of each nutritional status
    status_gizi_counts = df["Status Gizi"].value_counts().reset_index()
    status_gizi_counts.columns = ["Status Gizi", "Jumlah"]

    # Create a bar chart for nutritional status distribution
    fig_status_gizi_distribution = go.Figure()
    fig_status_gizi_distribution.add_trace(go.Bar(
        x=status_gizi_counts["Status Gizi"],
        y=status_gizi_counts["Jumlah"],
        marker_color=["#FFA07A", "#20B2AA", "#778899", "#DDA0DD"],  # Custom colors for the bars
    ))
    fig_status_gizi_distribution.update_layout(
        title="<b>Distribusi Status Gizi</b>",
        template="plotly_white",
        xaxis=dict(fixedrange=True),  # Disable zoom on x-axis
        yaxis=dict(fixedrange=True),  # Disable zoom on y-axis
        dragmode=False,  # Disable panning
        showlegend=False  # Hide legend if not necessary
    )

    st.markdown("")
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_gender_distribution, use_container_width=True)
    right_column.plotly_chart(fig_status_gizi_distribution, use_container_width=True)

if selected == "Prediksi":
    back_button_html = """
        <style>
            .back-button {
                background-color: #62ea39;
                text-decoration:None;
                padding:8px;
                color: #fff;
                font-weight: bold;
                border-radius: 25px;
                border: 2px solid #fff;
            }
            .back-button:hover {
                background-color: white;
                text-decoration: None;
                color: #62ea39;
                border: 2px solid #62ea39;
            }
        </style>
        <a class="back-button" href="https://dedel.pubhe.com/public/dashboard" target="_blank">🔙 Kembali</a>
        """
    st.markdown(back_button_html, unsafe_allow_html=True)

    # Ekstrak file model dari ZIP
    with zipfile.ZipFile('model_stunting.zip', 'r') as zipf:
        zipf.extract('model_stunting.joblib')

    # Load model
    stunting_model = joblib.load('model_stunting.joblib')

    st.title('Prediksi Status Gizi 📏')

    # Gaya CSS yang diterapkan pada input, selectbox, dan tombol
    custom_css = """
        <style>
        /* Gaya input teks */
        input[type="text"] {
            background-color: #62ea39 !important;
            color: #fff !important;
            border: 2px solid #62ea39 !important;
            border-radius: 8px !important;
        }

        input[type="text"]:focus {
            background-color: white !important;
            color: #62ea39 !important;
            border: 2px solid #62ea39 !important;
        }

        /* Gaya selectbox */
        .stSelectbox select {
            background-color: #62ea39 !important;
            color: #fff !important;
            border-radius: 8px !important;
            padding: 8px !important;
        }

        .stSelectbox select:focus {
            background-color: #62ea39 !important;
            color: #62ea39 !important;
            border: 2px solid #62ea39 !important;
        }

        /* Gaya tombol */
        .stButton > button {
            background-color: #62ea39 !important;
            color: white !important;
            border: 2px solid #62ea39 !important;
            padding: 10px 16px !important;
            font-weight: bold !important;
            border-radius: 25px !important;
        }

        .stButton > button:hover {
            background-color: white !important;
            color: #62ea39 !important;
            border: 2px solid #62ea39 !important;
        }
        </style>
        """

    # Terapkan CSS dengan markdown
    st.markdown(custom_css, unsafe_allow_html=True)

    tinggi = st.text_input('**Masukkan panjang badan anak anda (cm) :**')
    umur = st.text_input('**Masukkan umur anak anda (bulan) :**')
    jenis_kelamin = st.selectbox('**Jenis Kelamin**', ['laki-laki', 'perempuan'])

    tinggi_awal = 0.0
    umur_bulan = 0
    if tinggi.strip():  # Memastikan tinggi tidak kosong
        tinggi_awal = float(tinggi)  # Konversi tinggi menjadi float
    if umur.strip():
        umur_bulan = int(umur)  # Umur si bayi dalam bulan

    # Perhitungan prediksi tinggi badan setiap bulan
    for bulan in range(umur_bulan, 60):
        if bulan < 12:  # 0-12 bulan
            tinggi_awal += 2.083
        elif bulan < 24:  # 13-24 bulan
            tinggi_awal += 1.083
        elif bulan < 36:  # 25-36 bulan
            tinggi_awal += 0.75
        else:  # 37-60 bulan
            tinggi_awal += 0.416

    # Hasil prediksi tinggi badan pada usia 60 bulan
    hasil_prediksi = tinggi_awal

    # Ubah jenis kelamin menjadi bentuk numerik
    jenis_kelamin_num = 0 if jenis_kelamin == "laki-laki" else 1

    # Prediksi model
    diab_diagnosis = ''

    # Button prediksi
    if st.button('Prediksi Stunting'):
        # Buat DataFrame untuk prediksi
        data_baru = pd.DataFrame([[umur, jenis_kelamin_num, tinggi]],
                                 columns=['Umur (bulan)', 'Jenis Kelamin', 'Tinggi Badan (cm)'])

        # Prediksi
        diab_prediction = stunting_model.predict(data_baru)

        # Konversi hasil prediksi menjadi label yang sesuai
        if diab_prediction[0] == 0:
            diab_diagnosis = (
                "<hr><div style='background-color: rgba(255, 0, 0, 0.2); border-radius: 10px; padding: 10px;'>"
                "<p style='color:black; font-size:18px; text-align:justify;'>Berdasarkan data yang Anda masukkan, anak Anda tergolong <span style='color:red;'><b>Severely Stunted (Sangat Pendek)</b></span>. Kami memahami bahwa sebagai orang tua, Anda pasti telah melakukan yang terbaik. Untuk langkah selanjutnya, berikut saran kami: "
                "<br><br>1. <span style='color:red;'><b>Konsultasi</b></span>: Silakan berkonsultasi dengan kader posyandu atau tenaga kesehatan untuk mendapatkan bantuan lebih lanjut. "
                "<br>2. <span style='color:red;'><b>MPASI</b></span>: Jika anak sudah bisa mengonsumsi <span style='color:red;'><b>MPASI</b></span>, kunjungi bagian 'Panduan MPASI' di sebelah kiri untuk panduan makanan tambahan yang bergizi. "
                "<br><br>Kami berharap, dengan langkah-langkah ini, tinggi badan anak Anda dapat mencapai kategori normal di waktu yang akan datang.</p></div>")

            height_prediction = (
                f"<hr><div style='background-color: rgba(255, 0, 0, 0.2); border-radius: 10px; padding: 10px;'> "
                f"<p style='color:red; font-size:18px; text-align:justify;'>Prediksi <b>tinggi badan</b> si bayi pada usia <b>60 bulan</b> atau <b>5 tahun</b> yaitu <b>{hasil_prediksi:.2f}</b> cm.</p></div>")

        elif diab_prediction[0] == 1:
            diab_diagnosis = (
                "<hr><div style='background-color: rgba(255, 0, 0, 0.2); border-radius: 10px; padding: 10px;'>"
                "<p style='color:black; font-size:18px; text-align:justify;'>Berdasarkan data yang Anda masukkan, anak Anda tergolong <span style='color:red;'><b>Stunted (Pendek)</b></span>. Kami memahami bahwa sebagai orang tua, Anda pasti telah melakukan yang terbaik. Untuk langkah selanjutnya, berikut saran kami: "
                "<br><br>1. <span style='color:red;'><b>Konsultasi</b></span>: Silakan berkonsultasi dengan kader posyandu atau tenaga kesehatan untuk mendapatkan bantuan lebih lanjut. "
                "<br>2. <span style='color:red;'><b>MPASI</b></span>: Jika anak sudah bisa mengonsumsi <span style='color:red;'><b>MPASI</b></span>, kunjungi bagian 'Panduan MPASI' di sebelah kiri untuk panduan makanan tambahan yang bergizi. "
                "<br><br>Kami berharap, dengan langkah-langkah ini, tinggi badan anak Anda dapat mencapai kategori normal di waktu yang akan datang.</p></div>")

            height_prediction = (
                f"<hr><div style='background-color: rgba(255, 0, 0, 0.2); border-radius: 10px; padding: 10px;'> "
                f"<p style='color:red; font-size:18px; text-align:justify;'>Prediksi <b>tinggi badan</b> si bayi pada usia <b>60 bulan</b> atau <b>5 tahun</b> yaitu <b>{hasil_prediksi:.2f}</b> cm.</p></div>")

        elif diab_prediction[0] == 2:
            diab_diagnosis = (
                "<hr><div style='background-color: rgba(0, 255, 0, 0.2); border-radius: 10px; padding: 10px;'>"
                "<p style='color:black; font-size:18px; text-align:justify;'><span style='color:green;'><b>Selamat!</b></span> Berdasarkan data yang Anda masukkan, anak Anda tergolong <span style='color:green;'><b>Normal</b></span>. Tetaplah memberikan yang terbaik untuk pertumbuhan dan perkembangan anak Anda."
                "<br><br>Jika Anda memerlukan panduan tentang <span style='color:green;'><b>MPASI</b></span>, silakan kunjungi bagian 'Panduan MPASI' di sebelah kiri. Kami berharap tinggi badan anak Anda dapat terus meningkat di bulan yang akan datang.</p></div>")

            height_prediction = (
                f"<hr><div style='background-color: rgba(0, 255, 0, 0.2); border-radius: 10px; padding: 10px;'> "
                f"<p style='color:green; font-size:18px; text-align:justify;'>Prediksi <b>tinggi badan</b> si bayi pada usia <b>60 bulan</b> atau <b>5 tahun</b> yaitu <b>{hasil_prediksi:.2f}</b> cm.</p></div>")

        else:
            diab_diagnosis = (
                "<hr><div style='background-color: rgba(0, 255, 0, 0.2); border-radius: 10px; padding: 10px;'>"
                "<p style='color:black; font-size:18px; text-align:justify;'><span style='color:green;'><b>Selamat!</b></span> Berdasarkan data yang Anda masukkan, anak Anda tergolong <span style='color:green;'><b>Tinggi</b></span>. Ini menunjukkan bahwa pertumbuhan anak Anda sangat baik."
                "<br><br>Tetaplah memberikan yang terbaik untuk pertumbuhan dan perkembangan anak Anda. Pastikan anak mendapatkan pola makan yang seimbang dan cukup aktivitas fisik untuk menjaga kesehatannya."
                "<br><br>Jika Anda memerlukan panduan tentang <span style='color:green;'><a href='#mpasi'><b>MPASI</b></a></span> atau tips lainnya, silakan kunjungi bagian 'Panduan MPASI' di sebelah kiri.</p></div>")

            height_prediction = (
                f"<hr><div style='background-color: rgba(0, 255, 0, 0.2); border-radius: 10px; padding: 10px;'> "
                f"<p style='color:green; font-size:18px; text-align:justify;'>Prediksi <b>tinggi badan</b> si bayi pada usia <b>60 bulan</b> atau <b>5 tahun</b> yaitu <b>{hasil_prediksi:.2f}</b> cm.</p></div>")

        # Tampilkan hasil klasifikasi
        st.markdown(diab_diagnosis, unsafe_allow_html=True)

        # Tampilkan hasil prediksi
        st.markdown(height_prediction, unsafe_allow_html=True)

if selected == "Panduan MPASI":
    back_button_html = """
            <style>
                .back-button {
                    background-color: #62ea39;
                    text-decoration:None;
                    padding:8px;
                    color: #fff;
                    font-weight: bold;
                    border-radius: 25px;
                    border: 2px solid #fff;
                }
                .back-button:hover {
                    background-color: white;
                    text-decoration: None;
                    color: #62ea39;
                    border: 2px solid #62ea39;
                }
            </style>
            <a class="back-button" href="https://dedel.pubhe.com/public/dashboard" target="_blank">🔙 Kembali</a>
            """
    st.markdown(back_button_html, unsafe_allow_html=True)

    st.title("Panduan MPASI 📖")
    st.markdown("""
            <div style='color: black; font-size:18px; text-align:justify;'>
                <div style='background-color: #d4edda; padding: 1rem; border-radius: 0.5rem;'>
                    Peran ibu sangat penting dalam mencegah <b>stunting</b> sejak kehamilan dengan memberikan stimulasi yang tepat selama <b>masa emas (0-3 tahun)</b>. <b>Stunting</b> ditandai dengan pertumbuhan yang tidak sesuai standar <b>WHO</b>. Selain ibu, dukungan keluarga dan masyarakat juga diperlukan untuk mengurangi risiko <b>stunting</b> dan mewujudkan Generasi Emas 2045. Pemberian <b>MPASI</b> yang tepat merupakan salah satu metode pencegahan <b>stunting</b> pada bayi berusia 6 bulan keatas. Berikut kami paparkan informasi terkait <b>MPASI</b>.
                </div>
            </div><br>
        """, unsafe_allow_html=True)

    st.header("Tahapan Tekstur MPASI\n", divider="green")
    st.markdown("""
            <div style='color: black; font-size:18px; text-align:justify;'>
                <div style='background-color: #d4edda; padding: 1rem; border-radius: 0.5rem;'>
                    Pemberian MPASI tidak hanya untuk membuat bayi kenyang tetapi juga untuk melatih kemampuan mengunyah dan menelan, yang juga penting untuk perkembangan kemampuan berbicara. Tahapan tekstur MPASI sesuai usia bayi adalah:
                    <br><br>1. <b>Bubur Lumat (6 bulan)</b>: Pada tahap awal, bayi memerlukan bubur lumat yang bisa dihaluskan dengan blender atau saringan. Berikan 2-3 sendok makan MPASI ini dua kali sehari.
                    <br><br>2. <b>Bubur Kental dan Dihaluskan (6-9 bulan)</b>: Setelah bayi terbiasa dengan MPASI, tambahkan porsinya hingga tiga kali sehari dengan setengah mangkuk (250 ml). Lanjutkan dengan bubur yang dihaluskan.
                    <br><br>3. <b>Tekstur Agak Kasar (9-12 bulan)</b>: Pada usia ini, bayi mulai dikenalkan dengan makanan bertekstur agak kasar untuk melatih kemampuan makan dan menelan. Berikan makanan cincang halus, cincang kasar, atau finger food 3-4 kali sehari dengan porsi setengah mangkuk (250 ml).
                    <br><br>4. <b>Tekstur Kasar (di atas 12 bulan)</b>: Bayi mulai bisa makan berbagai macam tekstur makanan dan dapat diberikan menu keluarga 3-4 kali sehari. Makanan selingan seperti pancake, roti, puding, telur rebus, atau buah-buahan bisa diberikan 1-2 kali sehari.
                    <br><br>Penting untuk memperhatikan tekstur MPASI sesuai usia bayi untuk mencegah risiko tersedak. Pastikan bahan makanan dan peralatan bersih, dan masak bahan makanan hingga matang. Cuci tangan sebelum menyiapkan dan memberikan makanan pada bayi. Jika ada pertanyaan tentang MPASI, konsultasikan dengan dokter.
                </div>
            </div><br>
        """, unsafe_allow_html=True)

    st.header("Bahan Makanan Sehat untuk MPASI\n", divider="green")
    st.markdown("""
            <div style='color: black; font-size:18px; text-align:justify;'>
                <div style='background-color: #d4edda; padding: 1rem; border-radius: 0.5rem;'>
                    Berbagai makanan segar dan bergizi dapat mendukung tumbuh kembang bayi, di antaranya:
                    <br><br>1. <b>Alpukat 🥑</b>: Kaya <b>asam lemak omega-3</b>, baik untuk perkembangan otak. Bisa dihaluskan dan dicampur dengan ASI atau susu formula.
                    <br><br>2. <b>Ubi 🍠</b>: Mengandung <b>betakaroten</b> atau <b>vitamin A</b>, baik untuk kesehatan mata, kulit, dan mencegah infeksi. Rasanya manis dan disukai bayi.
                    <br><br>3. <b>Pisang 🍌</b>: Mudah diolah menjadi bubur atau dicampur dengan yoghurt dan buah lain. Mengandung <b>vitamin A, C, D, K</b>, serta <b>mineral</b> seperti kalsium dan zat besi.
                    <br><br>4. <b>Buah Berri 🫐</b>: Mengandung <b>antioksidan</b> dan <b>flavonoid</b> yang baik untuk otak, mata, dan saluran kemih. Bisa diolah menjadi bubur dan dicampur dengan yoghurt tawar atau ASI.
                    <br><br>5. <b>Brokoli 🥦</b>: Kaya <b>serat, kalsium, dan folat</b>. Baik untuk pencernaan dan tumbuh kembang anak. Bisa dikukus dan dilumatkan atau dipotong kecil-kecil.
                    <br><br>6. <b>Bubur Beras 🍚</b>: Sumber <b>vitamin B, mangan, dan magnesium</b>. Beras merah atau cokelat juga kaya antioksidan. Lumatkan nasi dengan ASI atau susu formula.
                    <br><br>7. <b>Daging Ayam dan Sapi 🥩</b>: Kaya <b>protein, zat besi, vitamin B</b>, dan <b>seng</b>. Haluskan dan campur dengan ASI atau bubur sayuran agar mudah dikonsumsi bayi.
                    <br><br>8. <b>Ikan 🐟</b>: Kaya <b>protein, mineral, vitamin</b>, dan <b>asam lemak omega-3</b>. Baik untuk perkembangan otak. Pastikan bebas duri dan dimasak matang.
                    <br><br>Makanan seperti ubi, alpukat, dan brokoli bisa diberikan sebagai finger food bagi bayi usia 9 bulan ke atas. Hindari makanan yang berisiko tersedak seperti permen dan anggur. Perkenalkan makanan baru secara bertahap. Jika bayi tidak menyukai makanan baru, coba tawarkan lagi beberapa hari kemudian tanpa memaksa.
                </div>
            </div><br>
        """, unsafe_allow_html=True)

    st.markdown("""
            <div style='color: black; font-size:18px; text-align:justify;'>
                <div style='background-color: #d4edda; padding: 1rem; border-radius: 0.5rem;'>
                    Untuk resep MPASI dengan bahan-bahan lokal, dapat anda akses pada tombol berikut:
                </div>
            </div><br>
        """, unsafe_allow_html=True)

    download_button = st.markdown(
        """
        <a href="https://ayosehat.kemkes.go.id/download/dp/d8a32723535961f3f2a6e44f0f8ba915.pdf" target="_blank">
            <button style="font-size:20px;padding:8px;border-radius:25px;border:none;background-color:#62ea39;color:white;">
                &#x1F4E5; Download
            </button>
        </a><br><br>
        """,
        unsafe_allow_html=True
    )

    st.header("Sumber Terkait: \n", divider="green")
    st.markdown("""
            <div style='color: black;'>
                <div style='background-color: #d4edda; padding: 1rem; border-radius: 0.5rem;'>
                    <a href="https://ayosehat.kemkes.go.id/peran-ibu-cegah-stunting">Peran Ibu Cegah Stunting</a>
                    <br><br><a href="https://www.alodokter.com/ini-daftar-bahan-makanan-sehat-untuk-MPASI-bayi-Bunda">Daftar Bahan Makanan Sehat untuk MPASI Bayi</a>
                    <br><br><a href="https://ayosehat.kemkes.go.id/resep-mpasi-lengkap">Resep MPASI Lengkap</a>
                    <br><br><a href="https://ayosehat.kemkes.go.id/buku-resep-makanan-lokal">Buku Resep Makanan Lokal</a>
                </div>
            </div>
        """, unsafe_allow_html=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)