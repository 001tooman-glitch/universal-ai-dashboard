import streamlit as st
import pandas as pd

from utils.profiler import build_profile
from utils.domain_detector import detect_domain
from utils.scenario_detector import detect_scenario
from utils.time_series import combine_tables
from utils.semantic_analyzer import analyze_semantics
from utils.semantic_report import build_semantic_report
from utils.kpi_detector import detect_kpis
from utils.kpi_report import build_kpi_report
from utils.analysis_recommender import recommend_analyses
from utils.insight_generator import generate_insights
from utils.business_rules import evaluate_business_rules

st.set_page_config(
    page_title="Universal AI Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Universal AI Dashboard")

uploaded_files = st.file_uploader(
    "Загрузите один или несколько файлов",
    type=["xlsx", "csv"],
