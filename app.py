import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import io
import base64

# Import custom modules
from utils.data_processor import DataProcessor
from utils.ai_analytics import AIAnalytics
from utils.visualizations import Visualizations
from components.player_analysis import PlayerAnalysis
from components.draft_simulator import DraftSimulator
from components.team_analysis import TeamAnalysis

# Page configuration
st.set_page_config(
    page_title="2025 NFL Draft Assistant",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'draft_data' not in st.session_state:
    st.session_state.draft_data = None
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# Header
st.markdown("""
<div class="main-header">
    <h1>🏈 2025 NFL Draft Assistant</h1>
    <p>Advanced AI Analytics & Statistical Breakdown</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for navigation and data upload
with st.sidebar:
    st.markdown("### Navigation")
    page = st.selectbox(
        "Select Analysis Module",
        ["Data Upload", "Player Analysis", "Draft Simulator", "Team Analysis", "AI Insights", "Statistical Reports"]
    )
    
    st.markdown("---")
    
    # Data upload section
    st.markdown("### Data Management")
    uploaded_file = st.file_uploader(
        "Upload NFL Draft Excel File",
        type=['xlsx', 'xls'],
        help="Upload your Excel file containing draft data across multiple sheets"
    )
    
    if uploaded_file is not None:
        if st.button("Process Data", type="primary"):
            with st.spinner("Processing Excel file..."):
                try:
                    # Initialize data processor
                    processor = DataProcessor()
                    
                    # Process the uploaded file
                    draft_data, processed_data = processor.process_excel_file(uploaded_file)
                    
                    # Store in session state
                    st.session_state.draft_data = draft_data
                    st.session_state.processed_data = processed_data
                    st.session_state.data_loaded = True
                    
                    st.success(f"✅ Successfully processed {len(draft_data)} sheets!")
                    st.info(f"Total players analyzed: {len(processed_data) if processed_data is not None else 0}")
                    
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")
    
    # Data status indicator
    if st.session_state.data_loaded:
        st.success("📊 Data Loaded Successfully")
        if st.session_state.processed_data is not None:
            st.metric("Total Players", len(st.session_state.processed_data))
    else:
        st.warning("⚠️ No data loaded. Please upload an Excel file.")

# Main content area
if page == "Data Upload":
    st.markdown("## 📈 Data Overview & Upload")
    
    if not st.session_state.data_loaded:
        st.markdown("""
        ### Welcome to the 2025 NFL Draft Assistant
        
        This comprehensive analysis tool provides:
        
        #### 🔍 **Advanced Analytics**
        - AI-powered player evaluation algorithms
        - Statistical correlation analysis
        - Performance projection modeling
        - Risk assessment calculations
        
        #### 📊 **Comprehensive Insights**
        - Multi-dimensional player comparisons
        - Team fit analysis and positional value
        - Historical trend analysis
        - Draft simulation scenarios
        
        #### 🎯 **Key Features**
        - Real-time analytical updates
        - Interactive visualizations
        - Customizable analytical weights
        - Export analytical reports
        
        **To get started, please upload your Excel file using the sidebar.**
        """)
        
        # Sample data structure information
        with st.expander("📋 Expected Data Format"):
            st.markdown("""
            Your Excel file should contain multiple sheets with player data:
            
            **Required Columns (flexible naming):**
            - Player Name/Name
            - Position/Pos
            - College/School
            - Height/Ht
            - Weight/Wt
            - 40-yard dash/40 Time
            - Bench Press/Bench
            - Vertical Jump/Vert
            - Broad Jump/Broad
            - 3-Cone Drill/3Cone
            - 20-yard Shuttle/Shuttle
            - Grade/Overall/Rating
            """)
    
    else:
        # Display data overview
        st.markdown("### 📊 Loaded Data Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Sheets", len(st.session_state.draft_data))
        
        with col2:
            total_players = len(st.session_state.processed_data) if st.session_state.processed_data is not None else 0
            st.metric("Total Players", total_players)
        
        with col3:
            positions = st.session_state.processed_data['position'].nunique() if st.session_state.processed_data is not None else 0
            st.metric("Positions", positions)
        
        with col4:
            if st.session_state.processed_data is not None:
                avg_grade = st.session_state.processed_data['grade'].mean() if 'grade' in st.session_state.processed_data.columns else 0
                st.metric("Avg Grade", f"{avg_grade:.1f}")
        
        # Sheet breakdown
        st.markdown("#### 📋 Sheet Breakdown")
        sheet_info = []
        for sheet_name, df in st.session_state.draft_data.items():
            sheet_info.append({
                "Sheet Name": sheet_name,
                "Players": len(df),
                "Columns": len(df.columns),
                "Positions": df['position'].nunique() if 'position' in df.columns else 0
            })
        
        sheet_df = pd.DataFrame(sheet_info)
        st.dataframe(sheet_df, use_container_width=True)
        
        # Data preview
        if st.session_state.processed_data is not None:
            st.markdown("#### 👀 Data Preview")
            st.dataframe(st.session_state.processed_data.head(10), use_container_width=True)

elif page == "Player Analysis" and st.session_state.data_loaded:
    player_analysis = PlayerAnalysis(st.session_state.processed_data)
    player_analysis.render()

elif page == "Draft Simulator" and st.session_state.data_loaded:
    draft_simulator = DraftSimulator(st.session_state.processed_data)
    draft_simulator.render()

elif page == "Team Analysis" and st.session_state.data_loaded:
    team_analysis = TeamAnalysis(st.session_state.processed_data)
    team_analysis.render()

elif page == "AI Insights" and st.session_state.data_loaded:
    st.markdown("## 🤖 AI-Powered Insights")
    
    ai_analytics = AIAnalytics(st.session_state.processed_data)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Performance Predictions", "Risk Assessment", "Clustering Analysis", "Market Value"])
    
    with tab1:
        ai_analytics.render_performance_predictions()
    
    with tab2:
        ai_analytics.render_risk_assessment()
    
    with tab3:
        ai_analytics.render_clustering_analysis()
    
    with tab4:
        ai_analytics.render_market_value_analysis()

elif page == "Statistical Reports" and st.session_state.data_loaded:
    st.markdown("## 📈 Statistical Reports")
    
    visualizations = Visualizations(st.session_state.processed_data)
    
    report_type = st.selectbox(
        "Select Report Type",
        ["Comprehensive Overview", "Position Analysis", "Combine Metrics", "Statistical Correlations", "Performance Trends"]
    )
    
    if report_type == "Comprehensive Overview":
        visualizations.render_comprehensive_overview()
    elif report_type == "Position Analysis":
        visualizations.render_position_analysis()
    elif report_type == "Combine Metrics":
        visualizations.render_combine_metrics()
    elif report_type == "Statistical Correlations":
        visualizations.render_statistical_correlations()
    elif report_type == "Performance Trends":
        visualizations.render_performance_trends()

else:
    if not st.session_state.data_loaded:
        st.warning("⚠️ Please upload and process your draft data first using the sidebar.")
        st.markdown("### Getting Started")
        st.markdown("1. Use the sidebar to upload your Excel file")
        st.markdown("2. Click 'Process Data' to analyze the file")
        st.markdown("3. Navigate through different analysis modules")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>2025 NFL Draft Assistant | Advanced Analytics Platform</p>
    <p>Built with Streamlit • Powered by AI Analytics</p>
</div>
""", unsafe_allow_html=True)
