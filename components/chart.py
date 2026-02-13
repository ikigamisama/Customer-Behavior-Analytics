import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from plotly.subplots import make_subplots

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
                line=dict(color='white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748", width=1)
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

    def create_gender_distribution(self, subscription_status, gender, category, shipping_type, age_group):
        gender_count = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group)['gender'].value_counts()

        fig = go.Figure(go.Pie(
            labels=gender_count.index,
            values=gender_count.values,
            marker=dict(colors=[PRIMARY_COLOR, SECONDARY_COLOR]),
            textinfo='label+percent+value',
            textposition='auto',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': 'Gender Distribution',
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

    def create_customer_count_age_group(self, subscription_status, gender, category, shipping_type, age_group):
        age_counts = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group)['age_group'].value_counts().reindex(['Young Adult', 'Adult', 'Middle-aged', 'Senior'])

        fig = go.Figure(go.Bar(
            x=age_counts.index,
            y=age_counts.values,
            marker=dict(
                color=[PRIMARY_COLOR, SECONDARY_COLOR,
                       ACCENT_COLOR, '#6b2d73'],
                line=dict(color='white', width=1)
            ),
            text=age_counts.values,
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Customers: %{y}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': 'Customer Count by Age Group',
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

    def create_purchase_by_age_boxplot(self, subscription_status, gender, category, shipping_type, age_group):
        age_order = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']

        fig = go.Figure()

        for i, age_group in enumerate(age_order):
            data = self.filter_data(
                subscription_status, gender, category, shipping_type, age_group)[self.filter_data(
                    subscription_status, gender, category, shipping_type, age_group)['age_group'] == age_group]['purchase_amount']
            fig.add_trace(go.Box(
                y=data,
                name=age_group,
                marker=dict(color=COLORS_PALETTE[i]),
                boxmean='sd',
                hovertemplate='<b>%{fullData.name}</b><br>Value: $%{y:.2f}<extra></extra>'
            ))

        fig.update_layout(
            title={
                'text': 'Purchase Amount by Age Group',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            yaxis_title='Purchase Amount ($)',
            xaxis_title='Age Group',
            font=dict(size=12),
            height=500,
            showlegend=False
        )

        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        return fig

    def create_previous_purchases_distribution(self, subscription_status, gender, category, shipping_type, age_group):
        fig = go.Figure(go.Histogram(
            x=self.filter_data(
                subscription_status, gender, category, shipping_type, age_group)['previous_purchases'],
            nbinsx=15,
            marker=dict(
                color=PRIMARY_COLOR,
                line=dict(color='white', width=1)
            ),
            opacity=0.75,
            hovertemplate='Previous Purchases: %{x}<br>Count: %{y}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': 'Previous Purchases Distribution',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title='Number of Previous Purchases',
            yaxis_title='Number of Customers',
            font=dict(size=12),
            height=450
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        return fig

    def create_review_rating_distribution(self, subscription_status, gender, category, shipping_type, age_group):
        rating_counts = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group)['review_rating'].value_counts().sort_index()

        colors = ['#e74c3c' if x < 3 else '#f39c12' if x <
                  4 else '#27ae60' for x in rating_counts.index]

        fig = go.Figure(go.Bar(
            x=rating_counts.index,
            y=rating_counts.values,
            marker=dict(
                color=colors,
                line=dict(color='white', width=1)
            ),
            text=rating_counts.values,
            textposition='outside',
            hovertemplate='Rating: %{x}<br>Count: %{y}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': 'Review Rating Distribution',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title='Rating',
            yaxis_title='Number of Reviews',
            font=dict(size=12),
            height=450
        )

        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        return fig

    def create_top_10_items(self, subscription_status, gender, category, shipping_type, age_group):
        top_items = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group)['item_purchased'].value_counts().head(10).sort_values(ascending=True)

        fig = go.Figure(go.Bar(
            x=top_items.values,
            y=top_items.index,
            orientation='h',
            marker=dict(
                color=PRIMARY_COLOR,
                line=dict(color='white', width=1)
            ),
            text=top_items.values,
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': 'Top 10 Items Purchased',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title='Number of Purchases',
            yaxis_title='Item',
            font=dict(size=12),
            height=450,
            margin=dict(l=120, r=40, t=80, b=60)
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        return fig

    def create_category_treemap(self, subscription_status, gender, category, shipping_type, age_group):
        category_item_counts = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group).groupby(['category', 'item_purchased']).size().reset_index(name='count')

        fig = px.treemap(
            category_item_counts,
            path=['category', 'item_purchased'],
            values='count',
            title='Category Breakdown',
            color='count',
            color_continuous_scale=['#f0e6f5',
                                    '#d8b4e2', '#a855b8', '#7b3785', '#4a1f52']
        )

        fig.update_layout(
            title={
                'text': 'Category Breakdown',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            font=dict(size=12),
            height=500
        )

        return fig

    def create_avg_rating_by_category(self, subscription_status, gender, category, shipping_type, age_group):
        avg_rating = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group).groupby('category')['review_rating'].mean().sort_values(ascending=False)
        overall_avg = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group)['review_rating'].mean()

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=avg_rating.index,
            y=avg_rating.values,
            marker=dict(
                color=PRIMARY_COLOR,
                line=dict(color='white', width=1)
            ),
            text=[f'{x:.2f}⭐' for x in avg_rating.values],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Avg Rating: %{y:.2f}⭐<extra></extra>'
        ))

        fig.add_hline(y=overall_avg, line_dash="dash", line_color="#e74c3c",
                      annotation_text=f"Overall Avg: {overall_avg:.2f}⭐", annotation_position="right")

        fig.update_layout(
            title={
                'text': 'Average Rating by Category',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title='Category',
            yaxis_title='Average Rating',
            font=dict(size=12),
            height=450,
            yaxis=dict(range=[0, 5])
        )

        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        return fig

    def create_category_by_season(self, subscription_status, gender, category, shipping_type, age_group):
        season_category = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group).groupby(['season', 'category']).size().reset_index(name='count')

        fig = px.bar(
            season_category,
            x='season',
            y='count',
            color='category',
            title='Product Category by Season',
            barmode='stack',
            color_discrete_sequence=COLORS_PALETTE,
            category_orders={'season': ['Spring', 'Summer', 'Fall', 'Winter']}
        )

        fig.update_layout(
            title={
                'text': 'Product Category by Season',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title='Season',
            yaxis_title='Number of Purchases',
            font=dict(size=12),
            height=450,
            legend_title='Category'
        )

        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        return fig

    def create_size_distribution(self, subscription_status, gender, category, shipping_type, age_group):
        size_counts = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group)['size'].value_counts()

        fig = go.Figure(go.Pie(
            labels=size_counts.index,
            values=size_counts.values,
            marker=dict(colors=COLORS_PALETTE),
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': 'Size Distribution',
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

    def create_top_colors(self, subscription_status, gender, category, shipping_type, age_group):
        top_colors = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group)['color'].value_counts().head(10).sort_values(ascending=True)

        fig = go.Figure(go.Bar(
            x=top_colors.values,
            y=top_colors.index,
            orientation='h',
            marker=dict(
                color=PRIMARY_COLOR,
                line=dict(color='white', width=1)
            ),
            text=top_colors.values,
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': 'Top 10 Colors Purchased',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title='Number of Purchases',
            yaxis_title='Color',
            font=dict(size=12),
            height=450,
            margin=dict(l=100, r=40, t=80, b=60)
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        return fig

    def create_purchase_frequency(self, subscription_status, gender, category, shipping_type, age_group):
        freq_order = ['Weekly', 'Bi-Weekly', 'Fortnightly',
                      'Monthly', 'Quarterly', 'Every 3 Months', 'Annually']
        freq_counts = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group)['frequency_of_purchases'].value_counts().reindex(freq_order, fill_value=0)

        fig = go.Figure(go.Bar(
            x=freq_counts.index,
            y=freq_counts.values,
            marker=dict(
                color=PRIMARY_COLOR,
                line=dict(color='white', width=1)
            ),
            text=freq_counts.values,
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': 'Purchase Frequency Distribution',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title='Frequency',
            yaxis_title='Number of Customers',
            font=dict(size=12),
            height=450,
            xaxis_tickangle=-45
        )

        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        return fig

    def create_payment_methods(self, subscription_status, gender, category, shipping_type, age_group):
        payment_counts = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group)['payment_method'].value_counts().sort_values(ascending=True)

        fig = go.Figure(go.Bar(
            x=payment_counts.values,
            y=payment_counts.index,
            orientation='h',
            marker=dict(
                color=PRIMARY_COLOR,
                line=dict(color='white', width=1)
            ),
            text=payment_counts.values,
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': 'Payment Method Preferences',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title='Number of Transactions',
            yaxis_title='Payment Method',
            font=dict(size=12),
            height=450,
            margin=dict(l=120, r=40, t=80, b=60)
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        return fig

    def create_subscription_comparison(self, subscription_status, gender, category, shipping_type, age_group):
        subscription_data = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group).groupby(['subscription_status', 'category']).size().reset_index(name='count')

        fig = px.bar(
            subscription_data,
            x='category',
            y='count',
            color='subscription_status',
            title='Subscription Status by Category',
            barmode='group',
            color_discrete_map={'Yes': PRIMARY_COLOR, 'No': SECONDARY_COLOR}
        )

        fig.update_layout(
            title={
                'text': 'Subscription vs Non-Subscription by Category',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title='Category',
            yaxis_title='Number of Customers',
            font=dict(size=12),
            height=450,
            legend_title='Subscription'
        )

        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        return fig

    def create_discount_impact(self, subscription_status, gender, category, shipping_type, age_group):
        discount_data = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group).groupby('discount_applied')['purchase_amount'].agg(['mean', 'count']).reset_index()

        fig = go.Figure()

        for discount in discount_data['discount_applied']:
            data = self.filter_data(
                subscription_status, gender, category, shipping_type, age_group)[self.filter_data(
                    subscription_status, gender, category, shipping_type, age_group)['discount_applied'] == discount]['purchase_amount']
            fig.add_trace(go.Box(
                y=data,
                name=f'Discount: {discount}',
                marker=dict(color=PRIMARY_COLOR if discount ==
                            'Yes' else SECONDARY_COLOR),
                boxmean='sd',
                hovertemplate='Value: $%{y:.2f}<extra></extra>'
            ))

        fig.update_layout(
            title={
                'text': 'Discount Impact on Purchase Amount',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            yaxis_title='Purchase Amount ($)',
            xaxis_title='Discount Applied',
            font=dict(size=12),
            height=450,
            showlegend=False
        )

        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        return fig

    def create_purchase_frequency_days(self, subscription_status, gender, category, shipping_type, age_group):
        freq_days_counts = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group)['purchase_frequency_days'].value_counts().sort_index()

        fig = go.Figure(go.Bar(
            x=freq_days_counts.index,
            y=freq_days_counts.values,
            marker=dict(
                color=PRIMARY_COLOR,
                line=dict(color='white', width=1)
            ),
            text=freq_days_counts.values,
            textposition='outside',
            hovertemplate='Days: %{x}<br>Count: %{y}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': 'Purchase Frequency (Days)',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title='Days Between Purchases',
            yaxis_title='Number of Customers',
            font=dict(size=12),
            height=450
        )

        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        return fig

    def create_shipping_distribution(self, subscription_status, gender, category, shipping_type, age_group):
        shipping_counts = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group)['shipping_type'].value_counts()

        fig = go.Figure(go.Pie(
            labels=shipping_counts.index,
            values=shipping_counts.values,
            hole=0.4,
            marker=dict(colors=GRADIENT_COLORS),
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': 'Shipping Type Distribution',
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

    def create_avg_purchase_by_shipping(self, subscription_status, gender, category, shipping_type, age_group):
        avg_by_shipping = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group).groupby('shipping_type')['purchase_amount'].mean().sort_values(ascending=False)

        fig = go.Figure(go.Bar(
            x=avg_by_shipping.index,
            y=avg_by_shipping.values,
            marker=dict(
                color=PRIMARY_COLOR,
                line=dict(color='white', width=1)
            ),
            text=[f'${x:.2f}' for x in avg_by_shipping.values],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Avg Purchase: $%{y:.2f}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': 'Average Purchase Amount by Shipping Type',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title='Shipping Type',
            yaxis_title='Average Purchase Amount ($)',
            font=dict(size=12),
            height=450,
            xaxis_tickangle=-45
        )

        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        return fig

    def create_shipping_by_category(self, subscription_status, gender, category, shipping_type, age_group):
        shipping_category = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group).groupby(['shipping_type', 'category']).size().reset_index(name='count')

        fig = px.bar(
            shipping_category,
            x='shipping_type',
            y='count',
            color='category',
            title='Shipping Type by Category',
            barmode='stack',
            color_discrete_sequence=COLORS_PALETTE
        )

        fig.update_layout(
            title={
                'text': 'Shipping Type by Category',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title='Shipping Type',
            yaxis_title='Number of Purchases',
            font=dict(size=12),
            height=450,
            legend_title='Category',
            xaxis_tickangle=-45
        )

        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        return fig

    def create_subscription_shipping(self, subscription_status, gender, category, shipping_type, age_group):
        sub_shipping = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group).groupby(
            ['subscription_status', 'shipping_type']).size().reset_index(name='count')

        fig = px.bar(
            sub_shipping,
            x='shipping_type',
            y='count',
            color='subscription_status',
            title='Subscription Status vs Shipping Preference',
            barmode='group',
            color_discrete_map={'Yes': PRIMARY_COLOR, 'No': SECONDARY_COLOR}
        )

        fig.update_layout(
            title={
                'text': 'Subscription Status vs Shipping Preference',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title='Shipping Type',
            yaxis_title='Number of Customers',
            font=dict(size=12),
            height=450,
            legend_title='Subscription',
            xaxis_tickangle=-45
        )

        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        return fig

    def create_top_states_revenue(self, subscription_status, gender, category, shipping_type, age_group):
        state_revenue = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group).groupby('location')['purchase_amount'].sum().sort_values(ascending=True).tail(15)

        fig = go.Figure(go.Bar(
            x=state_revenue.values,
            y=state_revenue.index,
            orientation='h',
            marker=dict(
                color=PRIMARY_COLOR,
                line=dict(color='white', width=1)
            ),
            text=[f'${x:,.0f}' for x in state_revenue.values],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.2f}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': 'Top 15 States by Revenue',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title='Total Revenue ($)',
            yaxis_title='State',
            font=dict(size=12),
            height=600,
            margin=dict(l=120, r=40, t=80, b=60)
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        return fig

    def create_top_states_customers(self, subscription_status, gender, category, shipping_type, age_group):
        state_customers = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group)['location'].value_counts().sort_values(ascending=True).tail(15)

        fig = go.Figure(go.Bar(
            x=state_customers.values,
            y=state_customers.index,
            orientation='h',
            marker=dict(
                color=SECONDARY_COLOR,
                line=dict(color='white', width=1)
            ),
            text=state_customers.values,
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Customers: %{x}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': 'Top 15 States by Customer Count',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title='Number of Customers',
            yaxis_title='State',
            font=dict(size=12),
            height=600,
            margin=dict(l=120, r=40, t=80, b=60)
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        return fig

    def create_avg_purchase_by_state(self, subscription_status, gender, category, shipping_type, age_group):
        state_avg = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group).groupby('location')['purchase_amount'].mean(
        ).sort_values(ascending=True).tail(15)

        fig = go.Figure(go.Bar(
            x=state_avg.values,
            y=state_avg.index,
            orientation='h',
            marker=dict(
                color=ACCENT_COLOR,
                line=dict(color='white', width=1)
            ),
            text=[f'${x:.2f}' for x in state_avg.values],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Avg Purchase: $%{x:.2f}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': 'Top 15 States by Average Purchase Amount',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title='Average Purchase Amount ($)',
            yaxis_title='State',
            font=dict(size=12),
            height=600,
            margin=dict(l=120, r=40, t=80, b=60)
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        return fig

    def create_correlation_heatmap(self, subscription_status, gender, category, shipping_type, age_group):
        numerical_cols = ['age', 'purchase_amount', 'review_rating',
                          'previous_purchases', 'purchase_frequency_days']
        corr_matrix = self.filter_data(
            subscription_status, gender, category, shipping_type, age_group)[numerical_cols].corr()

        fig = go.Figure(go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale=[[0, '#f0e6f5'], [0.5, '#7b3785'], [1, '#4a1f52']],
            text=np.round(corr_matrix.values, 2),
            texttemplate='%{text}',
            textfont={"size": 10},
            hovertemplate='%{y} vs %{x}<br>Correlation: %{z:.2f}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': 'Correlation Heatmap',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            font=dict(size=12),
            height=500,
            xaxis={'side': 'bottom'},
            yaxis={'side': 'left'}
        )

        return fig

    def create_age_vs_purchase(self, subscription_status, gender, category, shipping_type, age_group):
        df = self.filter_data(subscription_status, gender,
                              category, shipping_type, age_group)
        fig = px.scatter(
            df,
            x='age',
            y='purchase_amount',
            color='gender',
            title='Age vs Purchase Amount',
            trendline='ols',
            color_discrete_map={'Male': PRIMARY_COLOR,
                                'Female': SECONDARY_COLOR},
            opacity=0.6
        )

        fig.update_layout(
            title={
                'text': 'Age vs Purchase Amount',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title='Age',
            yaxis_title='Purchase Amount ($)',
            font=dict(size=12),
            height=500
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        return fig

    def create_previous_vs_current(self, subscription_status, gender, category, shipping_type, age_group):
        df = self.filter_data(subscription_status, gender,
                              category, shipping_type, age_group)

        fig = px.scatter(
            df,
            x='previous_purchases',
            y='purchase_amount',
            color='subscription_status',
            title='Previous Purchases vs Current Purchase Amount',
            trendline='ols',
            color_discrete_map={'Yes': PRIMARY_COLOR, 'No': SECONDARY_COLOR},
            opacity=0.6
        )

        fig.update_layout(
            title={
                'text': 'Previous Purchases vs Current Purchase Amount',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title='Previous Purchases',
            yaxis_title='Current Purchase Amount ($)',
            font=dict(size=12),
            height=500,
            legend_title='Subscription'
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        return fig

    def create_rating_vs_purchase(self, subscription_status, gender, category, shipping_type, age_group):
        df = self.filter_data(subscription_status, gender,
                              category, shipping_type, age_group)
        df['rating_group'] = pd.cut(df['review_rating'], bins=[0, 2, 3, 4, 5], labels=[
                                    '1-2', '2-3', '3-4', '4-5'])
        fig = go.Figure()

        for rating in ['1-2', '2-3', '3-4', '4-5']:
            data = df[df['rating_group'] == rating]['purchase_amount']
            fig.add_trace(go.Box(
                y=data,
                name=rating,
                marker=dict(
                    color=COLORS_PALETTE[['1-2', '2-3', '3-4', '4-5'].index(rating)]),
                boxmean='sd',
                hovertemplate='Value: $%{y:.2f}<extra></extra>'
            ))

        fig.update_layout(
            title={
                'text': 'Review Rating vs Purchase Amount',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title='Rating Group',
            yaxis_title='Purchase Amount ($)',
            font=dict(size=12),
            height=500,
            showlegend=False
        )

        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        return fig

    def create_age_group_metrics(self, subscription_status, gender, category, shipping_type, age_group):
        age_metrics = self.filter_data(subscription_status, gender, category, shipping_type, age_group).groupby('age_group').agg({
            'purchase_amount': 'mean',
            'review_rating': 'mean',
            'previous_purchases': 'mean',
            'customer_id': 'count'
        }).round(2)

        age_metrics.columns = [
            'Avg Purchase ($)', 'Avg Rating', 'Avg Previous Purchases', 'Count']
        age_metrics = age_metrics.reindex(
            ['Young Adult', 'Adult', 'Middle-aged', 'Senior'])

        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Avg Purchase Amount', 'Avg Rating',
                            'Avg Previous Purchases', 'Customer Count'),
            vertical_spacing=0.25,
            horizontal_spacing=0.1
        )

        # Avg Purchase
        fig.add_trace(
            go.Bar(x=age_metrics.index, y=age_metrics['Avg Purchase ($)'],
                   marker_color=PRIMARY_COLOR, name='Avg Purchase',
                   text=[f'${x:.2f}' for x in age_metrics['Avg Purchase ($)']],
                   textposition='outside'),
            row=1, col=1
        )

        # Avg Rating
        fig.add_trace(
            go.Bar(x=age_metrics.index, y=age_metrics['Avg Rating'],
                   marker_color=SECONDARY_COLOR, name='Avg Rating',
                   text=[f'{x:.2f}⭐' for x in age_metrics['Avg Rating']],
                   textposition='outside'),
            row=1, col=2
        )

        # Avg Previous Purchases
        fig.add_trace(
            go.Bar(x=age_metrics.index, y=age_metrics['Avg Previous Purchases'],
                   marker_color=ACCENT_COLOR, name='Avg Prev Purchases',
                   text=[f'{x:.1f}' for x in age_metrics['Avg Previous Purchases']],
                   textposition='outside'),
            row=2, col=1
        )

        # Customer Count
        fig.add_trace(
            go.Bar(x=age_metrics.index, y=age_metrics['Count'],
                   marker_color='#6b2d73', name='Count',
                   text=age_metrics['Count'].values,
                   textposition='outside'),
            row=2, col=2
        )

        fig.update_layout(
            title={
                'text': 'Multi-Metric Comparison by Age Group',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            showlegend=False,
            height=700,
            font=dict(size=10)
        )

        # Update all xaxes
        fig.update_xaxes(tickangle=-45)

        return fig
