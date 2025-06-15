# pages/analytics/analytics.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# =====SAMPLE DATA GENERATION=====
@st.cache_data
def generate_analytics_data():
    np.random.seed(42)
    
    # Generate time series data
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    
    # Website analytics data
    website_data = pd.DataFrame({
        'date': dates,
        'page_views': np.random.poisson(1000, len(dates)) + np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 200,
        'unique_visitors': np.random.poisson(300, len(dates)) + np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 50,
        'bounce_rate': np.random.beta(2, 3, len(dates)) * 100,
        'avg_session_duration': np.random.normal(180, 60, len(dates)).clip(30, 600),
        'conversion_rate': np.random.beta(1, 20, len(dates)) * 100
    })
    
    # Sales analytics data
    sales_data = pd.DataFrame({
        'product': ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'],
        'revenue': np.random.normal([50000, 35000, 25000, 15000, 10000], 5000),
        'units_sold': np.random.poisson([500, 350, 250, 150, 100]),
        'profit_margin': np.random.normal([25, 30, 20, 35, 15], 5)
    })
    
    # Geographic data
    geo_data = pd.DataFrame({
        'country': ['United States', 'United Kingdom', 'Germany', 'France', 'Canada', 'Australia', 'Japan', 'Brazil'],
        'users': np.random.poisson([5000, 2000, 1500, 1200, 800, 600, 400, 300]),
        'revenue': np.random.normal([100000, 40000, 30000, 25000, 15000, 12000, 8000, 6000], 5000)
    })
    
    return website_data, sales_data, geo_data

# =====ANALYTICS PAGE=====
def analytics_page():
    # Header
    st.markdown("""
    <div class='dashboard-header'>
        <div class='header-title'>📈 Advanced Analytics</div>
        <div class='header-subtitle'>Deep Insights & Data Analysis</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate data
    website_data, sales_data, geo_data = generate_analytics_data()
    
    # Time period selector
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        time_period = st.selectbox("Time Period", ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Year to Date"])
    with col2:
        metric_type = st.selectbox("Primary Metric", ["Page Views", "Revenue", "Users", "Conversions"])
    
    # Key Performance Indicators
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    st.subheader("📊 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    latest_data = website_data.iloc[-1]
    
    with col1:
        st.metric(
            "Page Views", 
            f"{latest_data['page_views']:.0f}",
            f"{np.random.randint(-15, 25)}%"
        )
    
    with col2:
        st.metric(
            "Unique Visitors", 
            f"{latest_data['unique_visitors']:.0f}",
            f"{np.random.randint(-10, 20)}%"
        )
    
    with col3:
        st.metric(
            "Bounce Rate", 
            f"{latest_data['bounce_rate']:.1f}%",
            f"{np.random.randint(-5, 15)}%",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            "Avg Session", 
            f"{latest_data['avg_session_duration']:.0f}s",
            f"{np.random.randint(-20, 30)}s"
        )
    
    with col5:
        st.metric(
            "Conversion Rate", 
            f"{latest_data['conversion_rate']:.2f}%",
            f"{np.random.randint(-2, 8)}%"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Main Analytics Charts
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("📈 Traffic Trends")
        
        # Multi-line chart
        fig_trends = go.Figure()
        
        fig_trends.add_trace(go.Scatter(
            x=website_data['date'],
            y=website_data['page_views'],
            mode='lines',
            name='Page Views',
            line=dict(color='#1f77b4', width=2)
        ))
        
        fig_trends.add_trace(go.Scatter(
            x=website_data['date'],
            y=website_data['unique_visitors'] * 3,  # Scale for visibility
            mode='lines',
            name='Unique Visitors (x3)',
            line=dict(color='#ff7f0e', width=2),
            yaxis='y2'
        ))
        
        fig_trends.update_layout(
            height=400,
            xaxis_title="Date",
            yaxis_title="Page Views",
            yaxis2=dict(
                title="Unique Visitors",
                overlaying='y',
                side='right'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        
        st.plotly_chart(fig_trends, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("🎯 Conversion Funnel")
        
        # Funnel chart
        funnel_data = ['Visitors', 'Product Views', 'Add to Cart', 'Checkout', 'Purchase']
        funnel_values = [10000, 6500, 2800, 1200, 450]
        
        fig_funnel = go.Figure(go.Funnel(
            y=funnel_data,
            x=funnel_values,
            textinfo="value+percent initial",
            marker_color=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']
        ))
        
        fig_funnel.update_layout(height=400)
        st.plotly_chart(fig_funnel, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Product Performance and Geography
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("🛍️ Product Performance")
        
        # Product revenue chart
        fig_products = px.bar(
            sales_data.sort_values('revenue', ascending=True),
            x='revenue',
            y='product',
            orientation='h',
            title="Revenue by Product",
            color='profit_margin',
            color_continuous_scale='RdYlGn'
        )
        fig_products.update_layout(height=350)
        st.plotly_chart(fig_products, use_container_width=True)
        
        # Product details table
        st.subheader("Product Details")
        display_data = sales_data.copy()
        display_data['revenue'] = display_data['revenue'].apply(lambda x: f"${x:,.0f}")
        display_data['profit_margin'] = display_data['profit_margin'].apply(lambda x: f"{x:.1f}%")
        st.dataframe(display_data, use_container_width=True, hide_index=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("🌍 Geographic Distribution")
        
        # Geographic data visualization
        fig_geo = px.bar(
            geo_data.sort_values('users', ascending=False),
            x='users',
            y='country',
            orientation='h',
            title="Users by Country",
            color='revenue',
            color_continuous_scale='Blues'
        )
        fig_geo.update_layout(height=350)
        st.plotly_chart(fig_geo, use_container_width=True)
        
        # Top countries metrics
        st.subheader("Top Markets")
        for i, row in geo_data.head(3).iterrows():
            col_flag, col_country, col_users, col_revenue = st.columns([0.5, 2, 1.5, 1.5])
            
            flags = {"United States": "🇺🇸", "United Kingdom": "🇬🇧", "Germany": "🇩🇪"}
            
            with col_flag:
                st.write(flags.get(row['country'], "🌍"))
            with col_country:
                st.write(row['country'])
            with col_users:
                st.write(f"{row['users']:,} users")
            with col_revenue:
                st.write(f"${row['revenue']:,.0f}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Advanced Analytics Section
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    st.subheader("🔬 Advanced Analytics")
    
    # Create tabs for different advanced analytics
    tab1, tab2, tab3 = st.tabs(["📊 Cohort Analysis", "🔍 Segmentation", "📈 Predictive Analytics"])
    
    with tab1:
        st.write("**User Cohort Analysis**")
        
        # Generate cohort data
        cohort_data = np.random.rand(12, 12) * 100
        cohort_df = pd.DataFrame(cohort_data, 
                               columns=[f"Month {i+1}" for i in range(12)],
                               index=[f"Jan Cohort", f"Feb Cohort", f"Mar Cohort", f"Apr Cohort",
                                     f"May Cohort", f"Jun Cohort", f"Jul Cohort", f"Aug Cohort",
                                     f"Sep Cohort", f"Oct Cohort", f"Nov Cohort", f"Dec Cohort"])
        
        fig_cohort = px.imshow(
            cohort_df.values,
            labels=dict(x="Months Since First Purchase", y="Cohort", color="Retention %"),
            x=cohort_df.columns,
            y=cohort_df.index,
            color_continuous_scale="RdYlBu_r"
        )
        fig_cohort.update_layout(height=400)
        st.plotly_chart(fig_cohort, use_container_width=True)
    
    with tab2:
        st.write("**Customer Segmentation**")
        
        # Generate segmentation data
        segments = ['High Value', 'Medium Value', 'Low Value', 'New Customers', 'At Risk']
        segment_sizes = [25, 35, 20, 15, 5]
        
        fig_segments = px.pie(
            values=segment_sizes,
            names=segments,
            title="Customer Segments Distribution"
        )
        fig_segments.update_layout(height=400)
        st.plotly_chart(fig_segments, use_container_width=True)
    
    with tab3:
        st.write("**Revenue Prediction**")
        
        # Generate prediction data
        future_dates = pd.date_range(start='2025-01-01', end='2025-12-31', freq='M')
        actual_revenue = np.random.normal(50000, 10000, 12)
        predicted_revenue = actual_revenue * np.random.normal(1.1, 0.1, 12)
        
        fig_prediction = go.Figure()
        
        fig_prediction.add_trace(go.Scatter(
            x=future_dates,
            y=predicted_revenue,
            mode='lines+markers',
            name='Predicted Revenue',
            line=dict(color='#1f77b4', dash='dash')
        ))
        
        fig_prediction.add_trace(go.Scatter(
            x=future_dates[:6],  # Show actual for first 6 months
            y=actual_revenue[:6],
            mode='lines+markers',
            name='Actual Revenue',
            line=dict(color='#ff7f0e')
        ))
        
        fig_prediction.update_layout(
            height=400,
            title="Revenue Prediction for 2025",
            xaxis_title="Month",
            yaxis_title="Revenue ($)"
        )
        st.plotly_chart(fig_prediction, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Call the analytics page function
analytics_page()