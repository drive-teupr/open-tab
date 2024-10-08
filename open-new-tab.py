import streamlit as st
from streamlit.components.v1 import html
import pandas as pd

def open_page(url):
    open_script = """
        <script type="text/javascript">
            window.open('%s', '_blank').focus();
        </script>
    """ % (url)
    html(open_script)

# Contoh DataFrame dengan kolom 'URL'
data = {
    "Nama Situs": ["Google", "GitHub", "LinkedIn"],
    "URL": ["https://portalapp.iconpln.co.id/acmt/DisplayBlobServlet1?idpel=325100092874&blth=202407&unitup=32510", 
            "https://portalapp.iconpln.co.id/acmt/DisplayBlobServlet1?idpel=325100204640&blth=202407&unitup=32510", 
            "https://portalapp.iconpln.co.id/acmt/DisplayBlobServlet1?idpel=325100086032&blth=202407&unitup=32510"]
}
df = pd.DataFrame(data)

st.title("Buka Beberapa Tab Baru dari DataFrame")

# Tampilkan DataFrame di Streamlit
st.write("Berikut adalah daftar URL yang akan dibuka:")
if st.button("Buka"):
    st.dataframe(df)

    if st.button("Buka Semua URL"):
        for url in df['URL']:
            open_page(url)
