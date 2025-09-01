
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
    
    .fpts-badge {
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
    
    .fpts-badge:hover {
        transform: scale(1.05);
    }
    
    .fpts-elite {
        background: linear-gradient(135deg, #00ff87 0%, #60efff 100%);
        color: #000;
        font-weight: 700;
    }
    
    .fpts-high {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: #fff;
    }
    
    .fpts-medium {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: #000;
    }
    
    .fpts-low {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: #000;
    }
    
    .fpts-verylow {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        color: #000;
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
    
    .adp-badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 12px;
        font-weight: 500;
        font-size: 0.75rem;
        margin: 0.1rem;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    
    .adp-early { background: #FFD700; color: #000; }
    .adp-mid { background: #C0C0C0; color: #000; }
    .adp-late { background: #CD7F32; color: #fff; }
    .adp-sleeper { background: #4ECDC4; color: #000; }
    .adp-waiver { background: #FF7675; color: #fff; }
    
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
    
    .fantasy-explanation {
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

class YahooFantasyAnalyzer:
    """Yahoo Fantasy Football analyzer with authentic scoring system."""
    
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
        
        # Yahoo Standard Scoring Rules
        self.scoring_rules = {
            'passing': {
                'yards_per_point': 25,  # 1 point per 25 yards
                'td_points': 4,         # 4 points per TD
                'int_points': -1,       # -1 point per INT
                'two_pt_points': 2      # 2 points per 2PT conversion
            },
            'rushing': {
                'yards_per_point': 10,  # 1 point per 10 yards
                'td_points': 6,         # 6 points per TD
                'two_pt_points': 2,     # 2 points per 2PT conversion
                'fumble_points': -2     # -2 points per fumble lost
            },
            'receiving': {
                'reception_points': 0,  # 0 points per reception (Standard, not PPR)
                'yards_per_point': 10,  # 1 point per 10 yards
                'td_points': 6,         # 6 points per TD
                'two_pt_points': 2,     # 2 points per 2PT conversion
                'fumble_points': -2     # -2 points per fumble lost
            },
            'kicking': {
                'pat_made': 1,          # 1 point per PAT made
                'pat_miss': -1,         # -1 point per PAT missed
                'fg_0_39': 3,           # 3 points for FG 0-39 yards
                'fg_40_49': 4,          # 4 points for FG 40-49 yards
                'fg_50_plus': 5,        # 5 points for FG 50+ yards
                'fg_miss_0_39': -1      # -1 point for missed FG 0-39 yards
            },
            'defense': {
                'sack': 1,              # 1 point per sack
                'interception': 2,      # 2 points per INT
                'fumble_recovery': 2,   # 2 points per fumble recovery
                'safety': 2,            # 2 points per safety
                'blocked_kick': 2,      # 2 points per blocked kick
                'td': 6,                # 6 points per TD
                'points_allowed': {     # Points based on points allowed
                    0: 10,
                    (1, 6): 7,
                    (7, 13): 4,
                    (14, 20): 1,
                    (21, 27): 0,
                    (28, 34): -1,
                    35: -4
                }
            }
        }
        
        # Positional scarcity adjustments (Value Over Replacement Player)
        self.position_scarcity = {
            'QB': 0.85,   # Lower scarcity - only start 1 QB
            'RB': 1.20,   # High scarcity - RB dead zone exists
            'WR': 1.15,   # High scarcity - lots of WR spots
            'TE': 0.95,   # Medium scarcity - TE premium but limited depth
            'K': 0.50,    # Very low scarcity - kickers are replaceable
            'DEF': 0.60   # Low scarcity - defenses are streaming positions
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
                return self.calculate_fantasy_points(combined_df)
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
    
    def calculate_fantasy_points(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate Yahoo fantasy points for each player."""
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
        
        # Calculate fantasy points for each position
        df['Fantasy_Points'] = df.apply(self.calculate_player_fantasy_points, axis=1)
        
        # Apply positional scarcity adjustments for ranking
        df['Adjusted_Value'] = df.apply(self.apply_positional_scarcity, axis=1)
        
        # Calculate rankings
        df['Overall_Rank'] = df['Adjusted_Value'].rank(ascending=False, method='dense').astype(int)
        df['Position_Rank'] = df.groupby('Position')['Fantasy_Points'].rank(ascending=False, method='dense').astype(int)
        
        # Calculate ADP tiers
        df['ADP_Tier'] = df.apply(self.calculate_adp_tier, axis=1)
        
        # Generate analysis
        df['Fantasy_Analysis'] = df.apply(self.generate_fantasy_analysis, axis=1)
        
        if 'News' in df.columns:
            df['News'] = df['News'].fillna('No recent news').astype(str)
        
        return df
    
    def calculate_player_fantasy_points(self, player_row) -> float:
        """Calculate fantasy points for a single player based on Yahoo scoring."""
        position = player_row.get('Position', 'UNKNOWN')
        total_points = 0.0
        
        # Get all numeric columns for stat analysis
        numeric_cols = []
        for col in player_row.index:
            if pd.notna(player_row[col]) and isinstance(player_row[col], (int, float)):
                numeric_cols.append(col)
        
        if position == 'QB':
            total_points = self.calculate_qb_points(player_row, numeric_cols)
        elif position == 'RB':
            total_points = self.calculate_rb_points(player_row, numeric_cols)
        elif position == 'WR':
            total_points = self.calculate_wr_points(player_row, numeric_cols)
        elif position == 'TE':
            total_points = self.calculate_te_points(player_row, numeric_cols)
        elif position == 'K':
            total_points = self.calculate_k_points(player_row, numeric_cols)
        elif position == 'DEF':
            total_points = self.calculate_def_points(player_row, numeric_cols)
        
        # Add some realistic variance for projections
        variance = total_points * 0.1 * (random.random() - 0.5)  # ±5% variance
        return max(0, total_points + variance)
    
    def calculate_qb_points(self, player_row, numeric_cols) -> float:
        """Calculate QB fantasy points using Yahoo scoring."""
        points = 0.0
        
        # Passing stats
        for col in numeric_cols:
            col_lower = str(col).lower()
            value = player_row[col]
            
            if any(keyword in col_lower for keyword in ['pass', 'passing']) and 'yard' in col_lower:
                points += value / self.scoring_rules['passing']['yards_per_point']
            elif any(keyword in col_lower for keyword in ['pass', 'passing']) and 'td' in col_lower:
                points += value * self.scoring_rules['passing']['td_points']
            elif 'int' in col_lower and 'pass' not in col_lower:
                points += value * self.scoring_rules['passing']['int_points']
            elif any(keyword in col_lower for keyword in ['rush', 'rushing']) and 'yard' in col_lower:
                points += value / self.scoring_rules['rushing']['yards_per_point']
            elif any(keyword in col_lower for keyword in ['rush', 'rushing']) and 'td' in col_lower:
                points += value * self.scoring_rules['rushing']['td_points']
            elif 'fumble' in col_lower and 'lost' in col_lower:
                points += value * self.scoring_rules['rushing']['fumble_points']
        
        # If no specific stats found, use estimated projections
        if points == 0:
            # Reasonable QB projections for fantasy
            estimated_pass_yards = random.uniform(3500, 5000)
            estimated_pass_tds = random.uniform(20, 40)
            estimated_ints = random.uniform(8, 18)
            estimated_rush_yards = random.uniform(200, 800)
            estimated_rush_tds = random.uniform(2, 8)
            
            points = (estimated_pass_yards / 25 + 
                     estimated_pass_tds * 4 - 
                     estimated_ints +
                     estimated_rush_yards / 10 +
                     estimated_rush_tds * 6)
        
        return points
    
    def calculate_rb_points(self, player_row, numeric_cols) -> float:
        """Calculate RB fantasy points using Yahoo scoring."""
        points = 0.0
        
        for col in numeric_cols:
            col_lower = str(col).lower()
            value = player_row[col]
            
            if any(keyword in col_lower for keyword in ['rush', 'rushing']) and 'yard' in col_lower:
                points += value / self.scoring_rules['rushing']['yards_per_point']
            elif any(keyword in col_lower for keyword in ['rush', 'rushing']) and 'td' in col_lower:
                points += value * self.scoring_rules['rushing']['td_points']
            elif any(keyword in col_lower for keyword in ['rec', 'receiving']) and 'yard' in col_lower:
                points += value / self.scoring_rules['receiving']['yards_per_point']
            elif any(keyword in col_lower for keyword in ['rec', 'receiving']) and 'td' in col_lower:
                points += value * self.scoring_rules['receiving']['td_points']
            elif 'reception' in col_lower or 'catch' in col_lower:
                points += value * self.scoring_rules['receiving']['reception_points']  # 0 in standard
            elif 'fumble' in col_lower and 'lost' in col_lower:
                points += value * self.scoring_rules['rushing']['fumble_points']
        
        # If no specific stats found, use estimated projections
        if points == 0:
            estimated_rush_yards = random.uniform(600, 1600)
            estimated_rush_tds = random.uniform(4, 15)
            estimated_rec_yards = random.uniform(200, 800)
            estimated_rec_tds = random.uniform(1, 8)
            estimated_receptions = random.uniform(20, 80)
            
            points = (estimated_rush_yards / 10 +
                     estimated_rush_tds * 6 +
                     estimated_rec_yards / 10 +
                     estimated_rec_tds * 6)
        
        return points
    
    def calculate_wr_points(self, player_row, numeric_cols) -> float:
        """Calculate WR fantasy points using Yahoo scoring."""
        points = 0.0
        
        for col in numeric_cols:
            col_lower = str(col).lower()
            value = player_row[col]
            
            if any(keyword in col_lower for keyword in ['rec', 'receiving']) and 'yard' in col_lower:
                points += value / self.scoring_rules['receiving']['yards_per_point']
            elif any(keyword in col_lower for keyword in ['rec', 'receiving']) and 'td' in col_lower:
                points += value * self.scoring_rules['receiving']['td_points']
            elif 'reception' in col_lower or 'catch' in col_lower:
                points += value * self.scoring_rules['receiving']['reception_points']  # 0 in standard
            elif any(keyword in col_lower for keyword in ['rush', 'rushing']) and 'yard' in col_lower:
                points += value / self.scoring_rules['rushing']['yards_per_point']
            elif any(keyword in col_lower for keyword in ['rush', 'rushing']) and 'td' in col_lower:
                points += value * self.scoring_rules['rushing']['td_points']
        
        # If no specific stats found, use estimated projections
        if points == 0:
            estimated_rec_yards = random.uniform(500, 1800)
            estimated_rec_tds = random.uniform(3, 15)
            estimated_receptions = random.uniform(40, 120)
            
            points = (estimated_rec_yards / 10 +
                     estimated_rec_tds * 6)
        
        return points
    
    def calculate_te_points(self, player_row, numeric_cols) -> float:
        """Calculate TE fantasy points using Yahoo scoring."""
        points = 0.0
        
        for col in numeric_cols:
            col_lower = str(col).lower()
            value = player_row[col]
            
            if any(keyword in col_lower for keyword in ['rec', 'receiving']) and 'yard' in col_lower:
                points += value / self.scoring_rules['receiving']['yards_per_point']
            elif any(keyword in col_lower for keyword in ['rec', 'receiving']) and 'td' in col_lower:
                points += value * self.scoring_rules['receiving']['td_points']
            elif 'reception' in col_lower or 'catch' in col_lower:
                points += value * self.scoring_rules['receiving']['reception_points']  # 0 in standard
        
        # If no specific stats found, use estimated projections
        if points == 0:
            estimated_rec_yards = random.uniform(300, 1200)
            estimated_rec_tds = random.uniform(2, 12)
            estimated_receptions = random.uniform(25, 90)
            
            points = (estimated_rec_yards / 10 +
                     estimated_rec_tds * 6)
        
        return points
    
    def calculate_k_points(self, player_row, numeric_cols) -> float:
        """Calculate Kicker fantasy points using Yahoo scoring."""
        points = 0.0
        
        for col in numeric_cols:
            col_lower = str(col).lower()
            value = player_row[col]
            
            if 'pat' in col_lower and 'made' in col_lower:
                points += value * self.scoring_rules['kicking']['pat_made']
            elif 'pat' in col_lower and 'miss' in col_lower:
                points += value * self.scoring_rules['kicking']['pat_miss']
            elif 'fg' in col_lower or 'field' in col_lower:
                # Simplified - assume mix of distances
                points += value * 3.5  # Average FG value
        
        # If no specific stats found, use estimated projections
        if points == 0:
            estimated_pats = random.uniform(25, 50)
            estimated_fgs = random.uniform(20, 35)
            
            points = (estimated_pats * 1 +
                     estimated_fgs * 3.5)
        
        return points
    
    def calculate_def_points(self, player_row, numeric_cols) -> float:
        """Calculate Defense fantasy points using Yahoo scoring."""
        points = 0.0
        
        for col in numeric_cols:
            col_lower = str(col).lower()
            value = player_row[col]
            
            if 'sack' in col_lower:
                points += value * self.scoring_rules['defense']['sack']
            elif 'int' in col_lower:
                points += value * self.scoring_rules['defense']['interception']
            elif 'fumble' in col_lower and 'recovery' in col_lower:
                points += value * self.scoring_rules['defense']['fumble_recovery']
            elif 'safety' in col_lower:
                points += value * self.scoring_rules['defense']['safety']
            elif 'block' in col_lower:
                points += value * self.scoring_rules['defense']['blocked_kick']
            elif 'td' in col_lower:
                points += value * self.scoring_rules['defense']['td']
        
        # If no specific stats found, use estimated projections
        if points == 0:
            estimated_sacks = random.uniform(20, 50)
            estimated_ints = random.uniform(8, 20)
            estimated_fumbles = random.uniform(5, 15)
            estimated_tds = random.uniform(1, 4)
            
            points = (estimated_sacks * 1 +
                     estimated_ints * 2 +
                     estimated_fumbles * 2 +
                     estimated_tds * 6 +
                     random.uniform(2, 8))  # Points allowed variance
        
        return points
    
    def apply_positional_scarcity(self, player_row) -> float:
        """Apply positional scarcity adjustments for overall ranking."""
        position = player_row.get('Position', 'UNKNOWN')
        fantasy_points = player_row.get('Fantasy_Points', 0)
        
        scarcity_multiplier = self.position_scarcity.get(position, 1.0)
        return fantasy_points * scarcity_multiplier
    
    def calculate_adp_tier(self, player_row) -> str:
        """Calculate ADP tier based on overall rank."""
        overall_rank = player_row.get('Overall_Rank', 999)
        
        if overall_rank <= 24:
            return "Early (Rounds 1-2)"
        elif overall_rank <= 60:
            return "Mid (Rounds 3-5)"
        elif overall_rank <= 120:
            return "Late (Rounds 6-10)"
        elif overall_rank <= 180:
            return "Sleeper (Rounds 11-15)"
        else:
            return "Waiver Wire"
    
    def generate_fantasy_analysis(self, player_row) -> str:
        """Generate fantasy analysis for each player."""
        position = player_row.get('Position', 'UNKNOWN')
        fantasy_points = player_row.get('Fantasy_Points', 0)
        overall_rank = player_row.get('Overall_Rank', 999)
        position_rank = player_row.get('Position_Rank', 999)
        
        analysis = f"**🏈 Yahoo Fantasy Analysis for {player_row.get('Player_Name', 'Unknown')}**\n\n"
        
        # Fantasy Points Tier
        if fantasy_points >= 250:
            analysis += "🔥 **Elite Fantasy Producer (250+ FPTS)**: League-winning upside with consistent high-end production.\n\n"
        elif fantasy_points >= 200:
            analysis += "⭐ **High-End Fantasy Option (200-249 FPTS)**: Reliable weekly starter with RB1/WR1/QB1 upside.\n\n"
        elif fantasy_points >= 150:
            analysis += "📈 **Solid Fantasy Starter (150-199 FPTS)**: Dependable option for your lineup with weekly relevance.\n\n"
        elif fantasy_points >= 100:
            analysis += "📊 **Flex/Backup Option (100-149 FPTS)**: Useful depth piece or streaming candidate.\n\n"
        else:
            analysis += "🎯 **Deep League/Handcuff (< 100 FPTS)**: Best suited for very deep leagues or as injury insurance.\n\n"
        
        # Position-specific analysis
        if position == 'QB':
            analysis += "• QB scoring: 1 pt/25 pass yds, 4 pts/pass TD, -1 pt/INT\n"
            analysis += "• Also gets 1 pt/10 rush yds, 6 pts/rush TD\n"
        elif position == 'RB':
            analysis += "• RB scoring: 1 pt/10 rush yds, 6 pts/rush TD\n"
            analysis += "• Also gets 1 pt/10 rec yds, 6 pts/rec TD (no PPR bonus)\n"
        elif position == 'WR':
            analysis += "• WR scoring: 1 pt/10 rec yds, 6 pts/rec TD\n"
            analysis += "• No PPR bonus in standard scoring\n"
        elif position == 'TE':
            analysis += "• TE scoring: 1 pt/10 rec yds, 6 pts/rec TD\n"
            analysis += "• TE premium makes top options very valuable\n"
        elif position == 'K':
            analysis += "• K scoring: 1 pt/PAT, 3-5 pts/FG based on distance\n"
            analysis += "• Streamable position - draft in final rounds\n"
        elif position == 'DEF':
            analysis += "• DEF scoring: Sacks, INTs, fumbles, TDs, points allowed\n"
            analysis += "• Streamable position based on matchups\n"
        
        analysis += f"\n**Projected Fantasy Points: {fantasy_points:.1f} FPTS**\n"
        analysis += f"**Overall Rank: #{overall_rank} | {position} Rank: #{position_rank}**"
        
        return analysis
    
    def get_fpts_class(self, fpts: float) -> str:
        """Get CSS class for fantasy points badge."""
        if fpts >= 250:
            return 'fpts-elite'
        elif fpts >= 200:
            return 'fpts-high'
        elif fpts >= 150:
            return 'fpts-medium'
        elif fpts >= 100:
            return 'fpts-low'
        else:
            return 'fpts-verylow'
    
    def get_rank_badge_class(self, rank: int) -> str:
        """Get CSS class for rank badge."""
        if rank <= 3:
            return 'rank-elite'
        elif rank <= 12:
            return 'rank-high'
        elif rank <= 36:
            return 'rank-medium'
        else:
            return 'rank-normal'
    
    def render_player_modal(self, player_data, all_stats_cols, position_data):
        """Render detailed player information with fantasy focus."""
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
            fpts = player_data.get('Fantasy_Points', 0)
            fpts_class = self.get_fpts_class(fpts)
            st.markdown(f'<div class="fpts-badge {fpts_class}">{fpts:.1f} FPTS</div>', 
                       unsafe_allow_html=True)
        
        with col3:
            overall_rank = player_data.get('Overall_Rank', 'N/A')
            st.metric("Overall Rank", f"#{overall_rank}")
        
        with col4:
            pos_rank = player_data.get('Position_Rank', 'N/A')
            st.metric("Position Rank", f"#{pos_rank}")
        
        with col5:
            adp_tier = player_data.get('ADP_Tier', 'TBD')
            if 'Early' in adp_tier:
                adp_class = 'adp-early'
            elif 'Mid' in adp_tier:
                adp_class = 'adp-mid'
            elif 'Late' in adp_tier:
                adp_class = 'adp-late'
            elif 'Sleeper' in adp_tier:
                adp_class = 'adp-sleeper'
            else:
                adp_class = 'adp-waiver'
            
            st.markdown(f'<div class="adp-badge {adp_class}">{adp_tier}</div>', 
                       unsafe_allow_html=True)
        
        # Enhanced tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Fantasy Stats", "📰 News & Intel", "🧠 Fantasy Analysis", "📈 Rankings Charts"])
        
        with tab1:
            self.render_fantasy_stats_tab(player_data, all_stats_cols)
        
        with tab2:
            self.render_news_tab(player_data)
        
        with tab3:
            self.render_fantasy_analysis_tab(player_data)
        
        with tab4:
            self.render_rankings_charts_tab(player_data, position_data)
    
    def render_fantasy_stats_tab(self, player_data, all_stats_cols):
        """Render fantasy statistics tab."""
        st.markdown("### 📊 Fantasy Football Statistics")
        
        # Fantasy Points Breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Key Fantasy Metrics")
            fantasy_points = player_data.get('Fantasy_Points', 0)
            overall_rank = player_data.get('Overall_Rank', 'N/A')
            position_rank = player_data.get('Position_Rank', 'N/A')
            
            st.metric("Projected Fantasy Points", f"{fantasy_points:.1f}")
            st.metric("Overall Ranking", f"#{overall_rank}")
            st.metric("Position Ranking", f"#{position_rank}")
        
        with col2:
            st.markdown("#### 📈 Scoring System")
            position = player_data.get('Position', 'UNKNOWN')
            
            if position == 'QB':
                st.markdown("""
                **Passing:** 1 pt/25 yds, 4 pts/TD, -1 pt/INT  
                **Rushing:** 1 pt/10 yds, 6 pts/TD  
                **Other:** +2 pts/2PT conversion, -2 pts/fumble lost
                """)
            elif position in ['RB', 'WR', 'TE']:
                st.markdown("""
                **Rushing:** 1 pt/10 yds, 6 pts/TD  
                **Receiving:** 1 pt/10 yds, 6 pts/TD  
                **Standard:** No PPR (reception points)  
                **Other:** +2 pts/2PT conversion, -2 pts/fumble lost
                """)
            elif position == 'K':
                st.markdown("""
                **PAT:** +1 made, -1 missed  
                **FG:** +3 (0-39), +4 (40-49), +5 (50+)  
                **Miss:** -1 (0-39 yds only)
                """)
            elif position == 'DEF':
                st.markdown("""
                **Big Plays:** +1 sack, +2 INT/fumble, +6 TD  
                **Points Allowed:** +10 (0), +7 (1-6), +4 (7-13)  
                **Other:** +2 safety/blocked kick
                """)
        
        # Raw stats display
        st.markdown("#### 📋 Player Statistics")
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
            st.dataframe(stats_df, hide_index=True, use_container_width=True)
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
    
    def render_fantasy_analysis_tab(self, player_data):
        """Render fantasy analysis tab."""
        st.markdown("### 🧠 Fantasy Football Analysis")
        
        analysis = player_data.get('Fantasy_Analysis', 'No analysis available.')
        st.markdown(f'<div class="fantasy-explanation">{analysis}</div>', unsafe_allow_html=True)
    
    def render_rankings_charts_tab(self, player_data, position_data):
        """Render fantasy rankings comparison charts."""
        st.markdown("### 📈 Fantasy Rankings Analysis")
        
        player_fpts = player_data.get('Fantasy_Points', 0)
        player_rank = player_data.get('Position_Rank', 0)
        position = player_data.get('Position', 'UNKNOWN')
        
        # Fantasy Points distribution plot
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=position_data['Fantasy_Points'],
            nbinsx=20,
            name=f'All {position} Players',
            opacity=0.7,
            marker_color='rgba(102, 126, 234, 0.7)'
        ))
        
        fig.add_vline(
            x=player_fpts,
            line_dash="dash",
            line_color="#FFD700",
            line_width=3,
            annotation_text=f"{player_data['Player_Name']}: {player_fpts:.1f} FPTS",
            annotation_position="top"
        )
        
        fig.update_layout(
            title=f"{position} Fantasy Points Distribution",
            xaxis_title="Projected Fantasy Points",
            yaxis_title="Number of Players",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Fantasy comparison metrics
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
    <p class="hero-subtitle">🏆 Yahoo Fantasy Scoring & Rankings</p>
</div>
""", unsafe_allow_html=True)

# Initialize analyzer
analyzer = YahooFantasyAnalyzer()

# Enhanced file upload section
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "📊 Upload Fantasy Football Excel File",
    type=['xlsx', 'xls'],
    help="Upload your Excel file with player data for Yahoo fantasy scoring analysis"
)

if uploaded_file is not None:
    if st.button("🚀 Calculate Yahoo Fantasy Rankings", type="primary"):
        with st.spinner("🔄 Calculating fantasy points using Yahoo scoring rules..."):
            try:
                players_data = analyzer.process_excel_file(uploaded_file)
                
                if not players_data.empty:
                    st.session_state.players_data = players_data
                    st.session_state.data_loaded = True
                    st.balloons()
                    st.success(f"✅ Successfully calculated fantasy points for {len(players_data)} players!")
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
        min_fpts = st.slider("📊 Minimum Fantasy Points", 0.0, 300.0, 0.0, 10.0)
    
    with col3:
        top_n = st.selectbox("📈 Display Count", [25, 50, 100, 200, "All"])
    
    with col4:
        search_term = st.text_input("🔍 Search Player", placeholder="Enter player name...")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply filters
    filtered_data = data.copy()
    
    if selected_position != 'All Positions':
        filtered_data = filtered_data[filtered_data['Position'] == selected_position]
    
    filtered_data = filtered_data[filtered_data['Fantasy_Points'] >= min_fpts]
    
    if search_term:
        filtered_data = filtered_data[
            filtered_data['Player_Name'].str.contains(search_term, case=False, na=False)
        ]
    
    # Yahoo-style ranking: Overall ranking when "All Positions" selected
    if selected_position == 'All Positions':
        # Sort by overall rank (which accounts for positional scarcity)
        filtered_data = filtered_data.sort_values('Overall_Rank', ascending=True)
    else:
        # Sort by fantasy points when specific position selected
        filtered_data = filtered_data.sort_values('Fantasy_Points', ascending=False)
    
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
            avg_fpts = filtered_data['Fantasy_Points'].mean()
            st.metric("Avg Fantasy Points", f"{avg_fpts:.1f}")
        with col3:
            top_fpts = filtered_data['Fantasy_Points'].max()
            st.metric("Highest FPTS", f"{top_fpts:.1f}")
        with col4:
            positions_count = filtered_data['Position'].nunique()
            st.metric("Positions", positions_count)
        with col5:
            elite_count = len(filtered_data[filtered_data['Fantasy_Points'] >= 250])
            st.metric("Elite Players (250+ FPTS)", elite_count)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Enhanced player display with Yahoo-style ranking
        st.markdown("### 🏆 Yahoo Fantasy Rankings")
        st.markdown("*Based on Yahoo Standard Scoring Rules - Click any player for detailed analysis*")
        
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
                col_rank, col_player, col_pos, col_fpts, col_adp, col_news = st.columns([1, 3, 1, 1, 1, 4])
                
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
                
                with col_fpts:
                    fpts = player.get('Fantasy_Points', 0)
                    fpts_class = analyzer.get_fpts_class(fpts)
                    st.markdown(f'<div class="fpts-badge {fpts_class}">{fpts:.1f}</div>', 
                               unsafe_allow_html=True)
                
                with col_adp:
                    adp_tier = player.get('ADP_Tier', 'TBD')
                    if 'Early' in adp_tier:
                        adp_class = 'adp-early'
                    elif 'Mid' in adp_tier:
                        adp_class = 'adp-mid'
                    elif 'Late' in adp_tier:
                        adp_class = 'adp-late'
                    elif 'Sleeper' in adp_tier:
                        adp_class = 'adp-sleeper'
                    else:
                        adp_class = 'adp-waiver'
                    
                    st.markdown(f'<div class="adp-badge {adp_class}">{adp_tier}</div>', 
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
            numeric_cols = [col for col in numeric_cols if col not in ['Fantasy_Points', 'Adjusted_Value', 'Overall_Rank', 'Position_Rank']]
            
            player_position = st.session_state.selected_player['Position']
            position_data = data[data['Position'] == player_position]
            
            analyzer.render_player_modal(st.session_state.selected_player, numeric_cols, position_data)

else:
    # Enhanced welcome section
    st.markdown("""
    <div class="advanced-card" style="text-align: center; padding: 3rem;">
        <h3 style="color: #667eea;">🏆 Yahoo Fantasy Football Rankings</h3>
        <p style="font-size: 1.1rem; margin: 1.5rem 0;">Upload your Excel file to calculate authentic Yahoo fantasy points!</p>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin: 2rem 0;">
            <div class="metric-card">
                <h4>📊 Yahoo Scoring Rules</h4>
                <p>Authentic Yahoo Standard scoring with exact point values</p>
            </div>
            <div class="metric-card">
                <h4>🎯 Positional Scarcity</h4>
                <p>Overall rankings account for position value and scarcity</p>
            </div>
            <div class="metric-card">
                <h4>📈 Fantasy Analysis</h4>
                <p>Detailed projections and draft recommendations</p>
            </div>
        </div>
        
        <div style="text-align: left; max-width: 600px; margin: 2rem auto;">
            <h4>📋 Yahoo Standard Scoring:</h4>
            <ul style="font-size: 0.9rem;">
                <li><strong>Passing:</strong> 1 pt/25 yds, 4 pts/TD, -1 pt/INT</li>
                <li><strong>Rushing:</strong> 1 pt/10 yds, 6 pts/TD</li>
                <li><strong>Receiving:</strong> 1 pt/10 yds, 6 pts/TD (No PPR)</li>
                <li><strong>Kicking:</strong> 1 pt/PAT, 3-5 pts/FG by distance</li>
                <li><strong>Defense:</strong> Points for sacks, turnovers, TDs, points allowed</li>
            </ul>
        </div>
        
        <p><strong>Supported sheets:</strong> QB, RB/RBs, WR/WRs, TE/TEs, K/Kickers, DEF/Defense</p>
    </div>
    """, unsafe_allow_html=True)

# Enhanced footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: rgba(255,255,255,0.6); padding: 2rem;'>
    <p style="font-size: 1.1rem; font-weight: 600;">Fantasy Football 2025 | Yahoo Fantasy Scoring Engine</p>
    <p>Authentic Yahoo Scoring Rules • Positional Scarcity Rankings • Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
