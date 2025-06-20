# src/bluebrie.py - Navigation Entry Point
import streamlit as st
from streamlit_option_menu import option_menu

# =====PAGE CONFIG=====
st.set_page_config(
    page_title="Professional Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.example.com/help',
        'Report a bug': "https://www.example.com/bug",
        'About': "# Professional Dashboard v1.0"
    }
)

# =====CUSTOM CSS=====
def load_css():
    st.markdown("""
    <style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    /* Reset and base styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(248, 250, 252, 0.95);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(148, 163, 184, 0.2);
    }
    
    /* Sidebar content */
    .css-1cypcdb {
        background: transparent;
    }
    
    /* Remove sidebar padding */
    .css-17eq0hr {
        padding-top: 1rem;
    }
    
    /* Minimalist metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid rgba(0, 0, 0, 0.05);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        text-align: center;
        margin: 16px 0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    .metric-value {
        font-size: 2.8rem;
        font-weight: 600;
        margin: 12px 0;
        color: #1a1a1a;
    }
    
    .metric-label {
        font-size: 0.9rem;
        font-weight: 500;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-sublabel {
        font-size: 0.8rem;
        color: #9ca3af;
        margin-top: 4px;
    }
    
    /* Minimal card container */
    .dashboard-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 28px;
        border-radius: 16px;
        border: 1px solid rgba(0, 0, 0, 0.05);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin: 20px 0;
        transition: all 0.3s ease;
    }
    
    .dashboard-card:hover {
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    /* Clean header */
    .dashboard-header {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 32px;
        border-radius: 16px;
        border: 1px solid rgba(0, 0, 0, 0.05);
        text-align: center;
        margin-bottom: 32px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    
    .header-title {
        font-size: 2.2rem;
        font-weight: 600;
        margin-bottom: 8px;
        color: #1a1a1a;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        font-weight: 400;
        color: #6b7280;
    }
    
    /* Clean sidebar navigation */
    .nav-brand {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        padding: 32px 24px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 32px;
        border: 1px solid rgba(148, 163, 184, 0.15);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    .nav-brand h1 {
        color: #1f2937;
        margin: 0;
        font-size: 1.75rem;
        font-weight: 400;
    }
    
    .nav-brand h3 {
        color: #374151;
        margin: 8px 0 4px 0;
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: -0.025em;
    }
    
    .nav-brand p {
        color: #6b7280;
        margin: 0;
        font-size: 0.8rem;
        font-weight: 400;
        letter-spacing: 0.025em;
        text-transform: uppercase;
    }
    
    /* Status indicators */
    .status-good { color: #10b981; }
    .status-warning { color: #f59e0b; }
    .status-danger { color: #ef4444; }
    
    /* Streamlit specific overrides */
    .stMetric {
        background: none !important;
        border: none !important;
        padding: 0 !important;
    }
    
    .stMetric > div {
        background: none !important;
        border: none !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: rgba(255, 255, 255, 1);
        border-color: rgba(0, 0, 0, 0.2);
        transform: translateY(-1px);
    }
    </style>
    """, unsafe_allow_html=True)

# =====NAVIGATION FUNCTION=====
def create_navigation():
    with st.sidebar:
        st.markdown("""
        <div class='nav-brand'>
            <h1>🖥️</h1>
            <h3>BlueBrie</h3>
            <p>Server Monitor</p>
        </div>
        """, unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title=None,
            options=["Overview", "System", "Network", "Logs", "Config"],
            icons=["circle", "square", "triangle", "hexagon", "octagon"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {
                    "padding": "0!important", 
                    "background-color": "transparent",
                    "border-radius": "16px"
                },
                "icon": {
                    "color": "#9ca3af", 
                    "font-size": "14px",
                    "margin-right": "12px"
                },
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "2px 0",
                    "padding": "14px 18px",
                    "border-radius": "14px",
                    "background-color": "rgba(255, 255, 255, 0.4)",
                    "color": "#4b5563",
                    "font-weight": "500",
                    "border": "1px solid rgba(148, 163, 184, 0.1)",
                    "transition": "all 0.2s ease",
                    "--hover-color": "rgba(255, 255, 255, 0.7)"
                },
                "nav-link-selected": {
                    "background-color": "rgba(255, 255, 255, 0.9)",
                    "color": "#1f2937",
                    "font-weight": "600",
                    "border": "1px solid rgba(148, 163, 184, 0.2)",
                    "box-shadow": "0 1px 3px rgba(0, 0, 0, 0.1)"
                },
            }
        )
        
        # Clean sidebar footer
        st.markdown("""
        <div style='margin-top: 48px; text-align: center; color: #9ca3af; font-size: 0.7rem; padding: 0;'>
            <div style='height: 1px; background: linear-gradient(90deg, transparent, rgba(148, 163, 184, 0.3), transparent); margin: 24px 0;'></div>
            <p style='margin: 0; font-weight: 500; letter-spacing: 0.025em;'>BLUEBRIE</p>
            <p style='margin: 4px 0 0 0; opacity: 0.7;'>v1.0.0</p>
        </div>
        """, unsafe_allow_html=True)
        
    return selected

# =====MAIN NAVIGATION FUNCTION=====
def start() -> None:
    """Enhanced navigation entry point with beautiful UI"""
    
    load_css()
    
    _overview = st.Page("src/pages/dashboard/bb_dashboard.py", title="Overview", icon="🖥️")
    _system = st.Page("src/pages/peripherals/bb_peripherals.py", title="System", icon="⚙️") 
    _network = st.Page("src/pages/analytics/bb_analytics.py", title="Network", icon="🌐")
    _logs = st.Page("src/pages/reports/bb_reports.py", title="Logs", icon="📄")
    _config = st.Page("src/pages/settings/bb_settings.py", title="Config", icon="🔧")
    
    navigation = st.navigation([_overview, _system, _network, _logs, _config])
    
    create_navigation()
    
    navigation.run()

__all__ = ["start"]
