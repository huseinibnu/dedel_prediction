import streamlit as st
import joblib
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
import zipfile
import os

st.set_page_config(
    page_title="DEDEL",
    page_icon=":bar_chart:",
    layout="wide"
)

# Sidebar Menu
# with st.sidebar:
#     selected = option_menu(
#         menu_title="Main Menu",
#         options=["Overview", "Prediction", "About Us"],
#         icons=["bar-chart-line", "question-circle", "file-person"],
#         menu_icon="cast",
#         default_index=1,
#     )

# Horizontal Menu
selected = option_menu(
    menu_title=None,
    options=["Overview", "Prediction", "About Us"],
    icons=["bar-chart-line", "question-circle", "file-person"],
    menu_icon="cast",
    default_index=1,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#000"},
        "icon": {"color": "#62ea39", "font-size": "22px"},
        "nav-link": {"color": "#7e8299", "font-size": "22px", "text-align": "center", "margin":"0px", "--hover-color": "#62ea39"},
        "nav-link-selected": {"color": "#62ea39", "background-color": "#f4f6fa"},
    }
)

if selected == "Overview":
    # st.title(f"You have selected {selected}")

    # Read Excel
    @st.cache_data
    def get_data():
        df = pd.read_csv("data_balita.csv")
        return df


    df = get_data()

    # ---- SIDEBAR ----
    st.sidebar.header("Please Filter Here:")
    stunting = st.sidebar.multiselect(
        "Status Gizi:",
        options=df["Status Gizi"].unique(),
        default=df["Status Gizi"].unique()
    )

    df_selection = df[df["Status Gizi"].isin(stunting)]

    # Check if the dataframe is empty:
    if df_selection.empty:
        st.warning("No data available based on the current filter settings!")
        st.stop()  # This will halt the app from further execution.

    st.title(":bar_chart: Child Growth Dashboard")

    # Top KPI
    total_children = df_selection["Umur (bulan)"].count()  # No need for int() conversion here
    average_height = round(df_selection["Tinggi Badan (cm)"].mean(), 1)
    average_age = round(df_selection["Umur (bulan)"].mean(), 1)

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
    gender_counts = df_selection["Jenis Kelamin"].value_counts().reset_index()
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
    )

    # Compute the count of each nutritional status
    status_gizi_counts = df_selection["Status Gizi"].value_counts().reset_index()
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
    )

    st.markdown("")
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_gender_distribution, use_container_width=True)
    right_column.plotly_chart(fig_status_gizi_distribution, use_container_width=True)

if selected == "Prediction":
    # st.title(f"You have selected {selected}")
    # Ekstrak file model dari ZIP
    with zipfile.ZipFile('model_stunting.zip', 'r') as zipf:
        zipf.extract('model_stunting.joblib')
    
    # Load model
    stunting_model = joblib.load('model_stunting.joblib')

    st.title('Aplikasi Prediksi Status Gizi')

    # Input data
    tinggi = st.text_input('Masukkan panjang badan anak anda (cm) : ')
    umur = st.text_input('Masukkan umur anak anda (bulan) : ')
    jenis_kelamin = st.selectbox('Jenis Kelamin', ['laki-laki', 'perempuan'])

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
            diab_diagnosis = "Severely Stunted"
        elif diab_prediction[0] == 1:
            diab_diagnosis = "Stunted"
        elif diab_prediction[0] == 2:
            diab_diagnosis = "Normal"
        else:
            diab_diagnosis = "Tinggi"

        # Tampilkan hasil prediksi
        st.success(diab_diagnosis)
        
if selected == "About Us":
    st.title(f"You have selected {selected}")

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

