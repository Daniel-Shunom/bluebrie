# src/pages/dashboard/bb_dashboard.py - Server Overview
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# =====SERVER DATA SIMULATION=====
@st.cache_data
def get_server_metrics():
    np.random.seed(42)
    
    # Simulate server uptime and basic metrics
    uptime_hours = np.random.randint(120, 8760)  # 5 days to 1 year
    cpu_usage = np.random.uniform(15, 85)
    memory_usage = np.random.uniform(40, 90)
    disk_usage = np.random.uniform(25, 75)
    
    # Network metrics
    requests_per_sec = np.random.poisson(45)
    active_connections = np.random.randint(10, 200)
    
    return {
        'uptime_hours': uptime_hours,
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'disk_usage': disk_usage,
        'requests_per_sec': requests_per_sec,
        'active_connections': active_connections
    }

@st.cache_data
def get_time_series_data():
    # Generate last 24 hours of data
    times = pd.date_range(start=datetime.now() - timedelta(hours=24), end=datetime.now(), freq='5min')
    
    data = pd.DataFrame({
        'timestamp': times,
        'cpu': np.random.normal(50, 15, len(times)).clip(0, 100),
        'memory': np.random.normal(65, 10, len(times)).clip(0, 100),
        'requests': np.random.poisson(40, len(times)),
        'response_time': np.random.gamma(2, 50, len(times))  # Response time in ms
    })
    
    return data

# =====SERVER OVERVIEW PAGE=====
def dashboard_page():
    # Header
    st.markdown("""
    <div class='dashboard-header'>
        <div class='header-title'>Server Overview</div>
        <div class='header-subtitle'>Real-time system metrics and status</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get server metrics
    metrics = get_server_metrics()
    time_data = get_time_series_data()
    
    # Server Status Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        uptime_days = metrics['uptime_hours'] // 24
        uptime_hours = metrics['uptime_hours'] % 24
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Uptime</div>
            <div class='metric-value'>{uptime_days}d {uptime_hours}h</div>
            <div class='metric-sublabel status-good'>Running</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        cpu_status = "status-danger" if metrics['cpu_usage'] > 80 else "status-warning" if metrics['cpu_usage'] > 60 else "status-good"
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>CPU</div>
            <div class='metric-value'>{metrics['cpu_usage']:.0f}%</div>
            <div class='metric-sublabel {cpu_status}'>{"High" if metrics['cpu_usage'] > 80 else "Normal" if metrics['cpu_usage'] < 60 else "Medium"}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Connections</div>
            <div class='metric-value'>{metrics['active_connections']}</div>
            <div class='metric-sublabel status-good'>Active</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Requests/sec</div>
            <div class='metric-value'>{metrics['requests_per_sec']}</div>
            <div class='metric-sublabel status-good'>{(metrics['requests_per_sec']*60):.0f}/min</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # System Metrics Row
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("Performance Trends")
        
        # Clean performance chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=time_data['timestamp'],
            y=time_data['cpu'],
            mode='lines',
            name='CPU',
            line=dict(color='#3b82f6', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=time_data['timestamp'],
            y=time_data['memory'],
            mode='lines',
            name='Memory',
            line=dict(color='#10b981', width=2)
        ))
        
        fig.update_layout(
            height=280,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(range=[0, 100], showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
            xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("System Health")
        
        # Clean metrics display
        memory_usage = (time_data['memory'].iloc[-1])
        disk_usage = np.random.uniform(35, 65)
        
        st.metric("Memory", f"{memory_usage:.0f}%", 
                 f"{np.random.randint(-3, 8)}%")
        st.metric("Disk", f"{disk_usage:.0f}%",
                 f"{np.random.randint(-1, 3)}%")
        
        st.markdown("**Services**")
        services = [
            ("HTTP Server", "Running"),
            ("Database", "Running"), 
            ("Cache", "Running"),
            ("Queue", "Running")
        ]
        
        for service, status in services:
            status_class = "status-good" if status == "Running" else "status-danger"
            st.markdown(f"<span class='{status_class}'>●</span> {service}", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Performance Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("Request Rate")
        
        fig_requests = go.Figure()
        fig_requests.add_trace(go.Scatter(
            x=time_data['timestamp'],
            y=time_data['requests'],
            mode='lines',
            name='Requests',
            line=dict(color='#8b5cf6', width=2),
            fill='tonexty'
        ))
        
        fig_requests.update_layout(
            height=200,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
            xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(fig_requests, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("Response Time")
        
        fig_response = go.Figure()
        fig_response.add_trace(go.Scatter(
            x=time_data['timestamp'],
            y=time_data['response_time'],
            mode='lines',
            name='Response Time',
            line=dict(color='#f59e0b', width=2)
        ))
        
        fig_response.update_layout(
            height=200,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
            xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(fig_response, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Call the dashboard page function
dashboard_page()