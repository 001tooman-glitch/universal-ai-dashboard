import streamlit as st

st.set_page_config(
    page_title="Universal AI Dashboard",
    page_icon="📊"
)

st.title("📊 Universal AI Dashboard")

uploaded_files = st.file_uploader(
    "Загрузите один или несколько файлов",
    type=["xlsx", "csv"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(
        f"Загружено файлов: {len(uploaded_files)}"
    )
else:
    st.info(
        "Загрузите Excel или CSV файлы."
    )
