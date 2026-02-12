import streamlit as st
import streamlit_shadcn_ui as ui

from components import Chart

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
st.title("Customer Analytics")
st.caption("Data-driven insights for smarter decisions")

c = Chart('data/customer_behavior.csv')
with st.sidebar:
    subscription_status = st.selectbox(
        'Subscription Status:', options=c.subscription_status())
    gender = st.selectbox('Gender:', options=c.gender())
    category = st.selectbox('Category: ', options=c.category())
    shipping_type = st.selectbox('Shipping Type: ', options=c.shipping_type())
    age_group = st.selectbox('Age Group: ', options=c.age_group())

    subscription_status = None if subscription_status == "All" else subscription_status
    gender = None if gender == "All" else gender
    category = None if category == "All" else category
    shipping_type = None if shipping_type == "All" else shipping_type
    age_group = None if age_group == "All" else age_group

total_revenue, average_order_value, total_customers, average_rating = c.compute_kpis(
    subscription_status, gender, category, shipping_type, age_group)

cols = st.columns(4, gap="small")

with cols[0]:
    st.metric(
        "💰 Total Revenue",
        f"${total_revenue:,.0f}",
        border=True
    )

with cols[1]:
    st.metric(
        "📈 Average Order Value",
        f"${average_order_value:,.0f}",
        border=True
    )

with cols[2]:
    st.metric(
        "👥 Total Customers",
        f"{total_customers:,.0f}",
        border=True
    )

with cols[3]:
    st.metric(
        "⭐ Average Rating",
        f"{average_rating:,.1f}",
        border=True
    )


tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Overview",
    "👥 Customer Insights",
    "🛍️ Product Performance",
    "💳 Purchase Behavior",
    "🚚 Shipping & Delivery",
    "🗺️ Geographic Analysis",
    "🔍 Advanced Analytics"
])

with tab1:
    colA1, colA2 = st.columns(2)
    with colA1:
        st.plotly_chart(c.create_revenue_by_category(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')

    with colA2:
        st.plotly_chart(c.create_revenue_by_season(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')

    colB1, colB2 = st.columns(2)

    with colB1:
        st.plotly_chart(c.create_purchase_amount_distribution(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')

    with colB2:
        st.plotly_chart(c.create_customer_by_age_group(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')
