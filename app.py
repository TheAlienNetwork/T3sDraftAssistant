
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import io
import base64
import re
from typing import Dict, List, Optional

# Page configuration
st.set_page_config(
    page_title="Fantasy Football 2025 Rankings",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    
    .player-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        color: white;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    .grade-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1.2rem;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 15px 0 rgba(31, 38, 135, 0.4);
    }
    
    .grade-elite {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
    }
    
    .grade-high {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
    }
    
    .grade-medium {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
    }
    
    .grade-low {
        background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%);
        color: white;
    }
    
    .position-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.2rem;
    }
    
    .pos-qb { background: #e74c3c; color: white; }
    .pos-rb { background: #3498db; color: white; }
    .pos-wr { background: #f39c12; color: white; }
    .pos-te { background: #27ae60; color: white; }
    .pos-k { background: #9b59b6; color: white; }
    .pos-def { background: #34495e; color: white; }
    
    .news-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        margin-top: 10px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .metric-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px;
        margin: 5px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

class SimpleFantasyAnalyzer:
    """Simplified fantasy football analyzer for specific position sheets."""
    
    def __init__(self):
        self.position_sheets = ['QB', 'RBs', 'WR', 'TE', 'K', 'DEF']
        self.colors = {
            'QB': '#e74c3c',
            'RB': '#3498db', 
            'WR': '#f39c12',
            'TE': '#27ae60',
            'K': '#9b59b6',
            'DEF': '#34495e'
        }
        
    def process_excel_file(self, uploaded_file) -> pd.DataFrame:
        """Process Excel file and extract specific position sheets."""
        try:
            all_players = []
            
            # Read specific sheets
            for sheet_name in self.position_sheets:
                try:
                    df = pd.read_excel(uploaded_file, sheet_name=sheet_name, engine='openpyxl')
                    if not df.empty:
                        # Clean column names
                        df.columns = [str(col).strip() for col in df.columns]
                        
                        # Add position from sheet name
                        position = 'RB' if sheet_name == 'RBs' else sheet_name
                        df['Position'] = position
                        df['Sheet_Source'] = sheet_name
                        
                        # Get news from column Y (index 24)
                        if len(df.columns) > 24:
                            df['News'] = df.iloc[:, 24]  # Column Y
                        else:
                            df['News'] = ''
                        
                        all_players.append(df)
                        
                except Exception as e:
                    st.warning(f"Could not read sheet '{sheet_name}': {str(e)}")
                    continue
            
            if all_players:
                combined_df = pd.concat(all_players, ignore_index=True)
                return self.clean_and_grade_data(combined_df)
            else:
                return pd.DataFrame()
                
        except Exception as e:
            st.error(f"Error processing Excel file: {str(e)}")
            return pd.DataFrame()
    
    def clean_and_grade_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean data and generate AI grades."""
        # Identify player name column (usually first non-empty column)
        name_col = None
        for col in df.columns:
            if df[col].notna().sum() > len(df) * 0.5:  # More than 50% non-null
                name_col = col
                break
        
        if name_col is None:
            name_col = df.columns[0]
        
        df['Player_Name'] = df[name_col].astype(str)
        
        # Remove rows with no player name
        df = df[df['Player_Name'].str.strip() != '']
        df = df[df['Player_Name'] != 'nan']
        
        # Extract numeric columns for stats
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Generate AI grades based on position and stats
        df['AI_Grade'] = df.apply(lambda row: self.generate_ai_grade(row, numeric_cols), axis=1)
        df['AI_Rank'] = df.groupby('Position')['AI_Grade'].rank(ascending=False, method='dense').astype(int)
        
        # Clean news column
        if 'News' in df.columns:
            df['News'] = df['News'].fillna('No recent news').astype(str)
        
        return df
    
    def generate_ai_grade(self, player_row, numeric_cols) -> float:
        """Generate AI grade based on position and available stats."""
        position = player_row.get('Position', 'UNKNOWN')
        base_grade = 50.0
        
        # Get numeric stats
        stats = {}
        for col in numeric_cols:
            if pd.notna(player_row.get(col)):
                stats[col] = player_row[col]
        
        if not stats:
            return base_grade
        
        # Position-specific grading
        if position == 'QB':
            # Look for passing stats, completions, TDs, etc.
            for col, value in stats.items():
                col_lower = str(col).lower()
                if any(keyword in col_lower for keyword in ['pass', 'td', 'completion', 'yard']):
                    if value > 0:
                        base_grade += min(value * 0.1, 15)
                elif 'int' in col_lower and 'interception' in col_lower:
                    base_grade -= min(value * 2, 10)
        
        elif position == 'RB':
            # Look for rushing stats
            for col, value in stats.items():
                col_lower = str(col).lower()
                if any(keyword in col_lower for keyword in ['rush', 'yard', 'td', 'carry']):
                    if value > 0:
                        base_grade += min(value * 0.15, 20)
        
        elif position == 'WR':
            # Look for receiving stats
            for col, value in stats.items():
                col_lower = str(col).lower()
                if any(keyword in col_lower for keyword in ['rec', 'catch', 'yard', 'td', 'target']):
                    if value > 0:
                        base_grade += min(value * 0.12, 18)
        
        elif position == 'TE':
            # Similar to WR but slightly different weighting
            for col, value in stats.items():
                col_lower = str(col).lower()
                if any(keyword in col_lower for keyword in ['rec', 'catch', 'yard', 'td']):
                    if value > 0:
                        base_grade += min(value * 0.1, 15)
        
        elif position == 'K':
            # Look for kicking stats
            for col, value in stats.items():
                col_lower = str(col).lower()
                if any(keyword in col_lower for keyword in ['fg', 'field', 'goal', 'point', 'extra']):
                    if value > 0:
                        base_grade += min(value * 0.2, 25)
        
        elif position == 'DEF':
            # Look for defensive stats
            for col, value in stats.items():
                col_lower = str(col).lower()
                if any(keyword in col_lower for keyword in ['sack', 'int', 'td', 'fumble', 'safety']):
                    if value > 0:
                        base_grade += min(value * 0.3, 20)
        
        # Normalize to 0-100 scale
        return max(0, min(100, base_grade))
    
    def get_grade_class(self, grade: float) -> str:
        """Get CSS class for grade badge."""
        if grade >= 80:
            return 'grade-elite'
        elif grade >= 70:
            return 'grade-high'
        elif grade >= 60:
            return 'grade-medium'
        else:
            return 'grade-low'
    
    def render_player_modal(self, player_data, all_stats_cols):
        """Render detailed player information in modal."""
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Player info
            st.markdown(f"### {player_data['Player_Name']}")
            
            position = player_data.get('Position', 'UNKNOWN')
            st.markdown(f'<span class="position-badge pos-{position.lower()}">{position}</span>', 
                       unsafe_allow_html=True)
            
            # AI Grade
            grade = player_data.get('AI_Grade', 0)
            rank = player_data.get('AI_Rank', 'N/A')
            grade_class = self.get_grade_class(grade)
            
            st.markdown(f'<div class="grade-badge {grade_class}">{grade:.1f}</div>', 
                       unsafe_allow_html=True)
            
            st.markdown(f"**AI Rank:** #{rank} {position}")
        
        with col2:
            # Stats
            st.markdown("#### Player Statistics")
            
            stats_data = []
            for col in all_stats_cols:
                if col in player_data and pd.notna(player_data[col]):
                    if isinstance(player_data[col], (int, float)):
                        stats_data.append({
                            'Stat': col,
                            'Value': f"{player_data[col]:.1f}" if isinstance(player_data[col], float) else str(player_data[col])
                        })
            
            if stats_data:
                stats_df = pd.DataFrame(stats_data)
                st.dataframe(stats_df, hide_index=True, use_container_width=True)
        
        # News section
        if 'News' in player_data and str(player_data['News']).strip() != 'No recent news':
            st.markdown("#### Latest News")
            st.markdown(f'<div class="news-container">{player_data["News"]}</div>', 
                       unsafe_allow_html=True)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'players_data' not in st.session_state:
    st.session_state.players_data = pd.DataFrame()

# Header
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="color: #667eea; font-size: 3rem; margin-bottom: 0;">🏈 Fantasy Football 2025</h1>
    <p style="color: #764ba2; font-size: 1.2rem;">AI-Powered Player Rankings & Analysis</p>
</div>
""", unsafe_allow_html=True)

# Initialize analyzer
analyzer = SimpleFantasyAnalyzer()

# File upload section
uploaded_file = st.file_uploader(
    "Upload Fantasy Football Excel File",
    type=['xlsx', 'xls'],
    help="Upload your Excel file with QB, RBs, WR, TE, K, DEF sheets"
)

if uploaded_file is not None:
    if st.button("🚀 Process Fantasy Data", type="primary"):
        with st.spinner("Processing fantasy football data..."):
            try:
                players_data = analyzer.process_excel_file(uploaded_file)
                
                if not players_data.empty:
                    st.session_state.players_data = players_data
                    st.session_state.data_loaded = True
                    st.success(f"✅ Successfully processed {len(players_data)} players!")
                else:
                    st.error("No player data found in the uploaded file.")
                    
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")

# Main content
if st.session_state.data_loaded and not st.session_state.players_data.empty:
    data = st.session_state.players_data
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        positions = ['All'] + sorted(data['Position'].unique().tolist())
        selected_position = st.selectbox("🎯 Position", positions)
    
    with col2:
        # Grade filter
        min_grade = st.slider("📊 Minimum AI Grade", 0.0, 100.0, 0.0, 5.0)
    
    with col3:
        # Top N players
        top_n = st.selectbox("📈 Show Top N Players", [25, 50, 100, 200, "All"])
    
    with col4:
        # Search
        search_term = st.text_input("🔍 Search Player", placeholder="Enter player name...")
    
    # Apply filters
    filtered_data = data.copy()
    
    if selected_position != 'All':
        filtered_data = filtered_data[filtered_data['Position'] == selected_position]
    
    filtered_data = filtered_data[filtered_data['AI_Grade'] >= min_grade]
    
    if search_term:
        filtered_data = filtered_data[
            filtered_data['Player_Name'].str.contains(search_term, case=False, na=False)
        ]
    
    # Sort by AI Grade
    filtered_data = filtered_data.sort_values('AI_Grade', ascending=False)
    
    if top_n != "All":
        filtered_data = filtered_data.head(top_n)
    
    if filtered_data.empty:
        st.warning("No players match the selected filters.")
    else:
        # Summary metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Players", len(filtered_data))
        with col2:
            avg_grade = filtered_data['AI_Grade'].mean()
            st.metric("Avg AI Grade", f"{avg_grade:.1f}")
        with col3:
            top_grade = filtered_data['AI_Grade'].max()
            st.metric("Highest Grade", f"{top_grade:.1f}")
        with col4:
            positions_count = filtered_data['Position'].nunique()
            st.metric("Positions", positions_count)
        with col5:
            elite_count = len(filtered_data[filtered_data['AI_Grade'] >= 80])
            st.metric("Elite Players (80+)", elite_count)
        
        st.markdown("---")
        
        # Player selection for detailed view
        st.markdown("### 🎯 Click on a player to see detailed analysis")
        
        # Create clickable player table
        for idx, (_, player) in enumerate(filtered_data.iterrows()):
            col_rank, col_player, col_pos, col_grade, col_news = st.columns([1, 3, 1, 1, 4])
            
            with col_rank:
                st.markdown(f"**#{idx + 1}**")
            
            with col_player:
                if st.button(f"{player['Player_Name']}", key=f"player_{idx}"):
                    st.session_state.selected_player = player
            
            with col_pos:
                position = player.get('Position', 'UNKNOWN')
                st.markdown(f'<span class="position-badge pos-{position.lower()}">{position}</span>', 
                           unsafe_allow_html=True)
            
            with col_grade:
                grade = player.get('AI_Grade', 0)
                grade_class = analyzer.get_grade_class(grade)
                st.markdown(f'<div class="grade-badge {grade_class}" style="font-size: 0.9rem; padding: 0.3rem 0.6rem;">{grade:.1f}</div>', 
                           unsafe_allow_html=True)
            
            with col_news:
                news = str(player.get('News', 'No recent news'))
                if len(news) > 100:
                    news = news[:100] + "..."
                st.markdown(f"*{news}*")
        
        # Display selected player details
        if 'selected_player' in st.session_state:
            st.markdown("---")
            st.markdown("### 📊 Player Analysis")
            
            # Get all numeric columns for stats display
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            # Remove our added columns
            numeric_cols = [col for col in numeric_cols if col not in ['AI_Grade', 'AI_Rank']]
            
            analyzer.render_player_modal(st.session_state.selected_player, numeric_cols)

else:
    # Welcome message
    st.markdown("""
    <div style="text-align: center; padding: 3rem;">
        <h3>Welcome to Fantasy Football 2025 Analytics</h3>
        <p>Upload your Excel file with player data to get started!</p>
        <p><strong>Required sheets:</strong> QB, RBs, WR, TE, K, DEF</p>
        <p><strong>Column Y should contain news for each player</strong></p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>Fantasy Football 2025 | AI-Powered Analytics</p>
    <p>Built with Streamlit • Powered by Advanced AI</p>
</div>
""", unsafe_allow_html=True)
