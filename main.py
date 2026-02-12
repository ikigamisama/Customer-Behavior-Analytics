import streamlit as st
import streamlit_shadcn_ui as ui

st.set_page_config(
    page_title="Customer Behavior Analytics Dashboard",
    layout="wide"
)

st.markdown(
    """
    <style>
        div[data-testid="stMetric"] {
            border-left: 0.5rem solid #6366f1 !important;
            box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;
            padding: 0 0 0 2% !important;
            border-radius: 12px !important;
            background-color: transparent !important;
        }
        div[data-testid="stMetric"] label{
            margin-bottom: 5px;
         }

        
    </style>
    """,
    unsafe_allow_html=True
)
st.header("📊 Sales Analysis")
st.caption("Acme Corporation — performance, trends, and revenue insights")
