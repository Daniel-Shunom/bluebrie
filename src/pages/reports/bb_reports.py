# src/pages/reports/reports.py - Server Logs
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

# =====LOG DATA GENERATION=====
@st.cache_data
def generate_log_data():
    np.random.seed(42)
    
    # Generate server logs for the last 24 hours
    log_levels = ['INFO', 'WARN', 'ERROR', 'DEBUG']
    log_sources = ['gleam_server', 'nginx', 'postgres', 'redis', 'system']
    
    # Generate timestamps
    base_time = datetime.now() - timedelta(hours=24)
    log_times = []
    for i in range(500):  # 500 log entries
        log_times.append(base_time + timedelta(seconds=np.random.exponential(172.8)))  # ~500 logs per day
    
    logs_data = []
    for timestamp in sorted(log_times):
        level = np.random.choice(log_levels, p=[0.7, 0.2, 0.05, 0.05])
        source = np.random.choice(log_sources, p=[0.4, 0.25, 0.15, 0.1, 0.1])
        
        # Generate realistic log messages based on source and level
        messages = {
            'gleam_server': {
                'INFO': ['Request processed successfully', 'Connection established', 'Cache hit', 'User authenticated'],
                'WARN': ['High memory usage detected', 'Slow query detected', 'Connection timeout'],
                'ERROR': ['Database connection failed', 'Authentication failed', 'Internal server error'],
                'DEBUG': ['Function entered', 'Variable state', 'Debug checkpoint']
            },
            'nginx': {
                'INFO': ['GET /api/health 200', 'POST /api/users 201', 'Static file served'],
                'WARN': ['Rate limit approaching', '404 error for unknown route'],
                'ERROR': ['Upstream server unreachable', '502 Bad Gateway'],
                'DEBUG': ['Request headers logged', 'Routing decision made']
            },
            'postgres': {
                'INFO': ['Query executed successfully', 'Connection opened', 'Checkpoint completed'],
                'WARN': ['Lock wait timeout', 'Table scan detected'],
                'ERROR': ['Connection limit reached', 'Disk space low'],
                'DEBUG': ['Query plan generated', 'Index usage statistics']
            }
        }
        
        if source in messages and level in messages[source]:
            message = np.random.choice(messages[source][level])
        else:
            message = f"{level} message from {source}"
        
        logs_data.append({
            'timestamp': timestamp,
            'level': level,
            'source': source,
            'message': message,
            'ip': f"192.168.1.{np.random.randint(1, 255)}",
            'user_id': np.random.randint(1000, 9999) if np.random.random() > 0.3 else None
        })
    
    return pd.DataFrame(logs_data)

# =====LOG ANALYSIS PAGE=====
def reports_page():
    # Header
    st.markdown("""
    <div class='dashboard-header'>
        <div class='header-title'>📄 Server Logs</div>
        <div class='header-subtitle'>Log Analysis & System Events</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate log data
    logs_df = generate_log_data()
    
    # Log level statistics
    level_counts = logs_df['level'].value_counts()
    error_count = level_counts.get('ERROR', 0)
    warn_count = level_counts.get('WARN', 0)
    info_count = level_counts.get('INFO', 0)
    total_logs = len(logs_df)
    
    # Log Summary Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card' style='background: linear-gradient(135deg, #28a745 0%, #20c997 100%);'>
            <div class='metric-label'>Total Logs (24h)</div>
            <div class='metric-value'>{total_logs}</div>
            <div class='metric-label'>📋 Entries</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        error_rate = (error_count / total_logs * 100) if total_logs > 0 else 0
        error_color = "#dc3545" if error_rate > 5 else "#ffc107" if error_rate > 2 else "#28a745"
        st.markdown(f"""
        <div class='metric-card' style='background: linear-gradient(135deg, {error_color} 0%, {error_color}aa 100%);'>
            <div class='metric-label'>Errors</div>
            <div class='metric-value'>{error_count}</div>
            <div class='metric-label'>{error_rate:.1f}% rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card' style='background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);'>
            <div class='metric-label'>Warnings</div>
            <div class='metric-value'>{warn_count}</div>
            <div class='metric-label'>⚠️ Issues</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        unique_sources = logs_df['source'].nunique()
        st.markdown(f"""
        <div class='metric-card' style='background: linear-gradient(135deg, #007bff 0%, #6610f2 100%);'>
            <div class='metric-label'>Active Sources</div>
            <div class='metric-value'>{unique_sources}</div>
            <div class='metric-label'>🔧 Services</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Log Filters and Search
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    st.subheader("🔍 Log Filters")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        selected_level = st.selectbox("Log Level", ["All"] + list(logs_df['level'].unique()))
    
    with col2:
        selected_source = st.selectbox("Source", ["All"] + list(logs_df['source'].unique()))
    
    with col3:
        time_filter = st.selectbox("Time Range", ["Last Hour", "Last 6 Hours", "Last 24 Hours"])
    
    with col4:
        search_term = st.text_input("Search in logs", placeholder="Enter search term...")
    
    # Apply filters
    filtered_logs = logs_df.copy()
    
    if selected_level != "All":
        filtered_logs = filtered_logs[filtered_logs['level'] == selected_level]
    
    if selected_source != "All":
        filtered_logs = filtered_logs[filtered_logs['source'] == selected_source]
    
    if search_term:
        filtered_logs = filtered_logs[filtered_logs['message'].str.contains(search_term, case=False, na=False)]
    
    # Time range filter
    now = datetime.now()
    if time_filter == "Last Hour":
        time_threshold = now - timedelta(hours=1)
    elif time_filter == "Last 6 Hours":
        time_threshold = now - timedelta(hours=6)
    else:
        time_threshold = now - timedelta(hours=24)
    
    filtered_logs = filtered_logs[filtered_logs['timestamp'] >= time_threshold]
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Log Analysis Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("📊 Log Distribution by Level")
        
        import plotly.express as px
        level_chart = px.pie(
            values=level_counts.values,
            names=level_counts.index,
            color_discrete_map={
                'INFO': '#28a745',
                'WARN': '#ffc107', 
                'ERROR': '#dc3545',
                'DEBUG': '#6c757d'
            }
        )
        level_chart.update_layout(height=300)
        st.plotly_chart(level_chart, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("🔧 Logs by Source")
        
        source_counts = logs_df['source'].value_counts()
        source_chart = px.bar(
            x=source_counts.index,
            y=source_counts.values,
            color=source_counts.values,
            color_continuous_scale='Blues'
        )
        source_chart.update_layout(
            height=300,
            xaxis_title="Source",
            yaxis_title="Log Count",
            showlegend=False
        )
        st.plotly_chart(source_chart, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Recent Logs Table
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    st.subheader("📋 Recent Log Entries")
    
    # Display recent logs
    display_logs = filtered_logs.tail(50).sort_values('timestamp', ascending=False)
    
    # Format the logs for display
    display_logs['time'] = display_logs['timestamp'].dt.strftime('%H:%M:%S')
    display_logs['level_icon'] = display_logs['level'].map({
        'ERROR': '🔴',
        'WARN': '🟡', 
        'INFO': '🟢',
        'DEBUG': '🔵'
    })
    
    # Show logs in a clean format
    for _, log in display_logs.head(20).iterrows():
        col1, col2, col3, col4 = st.columns([1, 1, 2, 6])
        
        with col1:
            st.text(log['time'])
        with col2:
            st.text(f"{log['level_icon']} {log['level']}")
        with col3:
            st.text(log['source'])
        with col4:
            st.text(log['message'])
    
    if len(display_logs) > 20:
        st.info(f"Showing 20 of {len(display_logs)} filtered logs")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Error Analysis
    if error_count > 0:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("🚨 Error Analysis")
        
        error_logs = logs_df[logs_df['level'] == 'ERROR']
        error_by_source = error_logs['source'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Errors by Source:**")
            for source, count in error_by_source.items():
                st.text(f"🔴 {source}: {count} errors")
        
        with col2:
            st.markdown("**Recent Errors:**")
            recent_errors = error_logs.tail(5)
            for _, error in recent_errors.iterrows():
                st.text(f"⚠️ {error['timestamp'].strftime('%H:%M')} - {error['message']}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Export Options
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    st.subheader("📤 Export Logs")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Download Filtered Logs"):
            csv_data = filtered_logs.to_csv(index=False)
            st.download_button(
                label="💾 Save as CSV",
                data=csv_data,
                file_name=f"server_logs_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📧 Email Error Report"):
            st.info("Error report will be emailed to administrators")
    
    with col3:
        if st.button("🔄 Refresh Logs"):
            st.cache_data.clear()
            st.success("Logs refreshed!")
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# Call the reports page function
reports_page()