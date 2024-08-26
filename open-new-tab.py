import pandas as pd
import streamlit as st
import numpy as np
from streamlit.components.v1 import html

def copyDataframe(lalu, akhir, blth_lalu, blth_kini):
    # Create juruslalu DataFrame
    juruslalu = pd.DataFrame()
    juruslalu['IDPEL'] = lalu['IDPEL']
    juruslalu['PEMKWH'] = lalu['PEMKWH']
    juruslalu['DLPD'] = lalu['DLPD']
    juruslalu['LWBP_LALU'] = lalu['SLALWBP']
    juruslalu['LWBP_CABUT'] = lalu['SAHLWBP_CABUT']
    juruslalu['LWBP_PASANG'] = lalu['SLALWBP_PASANG']
    juruslalu['LWBP_AKHIR'] = lalu['SAHLWBP']
    juruslalu['WBP_LALU'] = lalu['SLAWBP']
    juruslalu['WBP_CABUT'] = lalu['SAHWBP_CABUT']
    juruslalu['WBP_PASANG'] = lalu['SLAWBP_PASANG']
    juruslalu['WBP_AKHIR'] = lalu['SAHWBP']
    juruslalu['FAKM'] = lalu['FAKM']
    juruslalu['PEMKWH_REAL'] = (((juruslalu['LWBP_AKHIR']-juruslalu['LWBP_PASANG'])
                                +(juruslalu['LWBP_CABUT']-juruslalu['LWBP_LALU']))
                                +((juruslalu['WBP_AKHIR']-juruslalu['WBP_PASANG'])
                                +(juruslalu['WBP_CABUT']-juruslalu['WBP_LALU']))
                                )

    # Create jurusakhir DataFrame
    jurusakhir = pd.DataFrame()
    jurusakhir['IDPEL'] = akhir['IDPEL']
    jurusakhir['NAMA'] = akhir['NAMA']
    jurusakhir['PEMKWH'] = akhir['PEMKWH']
    jurusakhir['TARIF'] = akhir['TARIF']
    jurusakhir['DAYA'] = akhir['DAYA']
    jurusakhir['DLPD'] = akhir['DLPD']
    jurusakhir['LWBP_LALU'] = akhir['SLALWBP']
    jurusakhir['LWBP_CABUT'] = akhir['SAHLWBP_CABUT']
    jurusakhir['LWBP_PASANG'] = akhir['SLALWBP_PASANG']
    jurusakhir['LWBP_AKHIR'] = akhir['SAHLWBP']
    jurusakhir['WBP_LALU'] = akhir['SLAWBP']
    jurusakhir['WBP_CABUT'] = akhir['SAHWBP_CABUT']
    jurusakhir['WBP_PASANG'] = akhir['SLAWBP_PASANG']
    jurusakhir['WBP_AKHIR'] = akhir['SAHWBP']
    jurusakhir['JAM_NYALA'] = akhir['JAMNYALA']
    jurusakhir['FAKM'] = akhir['FAKM']
    jurusakhir['PEMKWH_REAL'] = (((jurusakhir['LWBP_AKHIR']-jurusakhir['LWBP_PASANG'])
                                +(jurusakhir['LWBP_CABUT']-jurusakhir['LWBP_LALU']))
                                +((jurusakhir['WBP_AKHIR']-jurusakhir['WBP_PASANG'])
                                +(jurusakhir['WBP_CABUT']-jurusakhir['WBP_LALU']))
                                )

    # Merge DataFrames
    kroscek_temp = pd.merge(juruslalu, jurusakhir, on='IDPEL', how='right')

    # Create kroscek DataFrame
    kroscek = pd.DataFrame()
    kroscek['IDPEL'] = kroscek_temp['IDPEL'].astype(str)
    kroscek['NAMA'] = kroscek_temp['NAMA']

    path_foto1 = 'https://portalapp.iconpln.co.id/acmt/DisplayBlobServlet1?idpel='
    path_foto2 = '&blth='

    kroscek['LWBP_LALU'] = kroscek_temp['LWBP_LALU_y']
    kroscek['FOTO_LALU'] = path_foto1 + kroscek['IDPEL'] + path_foto2 + blth_lalu + '&unitup=32510'

    kroscek['LWBP_AKHIR'] = kroscek_temp['LWBP_AKHIR_y']
    kroscek['FOTO_AKHIR'] = path_foto1 + kroscek['IDPEL'] + path_foto2 + blth_kini + '&unitup=32510'

    kroscek['WBP_LALU'] = kroscek_temp['WBP_LALU_y']
    kroscek['WBP_AKHIR'] = kroscek_temp['WBP_AKHIR_y']
    kroscek['PAKAI_LALU'] = kroscek_temp['PEMKWH_REAL_x']
    kroscek['PAKAI_AKHIR'] = kroscek_temp['PEMKWH_REAL_y']
    kroscek['SELISIH'] = kroscek_temp['PEMKWH_REAL_y'] - kroscek_temp['PEMKWH_REAL_x']
    kroscek['SELISIH %'] = (kroscek['SELISIH'] / kroscek_temp['PEMKWH_REAL_x']) * 100
    kroscek['DLPD_LALU'] = kroscek_temp['DLPD_x']
    kroscek['DLPD_KINI'] = kroscek_temp['DLPD_y']
    kroscek['TARIF'] = kroscek_temp['TARIF']
    kroscek['DAYA'] = kroscek_temp['DAYA']
    kroscek['JAM_NYALA'] = kroscek_temp['JAM_NYALA']

    conditions_50 = [(kroscek['SELISIH %'] > 50) | (kroscek['SELISIH %'] < -50),
                     (kroscek['SELISIH %'] < 50) | (kroscek['SELISIH %'] > -50)]

    conditions_100 = [(kroscek['SELISIH %'] > 100) | (kroscek['SELISIH %'] < -100),
                      (kroscek['SELISIH %'] < 100) | (kroscek['SELISIH %'] > -100)]

    letters = ['Selisih Besar', 'Normal']

    kroscek['SELISIH 50%'] = np.select(conditions_50, letters, default='Undefined')
    kroscek['SELISIH 100%'] = np.select(conditions_100, letters, default='Undefined')

    conditions_sub = [(kroscek['DAYA'] == 450) | (kroscek['DAYA'] == 900),
                      (kroscek['DAYA'] > 900)]

    letters_sub = ['Subs', 'Nonsubs']

    kroscek['SUBS_NONSUBS'] = np.select(conditions_sub, letters_sub, default='Undefined')

    conditions_minnol = [(kroscek['DLPD_LALU'] == 'K KWH NOL') | (kroscek['DLPD_LALU'] == 'C KWH < 40 JAM'),
                         (kroscek['DLPD_LALU'] == 'N KWH N O R M A L') | (kroscek['DLPD_LALU'] == 'J REKENING PECAHAN')]

    letters_minnol = ['Yes', 'No']

    kroscek['MIN_NOL'] = np.select(conditions_minnol, letters_minnol, default='Undefined')

    return kroscek

def maksFilter(lalu, akhir, blth_lalu, blth_kini):
    kroscek = copyDataframe(lalu, akhir, blth_lalu, blth_kini)
    maks_df = kroscek[kroscek['DLPD_KINI'].isin(['L STAND METER MUNDUR'])]
    return maks_df

def norm1Filter(lalu, akhir, blth_lalu, blth_kini):
    kroscek = copyDataframe(lalu, akhir, blth_lalu, blth_kini)

    temp = kroscek[kroscek['DLPD_KINI'].isin(['N KWH N O R M A L']) &
                   (kroscek['SELISIH 100%'] == 'Selisih Besar') &
                   (kroscek['SUBS_NONSUBS'] == 'Subs')]

    norm1_df = pd.DataFrame(temp[['IDPEL', 'SELISIH', 'SELISIH %', 'SUBS_NONSUBS', 'FOTO_LALU', 'FOTO_AKHIR']])
    return norm1_df

def upload():
    st.title("Upload Excel File")
    uploaded_file = st.file_uploader("Choose an Excel file")
    if uploaded_file is not None:
        data = pd.read_excel(uploaded_file)
        st.write("File uploaded successfully!")
        return data
    else:
        return None

def open_page(url):
    st.write(f'<a href="{url}" target="_blank">Open URL</a>', unsafe_allow_html=True)

data_lalu = None
data_akhir = None

tabs = st.tabs(["Upload Files", "Display Data", "Filter Data"])

with tabs[0]:
    st.write("Upload two Excel files.")
    data_lalu = upload()
    data_akhir = upload()

with tabs[1]:
    if data_lalu is not None and data_akhir is not None:
        st.write("First 5 rows of Data Lalu")
        st.dataframe(data_lalu.head())
        st.write("First 5 rows of Data Akhir")
        st.dataframe(data_akhir.head())

with tabs[2]:
    blth_lalu = st.text_input("Enter blth lalu:")
    blth_kini = st.text_input("Enter blth kini:")

    if st.button("Filter Maks Data"):
        filtered_maks = maksFilter(data_lalu, data_akhir, blth_lalu, blth_kini)
        st.dataframe(filtered_maks)

    if st.button("Filter Norm1 Data"):
        filtered_norm1 = norm1Filter(data_lalu, data_akhir, blth_lalu, blth_kini)
        st.dataframe(filtered_norm1)

    if st.button("Buka Semua URL"):
        if data_lalu is not None and data_akhir is not None:
            df_filtered_norm1 = norm1Filter(data_lalu, data_akhir, blth_lalu, blth_kini)
            urls = df_filtered_norm1['FOTO_AKHIR'].tolist()
            for url in urls:
                open_page(url)

