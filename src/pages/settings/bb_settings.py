
import streamlit as st
import json
from datetime import datetime

# =====SETTINGS PAGE=====
def settings_page():
    # Header
    st.markdown("""
    <div class='dashboard-header'>
        <div class='header-title'>⚙️ Settings</div>
        <div class='header-subtitle'>Configure Your Dashboard</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different settings categories
    tab1, tab2, tab3, tab4 = st.tabs(["🎨 Appearance", "📊 Data", "🔔 Notifications", "👤 Account"])
    
    with tab1:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("🎨 Appearance Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            theme = st.selectbox("Theme", ["Light", "Dark", "Auto"], index=0)
            color_scheme = st.selectbox("Color Scheme", ["Blue", "Green", "Purple", "Orange"], index=0)
            font_size = st.slider("Font Size", 10, 20, 14)
            
        with col2:
            show_animations = st.checkbox("Enable Animations", True)
            compact_mode = st.checkbox("Compact Mode", False)
            show_sidebar = st.checkbox("Show Sidebar by Default", True)
        
        st.markdown("**Dashboard Layout**")
        layout_option = st.radio(
            "Choose layout style:",
            ["Grid View", "List View", "Card View"],
            horizontal=True
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("📊 Data Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            data_source = st.selectbox("Primary Data Source", ["Database", "API", "File Upload", "Real-time Stream"])
            update_frequency = st.selectbox("Update Frequency", ["Real-time", "Every 5 minutes", "Hourly", "Daily"])
            data_retention = st.slider("Data Retention (days)", 1, 365, 30)
            
        with col2:
            cache_enabled = st.checkbox("Enable Data Caching", True)
            auto_refresh = st.checkbox("Auto Refresh", True)
            debug_mode = st.checkbox("Debug Mode", False)
        
        st.markdown("**Data Export Options**")
        export_formats = st.multiselect(
            "Available export formats:",
            ["CSV", "Excel", "JSON", "PDF"],
            default=["CSV", "Excel"]
        )
        
        st.markdown("**API Configuration**")
        api_endpoint = st.text_input("API Endpoint", placeholder="https://api.example.com/data")
        api_key = st.text_input("API Key", type="password", placeholder="Enter your API key")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("🔔 Notification Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            email_notifications = st.checkbox("Email Notifications", True)
            push_notifications = st.checkbox("Push Notifications", False)
            sms_notifications = st.checkbox("SMS Notifications", False)
            
        with col2:
            notification_frequency = st.selectbox(
                "Notification Frequency",
                ["Immediate", "Hourly Summary", "Daily Summary", "Weekly Summary"]
            )
        
        st.markdown("**Alert Thresholds**")
        col1, col2 = st.columns(2)
        with col1:
            cpu_threshold = st.slider("CPU Usage Alert (%)", 0, 100, 80)
            memory_threshold = st.slider("Memory Usage Alert (%)", 0, 100, 85)
            
        with col2:
            disk_threshold = st.slider("Disk Usage Alert (%)", 0, 100, 90)
            temp_threshold = st.slider("Temperature Alert (°C)", 0, 100, 75)
        
        st.markdown("**Email Settings**")
        email_address = st.text_input("Email Address", placeholder="your-email@example.com")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab4:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("👤 Account Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Username", value="admin")
            full_name = st.text_input("Full Name", value="Dashboard Administrator")
            email = st.text_input("Email", value="admin@dashboard.com")
            
        with col2:
            timezone = st.selectbox("Timezone", [
                "UTC", "EST", "PST", "GMT", "CET", "JST"
            ], index=0)
            language = st.selectbox("Language", ["English", "Spanish", "French", "German"], index=0)
            date_format = st.selectbox("Date Format", ["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"], index=0)
        
        st.markdown("**Security Settings**")
        col1, col2 = st.columns(2)
        with col1:
            two_factor = st.checkbox("Enable Two-Factor Authentication", False)
            session_timeout = st.slider("Session Timeout (minutes)", 15, 480, 60)
            
        with col2:
            password_expiry = st.slider("Password Expiry (days)", 30, 365, 90)
            login_attempts = st.slider("Max Login Attempts", 3, 10, 5)
        
        if st.button("🔑 Change Password", type="secondary"):
            st.info("Password change functionality would be implemented here.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Save Settings Section
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    st.subheader("💾 Save Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Save Settings", type="primary"):
            st.success("✅ Settings saved successfully!")
            st.balloons()
    
    with col2:
        if st.button("🔄 Reset to Default", type="secondary"):
            st.warning("⚠️ All settings will be reset to default values.")
            if st.button("Confirm Reset"):
                st.success("Settings reset to default.")
    
    with col3:
        if st.button("📤 Export Config", type="secondary"):
            config_data = {
                "theme": "Light",
                "data_source": "Database",
                "notifications": True,
                "export_timestamp": datetime.now().isoformat()
            }
            st.download_button(
                label="📥 Download Config",
                data=json.dumps(config_data, indent=2),
                file_name=f"dashboard_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # System Information
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    st.subheader("ℹ️ System Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Dashboard Version", "v1.0.0")
        st.metric("Last Updated", "2025-06-14")
    
    with col2:
        st.metric("Uptime", "7 days, 14 hours")
        st.metric("Active Users", "23")
    
    with col3:
        st.metric("Database Size", "2.4 GB")
        st.metric("Cache Size", "156 MB")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Call the settings page function
settings_page()