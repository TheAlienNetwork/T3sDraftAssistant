
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
import random

# Page configuration
st.set_page_config(
    page_title="Fantasy Football 2025 Rankings",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Advanced CSS for high-end styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .main {
        padding-top: 0rem;
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #24243e 50%, #302b63 100%);
        color: white;
    }
    
    .hero-header {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 3rem 2rem;
        margin: 2rem 0;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.15);
        box-shadow: 0 15px 35px rgba(0,0,0,0.1), 0 5px 15px rgba(0,0,0,0.07);
        position: relative;
        overflow: hidden;
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.02) 50%, transparent 70%);
        pointer-events: none;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        font-weight: 400;
        color: rgba(255,255,255,0.8);
        margin-bottom: 0;
    }
    
    .advanced-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .advanced-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        border-color: rgba(255,255,255,0.2);
    }
    
    .player-row {
        background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.03) 100%);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .player-row:hover {
        background: linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.06) 100%);
        transform: translateX(5px);
        border-color: rgba(255,255,255,0.2);
    }
    
    .rank-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1rem;
        margin-right: 1rem;
    }
    
    .rank-elite {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #000;
        box-shadow: 0 0 20px rgba(255,215,0,0.4);
    }
    
    .rank-high {
        background: linear-gradient(135deg, #C0C0C0 0%, #A8A8A8 100%);
        color: #000;
        box-shadow: 0 0 15px rgba(192,192,192,0.4);
    }
    
    .rank-medium {
        background: linear-gradient(135deg, #CD7F32 0%, #B8860B 100%);
        color: #fff;
        box-shadow: 0 0 10px rgba(205,127,50,0.4);
    }
    
    .rank-normal {
        background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.1) 100%);
        color: #fff;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .grade-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        text-align: center;
        margin: 0.2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: transform 0.2s ease;
        position: relative;
    }
    
    .grade-badge:hover {
        transform: scale(1.05);
    }
    
    .grade-elite {
        background: linear-gradient(135deg, #00ff87 0%, #60efff 100%);
        color: #000;
        font-weight: 700;
    }
    
    .grade-first-round {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: #fff;
    }
    
    .grade-early {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: #000;
    }
    
    .grade-mid {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: #000;
    }
    
    .grade-late {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        color: #000;
    }
    
    .grade-udfa {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #666;
    }
    
    .position-badge {
        display: inline-block;
        padding: 0.3rem 0.7rem;
        border-radius: 15px;
        font-weight: 600;
        font-size: 0.8rem;
        margin: 0.2rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .pos-qb { 
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
    }
    
    .pos-rb { 
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
    }
    
    .pos-wr { 
        background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
        color: white;
    }
    
    .pos-te { 
        background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
        color: white;
    }
    
    .pos-k { 
        background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%);
        color: white;
    }
    
    .pos-def { 
        background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
        color: white;
    }
    
    .draft-projection {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 12px;
        font-weight: 500;
        font-size: 0.75rem;
        margin: 0.1rem;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    
    .round-1 { background: #FFD700; color: #000; }
    .round-2 { background: #C0C0C0; color: #000; }
    .round-3 { background: #CD7F32; color: #fff; }
    .round-4-5 { background: #4ECDC4; color: #000; }
    .round-6-7 { background: #96CEB4; color: #000; }
    .udfa { background: #FF7675; color: #fff; }
    
    .news-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 1rem;
        margin-top: 0.5rem;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        font-style: italic;
        font-size: 0.9rem;
        color: rgba(255,255,255,0.8);
    }
    
    .ai-explanation {
        background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(102,126,234,0.2);
        backdrop-filter: blur(10px);
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        box-shadow: 0 5px 15px rgba(102,126,234,0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102,126,234,0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 10px;
        color: white;
        backdrop-filter: blur(10px);
    }
    
    .stMetric {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border-radius: 12px;
        padding: 1rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .filter-section {
        background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.04) 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(15px);
    }
</style>
""", unsafe_allow_html=True)

class AdvancedFantasyAnalyzer:
    """Advanced fantasy football analyzer with Yahoo Sports-style ranking."""
    
    def __init__(self):
        self.position_sheets = ['QB', 'RBs', 'WR', 'TE', 'K', 'DEF']
        self.sheet_variations = {
            'QB': ['QB', 'Quarterbacks', 'Quarterback', 'QBS'],
            'RB': ['RB', 'RBs', 'Running Back', 'Running Backs', 'RBS'],
            'WR': ['WR', 'WRs', 'Wide Receiver', 'Wide Receivers', 'WRS'],
            'TE': ['TE', 'TEs', 'Tight End', 'Tight Ends', 'TES'],
            'K': ['K', 'Kicker', 'Kickers', 'KS'],
            'DEF': ['DEF', 'Defense', 'Defenses', 'DST', 'D/ST']
        }
        
        # Advanced draft round projections based on position value
        self.position_draft_values = {
            'QB': {'elite': 1, 'tier1': 2, 'tier2': 3, 'tier3': 5, 'tier4': 7},
            'RB': {'elite': 1, 'tier1': 1, 'tier2': 2, 'tier3': 4, 'tier4': 6},
            'WR': {'elite': 1, 'tier1': 1, 'tier2': 2, 'tier3': 4, 'tier4': 6},
            'TE': {'elite': 2, 'tier1': 3, 'tier2': 4, 'tier3': 6, 'tier4': 7},
            'K': {'elite': 7, 'tier1': 7, 'tier2': 7, 'tier3': 7, 'tier4': 7},  # Kickers always late
            'DEF': {'elite': 6, 'tier1': 7, 'tier2': 7, 'tier3': 7, 'tier4': 7}  # Defense always late
        }
        
    def find_sheet_name(self, sheet_names: List[str], position: str) -> Optional[str]:
        """Find the actual sheet name for a position."""
        variations = self.sheet_variations.get(position, [position])
        
        for variation in variations:
            for sheet_name in sheet_names:
                if variation.lower() == sheet_name.lower():
                    return sheet_name
                elif variation.lower() in sheet_name.lower():
                    return sheet_name
        
        return None
        
    def process_excel_file(self, uploaded_file) -> pd.DataFrame:
        """Process Excel file and extract specific position sheets."""
        try:
            excel_file = pd.ExcelFile(uploaded_file, engine='openpyxl')
            available_sheets = excel_file.sheet_names
            
            st.info(f"📊 Available sheets: {', '.join(available_sheets)}")
            
            all_players = []
            
            for position in ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']:
                sheet_name = self.find_sheet_name(available_sheets, position)
                
                if sheet_name:
                    try:
                        df = pd.read_excel(uploaded_file, sheet_name=sheet_name, engine='openpyxl')
                        if not df.empty:
                            df.columns = [str(col).strip() for col in df.columns]
                            df['Position'] = position
                            df['Sheet_Source'] = sheet_name
                            
                            news_col = self.find_news_column(df)
                            if news_col:
                                df['News'] = df[news_col]
                            else:
                                df['News'] = 'No recent news'
                            
                            all_players.append(df)
                            st.success(f"✅ Loaded {position} data from '{sheet_name}' ({len(df)} players)")
                            
                    except Exception as e:
                        st.warning(f"⚠️ Error reading sheet '{sheet_name}' for {position}: {str(e)}")
                        continue
                else:
                    st.warning(f"❌ No sheet found for position {position}")
            
            if all_players:
                combined_df = pd.concat(all_players, ignore_index=True)
                return self.clean_and_grade_data(combined_df)
            else:
                return pd.DataFrame()
                
        except Exception as e:
            st.error(f"💥 Error processing Excel file: {str(e)}")
            return pd.DataFrame()
    
    def find_news_column(self, df: pd.DataFrame) -> Optional[str]:
        """Find the news column in the dataframe."""
        if len(df.columns) > 24:
            return df.columns[24]
        
        for col in df.columns:
            if 'news' in str(col).lower():
                return col
        
        for col in df.columns:
            if any(keyword in str(col).lower() for keyword in ['note', 'comment', 'update', 'status']):
                return col
        
        return None
    
    def clean_and_grade_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean data and generate advanced AI grades with draft projections."""
        name_col = None
        for col in df.columns:
            if df[col].notna().sum() > len(df) * 0.5:
                name_col = col
                break
        
        if name_col is None:
            name_col = df.columns[0]
        
        df['Player_Name'] = df[name_col].astype(str)
        df = df[df['Player_Name'].str.strip() != '']
        df = df[df['Player_Name'] != 'nan']
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Advanced AI grading system
        df['AI_Grade'] = df.apply(lambda row: self.generate_advanced_ai_grade(row, numeric_cols), axis=1)
        df['Overall_Rank'] = df['AI_Grade'].rank(ascending=False, method='dense').astype(int)
        df['Position_Rank'] = df.groupby('Position')['AI_Grade'].rank(ascending=False, method='dense').astype(int)
        
        # Draft round projections
        df['Draft_Round'] = df.apply(self.calculate_draft_round, axis=1)
        df['Draft_Projection'] = df.apply(self.get_draft_projection_text, axis=1)
        
        # AI explanations
        df['AI_Explanation'] = df.apply(lambda row: self.generate_advanced_explanation(row, numeric_cols), axis=1)
        
        if 'News' in df.columns:
            df['News'] = df['News'].fillna('No recent news').astype(str)
        
        return df
    
    def generate_advanced_ai_grade(self, player_row, numeric_cols) -> float:
        """Generate advanced AI grade with position-specific logic."""
        position = player_row.get('Position', 'UNKNOWN')
        base_grade = 50.0
        
        # Get numeric stats
        stats = {}
        for col in numeric_cols:
            if pd.notna(player_row.get(col)):
                stats[col] = player_row[col]
        
        if not stats:
            return base_grade + random.uniform(-10, 10)  # Add randomness for incomplete data
        
        # Position-specific advanced grading
        if position == 'QB':
            base_grade = self.grade_quarterback(stats, base_grade)
        elif position == 'RB':
            base_grade = self.grade_running_back(stats, base_grade)
        elif position == 'WR':
            base_grade = self.grade_wide_receiver(stats, base_grade)
        elif position == 'TE':
            base_grade = self.grade_tight_end(stats, base_grade)
        elif position == 'K':
            base_grade = self.grade_kicker(stats, base_grade)
        elif position == 'DEF':
            base_grade = self.grade_defense(stats, base_grade)
        
        # Add positional scarcity bonus/penalty
        position_scarcity = {'QB': 1.1, 'RB': 1.2, 'WR': 1.15, 'TE': 1.0, 'K': 0.7, 'DEF': 0.8}
        base_grade *= position_scarcity.get(position, 1.0)
        
        # Normalize and add variance
        final_grade = max(20, min(95, base_grade + random.uniform(-5, 5)))
        return final_grade
    
    def grade_quarterback(self, stats, base_grade):
        """Advanced QB grading."""
        for col, value in stats.items():
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in ['pass', 'completion', 'yard']):
                if value > 3000:  # High passing yards
                    base_grade += 20
                elif value > 2500:
                    base_grade += 15
                elif value > 2000:
                    base_grade += 10
            elif 'td' in col_lower and 'pass' in col_lower:
                if value > 25:  # High TD production
                    base_grade += 25
                elif value > 20:
                    base_grade += 20
                elif value > 15:
                    base_grade += 15
            elif 'int' in col_lower:
                base_grade -= min(value * 2, 15)  # Penalty for interceptions
            elif 'rating' in col_lower or 'qbr' in col_lower:
                if value > 100:
                    base_grade += 15
                elif value > 90:
                    base_grade += 10
        return base_grade
    
    def grade_running_back(self, stats, base_grade):
        """Advanced RB grading."""
        for col, value in stats.items():
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in ['rush', 'carry']):
                if value > 1200:  # High rushing yards
                    base_grade += 25
                elif value > 800:
                    base_grade += 20
                elif value > 500:
                    base_grade += 15
            elif 'td' in col_lower and 'rush' in col_lower:
                base_grade += value * 3  # TD bonus
            elif any(keyword in col_lower for keyword in ['rec', 'catch']):
                base_grade += value * 0.5  # Receiving bonus for RBs
        return base_grade
    
    def grade_wide_receiver(self, stats, base_grade):
        """Advanced WR grading."""
        for col, value in stats.items():
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in ['rec', 'catch']):
                if value > 80:  # High receptions
                    base_grade += 25
                elif value > 60:
                    base_grade += 20
                elif value > 40:
                    base_grade += 15
            elif 'yard' in col_lower and 'rec' in col_lower:
                if value > 1000:  # High receiving yards
                    base_grade += 25
                elif value > 800:
                    base_grade += 20
            elif 'td' in col_lower and 'rec' in col_lower:
                base_grade += value * 4  # TD bonus
            elif 'target' in col_lower:
                if value > 100:  # High target share
                    base_grade += 15
        return base_grade
    
    def grade_tight_end(self, stats, base_grade):
        """Advanced TE grading."""
        for col, value in stats.items():
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in ['rec', 'catch']):
                if value > 60:  # Good for TE
                    base_grade += 20
                elif value > 40:
                    base_grade += 15
            elif 'yard' in col_lower and 'rec' in col_lower:
                if value > 800:  # High for TE
                    base_grade += 20
            elif 'td' in col_lower and 'rec' in col_lower:
                base_grade += value * 5  # TE TDs are valuable
        return base_grade
    
    def grade_kicker(self, stats, base_grade):
        """Advanced K grading - intentionally lower due to late draft position."""
        base_grade = 35  # Start lower for kickers
        for col, value in stats.items():
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in ['fg', 'field', 'goal']):
                base_grade += min(value * 0.3, 15)  # Limited upside
            elif 'accuracy' in col_lower or '%' in col_lower:
                if value > 85:
                    base_grade += 10
        return base_grade
    
    def grade_defense(self, stats, base_grade):
        """Advanced DEF grading - intentionally lower due to late draft position."""
        base_grade = 40  # Start lower for defenses
        for col, value in stats.items():
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in ['sack', 'int', 'fumble']):
                base_grade += min(value * 0.5, 20)  # Limited upside
            elif 'td' in col_lower:
                base_grade += value * 2
        return base_grade
    
    def calculate_draft_round(self, player_row):
        """Calculate realistic draft round based on position and grade."""
        position = player_row.get('Position', 'UNKNOWN')
        grade = player_row.get('AI_Grade', 50)
        
        # Position-specific thresholds
        if position == 'QB':
            if grade >= 85: return 1
            elif grade >= 75: return 2
            elif grade >= 65: return 3
            elif grade >= 55: return 5
            else: return 7
        elif position in ['RB', 'WR']:
            if grade >= 90: return 1
            elif grade >= 80: return 1
            elif grade >= 70: return 2
            elif grade >= 60: return 4
            elif grade >= 50: return 6
            else: return 7
        elif position == 'TE':
            if grade >= 85: return 2
            elif grade >= 75: return 3
            elif grade >= 65: return 4
            elif grade >= 55: return 6
            else: return 7
        elif position == 'K':
            return 7  # Kickers always drafted late
        elif position == 'DEF':
            if grade >= 70: return 6
            else: return 7
        
        return 7  # Default late round
    
    def get_draft_projection_text(self, player_row):
        """Get draft projection text."""
        round_num = player_row.get('Draft_Round', 7)
        
        if round_num == 1:
            return "1st Round"
        elif round_num == 2:
            return "2nd Round"
        elif round_num == 3:
            return "3rd Round"
        elif round_num in [4, 5]:
            return f"{round_num}th Round"
        elif round_num in [6, 7]:
            return "Late Round"
        else:
            return "UDFA"
    
    def generate_advanced_explanation(self, player_row, numeric_cols) -> str:
        """Generate advanced AI explanation."""
        position = player_row.get('Position', 'UNKNOWN')
        grade = player_row.get('AI_Grade', 50)
        draft_round = player_row.get('Draft_Round', 7)
        
        explanation = f"**🧠 Advanced AI Analysis for {player_row.get('Player_Name', 'Unknown')}**\n\n"
        
        # Grade tier with more specific analysis
        if grade >= 85:
            explanation += "🔥 **Elite Tier (85+)**: Franchise-changing talent with immediate impact potential.\n\n"
        elif grade >= 75:
            explanation += "⭐ **First Round Tier (75-84)**: High-impact player with proven production metrics.\n\n"
        elif grade >= 65:
            explanation += "📈 **Early Round Tier (65-74)**: Solid contributor with upside potential.\n\n"
        elif grade >= 50:
            explanation += "📊 **Mid-Round Tier (50-64)**: Depth player with situational value.\n\n"
        else:
            explanation += "🎯 **Late Round/UDFA Tier (<50)**: Developmental prospect or camp body.\n\n"
        
        # Draft projection reasoning
        explanation += f"**📅 Draft Projection: {player_row.get('Draft_Projection', 'TBD')}**\n"
        
        if position == 'K':
            explanation += "• Kickers are consistently drafted in late rounds regardless of talent level\n"
            explanation += "• Fantasy value doesn't translate to early draft capital\n"
        elif position == 'DEF':
            explanation += "• Defensive units are typically selected in rounds 6-7\n"
            explanation += "• Team need and scheme fit outweigh individual metrics\n"
        else:
            explanation += f"• Position scarcity and NFL draft trends factored into projection\n"
            explanation += f"• {position} players at this grade level typically selected in Round {draft_round}\n"
        
        explanation += f"\n**Final AI Grade: {grade:.1f}/100**"
        
        return explanation
    
    def get_grade_class(self, grade: float) -> str:
        """Get CSS class for grade badge."""
        if grade >= 85:
            return 'grade-elite'
        elif grade >= 75:
            return 'grade-first-round'
        elif grade >= 65:
            return 'grade-early'
        elif grade >= 50:
            return 'grade-mid'
        elif grade >= 35:
            return 'grade-late'
        else:
            return 'grade-udfa'
    
    def get_rank_badge_class(self, rank: int) -> str:
        """Get CSS class for rank badge."""
        if rank <= 3:
            return 'rank-elite'
        elif rank <= 10:
            return 'rank-high'
        elif rank <= 25:
            return 'rank-medium'
        else:
            return 'rank-normal'
    
    def render_player_modal(self, player_data, all_stats_cols, position_data):
        """Render detailed player information with advanced styling."""
        st.markdown(f"""
        <div class="advanced-card">
            <h2 style="margin-bottom: 1rem;">🏈 {player_data['Player_Name']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced player basic info
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            position = player_data.get('Position', 'UNKNOWN')
            st.markdown(f'<span class="position-badge pos-{position.lower()}">{position}</span>', 
                       unsafe_allow_html=True)
        
        with col2:
            grade = player_data.get('AI_Grade', 0)
            grade_class = self.get_grade_class(grade)
            st.markdown(f'<div class="grade-badge {grade_class}">{grade:.1f}</div>', 
                       unsafe_allow_html=True)
        
        with col3:
            overall_rank = player_data.get('Overall_Rank', 'N/A')
            st.metric("Overall Rank", f"#{overall_rank}")
        
        with col4:
            pos_rank = player_data.get('Position_Rank', 'N/A')
            st.metric("Position Rank", f"#{pos_rank}")
        
        with col5:
            draft_proj = player_data.get('Draft_Projection', 'TBD')
            round_class = f"round-{player_data.get('Draft_Round', 7)}"
            st.markdown(f'<div class="draft-projection {round_class}">{draft_proj}</div>', 
                       unsafe_allow_html=True)
        
        # Enhanced tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Advanced Stats", "📰 News & Intel", "🧠 AI Deep Dive", "📈 Performance Charts"])
        
        with tab1:
            self.render_advanced_stats_tab(player_data, all_stats_cols)
        
        with tab2:
            self.render_news_tab(player_data)
        
        with tab3:
            self.render_ai_analysis_tab(player_data)
        
        with tab4:
            self.render_performance_charts_tab(player_data, position_data)
    
    def render_advanced_stats_tab(self, player_data, all_stats_cols):
        """Render advanced statistics tab."""
        st.markdown("### 📊 Advanced Statistical Analysis")
        
        stats_data = []
        for col in all_stats_cols:
            if col in player_data and pd.notna(player_data[col]):
                if isinstance(player_data[col], (int, float)):
                    stats_data.append({
                        'Statistic': col.replace('_', ' ').title(),
                        'Value': f"{player_data[col]:.1f}" if isinstance(player_data[col], float) else str(player_data[col])
                    })
        
        if stats_data:
            stats_df = pd.DataFrame(stats_data)
            st.dataframe(stats_df, hide_index=True, width='stretch')
        else:
            st.info("📋 No detailed statistics available for this player.")
    
    def render_news_tab(self, player_data):
        """Render enhanced news tab."""
        st.markdown("### 📰 Latest News & Intelligence")
        
        news = str(player_data.get('News', 'No recent news'))
        if news and news.strip() != 'No recent news' and news != 'nan':
            st.markdown(f'<div class="news-container">📝 {news}</div>', unsafe_allow_html=True)
        else:
            st.info("📰 No recent news or updates available for this player.")
    
    def render_ai_analysis_tab(self, player_data):
        """Render enhanced AI analysis tab."""
        st.markdown("### 🧠 AI Deep Dive Analysis")
        
        explanation = player_data.get('AI_Explanation', 'No analysis available.')
        st.markdown(f'<div class="ai-explanation">{explanation}</div>', unsafe_allow_html=True)
    
    def render_performance_charts_tab(self, player_data, position_data):
        """Render performance comparison charts."""
        st.markdown("### 📈 Performance Analysis & Comparisons")
        
        player_grade = player_data.get('AI_Grade', 0)
        player_rank = player_data.get('Position_Rank', 0)
        position = player_data.get('Position', 'UNKNOWN')
        
        # Enhanced grade distribution plot
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=position_data['AI_Grade'],
            nbinsx=20,
            name=f'All {position} Players',
            opacity=0.7,
            marker_color='rgba(102, 126, 234, 0.7)'
        ))
        
        fig.add_vline(
            x=player_grade,
            line_dash="dash",
            line_color="#FFD700",
            line_width=3,
            annotation_text=f"{player_data['Player_Name']}: {player_grade:.1f}",
            annotation_position="top"
        )
        
        fig.update_layout(
            title=f"{position} AI Grade Distribution",
            xaxis_title="AI Grade",
            yaxis_title="Number of Players",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Enhanced comparison metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Players Ranked Higher", player_rank - 1 if player_rank > 0 else 0)
        
        with col2:
            st.metric("Players Ranked Lower", len(position_data) - player_rank if player_rank > 0 else len(position_data))
        
        with col3:
            percentile = ((len(position_data) - player_rank + 1) / len(position_data)) * 100 if player_rank > 0 else 0
            st.metric("Percentile Rank", f"{percentile:.0f}%")

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'players_data' not in st.session_state:
    st.session_state.players_data = pd.DataFrame()

# Enhanced Hero Header
st.markdown("""
<div class="hero-header">
    <h1 class="hero-title">Fantasy Football 2025</h1>
    <p class="hero-subtitle">🚀 Advanced AI-Powered Player Rankings & Draft Analysis</p>
</div>
""", unsafe_allow_html=True)

# Initialize analyzer
analyzer = AdvancedFantasyAnalyzer()

# Enhanced file upload section
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "📊 Upload Fantasy Football Excel File",
    type=['xlsx', 'xls'],
    help="Upload your Excel file with player data for advanced AI analysis"
)

if uploaded_file is not None:
    if st.button("🚀 Launch Advanced Analysis", type="primary"):
        with st.spinner("🔄 Processing with advanced AI algorithms..."):
            try:
                players_data = analyzer.process_excel_file(uploaded_file)
                
                if not players_data.empty:
                    st.session_state.players_data = players_data
                    st.session_state.data_loaded = True
                    st.balloons()
                    st.success(f"✅ Successfully analyzed {len(players_data)} players with advanced AI!")
                else:
                    st.error("❌ No player data found in the uploaded file.")
                    
            except Exception as e:
                st.error(f"💥 Error processing file: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# Enhanced main content
if st.session_state.data_loaded and not st.session_state.players_data.empty:
    data = st.session_state.players_data
    
    # Advanced filters section
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        positions = ['All Positions'] + sorted(data['Position'].unique().tolist())
        selected_position = st.selectbox("🎯 Position Filter", positions)
    
    with col2:
        min_grade = st.slider("📊 Minimum AI Grade", 0.0, 100.0, 0.0, 5.0)
    
    with col3:
        top_n = st.selectbox("📈 Display Count", [25, 50, 100, 200, "All"])
    
    with col4:
        search_term = st.text_input("🔍 Search Player", placeholder="Enter player name...")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply filters
    filtered_data = data.copy()
    
    if selected_position != 'All Positions':
        filtered_data = filtered_data[filtered_data['Position'] == selected_position]
    
    filtered_data = filtered_data[filtered_data['AI_Grade'] >= min_grade]
    
    if search_term:
        filtered_data = filtered_data[
            filtered_data['Player_Name'].str.contains(search_term, case=False, na=False)
        ]
    
    # Yahoo Sports-style ranking: Overall ranking when "All Positions" selected
    if selected_position == 'All Positions':
        # Sort by overall rank (which is based on AI_Grade across all positions)
        filtered_data = filtered_data.sort_values('Overall_Rank', ascending=True)
    else:
        # Sort by position rank when specific position selected
        filtered_data = filtered_data.sort_values('Position_Rank', ascending=True)
    
    if top_n != "All":
        filtered_data = filtered_data.head(top_n)
    
    if filtered_data.empty:
        st.warning("⚠️ No players match the selected filters.")
    else:
        # Enhanced summary metrics
        st.markdown('<div class="advanced-card">', unsafe_allow_html=True)
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
            elite_count = len(filtered_data[filtered_data['AI_Grade'] >= 85])
            st.metric("Elite Players (85+)", elite_count)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Enhanced player display with Yahoo Sports-style ranking
        st.markdown("### 🏆 Advanced Player Rankings")
        st.markdown("*Click on any player for detailed AI analysis and projections*")
        
        for idx, (_, player) in enumerate(filtered_data.iterrows()):
            # Use appropriate rank based on filter
            if selected_position == 'All Positions':
                display_rank = player['Overall_Rank']
                rank_label = "Overall"
            else:
                display_rank = player['Position_Rank']
                rank_label = selected_position
            
            rank_class = analyzer.get_rank_badge_class(display_rank)
            
            # Enhanced player row
            player_container = st.container()
            with player_container:
                col_rank, col_player, col_pos, col_grade, col_proj, col_news = st.columns([1, 3, 1, 1, 1, 4])
                
                with col_rank:
                    st.markdown(f'<div class="rank-badge {rank_class}">#{display_rank}</div>', 
                               unsafe_allow_html=True)
                    st.markdown(f"<small>{rank_label}</small>", unsafe_allow_html=True)
                
                with col_player:
                    if st.button(f"🏈 {player['Player_Name']}", key=f"player_{idx}", use_container_width=True):
                        st.session_state.selected_player = player
                
                with col_pos:
                    position = player.get('Position', 'UNKNOWN')
                    st.markdown(f'<span class="position-badge pos-{position.lower()}">{position}</span>', 
                               unsafe_allow_html=True)
                
                with col_grade:
                    grade = player.get('AI_Grade', 0)
                    grade_class = analyzer.get_grade_class(grade)
                    st.markdown(f'<div class="grade-badge {grade_class}">{grade:.1f}</div>', 
                               unsafe_allow_html=True)
                
                with col_proj:
                    draft_proj = player.get('Draft_Projection', 'TBD')
                    round_num = player.get('Draft_Round', 7)
                    if round_num == 1:
                        proj_class = 'round-1'
                    elif round_num == 2:
                        proj_class = 'round-2'
                    elif round_num == 3:
                        proj_class = 'round-3'
                    elif round_num in [4, 5]:
                        proj_class = 'round-4-5'
                    elif round_num in [6, 7]:
                        proj_class = 'round-6-7'
                    else:
                        proj_class = 'udfa'
                    
                    st.markdown(f'<div class="draft-projection {proj_class}">{draft_proj}</div>', 
                               unsafe_allow_html=True)
                
                with col_news:
                    news = str(player.get('News', 'No recent news'))
                    if len(news) > 120:
                        news = news[:120] + "..."
                    st.markdown(f"<div class='news-container'>{news}</div>", unsafe_allow_html=True)
        
        # Display selected player details
        if 'selected_player' in st.session_state:
            st.markdown("---")
            
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            numeric_cols = [col for col in numeric_cols if col not in ['AI_Grade', 'Overall_Rank', 'Position_Rank', 'Draft_Round']]
            
            player_position = st.session_state.selected_player['Position']
            position_data = data[data['Position'] == player_position]
            
            analyzer.render_player_modal(st.session_state.selected_player, numeric_cols, position_data)

else:
    # Enhanced welcome section
    st.markdown("""
    <div class="advanced-card" style="text-align: center; padding: 3rem;">
        <h3 style="color: #667eea;">🚀 Welcome to Advanced Fantasy Analytics</h3>
        <p style="font-size: 1.1rem; margin: 1.5rem 0;">Upload your Excel file to unlock AI-powered insights!</p>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin: 2rem 0;">
            <div class="metric-card">
                <h4>🧠 Advanced AI Grading</h4>
                <p>Position-specific algorithms with draft round projections</p>
            </div>
            <div class="metric-card">
                <h4>📊 Yahoo Sports Style</h4>
                <p>Professional ranking system with overall and position rankings</p>
            </div>
            <div class="metric-card">
                <h4>🎯 Smart Draft Logic</h4>
                <p>Realistic projections - Kickers in late rounds, elite skill players early</p>
            </div>
        </div>
        
        <p><strong>Supported sheets:</strong> QB, RB/RBs, WR/WRs, TE/TEs, K/Kickers, DEF/Defense</p>
    </div>
    """, unsafe_allow_html=True)

# Enhanced footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: rgba(255,255,255,0.6); padding: 2rem;'>
    <p style="font-size: 1.1rem; font-weight: 600;">Fantasy Football 2025 | Advanced AI Analytics Platform</p>
    <p>Powered by Next-Generation Machine Learning • Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
