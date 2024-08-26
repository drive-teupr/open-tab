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
    "URL": ["https://www.google.com", "https://www.github.com", "https://www.linkedin.com"]
}
df = pd.DataFrame(data)

st.title("Buka Beberapa Tab Baru dari DataFrame")

# Tampilkan DataFrame di Streamlit
st.write("Berikut adalah daftar URL yang akan dibuka:")
st.dataframe(df)

if st.button("Buka Semua URL"):
    for url in df['URL']:
        open_page(url)
