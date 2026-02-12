import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st


class Chart:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
