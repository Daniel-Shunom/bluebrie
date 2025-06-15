
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# =====PERIPHERALS PAGE=====
def peripherals_page():
    # Header
    st.markdown("""
    <div class='dashboard-header'>
        <div class='header-title'>🔧 Peripherals</div>
        <div class='header-subtitle'>System Components & Hardware Status</div>
    </div>
    """, unsafe_allow_html=True)
    
    # System Overview Row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("💻 System Status")
        
        # Mock system data
        system_data = {
            "CPU Usage": 65,
            "Memory Usage": 78,
            "Disk Usage": 45,
            "Network": 23
        }
        
        for metric, value in system_data.items():
            delta_value = np.random.randint(-5, 10)
            delta_color = "normal" if delta_value >= 0 else "inverse"
            st.metric(metric, f"{value}%", f"{delta_value}%", delta_color=delta_color)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("🌡️ Temperature Monitoring")
        
        # Temperature gauge
        temp_fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 67,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "CPU Temperature (°C)"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#ff7f0e"},
                'steps': [
                    {'range': [0, 60], 'color': "lightgreen"},
                    {'range': [60, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "red"}
                ]
            }
        ))
        
        temp_fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(temp_fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("⚡ Power Consumption")
        
        # Power gauge
        power_fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 145,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Power Usage (W)"},
            gauge = {
                'axis': {'range': [None, 300]},
                'bar': {'color': "#2ca02c"},
                'steps': [
                    {'range': [0, 150], 'color': "lightgreen"},
                    {'range': [150, 250], 'color': "yellow"},
                    {'range': [250, 300], 'color': "red"}
                ]
            }
        ))
        
        power_fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(power_fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Hardware Details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("🖥️ Hardware Information")
        
        hardware_info = {
            "Processor": "Intel Core i7-12700K",
            "Memory": "32 GB DDR4-3200",
            "Storage": "1TB NVMe SSD",
            "Graphics": "NVIDIA RTX 4070",
            "Motherboard": "ASUS ROG Strix Z690",
            "OS": "Windows 11 Pro"
        }
        
        for component, spec in hardware_info.items():
            st.text(f"**{component}:** {spec}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("📊 Performance History")
        
        # Generate sample performance data
        np.random.seed(42)
        dates = pd.date_range(start=datetime.now() - timedelta(days=7), end=datetime.now(), freq='H')
        perf_data = pd.DataFrame({
            'CPU': np.random.normal(65, 15, len(dates)).clip(0, 100),
            'Memory': np.random.normal(70, 10, len(dates)).clip(0, 100),
            'Disk': np.random.normal(40, 20, len(dates)).clip(0, 100)
        }, index=dates)
        
        fig_perf = px.line(
            perf_data.reset_index(), 
            x='index', 
            y=['CPU', 'Memory', 'Disk'],
            title="System Performance (Last 7 Days)",
            labels={'index': 'Time', 'value': 'Usage (%)', 'variable': 'Component'}
        )
        fig_perf.update_layout(height=350)
        st.plotly_chart(fig_perf, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Network and Storage Details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("🌐 Network Status")
        
        network_data = {
            "Interface": "Ethernet",
            "Speed": "1 Gbps",
            "Status": "Connected",
            "IP Address": "192.168.1.100",
            "Download": "45.2 Mbps",
            "Upload": "12.8 Mbps",
            "Latency": "15 ms"
        }
        
        for item, value in network_data.items():
            if item == "Status" and value == "Connected":
                st.success(f"**{item}:** {value}")
            else:
                st.text(f"**{item}:** {value}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("💾 Storage Details")
        
        # Storage usage chart
        storage_data = pd.DataFrame({
            'Drive': ['C: System', 'D: Data', 'E: Backup'],
            'Used': [450, 750, 200],
            'Total': [1000, 2000, 1000]
        })
        storage_data['Free'] = storage_data['Total'] - storage_data['Used']
        storage_data['Usage %'] = (storage_data['Used'] / storage_data['Total'] * 100).round(1)
        
        fig_storage = px.bar(
            storage_data, 
            x='Drive', 
            y=['Used', 'Free'],
            title="Storage Usage (GB)",
            color_discrete_map={'Used': '#ff7f0e', 'Free': '#2ca02c'}
        )
        fig_storage.update_layout(height=300)
        st.plotly_chart(fig_storage, use_container_width=True)
        
        # Display usage percentages
        for _, row in storage_data.iterrows():
            usage_color = "🔴" if row['Usage %'] > 80 else "🟡" if row['Usage %'] > 60 else "🟢"
            st.text(f"{usage_color} {row['Drive']}: {row['Usage %']}% used")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Call the peripherals page function
peripherals_page()