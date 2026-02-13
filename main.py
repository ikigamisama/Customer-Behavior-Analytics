import streamlit as st

from components import Chart

st.set_page_config(
    page_title="Customer Behavior Analytics Dashboard",
    layout="wide"
)

st.markdown(
    """
    <style>
        div[data-testid="stMetric"] {
            border-left: 0.5rem solid #7b3785 !important;
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
    st.header("🔍 Filters")
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

with tab2:
    colA1, colA2 = st.columns(2)
    with colA1:
        st.plotly_chart(c.create_gender_distribution(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')

    with colA2:
        st.plotly_chart(c.create_customer_count_age_group(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')

    colB1, colB2 = st.columns(2)

    with colB1:
        st.plotly_chart(c.create_purchase_by_age_boxplot(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')

    with colB2:
        st.plotly_chart(c.create_previous_purchases_distribution(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')

    st.plotly_chart(c.create_review_rating_distribution(
        subscription_status, gender, category, shipping_type, age_group), width='stretch')

with tab3:
    colA1, colA2 = st.columns(2)
    with colA1:
        st.plotly_chart(c.create_top_10_items(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')

    with colA2:
        st.plotly_chart(c.create_top_colors(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')
    colB1, colB2 = st.columns(2)
    with colB1:
        st.plotly_chart(c.create_category_treemap(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')

    with colB2:
        st.plotly_chart(c.create_avg_rating_by_category(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')

    colC1, colC2 = st.columns(2)

    with colC1:
        st.plotly_chart(c.create_category_by_season(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')

    with colC2:
        st.plotly_chart(c.create_size_distribution(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')


with tab4:
    colA1, colA2 = st.columns(2)
    with colA1:
        st.plotly_chart(c.create_purchase_frequency(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')

    with colA2:
        st.plotly_chart(c.create_payment_methods(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')
    colB1, colB2 = st.columns(2)
    with colB1:
        st.plotly_chart(c.create_subscription_comparison(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')

    with colB2:
        st.plotly_chart(c.create_discount_impact(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')

    st.plotly_chart(c.create_purchase_frequency_days(
        subscription_status, gender, category, shipping_type, age_group), width='stretch')

with tab5:
    colA1, colA2 = st.columns(2)
    with colA1:
        st.plotly_chart(c.create_shipping_distribution(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')

    with colA2:
        st.plotly_chart(c.create_avg_purchase_by_shipping(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')
    colB1, colB2 = st.columns(2)
    with colB1:
        st.plotly_chart(c.create_shipping_by_category(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')

    with colB2:
        st.plotly_chart(c.create_subscription_shipping(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')

with tab6:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.plotly_chart(c.create_top_states_revenue(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')

    with col2:
        st.plotly_chart(c.create_top_states_customers(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')

    with col3:
        st.plotly_chart(c.create_avg_purchase_by_state(
            subscription_status, gender, category, shipping_type, age_group), width='stretch')

with tab7:
    st.plotly_chart(c.create_correlation_heatmap(
        subscription_status, gender, category, shipping_type, age_group), width='stretch')

    st.plotly_chart(c.create_age_vs_purchase(
        subscription_status, gender, category, shipping_type, age_group), width='stretch')

    st.plotly_chart(c.create_previous_vs_current(
        subscription_status, gender, category, shipping_type, age_group), width='stretch')

    st.plotly_chart(c.create_rating_vs_purchase(
        subscription_status, gender, category, shipping_type, age_group), width='stretch')

    st.plotly_chart(c.create_age_group_metrics(
        subscription_status, gender, category, shipping_type, age_group), width='stretch')
