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

# Horizontal Menu
with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Pengenalan", "Prediksi", "Panduan MPASI"],
        icons=["bar-chart-line", "question-circle", "journal-text"],
        menu_icon="cast",
        default_index=1,
        styles={
            "container": {"padding": "0!important", "background-color": "#62ea39"},
            "icon": {"color": "#000", "font-size": "22px"},
            "nav-link": {"color": "#000", "font-size": "22px", "text-align": "left", "margin": "0px",
                         "--hover-color": "#62ea39"},
            "nav-link-selected": {"color": "#62ea39", "background-color": "#f4f6fa"},
        }
    )

if selected == "Pengenalan":
    if st.button("🔙 Back"):
        import webbrowser
        webbrowser.open("https://dedel.pubhe.com/public/dashboard")
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
    if st.button("🔙 Back"):
        import webbrowser
        webbrowser.open("https://dedel.pubhe.com/public/dashboard")

    # Ekstrak file model dari ZIP
    with zipfile.ZipFile('model_stunting.zip', 'r') as zipf:
        zipf.extract('model_stunting.joblib')

    # Load model
    stunting_model = joblib.load('model_stunting.joblib')

    st.title('Aplikasi Prediksi Status Gizi❓')

    tinggi = st.text_input('**Masukkan panjang badan anak anda (cm) :**')
    umur = st.text_input('**Masukkan umur anak anda (bulan) :**')
    jenis_kelamin = st.selectbox('**Jenis Kelamin**', ['laki-laki', 'perempuan'])

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
            diab_diagnosis = ("Berdasarkan data yang Anda masukkan, anak Anda tergolong **Severely Stunted (Sangat Pendek)**. Kami memahami bahwa sebagai orang tua, Anda pasti telah melakukan yang terbaik. Untuk langkah selanjutnya, berikut saran kami: "
                              "\n1. **Konsultasi**: Silakan berkonsultasi dengan kader posyandu atau tenaga kesehatan untuk mendapatkan bantuan lebih lanjut. "
                              "\n2. **MPASI**: Jika anak sudah bisa mengonsumsi MPASI, kunjungi bagian 'Panduan MPASI' di sebelah kiri untuk panduan makanan tambahan yang bergizi. "
                              "\n\nKami berharap, dengan langkah-langkah ini, tinggi badan anak Anda dapat mencapai kategori normal di waktu yang akan datang.")
        elif diab_prediction[0] == 1:
            diab_diagnosis = ("Berdasarkan data yang Anda masukkan, anak Anda tergolong **Stunted (Pendek)**. Kami memahami bahwa sebagai orang tua, Anda pasti telah melakukan yang terbaik. Untuk langkah selanjutnya, berikut saran kami: "
                              "\n1. **Konsultasi**: Silakan berkonsultasi dengan kader posyandu atau tenaga kesehatan untuk mendapatkan bantuan lebih lanjut. "
                              "\n2. **MPASI**: Jika anak sudah bisa mengonsumsi MPASI, kunjungi bagian 'Panduan MPASI' di sebelah kiri untuk panduan makanan tambahan yang bergizi. "
                              "\n\nKami berharap, dengan langkah-langkah ini, tinggi badan anak Anda dapat mencapai kategori normal di waktu yang akan datang.")
        elif diab_prediction[0] == 2:
            diab_diagnosis = ("**Selamat!** Berdasarkan data yang Anda masukkan, anak Anda tergolong **Normal**. Tetaplah memberikan yang terbaik untuk pertumbuhan dan perkembangan anak Anda."
                              "\n\nJika Anda memerlukan panduan tentang **MPASI**, silakan kunjungi bagian 'Panduan MPASI' di sebelah kiri. Kami berharap tinggi badan anak Anda dapat terus meningkat di bulan yang akan datang.")
        else:
            diab_diagnosis = ("**Selamat!** Berdasarkan data yang Anda masukkan, anak Anda tergolong **Tinggi**. Ini menunjukkan bahwa pertumbuhan anak Anda sangat baik."
                              "\n\nTetaplah memberikan yang terbaik untuk pertumbuhan dan perkembangan anak Anda. Pastikan anak mendapatkan pola makan yang seimbang dan cukup aktivitas fisik untuk menjaga kesehatannya."
                              "\n\nJika Anda memerlukan panduan tentang **MPASI** atau tips lainnya, silakan kunjungi bagian 'Panduan MPASI' di sebelah kiri.")

        # Tampilkan hasil prediksi
        st.success(diab_diagnosis)


if selected == "Panduan MPASI":
    st.title("Panduan MPASI 📖")
    st.success("Peran ibu sangat penting dalam mencegah **stunting** sejak kehamilan dengan memberikan stimulasi yang tepat selama **masa emas (0-3 tahun)**. **Stunting** ditandai dengan pertumbuhan yang tidak sesuai standar **WHO**. Selain ibu, dukungan keluarga dan masyarakat juga diperlukan untuk mengurangi risiko **stunting** dan mewujudkan Generasi Emas 2045. Berikut informasi terkait **MPASI**.")

    st.header("Tahapan Tekstur MPASI\n", divider="green")
    st.success("Pemberian MPASI tidak hanya untuk membuat bayi kenyang tetapi juga untuk melatih kemampuan mengunyah dan menelan, yang juga penting untuk perkembangan kemampuan berbicara. Tahapan tekstur MPASI sesuai usia bayi adalah: "
             "\n\n1. **Bubur Lumat (6 bulan)**:"
             "ada tahap awal, bayi memerlukan bubur lumat yang bisa dihaluskan dengan blender atau saringan. Berikan 2-3 sendok makan MPASI ini dua kali sehari."
             "\n\n2. **Bubur Kental dan Dihaluskan (6-9 bulan)**:"
             "Setelah bayi terbiasa dengan MPASI, tambahkan porsinya hingga tiga kali sehari dengan setengah mangkuk (250 ml). Lanjutkan dengan bubur yang dihaluskan."
             "\n\n3. **Tekstur Agak Kasar (9-12 bulan)**:"
             "Pada usia ini, bayi mulai dikenalkan dengan makanan bertekstur agak kasar untuk melatih kemampuan makan dan menelan. Berikan makanan cincang halus, cincang kasar, atau finger food 3-4 kali sehari dengan porsi setengah mangkuk (250 ml)."
             "\n\n4. **Tekstur Kasar (di atas 12 bulan)**:"
             "Bayi mulai bisa makan berbagai macam tekstur makanan dan dapat diberikan menu keluarga 3-4 kali sehari. Makanan selingan seperti pancake, roti, puding, telur rebus, atau buah-buahan bisa diberikan 1-2 kali sehari."
             "\n\nPenting untuk memperhatikan tekstur MPASI sesuai usia bayi untuk mencegah risiko tersedak. Pastikan bahan makanan dan peralatan bersih, dan masak bahan makanan hingga matang. Cuci tangan sebelum menyiapkan dan memberikan makanan pada bayi. Jika ada pertanyaan tentang MPASI, konsultasikan dengan dokter.")

    st.header("Bahan Makanan Sehat untuk MPASI\n", divider="green")
    st.success("Berbagai makanan segar dan bergizi dapat mendukung tumbuh kembang bayi, di antaranya:"
               "\n\n1. **Alpukat** 🥑: Kaya **asam lemak omega-3**, baik untuk perkembangan otak. Bisa dihaluskan dan dicampur dengan ASI atau susu formula."
               "\n\n2. **Ubi** 🍠: Mengandung **betakaroten** atau **vitamin A**, baik untuk kesehatan mata, kulit, dan mencegah infeksi. Rasanya manis dan disukai bayi."
               "\n\n3. **Pisang** 🍌: Mudah diolah menjadi bubur atau dicampur dengan yoghurt dan buah lain. Mengandung **vitamin A, C, D, K**, serta **mineral** seperti kalsium dan zat besi."
               "\n\n4. **Buah Berri** 🫐: Mengandung **antioksidan** dan **flavonoid** yang baik untuk otak, mata, dan saluran kemih. Bisa diolah menjadi bubur dan dicampur dengan yoghurt tawar atau ASI."
               "\n\n5. **Brokoli** 🥦: Kaya **serat, kalsium, dan folat**. Baik untuk pencernaan dan tumbuh kembang anak. Bisa dikukus dan dilumatkan atau dipotong kecil-kecil."
               "\n\n6. **Bubur Beras** 🍚: Sumber **vitamin B, mangan, dan magnesium**. Beras merah atau cokelat juga kaya antioksidan. Lumatkan nasi dengan ASI atau susu formula."
               "\n\n7. **Daging Ayam dan Sapi** 🥩: Kaya **protein, zat besi, vitamin B**, dan **seng**. Haluskan dan campur dengan ASI atau bubur sayuran agar mudah dikonsumsi bayi."
               "\n\n8. **Ikan** 🐟: Kaya **protein, mineral, vitamin**, dan **asam lemak omega-3**. Baik untuk perkembangan otak. Pastikan bebas duri dan dimasak matang."
               "\n\nMakanan seperti ubi, alpukat, dan brokoli bisa diberikan sebagai finger food bagi bayi usia 9 bulan ke atas. Hindari makanan yang berisiko tersedak seperti permen dan anggur. Perkenalkan makanan baru secara bertahap. Jika bayi tidak menyukai makanan baru, coba tawarkan lagi beberapa hari kemudian tanpa memaksa.")
    st.success("\nUntuk resep MPASI dengan bahan-bahan lokal, dapat anda akses pada tombol berikut : ")

    download_button = st.markdown(
        """
        <a href="https://ayosehat.kemkes.go.id/download/dp/d8a32723535961f3f2a6e44f0f8ba915.pdf" target="_blank">
            <button style="font-size:20px;padding:8px;border-radius:3px;border:none;background-color:#62ea39;color:white;">
                &#x1F4E5; Download
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

    st.header("Sumber Terkait: \n", divider="green")
    st.success("https://ayosehat.kemkes.go.id/peran-ibu-cegah-stunting"
               "\n\nhttps://www.alodokter.com/ini-daftar-bahan-makanan-sehat-untuk-MPASI-bayi-Bunda"
               "\n\nhttps://ayosehat.kemkes.go.id/resep-mpasi-lengkap"
               "\n\nhttps://ayosehat.kemkes.go.id/buku-resep-makanan-lokal")

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)