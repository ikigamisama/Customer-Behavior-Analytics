import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

PRIMARY_COLOR = '#7b3785'
SECONDARY_COLOR = '#a855b8'
ACCENT_COLOR = '#d8b4e2'
COLORS_PALETTE = ['#7b3785', '#a855b8', '#d8b4e2', '#6b2d73', '#8e4a94']
GRADIENT_COLORS = ['#4a1f52', '#7b3785', '#a855b8', '#d8b4e2', '#f0e6f5']


class Chart:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)

    def filter_data(self, subscription_status, gender, category, shipping_type, age_group):
        df = self.df.copy()

        if subscription_status is not None:
            df = df[df['subscription_status'] == subscription_status]

        if gender is not None:
            df = df[df['gender'] == gender]

        if category is not None:
            df = df[df['category'] == category]

        if shipping_type is not None:
            df = df[df['shipping_type'] == shipping_type]

        if age_group is not None:
            df = df[df['age_group'] == age_group]

        return df

    def subscription_status(self):
        return ['All'] + self.df['subscription_status'].unique().tolist()

    def gender(self):
        return ['All'] + self.df['gender'].unique().tolist()

    def category(self):
        return ['All'] + self.df['category'].unique().tolist()

    def age_group(self):
        return ['All'] + self.df['age_group'].unique().tolist()

    def shipping_type(self):
        return ['All'] + self.df['shipping_type'].unique().tolist()

    def compute_kpis(self, subscription_status, gender, category, shipping_type, age_group):
        df = self.filter_data(subscription_status, gender,
                              category, shipping_type, age_group)

        total_revenue = df['purchase_amount'].sum().item()
        average_order_value = df['purchase_amount'].mean().item()
        total_customers = df['customer_id'].nunique()
        average_rating = df['review_rating'].mean().item()

        return total_revenue, average_order_value, total_customers, average_rating

    def create_revenue_by_category(self, subscription_status, gender, category, shipping_type, age_group):
        revenue_category = self.filter_data(subscription_status, gender, category, shipping_type, age_group).groupby(
            'category')['purchase_amount'].sum().sort_values(ascending=True)

        fig = go.Figure(go.Bar(
            x=revenue_category.values,
            y=revenue_category.index,
            orientation='h',
            marker=dict(
                color=PRIMARY_COLOR,
                line=dict(color='white', width=1)
            ),
            text=[f'${x:,.0f}' for x in revenue_category.values],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.2f}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': 'Revenue by Category',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title='Total Revenue ($)',
            yaxis_title='Category',
            font=dict(size=12),
            height=400,
            margin=dict(l=100, r=40, t=80, b=60)
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        return fig

    def create_revenue_by_season(self, subscription_status, gender, category, shipping_type, age_group):
        revenue_season = self.filter_data(subscription_status, gender, category, shipping_type, age_group).groupby(
            'season')['purchase_amount'].sum().sort_values(ascending=True)

        fig = go.Figure(go.Pie(
            labels=revenue_season.index,
            values=revenue_season.values,
            hole=0.4,
            marker=dict(colors=COLORS_PALETTE),
            textinfo='label+percent',
            textposition='auto',
            hovertemplate='<b>%{label}</b><br>Revenue: $%{value:,.2f}<br>Percentage: %{percent}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': 'Revenue by Season',
                'x': 0.5,
                'xanchor': 'center',
                'y': 0.95,
                'yanchor': 'top',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            font=dict(size=12),
            height=450,
            legend=dict(
                orientation="h",
                x=0.5,
                xanchor="center",
                y=1.20,
                yanchor="top"
            ),
            margin=dict(
                t=125
            )
        )

        return fig

    def create_purchase_amount_distribution(self, subscription_status, gender, category, shipping_type, age_group):
        mean_amount = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group)['purchase_amount'].mean()
        median_amount = self.filter_data(subscription_status, gender, category, shipping_type, age_group)[
            'purchase_amount'].median()

        fig = go.Figure()

        fig.add_trace(go.Histogram(
            x=self.filter_data(
                subscription_status, gender, category, shipping_type, age_group)['purchase_amount'],
            nbinsx=20,
            name='Distribution',
            marker=dict(
                color=PRIMARY_COLOR,
                line=dict(color='white', width=1)
            ),
            opacity=0.75,
            hovertemplate='Amount: $%{x:.2f}<br>Count: %{y}<extra></extra>'
        ))

        fig.add_vline(x=mean_amount, line_dash="dash", line_color="#e74c3c", line_width=2,
                      annotation_text=f"Mean: ${mean_amount:.2f}", annotation_position="top right")
        fig.add_vline(x=median_amount, line_dash="dot", line_color="#27ae60", line_width=2,
                      annotation_text=f"Median: ${median_amount:.2f}", annotation_position="bottom right")

        fig.update_layout(
            title={
                'text': 'Purchase Amount Distribution',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title='Purchase Amount ($)',
            yaxis_title='Number of Purchases',
            font=dict(size=12),
            height=450,
            showlegend=False,
            hovermode='x unified'
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        return fig

    def create_customer_by_age_group(self, subscription_status, gender, category, shipping_type, age_group):
        age_distribution = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group)['age_group'].value_counts().reindex(['Young Adult', 'Adult', 'Middle-aged', 'Senior'])

        fig = go.Figure(go.Bar(
            x=age_distribution.index,
            y=age_distribution.values,
            marker=dict(
                color=COLORS_PALETTE,
                line=dict(color='white', width=1)
            ),
            text=age_distribution.values,
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': 'Customer Distribution by Age Group',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title='Age Group',
            yaxis_title='Number of Customers',
            font=dict(size=12),
            height=450
        )

        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        return fig
