import streamlit as st

st.set_page_config(
    page_title="Universal AI Dashboard",
    page_icon="📊"
)

st.title("📊 Universal AI Dashboard")

st.success("Приложение работает")

uploaded_file = st.file_uploader(
    "Загрузите файл",
    type=["xlsx", "csv"]
)

if uploaded_file:
    st.write("Файл успешно загружен")
