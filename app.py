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
import time
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="T3's AI Powered Fantasy Football 2025",
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

    .navbar {
        background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.08) 100%);
        backdrop-filter: blur(20px);
        border-radius: 15px;
        padding: 1rem 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2rem;
    }

    .nav-button {
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
        border: 1px solid rgba(255,255,255,0.2);
        background: rgba(255,255,255,0.1);
        color: white;
        text-decoration: none;
    }

    .nav-button:hover {
        background: rgba(255,255,255,0.2);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }

    .nav-button.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 5px 15px rgba(102,126,234,0.3);
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

    .vbd-analysis-container {
        background: linear-gradient(135deg, rgba(102,126,234,0.15) 0%, rgba(118,75,162,0.15) 100%);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        border: 2px solid rgba(102,126,234,0.3);
        box-shadow: 0 20px 40px rgba(102,126,234,0.1);
        position: relative;
        overflow: hidden;
    }

    .vbd-analysis-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
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

    .vbd-badge {
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

    .vbd-badge:hover {
        transform: scale(1.05);
    }

    .vbd-elite {
        background: linear-gradient(135deg, #00ff87 0%, #60efff 100%);
        color: #000;
        font-weight: 700;
    }

    .vbd-high {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: #fff;
    }

    .vbd-medium {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: #000;
    }

    .vbd-low {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: #000;
    }

    .vbd-negative {
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

    .draft-round-badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 12px;
        font-weight: 500;
        font-size: 0.75rem;
        margin: 0.1rem;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }

    .round-1-2 { background: #FFD700; color: #000; }
    .round-3-5 { background: #C0C0C0; color: #000; }
    .round-6-10 { background: #CD7F32; color: #fff; }
    .round-11-15 { background: #4ECDC4; color: #000; }
    .round-waiver { background: #FF7675; color: #fff; }

    .ai-insight {
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

    .filter-section {
        background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.04) 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(15px);
    }

    .draft-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }

    .draft-pick {
        background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.03) 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .pick-number {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem;
        border-radius: 8px;
        font-weight: 700;
        min-width: 60px;
        text-align: center;
    }

    .team-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.8rem;
        margin: 0.2rem;
        text-transform: uppercase;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }

    .bye-week {
        display: inline-block;
        padding: 0.2rem 0.5rem;
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.7rem;
        background: rgba(255,255,255,0.15);
        color: #fff;
        border: 1px solid rgba(255,255,255,0.2);
    }

    .timer-display {
        background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.1) 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid rgba(255,255,255,0.2);
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        backdrop-filter: blur(20px);
    }

    .timer-urgent {
        animation: pulse 1s infinite;
        border-color: #ff4444 !important;
        box-shadow: 0 0 20px rgba(255, 68, 68, 0.5) !important;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    .user-turn-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 15px 35px rgba(102,126,234,0.3);
        margin: 1rem 0;
        animation: glow 2s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from { box-shadow: 0 15px 35px rgba(102,126,234,0.3); }
        to { box-shadow: 0 15px 35px rgba(102,126,234,0.6); }
    }

    .ai-turn-banner {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
        margin: 1rem 0;
    }

    .draft-grade-display {
        background: linear-gradient(135deg, rgba(102,126,234,0.2) 0%, rgba(118,75,162,0.2) 100%);
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        border: 3px solid rgba(102,126,234,0.4);
        box-shadow: 0 20px 40px rgba(102,126,234,0.2);
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    }

    .draft-grade-display::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    }

    .grade-letter {
        font-size: 6rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 30px rgba(102,126,234,0.5);
        margin: 0;
        line-height: 1;
    }

    .available-player-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.03) 100%);
        border-radius: 12px;
        padding: 0.8rem;
        margin: 0.3rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.2s ease;
        cursor: pointer;
    }

    .available-player-card:hover {
        background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.08) 100%);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        border-color: rgba(255,255,255,0.3);
    }
</style>
""", unsafe_allow_html=True)

class AdvancedFantasyAnalyzer:
    """Advanced Fantasy Football analyzer with VBD-based scoring and AI insights."""

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

        # VBD column mappings for each position
        self.vbd_columns = {
            'QB': 'X',    # Column X for QBs
            'RB': 'X',    # Column X for RBs  
            'WR': 'X',    # Column X for WRs
            'TE': 'S',    # Column S for TEs
            'K': 'L',     # Column L for Ks (reverse scoring)
            'DEF': 'L'    # Column L for DEFs (reverse scoring)
        }

        # Positional draft round logic
        self.draft_round_logic = {
            'QB': {
                'early_rounds': (1, 5),      # Elite QBs can go early
                'typical_rounds': (6, 12),   # Most QBs drafted here
                'late_rounds': (13, 16),     # Backup/streaming QBs
                'scarcity_factor': 0.7       # Lower scarcity
            },
            'RB': {
                'early_rounds': (1, 3),      # Elite RBs are premium
                'typical_rounds': (2, 8),    # RB dead zone consideration
                'late_rounds': (9, 15),      # Handcuffs/lottery tickets
                'scarcity_factor': 1.3       # High scarcity
            },
            'WR': {
                'early_rounds': (1, 4),      # Top WRs go early
                'typical_rounds': (3, 10),   # Deep WR pool
                'late_rounds': (11, 16),     # Upside picks
                'scarcity_factor': 1.1       # Medium scarcity
            },
            'TE': {
                'early_rounds': (3, 6),      # Elite TEs have premium
                'typical_rounds': (7, 12),   # Mid-tier TEs
                'late_rounds': (13, 16),     # Streaming options
                'scarcity_factor': 0.9       # TE premium exists
            },
            'K': {
                'early_rounds': (14, 16),    # Never draft early
                'typical_rounds': (15, 16),  # Final rounds only
                'late_rounds': (16, 16),     # Or pick up from waivers
                'scarcity_factor': 0.3       # Very low scarcity
            },
            'DEF': {
                'early_rounds': (12, 14),    # Sometimes drafted earlier
                'typical_rounds': (14, 16),  # Usually late
                'late_rounds': (16, 16),     # Or stream
                'scarcity_factor': 0.4       # Low scarcity
            }
        }

        # Initialize ML models
        self.scaler = StandardScaler()
        self.ranking_model = None
        self.value_model = None

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
        """Process Excel file and extract VBD-based rankings."""
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

                            # Extract VBD value based on position
                            vbd_col = self.vbd_columns.get(position, 'X')
                            vbd_value = self.extract_vbd_value(df, vbd_col, position)

                            if vbd_value is not None:
                                df['Position'] = position
                                df['Sheet_Source'] = sheet_name
                                df['VBD_Value'] = vbd_value

                                # Extract additional data including team and bye week
                                df = self.extract_player_data(df, position)

                                all_players.append(df)
                                st.success(f"✅ Loaded {position} data from '{sheet_name}' ({len(df)} players)")

                            else:
                                st.warning(f"⚠️ Could not find VBD column '{vbd_col}' in {sheet_name}")

                    except Exception as e:
                        st.warning(f"⚠️ Error reading sheet '{sheet_name}' for {position}: {str(e)}")
                        continue
                else:
                    st.warning(f"❌ No sheet found for position {position}")

            if all_players:
                combined_df = pd.concat(all_players, ignore_index=True)
                return self.calculate_advanced_rankings(combined_df)
            else:
                return pd.DataFrame()

        except Exception as e:
            st.error(f"💥 Error processing Excel file: {str(e)}")
            return pd.DataFrame()

    def extract_vbd_value(self, df: pd.DataFrame, vbd_col: str, position: str) -> Optional[pd.Series]:
        """Extract VBD values from the specified column."""
        try:
            # Convert column letter to index
            if vbd_col.isalpha():
                col_index = ord(vbd_col.upper()) - ord('A')
                if col_index < len(df.columns):
                    vbd_series = pd.to_numeric(df.iloc[:, col_index], errors='coerce')

                    # For K and DEF, reverse the scoring (0 is best, higher is worse)
                    if position in ['K', 'DEF']:
                        # Convert to positive VBD where higher is better
                        max_val = vbd_series.max()
                        vbd_series = max_val - vbd_series

                    return vbd_series

            return None
        except Exception as e:
            st.warning(f"Error extracting VBD for {position}: {str(e)}")
            return None

    def extract_player_data(self, df: pd.DataFrame, position: str) -> pd.DataFrame:
        """Extract player names and additional data including team information."""
        # Extract first name (Column A), last name (Column B), team (Column C)
        if len(df.columns) > 0:
            df['First_Name'] = df.iloc[:, 0].astype(str).fillna('')
        else:
            df['First_Name'] = ''

        if len(df.columns) > 1:
            df['Last_Name'] = df.iloc[:, 1].astype(str).fillna('')
        else:
            df['Last_Name'] = ''

        if len(df.columns) > 2:
            df['Team'] = df.iloc[:, 2].astype(str).fillna('')
        else:
            df['Team'] = ''

        # Create full player name
        df['Player_Name'] = (df['First_Name'] + ' ' + df['Last_Name']).str.strip()
        df = df[df['Player_Name'].str.strip() != '']
        df = df[df['Player_Name'] != 'nan nan']

        # Extract bye week information (look for common bye week columns)
        bye_week_col = None
        for col in df.columns:
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in ['bye', 'week', 'off']):
                bye_week_col = col
                break

        if bye_week_col:
            df['Bye_Week'] = pd.to_numeric(df[bye_week_col], errors='coerce').fillna(0).astype(int)
        else:
            # Assign random bye weeks if not found
            df['Bye_Week'] = np.random.choice([4, 5, 6, 7, 9, 10, 11, 12, 13, 14], size=len(df))

        # Extract Points column if available
        points_col = self.find_points_column(df)
        if points_col:
            df['Points'] = pd.to_numeric(df[points_col], errors='coerce')
        else:
            df['Points'] = 0

        # Extract news column (column Y - 25th column)
        if len(df.columns) > 24:
            df['News'] = df.iloc[:, 24].fillna('No recent news').astype(str)
        else:
            df['News'] = 'No recent news'

        return df

    def find_points_column(self, df: pd.DataFrame) -> Optional[str]:
        """Find the points column in the dataframe."""
        for col in df.columns:
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in ['point', 'pts', 'fantasy', 'proj']):
                return col
        return None

    def calculate_advanced_rankings(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate advanced rankings using VBD values and AI insights."""
        # Clean and prepare data
        df = df.dropna(subset=['VBD_Value'])
        df['VBD_Value'] = pd.to_numeric(df['VBD_Value'], errors='coerce')
        df = df.dropna(subset=['VBD_Value'])

        # Calculate positional rankings based on VBD
        df['Position_Rank'] = df.groupby('Position')['VBD_Value'].rank(ascending=False, method='dense').astype(int)

        # Apply positional scarcity and draft logic for overall ranking
        df['Adjusted_VBD'] = df.apply(self.apply_draft_logic, axis=1)

        # Calculate overall rankings
        df['Overall_Rank'] = df['Adjusted_VBD'].rank(ascending=False, method='dense').astype(int)

        # Add draft round recommendations
        df['Draft_Round'] = df.apply(self.recommend_draft_round, axis=1)

        # Train ML models for advanced insights
        df = self.add_ml_insights(df)

        # Generate AI analysis
        df['AI_Analysis'] = df.apply(self.generate_ai_analysis, axis=1)

        return df.sort_values('Overall_Rank')

    def apply_draft_logic(self, player_row) -> float:
        """Apply advanced draft logic to adjust VBD values."""
        position = player_row.get('Position', 'UNKNOWN')
        vbd_value = player_row.get('VBD_Value', 0)
        pos_rank = player_row.get('Position_Rank', 999)

        # Get position-specific factors
        logic = self.draft_round_logic.get(position, {})
        scarcity_factor = logic.get('scarcity_factor', 1.0)

        # Apply scarcity multiplier
        adjusted_vbd = vbd_value * scarcity_factor

        # Position-specific adjustments
        if position == 'QB':
            # QBs have diminishing returns after top tier
            if pos_rank <= 3:
                adjusted_vbd *= 1.2  # Premium for elite QBs
            elif pos_rank <= 12:
                adjusted_vbd *= 0.9  # Devalue mid-tier QBs
            else:
                adjusted_vbd *= 0.7  # Significant devaluation for late QBs

        elif position == 'RB':
            # RBs maintain value due to scarcity
            if pos_rank <= 12:
                adjusted_vbd *= 1.1  # Premium for startable RBs
            elif pos_rank <= 24:
                adjusted_vbd *= 0.95 # Slight devaluation for RB3s

        elif position == 'WR':
            # WRs have deep pool but top tier is valuable
            if pos_rank <= 8:
                adjusted_vbd *= 1.05 # Slight premium for WR1s

        elif position == 'TE':
            # TE premium for top options
            if pos_rank <= 5:
                adjusted_vbd *= 1.15 # Strong premium for elite TEs
            elif pos_rank <= 12:
                adjusted_vbd *= 0.8  # Devalue middle TEs

        elif position in ['K', 'DEF']:
            # Heavy devaluation for streaming positions
            adjusted_vbd *= 0.3

        return adjusted_vbd

    def recommend_draft_round(self, player_row) -> str:
        """Recommend draft round based on ranking and position."""
        position = player_row.get('Position', 'UNKNOWN')
        overall_rank = player_row.get('Overall_Rank', 999)
        pos_rank = player_row.get('Position_Rank', 999)

        # Round estimates based on 12-team league
        if overall_rank <= 12:
            return "Round 1"
        elif overall_rank <= 24:
            return "Round 2"
        elif overall_rank <= 36:
            return "Round 3"
        elif overall_rank <= 48:
            return "Round 4"
        elif overall_rank <= 60:
            return "Round 5"
        elif overall_rank <= 84:
            return "Rounds 6-7"
        elif overall_rank <= 120:
            return "Rounds 8-10"
        elif overall_rank <= 156:
            return "Rounds 11-13"
        elif overall_rank <= 180:
            return "Rounds 14-15"
        else:
            return "Round 16 / Waiver"

    def add_ml_insights(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add machine learning insights to player rankings."""
        try:
            # Prepare features for ML model
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            feature_cols = [col for col in numeric_cols if col not in ['Overall_Rank', 'Position_Rank', 'Adjusted_VBD']]

            if len(feature_cols) >= 2 and len(df) >= 10:
                # Prepare data
                X = df[feature_cols].fillna(0)
                y = df['VBD_Value']

                # Train value prediction model
                if len(X) > 5:
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                    self.value_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
                    self.value_model.fit(X_train, y_train)

                    # Predict values and calculate confidence
                    df['Predicted_VBD'] = self.value_model.predict(X)
                    df['Value_Confidence'] = np.abs(df['VBD_Value'] - df['Predicted_VBD'])

                    # Identify value picks (actual VBD > predicted VBD)
                    df['Value_Pick'] = df['VBD_Value'] > df['Predicted_VBD']

        except Exception as e:
            st.warning(f"ML insights generation failed: {str(e)}")
            df['Predicted_VBD'] = df['VBD_Value']
            df['Value_Confidence'] = 0
            df['Value_Pick'] = False

        return df

    def generate_ai_analysis(self, player_row) -> str:
        """Generate AI-powered analysis for each player."""
        position = player_row.get('Position', 'UNKNOWN')
        vbd_value = player_row.get('VBD_Value', 0)
        overall_rank = player_row.get('Overall_Rank', 999)
        position_rank = player_row.get('Position_Rank', 999)
        draft_round = player_row.get('Draft_Round', 'TBD')
        value_pick = player_row.get('Value_Pick', False)

        analysis = f"**🤖 Advanced AI Analysis for {player_row.get('Player_Name', 'Unknown')}**\n\n"

        # VBD Analysis
        if vbd_value >= 50:
            analysis += "🔥 **Elite VBD Score (50+)**: Exceptional value over replacement. Must-have player.\n\n"
        elif vbd_value >= 25:
            analysis += "⭐ **High VBD Score (25-49)**: Strong value proposition. Reliable starter.\n\n"
        elif vbd_value >= 10:
            analysis += "📈 **Solid VBD Score (10-24)**: Good value option. Useful roster piece.\n\n"
        elif vbd_value >= 0:
            analysis += "📊 **Positive VBD (0-9)**: Above replacement level. Depth option.\n\n"
        else:
            analysis += "⚠️ **Negative VBD**: Below replacement level. Avoid unless desperate.\n\n"

        # Position-specific insights
        logic = self.draft_round_logic.get(position, {})

        if position == 'QB':
            if position_rank <= 3:
                analysis += "• **Elite QB Tier**: Consistent 20+ fantasy points weekly. Worth early pick.\n"
            elif position_rank <= 12:
                analysis += "• **Starting QB Tier**: Reliable option but can wait for value.\n"
            else:
                analysis += "• **Streaming/Backup Tier**: Matchup-dependent option.\n"

        elif position == 'RB':
            if position_rank <= 8:
                analysis += "• **RB1 Tier**: Bellcow back with 250+ touches. Draft early.\n"
            elif position_rank <= 20:
                analysis += "• **RB2 Tier**: Solid contributor but may lack ceiling.\n"
            else:
                analysis += "• **Handcuff/Lottery Ticket**: Injury away from relevance.\n"

        elif position == 'WR':
            if position_rank <= 12:
                analysis += "• **WR1 Tier**: 100+ targets with TD upside. Safe pick.\n"
            elif position_rank <= 30:
                analysis += "• **WR2/Flex Tier**: Consistent producer in good offense.\n"
            else:
                analysis += "• **Depth/Upside Pick**: Boom-or-bust potential.\n"

        elif position == 'TE':
            if position_rank <= 5:
                analysis += "• **Elite TE Tier**: Massive positional advantage. Worth premium.\n"
            elif position_rank <= 12:
                analysis += "• **Streaming Tier**: Matchup-dependent production.\n"
            else:
                analysis += "• **Deep League Option**: Desperation play only.\n"

        elif position == 'K':
            analysis += "• **Kicker**: Draft in final round or stream based on matchups.\n"

        elif position == 'DEF':
            analysis += "• **Defense**: Stream based on schedule or draft elite unit late.\n"

        # Draft strategy
        analysis += f"\n**📈 Draft Strategy:**\n"
        analysis += f"• Recommended Round: {draft_round}\n"
        analysis += f"• Overall Rank: #{overall_rank} | Position Rank: {position}#{position_rank}\n"

        if value_pick:
            analysis += "• 💎 **VALUE PICK**: AI model suggests this player outperforms ranking!\n"

        analysis += f"• VBD Score: {vbd_value:.1f}"

        return analysis

    def get_vbd_class(self, vbd: float) -> str:
        """Get CSS class for VBD badge."""
        if vbd >= 50:
            return 'vbd-elite'
        elif vbd >= 25:
            return 'vbd-high'
        elif vbd >= 10:
            return 'vbd-medium'
        elif vbd >= 0:
            return 'vbd-low'
        else:
            return 'vbd-negative'

    def get_rank_badge_class(self, rank: int) -> str:
        """Get CSS class for rank badge."""
        if rank <= 5:
            return 'rank-elite'
        elif rank <= 15:
            return 'rank-high'
        elif rank <= 50:
            return 'rank-medium'
        else:
            return 'rank-normal'

    def render_player_modal(self, player_data, all_data):
        """Render detailed player analysis modal."""
        st.markdown(f"""
        <div class="advanced-card">
            <h2 style="margin-bottom: 1rem;">🏈 {player_data['Player_Name']} ({player_data.get('Team', 'Unknown Team')})</h2>
        </div>
        """, unsafe_allow_html=True)

        # Enhanced player info
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            position = player_data.get('Position', 'UNKNOWN')
            st.markdown(f'<span class="position-badge pos-{position.lower()}">{position}</span>', 
                       unsafe_allow_html=True)

        with col2:
            vbd = player_data.get('VBD_Value', 0)
            vbd_class = self.get_vbd_class(vbd)
            st.markdown(f'<div class="vbd-badge {vbd_class}">{vbd:.1f} VBD</div>', 
                       unsafe_allow_html=True)

        with col3:
            overall_rank = player_data.get('Overall_Rank', 'N/A')
            st.metric("Overall Rank", f"#{overall_rank}")

        with col4:
            pos_rank = player_data.get('Position_Rank', 'N/A')
            st.metric("Position Rank", f"#{pos_rank}")

        with col5:
            draft_round = player_data.get('Draft_Round', 'TBD')
            if 'Round 1' in draft_round or 'Round 2' in draft_round:
                round_class = 'round-1-2'
            elif 'Round 3' in draft_round or 'Round 4' in draft_round or 'Round 5' in draft_round:
                round_class = 'round-3-5'
            elif 'Rounds 6' in draft_round or 'Round 8' in draft_round or 'Round 9' in draft_round or 'Round 10' in draft_round:
                round_class = 'round-6-10'
            elif 'Round 11' in draft_round or 'Round 12' in draft_round or 'Round 13' in draft_round or 'Round 14' in draft_round or 'Round 15' in draft_round:
                round_class = 'round-11-15'
            else:
                round_class = 'round-waiver'

            st.markdown(f'<div class="draft-round-badge {round_class}">{draft_round}</div>', 
                       unsafe_allow_html=True)

        # Prominent VBD Analysis at the top
        st.markdown('<div class="vbd-analysis-container">', unsafe_allow_html=True)
        st.markdown("### 📊 Value Based Drafting Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### 🎯 VBD Metrics")
            vbd_value = player_data.get('VBD_Value', 0)
            predicted_vbd = player_data.get('Predicted_VBD', vbd_value)
            value_pick = player_data.get('Value_Pick', False)

            st.metric("VBD Score", f"{vbd_value:.1f}")
            st.metric("AI Predicted VBD", f"{predicted_vbd:.1f}")
            st.metric("Value Differential", f"{vbd_value - predicted_vbd:.1f}")

            if value_pick:
                st.success("💎 **VALUE PICK ALERT**: This player may outperform their current ranking!")

        with col2:
            st.markdown("#### 📈 VBD Explanation")
            st.markdown("""
            **Value Based Drafting (VBD)** measures how much better a player is compared to a 
            replacement-level player at the same position.

            **Key Points:**
            - Higher VBD = More valuable pick
            - Considers positional scarcity
            - Accounts for draft opportunity cost
            - AI-enhanced for accuracy
            """)

        with col3:
            # Points breakdown if available
            if 'Points' in player_data and player_data['Points'] > 0:
                st.markdown("#### 🏈 Fantasy Points Projection")
                points = player_data.get('Points', 0)
                st.metric("Projected Fantasy Points", f"{points:.1f}")

            # Team and bye week info
            team = player_data.get('Team', 'Unknown')
            bye_week = player_data.get('Bye_Week', 0)
            st.metric("Team", team)
            st.metric("Bye Week", f"Week {bye_week}" if bye_week > 0 else "TBD")

        st.markdown('</div>', unsafe_allow_html=True)

        # Tabs for detailed analysis
        tab1, tab2, tab3 = st.tabs(["📰 News & Intel", "🤖 AI Insights", "📈 Comparison"])

        with tab1:
            self.render_news_tab(player_data)

        with tab2:
            self.render_ai_insights_tab(player_data)

        with tab3:
            self.render_comparison_tab(player_data, all_data)

    def render_news_tab(self, player_data):
        """Render news tab."""
        st.markdown("### 📰 Latest News & Intelligence")

        news = str(player_data.get('News', 'No recent news'))
        if news and news.strip() != 'No recent news' and news != 'nan':
            st.markdown(f'<div class="ai-insight">📝 {news}</div>', unsafe_allow_html=True)
        else:
            st.info("📰 No recent news or updates available for this player.")

    def render_ai_insights_tab(self, player_data):
        """Render AI insights tab."""
        st.markdown("### 🤖 Advanced AI Analysis")

        analysis = player_data.get('AI_Analysis', 'No analysis available.')
        st.markdown(f'<div class="ai-insight">{analysis}</div>', unsafe_allow_html=True)

    def render_comparison_tab(self, player_data, all_data):
        """Render comparison analysis."""
        st.markdown("### 📈 Player Comparison Analysis")

        position = player_data.get('Position', 'UNKNOWN')
        position_data = all_data[all_data['Position'] == position]

        if len(position_data) > 1:
            player_vbd = player_data.get('VBD_Value', 0)
            player_rank = player_data.get('Position_Rank', 0)

            # VBD distribution plot
            fig = go.Figure()

            fig.add_trace(go.Histogram(
                x=position_data['VBD_Value'],
                nbinsx=20,
                name=f'All {position} Players',
                opacity=0.7,
                marker_color='rgba(102, 126, 234, 0.7)'
            ))

            fig.add_vline(
                x=player_vbd,
                line_dash="dash",
                line_color="#FFD700",
                line_width=3,
                annotation_text=f"{player_data['Player_Name']}: {player_vbd:.1f} VBD",
                annotation_position="top"
            )

            fig.update_layout(
                title=f"{position} VBD Distribution",
                xaxis_title="VBD Score",
                yaxis_title="Number of Players",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=False,
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

            # Enhanced Positional Ranking Analysis
            st.markdown("#### 🏆 Positional Ranking Analysis")

            # Key ranking metrics
            col1, col2, col3, col4 = st.columns(4)

            total_position_players = len(position_data)
            higher_ranked = len(position_data[position_data['Position_Rank'] < player_rank])
            lower_ranked = len(position_data[position_data['Position_Rank'] > player_rank])
            percentile = ((len(position_data) - player_rank + 1) / len(position_data)) * 100

            with col1:
                st.metric("Position Rank", f"#{player_rank} of {total_position_players}", 
                         help=f"This player ranks #{player_rank} among all {position} players")

            with col2:
                st.metric("Players Ranked Higher", higher_ranked,
                         help=f"{higher_ranked} {position} players are ranked above this player")

            with col3:
                st.metric("Players Ranked Lower", lower_ranked,
                         help=f"{lower_ranked} {position} players are ranked below this player")

            with col4:
                # Enhanced percentile with tier information
                if percentile >= 90:
                    tier = "🥇 Elite Tier"
                    tier_color = "#FFD700"
                elif percentile >= 75:
                    tier = "🥈 Top Tier"
                    tier_color = "#C0C0C0"
                elif percentile >= 50:
                    tier = "🥉 Mid Tier"
                    tier_color = "#CD7F32"
                elif percentile >= 25:
                    tier = "📊 Lower Tier"
                    tier_color = "#666666"
                else:
                    tier = "⚠️ Bottom Tier"
                    tier_color = "#FF6B6B"

                st.metric("Percentile Rank", f"{percentile:.0f}%",
                         help=f"This player is better than {percentile:.0f}% of all {position} players")
                st.markdown(f"<div style='text-align: center; color: {tier_color}; font-weight: bold; margin-top: 0.5rem;'>{tier}</div>", 
                           unsafe_allow_html=True)

            # Positional comparison table with nearby players
            st.markdown("#### 📋 Position Rankings Comparison")

            # Get players around this player's rank (±3 positions)
            rank_window = 3
            min_rank = max(1, player_rank - rank_window)
            max_rank = min(total_position_players, player_rank + rank_window)

            nearby_players = position_data[
                (position_data['Position_Rank'] >= min_rank) & 
                (position_data['Position_Rank'] <= max_rank)
            ].sort_values('Position_Rank')

            # Create comparison table
            if len(nearby_players) > 1:
                comparison_cols = st.columns([1, 3, 1, 1, 1])

                # Table headers
                with comparison_cols[0]:
                    st.markdown("**Rank**")
                with comparison_cols[1]:
                    st.markdown("**Player**")
                with comparison_cols[2]:
                    st.markdown("**Team**")
                with comparison_cols[3]:
                    st.markdown("**VBD**")
                with comparison_cols[4]:
                    st.markdown("**Draft Round**")

                st.markdown("---")

                # Player rows
                for _, comp_player in nearby_players.iterrows():
                    comp_cols = st.columns([1, 3, 1, 1, 1])

                    # Highlight the current player
                    is_current_player = comp_player['Player_Name'] == player_data['Player_Name']
                    name_style = "**🎯 " if is_current_player else "**"
                    name_end = "** ← YOU" if is_current_player else "**"

                    with comp_cols[0]:
                        rank_display = f"#{int(comp_player['Position_Rank'])}"
                        if is_current_player:
                            st.markdown(f"**🎯 {rank_display}**")
                        else:
                            st.markdown(rank_display)

                    with comp_cols[1]:
                        st.markdown(f"{name_style}{comp_player['Player_Name']}{name_end}")

                    with comp_cols[2]:
                        st.markdown(comp_player.get('Team', 'UNK'))

                    with comp_cols[3]:
                        vbd_val = comp_player.get('VBD_Value', 0)
                        st.markdown(f"{vbd_val:.1f}")

                    with comp_cols[4]:
                        draft_round = comp_player.get('Draft_Round', 'TBD')
                        st.markdown(f"{draft_round}")

            # Additional insights
            st.markdown("#### 💡 Positional Insights")

            insights_col1, insights_col2 = st.columns(2)

            with insights_col1:
                st.markdown("**🎯 Ranking Context:**")
                if percentile >= 90:
                    st.success(f"🌟 This {position} is among the absolute elite at the position")
                elif percentile >= 75:
                    st.success(f"⭐ This {position} is a top-tier option with excellent value")
                elif percentile >= 50:
                    st.info(f"📈 This {position} offers solid mid-tier production")
                elif percentile >= 25:
                    st.warning(f"⚠️ This {position} is a lower-tier option - consider other positions")
                else:
                    st.error(f"🚨 This {position} ranks very low at the position - high risk pick")

            with insights_col2:
                st.markdown("**📊 VBD Comparison:**")
                position_vbd_avg = position_data['VBD_Value'].mean()
                vbd_diff = player_vbd - position_vbd_avg

                if vbd_diff > 5:
                    st.success(f"💎 VBD is {vbd_diff:.1f} points above position average")
                elif vbd_diff > 0:
                    st.info(f"📈 VBD is {vbd_diff:.1f} points above position average")
                elif vbd_diff > -5:
                    st.warning(f"📉 VBD is {abs(vbd_diff):.1f} points below position average")
                else:
                    st.error(f"⚠️ VBD is {abs(vbd_diff):.1f} points below position average")

                st.markdown(f"Position Average VBD: **{position_vbd_avg:.1f}**")

class DraftSimulator:
    """Fantasy draft simulator with AI logic and real-time features."""

    def __init__(self, players_data: pd.DataFrame):
        self.players_data = players_data
        self.drafted_players = []
        self.user_team = []
        self.ai_teams = [[] for _ in range(9)]  # 9 AI teams
        self.current_pick = 1
        self.snake_draft = True
        self.draft_active = False
        self.pick_timer = 60  # 60 seconds per pick
        self.start_time = None

        # 12-player roster requirements
        self.roster_requirements = {
            'QB': 1,
            'WR': 2,  # WR1, WR2
            'RB': 2,  # RB1, RB2
            'TE': 1,
            'FLEX': 1,  # WR/RB/TE
            'K': 1,
            'DEF': 1,
            'BENCH': 3  # Any position
        }

        # Draft order for each position
        self.position_draft_order = [
            'QB', 'WR', 'WR', 'RB', 'RB', 'TE', 'FLEX', 'K', 'DEF', 'BENCH', 'BENCH', 'BENCH'
        ]

    def get_pick_order(self, pick_number: int) -> int:
        """Get the team index for snake draft."""
        round_num = ((pick_number - 1) // 10) + 1
        pick_in_round = ((pick_number - 1) % 10) + 1

        if round_num % 2 == 1:  # Odd rounds go 1-10
            return pick_in_round - 1
        else:  # Even rounds go 10-1
            return 10 - pick_in_round

    def get_roster_slot_for_pick(self, pick_number: int, team_index: int) -> str:
        """Get the roster slot being filled for this pick."""
        team_pick_num = ((pick_number - 1) // 10) * 10 + (team_index + 1)
        team_round = ((team_pick_num - 1) // 10) + 1

        if team_round <= len(self.position_draft_order):
            return self.position_draft_order[team_round - 1]
        else:
            return 'BENCH'

    def ai_draft_pick(self, team_index: int, available_players: pd.DataFrame, pick_num: int = None) -> dict:
        """Enhanced AI logic with realistic team personalities and advanced strategy."""
        # Ensure team_index is within valid range for AI teams (0-8)
        if team_index < 0 or team_index >= 9:
            team_index = 0

        team_roster = self.ai_teams[team_index]
        current_round = ((st.session_state.current_pick_number - 1) // 10) + 1

        # Enhanced AI team personalities with distinct strategies
        ai_strategies = {
            0: 'zero_rb',        # Zero RB strategy - WRs early, RBs late
            1: 'rb_heavy',       # RB focused - secures RB early and often
            2: 'value_based',    # Strict VBD following
            3: 'balanced',       # Traditional balanced approach
            4: 'late_round_qb',  # Waits on QB, builds skill positions
            5: 'te_premium',     # Values TE highly, drafts early
            6: 'upside_hunter',  # Targets high-ceiling, low-floor players
            7: 'safe_floor',     # Conservative, high-floor players
            8: 'contrarian'      # Goes against consensus, makes surprising picks
        }

        strategy = ai_strategies.get(team_index, 'balanced')

        # Count current positions
        position_counts = {}
        for player in team_roster:
            pos = player.get('Position', 'UNKNOWN')
            position_counts[pos] = position_counts.get(pos, 0) + 1

        # Strategy-based candidate filtering
        candidates = self.get_candidates_by_strategy(
            available_players, strategy, position_counts, current_round, len(team_roster)
        )

        if len(candidates) == 0:
            candidates = available_players.head(8)  # Fallback

        # Strategy-based selection with realistic variance
        selected_player = self.select_by_strategy(candidates, strategy, current_round)

        return selected_player.to_dict() if selected_player is not None else None

    def get_candidates_by_strategy(self, available: pd.DataFrame, strategy: str, 
                                 position_counts: dict, round_num: int, picks_made: int) -> pd.DataFrame:
        """Get candidate players based on AI team strategy."""

        if strategy == 'zero_rb':
            # Zero RB: WRs early, avoid RBs until late
            if round_num <= 6:
                if position_counts.get('QB', 0) == 0 and round_num == 1:
                    return available[available['Position'] == 'QB'].head(5)
                else:
                    # Prioritize WRs and TEs
                    return available[available['Position'].isin(['WR', 'TE'])].head(8)
            else:
                # Late rounds: fill needs including RBs
                return self.get_positional_need_candidates(available, position_counts)

        elif strategy == 'rb_heavy':
            # RB Heavy: Secure RBs early and often
            if round_num <= 8 and position_counts.get('RB', 0) < 3:
                rb_candidates = available[available['Position'] == 'RB'].head(6)
                if len(rb_candidates) > 0:
                    return rb_candidates
            return self.get_positional_need_candidates(available, position_counts)

        elif strategy == 'value_based':
            # Strict VBD: Always take highest VBD regardless of position
            return available.nlargest(6, 'VBD_Value')

        elif strategy == 'late_round_qb':
            # Late Round QB: Avoid QB until round 8+
            if round_num <= 7 and position_counts.get('QB', 0) == 0:
                return available[available['Position'] != 'QB'].head(8)
            return self.get_positional_need_candidates(available, position_counts)

        elif strategy == 'te_premium':
            # TE Premium: Draft TE earlier than consensus
            if round_num <= 4 and position_counts.get('TE', 0) == 0:
                te_candidates = available[available['Position'] == 'TE'].head(4)
                if len(te_candidates) > 0:
                    return te_candidates
            return self.get_positional_need_candidates(available, position_counts)

        elif strategy == 'upside_hunter':
            # Target high-upside players
            upside_candidates = available[
                (available.get('Value_Pick', False) == True) |
                (available['VBD_Value'] > available['VBD_Value'].quantile(0.75))
            ].head(8)
            if len(upside_candidates) > 0:
                return upside_candidates
            return available.head(6)

        elif strategy == 'safe_floor':
            # Conservative picks - established players with good floors
            safe_candidates = available[
                (available['VBD_Value'] >= 8) & 
                (available['Overall_Rank'] <= 80)
            ].head(6)
            if len(safe_candidates) > 0:
                return safe_candidates
            return available.head(6)

        elif strategy == 'contrarian':
            # Contrarian picks - sometimes makes surprising choices
            if random.random() < 0.25:  # 25% chance of contrarian move
                # Draft K/DEF early or reach for sleepers
                if round_num <= 6:
                    contrarian_options = available[available['Position'].isin(['K', 'DEF', 'TE'])].head(3)
                    if len(contrarian_options) > 0:
                        return contrarian_options
            return self.get_positional_need_candidates(available, position_counts)

        else:  # balanced strategy
            return self.get_positional_need_candidates(available, position_counts)

    def get_positional_need_candidates(self, available: pd.DataFrame, position_counts: dict) -> pd.DataFrame:
        """Get candidates based on positional needs."""
        # Standard positional requirements
        needs = []

        if position_counts.get('QB', 0) == 0:
            needs.append('QB')
        if position_counts.get('RB', 0) < 2:
            needs.append('RB')
        if position_counts.get('WR', 0) < 2:
            needs.append('WR')
        if position_counts.get('TE', 0) == 0:
            needs.append('TE')
        if position_counts.get('K', 0) == 0:
            needs.append('K')
        if position_counts.get('DEF', 0) == 0:
            needs.append('DEF')

        if needs:
            need_candidates = available[available['Position'].isin(needs)].head(8)
            if len(need_candidates) > 0:
                return need_candidates

        # If no specific needs, return best available
        return available.head(8)

    def select_by_strategy(self, candidates: pd.DataFrame, strategy: str, round_num: int) -> pd.Series:
        """Select player from candidates based on strategy with realistic variance."""
        if len(candidates) == 0:
            return None

        # Strategy-specific selection logic
        if strategy == 'value_based':
            # Heavy bias toward top VBD
            weights = [1.0 / (i + 1) ** 2 for i in range(len(candidates))]
        elif strategy == 'upside_hunter':
            # More willing to reach for upside
            weights = [1.0 / (i + 1) ** 0.7 for i in range(len(candidates))]
        elif strategy == 'safe_floor':
            # Prefer consensus picks
            weights = [1.0 / (i + 1) ** 1.3 for i in range(len(candidates))]
        elif strategy == 'contrarian':
            # Sometimes makes unexpected picks
            if random.random() < 0.2:  # 20% chance of surprise
                weights = [1.0 for _ in range(len(candidates))]  # Equal probability
            else:
                weights = [1.0 / (i + 1) for i in range(len(candidates))]
        else:
            # Standard weighting for most strategies
            weights = [1.0 / (i + 1) ** 1.1 for i in range(len(candidates))]

        # Add slight randomness for realism
        randomness = [random.uniform(0.8, 1.2) for _ in range(len(candidates))]
        weights = [w * r for w, r in zip(weights, randomness)]

        # Normalize weights
        weights = [w / sum(weights) for w in weights]

        # Select player
        selected_idx = np.random.choice(len(candidates), p=weights)
        return candidates.iloc[selected_idx]

    def simulate_draft(self, user_picks: List[int]) -> List[dict]:
        """Simulate a full 12-round draft."""
        draft_results = []
        available_players = self.players_data.copy().sort_values('Overall_Rank')

        for pick_num in range(1, 121):  # 12 rounds, 10 teams
            team_index = self.get_pick_order(pick_num)

            if team_index == 0 and pick_num in user_picks:
                # User's turn - they'll select manually
                continue
            else:
                # AI pick
                if len(available_players) > 0:
                    # Correctly map team_index to AI teams (team 0 is user, teams 1-9 map to ai_teams 0-8)
                    ai_team_index = team_index - 1 if team_index > 0 else 8
                    ai_pick = self.ai_draft_pick(ai_team_index, available_players, pick_num)
                    if ai_pick:
                        draft_results.append({
                            'pick': pick_num,
                            'round': ((pick_num - 1) // 10) + 1,
                            'team': f"Team {team_index + 1}" if team_index < 9 else "Your Team",
                            'player': ai_pick['Player_Name'],
                            'position': ai_pick['Position'],
                            'team_name': ai_pick.get('Team', 'Unknown'),
                            'vbd': ai_pick.get('VBD_Value', 0),
                            'overall_rank': ai_pick.get('Overall_Rank', 999),
                            'roster_slot': self.get_roster_slot_for_pick(pick_num, team_index)
                        })

                        # Remove drafted player
                        available_players = available_players[
                            available_players['Player_Name'] != ai_pick['Player_Name']
                        ]

                        # Add to team roster
                        if team_index == 0:
                            self.user_team.append(ai_pick)
                        else:
                            # Use the same AI team index mapping
                            ai_team_index = team_index - 1 if team_index > 0 else 8
                            if ai_team_index < 9:  # Safety check
                                self.ai_teams[ai_team_index].append(ai_pick)

        return draft_results

    def run_real_time_draft(self):
        """Run the enhanced real-time draft with mock draft interface."""
        simulator = st.session_state.draft_simulator
        current_pick = st.session_state.current_pick_number
        max_picks = st.session_state.draft_rounds * 10

        if current_pick > max_picks:
            st.session_state.draft_completed = True
            st.rerun()
            return

        # Calculate current team and round
        team_index = simulator.get_pick_order(current_pick)
        round_num = ((current_pick - 1) // 10) + 1
        pick_in_round = ((current_pick - 1) % 10) + 1
        is_user_turn = (team_index == st.session_state.user_draft_position - 1)

        # Set waiting for user pick flag
        if is_user_turn and not st.session_state.waiting_for_user_pick:
            st.session_state.waiting_for_user_pick = True
            st.session_state.pick_timer_start = datetime.now()
        elif not is_user_turn:
            st.session_state.waiting_for_user_pick = False

        # Enhanced Draft Header
        st.markdown(f"""
        <div class="draft-container" style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); text-align: center; padding: 2rem; margin-bottom: 1rem; border-radius: 20px; box-shadow: 0 15px 35px rgba(30,60,114,0.3);">
            <h1 style="margin: 0; font-size: 2.5rem; background: linear-gradient(135deg, #00ff87 0%, #60efff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🏈 LIVE FANTASY DRAFT</h1>
            <h2 style="margin: 0.5rem 0; color: #ffffff;">Round {round_num} | Pick {pick_in_round} | Overall #{current_pick}</h2>
            <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem; flex-wrap: wrap;">
                <div><strong>Position:</strong> {st.session_state.user_draft_position}</div>
                <div><strong>League:</strong> 10 Team</div>
                <div><strong>Rounds:</strong> {st.session_state.draft_rounds}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Main Draft Layout
        if is_user_turn and st.session_state.waiting_for_user_pick:
            # USER'S TURN - Enhanced Interface
            self.render_user_draft_interface(current_pick, remaining_time=self.get_remaining_time())
        else:
            # AI TURN - Show draft board and AI activity
            self.render_ai_draft_interface(team_index, current_pick)
            self.handle_ai_pick()

        # Handle pick logic
        if is_user_turn and st.session_state.waiting_for_user_pick:
            self.handle_user_pick()

    def get_user_roster_slot(self, pick_number: int) -> str:
        """Get the roster slot for the user's pick number."""
        if pick_number <= len(self.position_draft_order):
            return self.position_draft_order[pick_number - 1]
        else:
            return 'BENCH'

    def get_remaining_time(self):
        """Get remaining time for current pick."""
        if st.session_state.pick_timer_start:
            elapsed = (datetime.now() - st.session_state.pick_timer_start).total_seconds()
            return max(0, 60 - elapsed)
        return 60

    def start_pick_timer(self):
        """Start the pick timer for the current turn."""
        st.session_state.pick_timer_start = datetime.now()

    def is_timer_expired(self, time_limit=60):
        """Check if the pick timer has expired."""
        if not st.session_state.pick_timer_start:
            return False
        elapsed = (datetime.now() - st.session_state.pick_timer_start).total_seconds()
        return elapsed >= time_limit

    def render_user_draft_interface(self, current_pick, remaining_time):
        """Render enhanced user draft interface with improved containers and organization."""
        # Calculate picks until next user turn for better context
        picks_until_next = self.calculate_picks_until_user_turn()

        # Enhanced timer and urgency indicator with better context
        timer_color = "#ff4444" if remaining_time < 10 else "#ffaa00" if remaining_time < 30 else "#44ff44"
        urgency_class = "timer-urgent" if remaining_time < 10 else ""

        # Main user turn banner with enhanced information
        with st.container():
            st.markdown(f"""
            <div class="user-turn-banner {urgency_class}" style="
                text-align: center; 
                padding: 2.5rem; 
                margin: 1rem 0; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 20px;
                box-shadow: 0 15px 35px rgba(102,126,234,0.4);
                border: 2px solid rgba(255,255,255,0.2);
            ">
                <h1 style="margin: 0; font-size: 3rem; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">🎯 YOUR TURN TO PICK!</h1>
                <div style="display: flex; justify-content: center; align-items: center; gap: 3rem; margin-top: 1.5rem; flex-wrap: wrap;">
                    <div style="font-size: 2.5rem; color: {timer_color}; font-weight: bold; text-shadow: 0 2px 4px rgba(0,0,0,0.5);">⏱️ {remaining_time:.0f}s</div>
                    <div style="font-size: 1.2rem;">Pick #{current_pick}</div>
                    <div style="font-size: 1.2rem;">Round {((current_pick - 1) // 10) + 1}</div>
                    <div style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 10px;">
                        Next Pick in {picks_until_next + 20} picks
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Enhanced three-column layout with better containers
        with st.container():
            col1, col2, col3 = st.columns([1.2, 2.5, 1.3])

            with col1:
                # Left sidebar container
                with st.container():
                    self.render_enhanced_ai_suggestions()
                    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)
                    self.render_enhanced_my_team()

            with col2:
                # Main draft board container
                with st.container():
                    self.render_draft_board(is_user_turn=True)

            with col3:
                # Right sidebar container
                with st.container():
                    self.render_enhanced_draft_progress()
                    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)
                    self.render_enhanced_recent_picks()

    def render_enhanced_ai_suggestions(self):
        """Enhanced AI suggestions with better container styling."""
        with st.container():
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, rgba(102,126,234,0.2) 0%, rgba(118,75,162,0.2) 100%); 
                border-radius: 16px; 
                padding: 2rem; 
                margin: 1rem 0; 
                border: 2px solid rgba(102,126,234,0.4); 
                box-shadow: 0 12px 30px rgba(102,126,234,0.15);
                backdrop-filter: blur(20px);
            ">
                <h3 style="margin-top: 0; color: #667eea; font-size: 1.3rem; text-align: center; font-weight: 700;">
                    🤖 AI DRAFT ASSISTANT
                </h3>
            </div>
            """, unsafe_allow_html=True)

            # Get AI suggestions with enhanced logic
            suggestions = self.get_ai_suggestions_for_user()
            current_round = ((st.session_state.current_pick_number - 1) // 10) + 1

            # Enhanced draft context
            user_picks = [pick for pick in st.session_state.draft_results if pick['team'] == 'Your Team']
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); border-radius: 12px; padding: 1rem; margin: 1rem 0; border: 1px solid rgba(255,255,255,0.2);">
                <div style="text-align: center; font-weight: 600;">
                    <div>📊 Round {current_round} Analysis</div>
                    <div style="font-size: 0.9rem; color: rgba(255,255,255,0.8); margin-top: 0.5rem;">
                        Picks Made: {len(user_picks)} | Available: {len(st.session_state.available_players)}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if suggestions:
                st.markdown("**🎯 Strategic Recommendations:**")

                for i, player in enumerate(suggestions[:4]):  # Show top 4 suggestions
                    suggestion_type = player.get('suggestion_type', 'VALUE')
                    reason = player.get('reason', 'Strong pick at this position')

                    # Enhanced suggestion display with better styling
                    with st.container():
                        st.markdown(f"""
                        <div style="
                            background: rgba(255,255,255,0.08); 
                            border-radius: 12px; 
                            padding: 1.2rem; 
                            margin: 0.8rem 0; 
                            border: 1px solid rgba(255,255,255,0.15);
                            transition: all 0.3s ease;
                        ">
                        """, unsafe_allow_html=True)

                        sug_cols = st.columns([3, 1])

                        with sug_cols[0]:
                            # Enhanced suggestion type indicators
                            type_styles = {
                                'NEED': ('🔥', '#ff4444', 'ROSTER NEED'),
                                'VALUE': ('💎', '#00ff87', 'VALUE PICK'), 
                                'BPA': ('⭐', '#ffd700', 'BEST AVAILABLE'),
                                'SLEEPER': ('🚀', '#4facfe', 'SLEEPER PICK')
                            }

                            icon, color, label = type_styles.get(suggestion_type, ('⭐', '#666', 'RECOMMENDED'))

                            st.markdown(f"""
                            <div style="margin-bottom: 0.8rem;">
                                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                                    <span style="font-size: 1.3rem; margin-right: 0.7rem;">{icon}</span>
                                    <span style="background: {color}; color: black; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.7rem; font-weight: bold; margin-right: 0.7rem;">{label}</span>
                                </div>
                                <div style="font-weight: bold; font-size: 1.2rem; margin-bottom: 0.3rem;">{player['Player_Name']}</div>
                                <div style="color: rgba(255,255,255,0.9); font-size: 0.95rem; line-height: 1.4;">{reason}</div>
                            </div>
                            """, unsafe_allow_html=True)

                            # Enhanced player stats display
                            stats_cols = st.columns([1, 1, 1, 1])
                            with stats_cols[0]:
                                st.markdown(f"<div style='text-align: center; font-size: 0.8rem;'><strong>#{int(player['Overall_Rank'])}</strong><br><small>Rank</small></div>", unsafe_allow_html=True)
                            with stats_cols[1]:
                                st.markdown(f"<div style='text-align: center; font-size: 0.8rem;'><strong>{player['VBD_Value']:.1f}</strong><br><small>VBD</small></div>", unsafe_allow_html=True)
                            with stats_cols[2]:
                                st.markdown(f"<div style='text-align: center; font-size: 0.8rem;'><strong>#{int(player['Position_Rank'])}</strong><br><small>{player['Position']}</small></div>", unsafe_allow_html=True)
                            with stats_cols[3]:
                                st.markdown(f"<div style='text-align: center; font-size: 0.8rem;'><strong>{player.get('Team', 'UNK')}</strong><br><small>Team</small></div>", unsafe_allow_html=True)

                        with sug_cols[1]:
                            if st.button(f"📝 DRAFT", key=f"ai_suggestion_{i}", type="primary", use_container_width=True):
                                self.make_user_pick(player)
                                st.rerun()

                        st.markdown("</div>", unsafe_allow_html=True)

                # Enhanced draft insights
                st.markdown("---")
                st.markdown("**💡 Advanced Draft Insights:**")
                insights = self.get_enhanced_draft_insights()
                for insight in insights[:3]:
                    st.markdown(f"• {insight}")

            else:
                st.markdown("<div style='text-align: center; color: rgba(255,255,255,0.5); padding: 2rem;'>🔄 Analyzing optimal picks for your roster...</div>", unsafe_allow_html=True)

    def render_enhanced_my_team(self):
        """Enhanced user team display with better organization."""
        with st.container():
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 16px; 
                padding: 2rem; 
                margin: 1rem 0; 
                box-shadow: 0 12px 30px rgba(102,126,234,0.4);
                border: 2px solid rgba(255,255,255,0.2);
            ">
                <h3 style="margin-top: 0; color: white; font-size: 1.3rem; text-align: center; font-weight: 700;">
                    🏆 MY DRAFT PICKS
                </h3>
            </div>
            """, unsafe_allow_html=True)

            user_picks = [pick for pick in st.session_state.draft_results if pick['team'] == 'Your Team']

            if user_picks:
                # Enhanced team display with roster slots
                for i, pick in enumerate(user_picks):
                    roster_slot = self.get_user_roster_slot(i + 1)

                    # Slot colors
                    slot_colors = {
                        'QB': '#e74c3c', 'WR': '#f39c12', 'RB': '#3498db', 
                        'TE': '#27ae60', 'FLEX': '#9b59b6', 'K': '#34495e', 'DEF': '#7f8c8d', 'BENCH': '#95a5a6'
                    }
                    slot_color = slot_colors.get(roster_slot, '#667eea')

                    st.markdown(f"""
                    <div style="
                        background: rgba(255,255,255,0.1); 
                        border-radius: 12px; 
                        padding: 1rem; 
                        margin: 0.5rem 0; 
                        border-left: 4px solid {slot_color};
                        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                    ">
                        <div style="display: flex; align-items: center; gap: 1rem;">
                            <div style="background: {slot_color}; color: white; padding: 0.4rem 0.8rem; border-radius: 8px; font-weight: bold; font-size: 0.8rem; min-width: 60px; text-align: center;">
                                {roster_slot}
                            </div>
                            <div style="flex-grow: 1;">
                                <div style="font-weight: 600; font-size: 1rem; margin-bottom: 0.2rem;">{pick['player']}</div>
                                <div style="font-size: 0.8rem; color: rgba(255,255,255,0.8);">
                                    R{pick['round']}.{pick['pick'] - (pick['round']-1)*10} | VBD: {pick['vbd']:.1f}
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="
                    text-align: center; 
                    color: rgba(255,255,255,0.6); 
                    padding: 3rem 1rem;
                    background: rgba(255,255,255,0.05);
                    border-radius: 12px;
                    border: 2px dashed rgba(255,255,255,0.2);
                    margin: 1rem 0;
                ">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
                    <div style="font-weight: 600;">Your draft picks will appear here</div>
                    <div style="font-size: 0.9rem; margin-top: 0.5rem;">Start drafting to build your team!</div>
                </div>
                """, unsafe_allow_html=True)

    def render_enhanced_draft_progress(self):
        """Enhanced draft progress with better visual organization."""
        current_pick = st.session_state.current_pick_number
        max_picks = st.session_state.draft_rounds * 10
        progress = (current_pick - 1) / max_picks

        with st.container():
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.08) 100%); 
                border-radius: 16px; 
                padding: 2rem; 
                margin: 1rem 0; 
                border: 2px solid rgba(255,255,255,0.2);
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            ">
                <h3 style="margin-top: 0; color: #667eea; font-size: 1.3rem; text-align: center; font-weight: 700;">
                    📊 DRAFT PROGRESS
                </h3>
            </div>
            """, unsafe_allow_html=True)

            # Enhanced progress display
            st.progress(progress)

            st.markdown(f"""
            <div style="
                text-align: center; 
                padding: 1rem;
                background: rgba(255,255,255,0.05);
                border-radius: 12px;
                margin: 1rem 0;
            ">
                <div style="font-size: 1.4rem; font-weight: 700; color: #667eea;">{current_pick - 1} / {max_picks}</div>
                <div style="font-size: 0.9rem; color: rgba(255,255,255,0.7); margin-top: 0.3rem;">Picks Completed</div>
                <div style="font-size: 0.8rem; color: rgba(255,255,255,0.6); margin-top: 0.5rem;">
                    {((progress * 100):.1f}% Complete
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Enhanced position breakdown
            if st.session_state.draft_results:
                pos_counts = {}
                for pick in st.session_state.draft_results:
                    pos = pick['position']
                    pos_counts[pos] = pos_counts.get(pos, 0) + 1

                st.markdown("**📈 Positions Drafted:**")

                # Create visual position breakdown
                for pos, count in sorted(pos_counts.items()):
                    pos_colors = {
                        'QB': '#e74c3c', 'RB': '#3498db', 'WR': '#f39c12', 
                        'TE': '#27ae60', 'K': '#9b59b6', 'DEF': '#34495e'
                    }
                    pos_color = pos_colors.get(pos, '#666')

                    st.markdown(f"""
                    <div style="
                        display: flex; 
                        justify-content: space-between; 
                        align-items: center; 
                        padding: 0.5rem; 
                        margin: 0.3rem 0;
                        background: rgba(255,255,255,0.05);
                        border-radius: 8px;
                        border-left: 4px solid {pos_color};
                    ">
                        <span style="font-weight: 600;">{pos}</span>
                        <span style="background: {pos_color}; color: white; padding: 0.2rem 0.6rem; border-radius: 6px; font-size: 0.8rem; font-weight: bold;">{count}</span>
                    </div>
                    """, unsafe_allow_html=True)

    def render_enhanced_recent_picks(self):
        """Enhanced recent picks with better container and styling."""
        with st.container():
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.08) 100%); 
                border-radius: 16px; 
                padding: 2rem; 
                margin: 1rem 0; 
                border: 2px solid rgba(255,255,255,0.2);
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            ">
                <h3 style="margin-top: 0; color: #667eea; font-size: 1.3rem; text-align: center; font-weight: 700;">
                    📋 LIVE DRAFT FEED
                </h3>
            </div>
            """, unsafe_allow_html=True)

            recent_picks = st.session_state.draft_results[-8:] if st.session_state.draft_results else []

            if recent_picks:
                # Enhanced scrollable container for recent picks
                st.markdown("""
                <div style="
                    max-height: 400px;
                    overflow-y: auto;
                    border: 2px solid rgba(255,255,255,0.2);
                    border-radius: 12px;
                    background: rgba(0,0,0,0.1);
                    padding: 1rem;
                ">
                """, unsafe_allow_html=True)

                for i, pick_info in enumerate(reversed(recent_picks)):
                    team_color = "#667eea" if "Your Team" in pick_info['team'] else "#888"
                    is_user_pick = "Your Team" in pick_info['team']

                    # Position colors
                    pos_colors = {
                        'QB': '#e74c3c', 'RB': '#3498db', 'WR': '#f39c12', 
                        'TE': '#27ae60', 'K': '#9b59b6', 'DEF': '#34495e'
                    }
                    pos_color = pos_colors.get(pick_info['position'], '#666')

                    # Enhanced pick display
                    st.markdown(f"""
                    <div style="
                        background: {'rgba(102,126,234,0.15)' if is_user_pick else 'rgba(255,255,255,0.05)'};
                        border-radius: 10px;
                        padding: 1rem;
                        margin: 0.5rem 0;
                        border: {'2px solid rgba(102,126,234,0.4)' if is_user_pick else '1px solid rgba(255,255,255,0.1)'};
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="flex-grow: 1;">
                                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.3rem;">
                                    <div style="background: {team_color}; color: white; padding: 0.2rem 0.5rem; border-radius: 6px; font-size: 0.7rem; font-weight: bold;">
                                        #{pick_info['pick']}
                                    </div>
                                    <span style="font-weight: 600; font-size: 0.9rem;">{'🎯 ' if is_user_pick else ''}{pick_info['player']}</span>
                                </div>
                                <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">
                                    <span style="background: {pos_color}; color: white; padding: 0.1rem 0.4rem; border-radius: 4px; margin-right: 0.5rem;">{pick_info['position']}</span>
                                    {pick_info['team']} | VBD: {pick_info['vbd']:.1f}
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="
                    text-align: center; 
                    color: rgba(255,255,255,0.5); 
                    padding: 3rem 1rem;
                    background: rgba(255,255,255,0.05);
                    border-radius: 12px;
                    border: 2px dashed rgba(255,255,255,0.2);
                ">
                    <div style="font-size: 2.5rem; margin-bottom: 1rem;">📋</div>
                    <div>Draft picks will appear here</div>
                </div>
                """, unsafe_allow_html=True)

    def render_draft_board(self, is_user_turn=False):
        """Render the complete draft board with all available players in a scrollable table."""
        # Show picks until user's next turn
        current_pick = st.session_state.current_pick_number
        user_position = st.session_state.user_draft_position

        # Calculate next user pick
        picks_until_user = self.calculate_picks_until_user_turn()

        # Draft board container with better organization
        with st.container():
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
                       border-radius: 16px; padding: 2rem; margin: 1rem 0; 
                       border: 2px solid rgba(255,255,255,0.2); box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                    <h3 style="margin: 0; color: #667eea; font-size: 1.5rem;">📋 AVAILABLE PLAYERS</h3>
                    <div style="text-align: right;">
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                   color: white; padding: 0.8rem 1.5rem; border-radius: 12px; 
                                   font-weight: bold; box-shadow: 0 4px 15px rgba(102,126,234,0.3);">
                            🎯 Next User Pick: {picks_until_user} picks away
                        </div>
                        <div style="font-size: 0.9rem; color: rgba(255,255,255,0.7); margin-top: 0.5rem;">
                            Position: #{user_position} | Available: {len(st.session_state.available_players)}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Filters in a better organized container
            with st.container():
                st.markdown("""
                <div style="background: rgba(255,255,255,0.08); border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border: 1px solid rgba(255,255,255,0.1);">
                """, unsafe_allow_html=True)

                filter_col1, filter_col2, filter_col3 = st.columns([1, 1, 1])

                with filter_col1:
                    positions = ['ALL'] + sorted(st.session_state.available_players['Position'].unique())
                    selected_pos = st.selectbox("🎯 Filter Position", positions, key="pos_filter")

                with filter_col2:
                    search_term = st.text_input("🔍 Search Players", placeholder="Player name...", key="board_search")

                with filter_col3:
                    show_count = st.selectbox("📊 Show Players", [25, 50, 100, "All"], index=0)

                st.markdown("</div>", unsafe_allow_html=True)

        # Filter players
        filtered_players = st.session_state.available_players.copy()
        if selected_pos != 'ALL':
            filtered_players = filtered_players[filtered_players['Position'] == selected_pos]
        if search_term:
            filtered_players = filtered_players[
                filtered_players['Player_Name'].str.contains(search_term, case=False, na=False)
            ]

        # Sort by overall rank and apply show count
        filtered_players = filtered_players.sort_values('Overall_Rank')
        if show_count != "All":
            filtered_players = filtered_players.head(show_count)

        # Scrollable player table container with enhanced styling
        with st.container():
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
                backdrop-filter: blur(15px);
                border-radius: 16px;
                padding: 1.5rem;
                margin: 1rem 0;
                border: 2px solid rgba(255,255,255,0.2);
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            ">
                <div style="
                    max-height: 500px;
                    overflow-y: auto;
                    overflow-x: hidden;
                    border: 2px solid rgba(255,255,255,0.2);
                    border-radius: 12px;
                    background: rgba(0,0,0,0.1);
                    padding: 1rem;
                ">
            """, unsafe_allow_html=True)

            # Enhanced table header with better styling
            header_cols = st.columns([1, 3, 1, 1, 1, 2])
            with header_cols[0]:
                st.markdown("**🏆 Rank**")
            with header_cols[1]:
                st.markdown("**👤 Player**")
            with header_cols[2]:
                st.markdown("**📍 Pos**")
            with header_cols[3]:
                st.markdown("**🏟️ Team**")
            with header_cols[4]:
                st.markdown("**📊 VBD**")
            with header_cols[5]:
                st.markdown("**⚡ Action**")

            st.markdown("<hr style='margin: 1rem 0; border: 2px solid rgba(255,255,255,0.3);'>", unsafe_allow_html=True)

            # Player rows with enhanced styling
            for idx, (_, player) in enumerate(filtered_players.iterrows()):
                self.render_enhanced_player_row(player, idx, is_user_turn)

            st.markdown("</div></div>", unsafe_allow_html=True)

    def calculate_picks_until_user_turn(self) -> int:
        """Calculate how many picks until the user's next turn."""
        current_pick = st.session_state.current_pick_number
        user_position = st.session_state.user_draft_position

        # Find next user pick
        next_user_pick = current_pick
        while next_user_pick <= 120:  # 12 rounds * 10 teams
            team_index = self.get_pick_order(next_user_pick)
            if team_index == user_position - 1:
                return next_user_pick - current_pick
            next_user_pick += 1

        return 0  # Draft complete

    def render_enhanced_player_row(self, player, idx, is_user_turn):
        """Render enhanced individual player row with better styling."""
        # Position-based styling
        pos_colors = {
            'QB': '#e74c3c', 'RB': '#3498db', 'WR': '#f39c12', 
            'TE': '#27ae60', 'K': '#9b59b6', 'DEF': '#34495e'
        }
        pos_color = pos_colors.get(player['Position'], '#666')

        # Create enhanced table row with hover effects
        row_cols = st.columns([1, 3, 1, 1, 1, 2])

        # Row styling with alternating colors
        row_bg = "rgba(255,255,255,0.08)" if idx % 2 == 0 else "rgba(255,255,255,0.04)"

        st.markdown(f"""
        <div style="
            background: {row_bg}; 
            border-radius: 8px; 
            padding: 0.8rem 0.5rem; 
            margin: 0.3rem 0;
            border: 1px solid rgba(255,255,255,0.1);
            transition: all 0.2s ease;
        ">
        """, unsafe_allow_html=True)

        with row_cols[0]:
            rank_color = "#FFD700" if player['Overall_Rank'] <= 10 else "#C0C0C0" if player['Overall_Rank'] <= 25 else "#CD7F32" if player['Overall_Rank'] <= 50 else "#666"
            st.markdown(f"<div style='font-weight: bold; color: {rank_color}; font-size: 1.1rem;'>#{int(player['Overall_Rank'])}</div>", unsafe_allow_html=True)

        with row_cols[1]:
            # Enhanced player name display with value indicators
            player_name = str(player.get('Player_Name', 'Unknown Player'))
            value_indicator = "💎 " if player.get('Value_Pick', False) else ""
            st.markdown(f"<div style='font-weight: 600; font-size: 1rem;'>{value_indicator}{player_name}</div>", unsafe_allow_html=True)

        with row_cols[2]:
            st.markdown(f"<span style='background: {pos_color}; color: white; padding: 0.3rem 0.6rem; border-radius: 6px; font-size: 0.8rem; font-weight: bold;'>{player['Position']}</span>", unsafe_allow_html=True)

        with row_cols[3]:
            team_name = str(player.get('Team', 'UNK'))
            st.markdown(f"<div style='font-weight: 500;'>{team_name}</div>", unsafe_allow_html=True)

        with row_cols[4]:
            try:
                vbd_val = float(player.get('VBD_Value', 0))
            except (ValueError, TypeError):
                vbd_val = 0.0

            if vbd_val >= 15:
                vbd_color = '#00ff87'  # Elite
                vbd_emoji = '🔥'
            elif vbd_val >= 10:
                vbd_color = '#4facfe'  # High
                vbd_emoji = '⭐'
            elif vbd_val >= 5:
                vbd_color = '#43e97b'  # Medium
                vbd_emoji = '📈'
            else:
                vbd_color = '#fa709a'  # Low
                vbd_emoji = '📊'
            st.markdown(f"<div style='color: {vbd_color}; font-weight: bold; font-size: 1rem;'>{vbd_emoji} {vbd_val:.1f}</div>", unsafe_allow_html=True)

        with row_cols[5]:
            if is_user_turn:
                player_name = str(player.get('Player_Name', f'player_{idx}'))
                button_key = f"draft_{player_name}_{idx}"
                if st.button(f"📝 DRAFT", key=button_key, type="primary", use_container_width=True):
                    self.make_user_pick(player)
                    st.rerun()
            else:
                st.markdown("<div style='text-align: center; padding: 0.6rem; background: rgba(102,126,234,0.1); border-radius: 8px; font-size: 0.8rem; color: rgba(255,255,255,0.7);'>Available</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    def render_player_table_row(self, player, idx, is_user_turn):
        """Render individual player row in the draft board table."""
        # Position-based styling
        pos_colors = {
            'QB': '#e74c3c', 'RB': '#3498db', 'WR': '#f39c12', 
            'TE': '#27ae60', 'K': '#9b59b6', 'DEF': '#34495e'
        }
        pos_color = pos_colors.get(player['Position'], '#666')

        # Create table row with columns
        row_cols = st.columns([1, 3, 1, 1, 1, 2])

        with row_cols[0]:
            st.markdown(f"**#{int(player['Overall_Rank'])}**")

        with row_cols[1]:
            # Safe player name display
            player_name = str(player.get('Player_Name', 'Unknown Player'))
            st.markdown(f"**{player_name}**")

        with row_cols[2]:
            st.markdown(f"<span style='background: {pos_color}; color: white; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem;'>{player['Position']}</span>", unsafe_allow_html=True)

        with row_cols[3]:
            # Safe team display
            team_name = str(player.get('Team', 'UNK'))
            st.markdown(f"{team_name}")

        with row_cols[4]:
            # Safe VBD value display with proper type conversion
            try:
                vbd_val = float(player.get('VBD_Value', 0))
            except (ValueError, TypeError):
                vbd_val = 0.0

            if vbd_val >= 10:
                vbd_color = '#00ff87'  # Elite
            elif vbd_val >= 5:
                vbd_color = '#4facfe'  # High
            elif vbd_val >= 2:
                vbd_color = '#43e97b'  # Medium
            else:
                vbd_color = '#fa709a'  # Low
            st.markdown(f"<span style='color: {vbd_color}; font-weight: bold;'>{vbd_val:.1f}</span>", unsafe_allow_html=True)

        with row_cols[5]:
            if is_user_turn:
                # Use unique key based on player name to prevent issues
                player_name = str(player.get('Player_Name', f'player_{idx}'))
                button_key = f"draft_{player_name}_{idx}"
                if st.button(f"📝 DRAFT", key=button_key, type="primary", use_container_width=True):
                    self.make_user_pick(player)
                    st.rerun()
            else:
                st.markdown("<div style='text-align: center; padding: 0.5rem; background: rgba(255,255,255,0.1); border-radius: 6px; font-size: 0.8rem;'>Available</div>", unsafe_allow_html=True)

        # Add subtle divider (optimized)
        if idx < 19:  # Don't add divider after last row (updated from 29 to 19)
            st.markdown("<hr style='margin: 0.5rem 0; border: 1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

    def make_user_pick(self, player_row):
        """Process user's player selection with optimized data handling."""
        # Ensure player_row is a Series or dict
        if hasattr(player_row, 'to_dict'):
            player_dict = player_row.to_dict()
        else:
            player_dict = player_row

        # Calculate roster slot for this pick
        user_picks_count = len([p for p in st.session_state.draft_results if p['team'] == 'Your Team'])
        roster_slot = self.get_user_roster_slot(user_picks_count + 1)

        # Add pick to results with safe data access
        pick_info = {
            'pick': st.session_state.current_pick_number,
            'round': ((st.session_state.current_pick_number - 1) // 10) + 1,
            'team': 'Your Team',
            'player': str(player_dict.get('Player_Name', 'Unknown Player')),
            'position': str(player_dict.get('Position', 'UNKNOWN')),
            'team_name': str(player_dict.get('Team', 'Unknown')),
            'vbd': float(player_dict.get('VBD_Value', 0)),
            'overall_rank': int(player_dict.get('Overall_Rank', 999)),
            'roster_slot': roster_slot
        }

        st.session_state.draft_results.append(pick_info)

        # Remove player from available (optimized)
        player_name = player_dict.get('Player_Name')
        st.session_state.available_players = st.session_state.available_players[
            st.session_state.available_players['Player_Name'] != player_name
        ].reset_index(drop=True)

        # Add to user team
        if st.session_state.draft_simulator:
            st.session_state.draft_simulator.user_team.append(player_dict)

        # Move to next pick and reset timer
        st.session_state.current_pick_number += 1
        st.session_state.waiting_for_user_pick = False
        st.session_state.pick_timer_start = datetime.now()

        # Check if draft is complete (12 rounds * 10 teams = 120 picks)
        max_picks = 12 * 10
        if st.session_state.current_pick_number > max_picks:
            st.session_state.draft_completed = True

        # Show success message
        st.success(f"🎯 Excellent pick! You drafted {pick_info['player']} ({pick_info['position']}) in Round {pick_info['round']}")

    def handle_user_pick(self):
        """Handle when it's the user's turn to pick."""
        # Initialize timer if not started
        if not st.session_state.pick_timer_start:
            self.start_pick_timer()

        # Check if timer expired
        if self.is_timer_expired(60):
            # Auto-pick best available player
            if len(st.session_state.available_players) > 0:
                best_player = st.session_state.available_players.iloc[0]
                st.error(f"⏰ Time expired! Auto-drafted {best_player['Player_Name']}")
                self.make_user_pick(best_player)
                st.rerun()
        else:
            # Show remaining time countdown every few seconds
            remaining = self.get_remaining_time()
            if remaining <= 10 and int(remaining) % 2 == 0:  # Update every 2 seconds when time is low
                st.rerun()

    def handle_ai_pick(self):
        """Handle AI picks with faster, more realistic timing and improved logic."""
        if not st.session_state.pick_timer_start:
            self.start_pick_timer()
            return

        elapsed = (datetime.now() - st.session_state.pick_timer_start).total_seconds()

        # Faster AI picks: 1.5-3 seconds (more realistic draft pace)
        if not hasattr(st.session_state, 'ai_pick_time'):
            st.session_state.ai_pick_time = random.uniform(1.5, 3.0)

        if elapsed >= st.session_state.ai_pick_time and not st.session_state.waiting_for_user_pick:
            # Make AI pick with enhanced logic
            simulator = st.session_state.draft_simulator
            team_index = simulator.get_pick_order(st.session_state.current_pick_number)

            if len(st.session_state.available_players) > 0:
                # Correct AI team mapping
                if team_index == st.session_state.user_draft_position - 1:
                    return  # This is actually the user's turn, don't make AI pick

                # Enhanced AI team mapping
                ai_team_index = self.get_ai_team_index(team_index)
                ai_pick = self.make_enhanced_ai_pick(ai_team_index, st.session_state.available_players)

                if ai_pick:
                    pick_info = {
                        'pick': st.session_state.current_pick_number,
                        'round': ((st.session_state.current_pick_number - 1) // 10) + 1,
                        'team': f'AI Team {team_index + 1}',
                        'player': ai_pick.get('Player_Name', 'Unknown Player'),
                        'position': ai_pick.get('Position', 'UNKNOWN'),
                        'team_name': ai_pick.get('Team', 'Unknown'),
                        'vbd': float(ai_pick.get('VBD_Value', 0)),
                        'overall_rank': int(ai_pick.get('Overall_Rank', 999))
                    }

                    st.session_state.draft_results.append(pick_info)

                    # Remove player from available
                    st.session_state.available_players = st.session_state.available_players[
                        st.session_state.available_players['Player_Name'] != ai_pick.get('Player_Name')
                    ].reset_index(drop=True)

                    # Add to correct AI team
                    if ai_team_index < 9:
                        simulator.ai_teams[ai_team_index].append(ai_pick)

                    # Move to next pick
                    st.session_state.current_pick_number += 1
                    st.session_state.pick_timer_start = datetime.now()
                    if hasattr(st.session_state, 'ai_pick_time'):
                        del st.session_state.ai_pick_time

                    # Check if draft is complete
                    max_picks = st.session_state.draft_rounds * 10
                    if st.session_state.current_pick_number > max_picks:
                        st.session_state.draft_completed = True

                    # Enhanced pick notification with more context
                    round_num = pick_info['round']
                    pick_context = self.get_pick_context(pick_info)
                    st.success(f"🤖 R{round_num} Pick #{pick_info['pick']}: {pick_info['team']} selected {pick_info['player']} ({pick_info['position']}) {pick_context}")

                    st.rerun()

        # More responsive refresh timing
        if not st.session_state.waiting_for_user_pick and st.session_state.pick_timer_start:
            elapsed = (datetime.now() - st.session_state.pick_timer_start).total_seconds()
            # Faster refresh rate for better user experience
            if elapsed < 5:  # Refresh more frequently during AI pick window
                time.sleep(0.3)
                st.rerun()

    def get_ai_team_index(self, team_index: int) -> int:
        """Get correct AI team index with improved mapping."""
        # Map team index to AI team (exclude user position)
        ai_teams_mapping = [i for i in range(10) if i != st.session_state.user_draft_position - 1]

        if team_index < len(ai_teams_mapping):
            return ai_teams_mapping.index(team_index) if team_index in ai_teams_mapping else 0
        else:
            return 0

    def make_enhanced_ai_pick(self, ai_team_index: int, available_players: pd.DataFrame) -> dict:
        """Enhanced AI pick logic with more realistic decision making."""
        simulator = st.session_state.draft_simulator

        # Ensure valid AI team index
        if ai_team_index < 0 or ai_team_index >= 9:
            ai_team_index = 0

        team_roster = simulator.ai_teams[ai_team_index]
        current_round = ((st.session_state.current_pick_number - 1) // 10) + 1

        # Advanced AI logic based on draft philosophy
        ai_personalities = [
            'value_focused',    # Strictly follows VBD
            'positional_need',  # Fills roster slots methodically  
            'best_available',   # Always takes highest ranked
            'sleeper_hunter',   # Looks for breakout candidates
            'conservative',     # Safe, proven players
            'aggressive',       # High upside, high risk
            'balanced',         # Mix of strategies
            'contrarian',       # Goes against conventional wisdom
            'analytics_heavy'   # Data-driven decisions
        ]

        # Assign AI personality based on team index
        ai_personality = ai_personalities[ai_team_index % len(ai_personalities)]

        # Get team needs analysis
        position_counts = {}
        for player in team_roster:
            pos = player.get('Position', 'UNKNOWN')
            position_counts[pos] = position_counts.get(pos, 0) + 1

        # Apply AI personality to pick selection
        candidates = self.filter_candidates_by_ai_logic(
            available_players, ai_personality, position_counts, current_round, team_roster
        )

        if len(candidates) == 0:
            candidates = available_players.head(10)  # Fallback to top players

        # Select player with personality-based weighting
        selected_player = self.select_player_with_personality(candidates, ai_personality, current_round)

        return selected_player.to_dict() if selected_player is not None else None

    def filter_candidates_by_ai_logic(self, available: pd.DataFrame, personality: str, 
                                    position_counts: dict, current_round: int, team_roster: list) -> pd.DataFrame:
        """Filter candidates based on AI personality and advanced logic."""
        if personality == 'value_focused':
            # VBD-focused: Top VBD players regardless of position
            return available.nlargest(8, 'VBD_Value')

        elif personality == 'positional_need':
            # Methodical roster building
            needed_positions = self.get_positional_needs(position_counts, current_round)
            if needed_positions:
                return available[available['Position'].isin(needed_positions)].head(10)
            return available.head(8)

        elif personality == 'best_available':
            # Strictly by overall rank
            return available.head(5)

        elif personality == 'sleeper_hunter':
            # Look for high upside players ranked lower
            if current_round >= 6:
                sleepers = available[
                    (available['VBD_Value'] > 8) & 
                    (available['Overall_Rank'] > 60)
                ]
                if len(sleepers) > 0:
                    return sleepers.head(6)
            return available.head(8)

        elif personality == 'conservative':
            # Prefer proven, safe picks with good floors
            return available[available['VBD_Value'] >= 5].head(8)

        elif personality == 'aggressive':
            # High ceiling players, might reach for upside
            high_upside = available[
                (available.get('Value_Pick', False) == True) |
                (available['VBD_Value'] > 12)
            ]
            if len(high_upside) > 0:
                return high_upside.head(6)
            return available.head(8)

        elif personality == 'contrarian':
            # Goes against the grain, might draft positions early/late
            if current_round <= 5:
                # Might draft TE or QB early
                contrarian_picks = available[available['Position'].isin(['TE', 'QB'])].head(3)
                if len(contrarian_picks) > 0:
                    return pd.concat([contrarian_picks, available.head(5)])
            return available.head(8)

        elif personality == 'analytics_heavy':
            # Heavy focus on advanced metrics and value picks
            analytics_picks = available[
                (available.get('Value_Pick', False) == True) |
                (available['VBD_Value'] > available['VBD_Value'].quantile(0.7))
            ]
            if len(analytics_picks) > 0:
                return analytics_picks.head(8)
            return available.head(6)

        else:  # balanced
            # Mix of BPA and positional need
            bpa_count = 4
            need_count = 4

            bpa_players = available.head(bpa_count)
            needed_positions = self.get_positional_needs(position_counts, current_round)

            if needed_positions:
                need_players = available[available['Position'].isin(needed_positions)].head(need_count)
                return pd.concat([bpa_players, need_players]).drop_duplicates()

            return bpa_players

    def get_positional_needs(self, position_counts: dict, current_round: int) -> list:
        """Get positional needs for AI team based on current roster and round."""
        needs = []

        # Basic positional requirements check
        if position_counts.get('QB', 0) == 0 and current_round <= 8:
            needs.append('QB')

        if position_counts.get('RB', 0) < 2 and current_round <= 10:
            needs.append('RB')

        if position_counts.get('WR', 0) < 2 and current_round <= 10:
            needs.append('WR')

        if position_counts.get('TE', 0) == 0 and current_round <= 12:
            needs.append('TE')

        # Late round needs
        if current_round >= 8:
            if position_counts.get('K', 0) == 0:
                needs.append('K')
            if position_counts.get('DEF', 0) == 0:
                needs.append('DEF')

        return needs

    def select_player_with_personality(self, candidates: pd.DataFrame, 
                                     personality: str, current_round: int) -> pd.Series:
        """Select player from candidates based on AI personality."""
        if len(candidates) == 0:
            return None

        # Personality-based selection weights
        if personality in ['value_focused', 'analytics_heavy']:
            # Heavy bias toward top VBD
            weights = [1.0 / (i + 1) ** 1.5 for i in range(len(candidates))]
        elif personality == 'best_available':
            # Strong bias toward top ranked
            weights = [1.0 / (i + 1) ** 2 for i in range(len(candidates))]
        elif personality in ['sleeper_hunter', 'aggressive']:
            # More random, willing to reach
            weights = [1.0 / (i + 1) ** 0.8 for i in range(len(candidates))]
        elif personality == 'contrarian':
            # Sometimes picks unexpectedly
            if random.random() < 0.3:  # 30% chance of surprise pick
                weights = [1.0 for _ in range(len(candidates))]  # Equal probability
            else:
                weights = [1.0 / (i + 1) for i in range(len(candidates))]
        else:  # conservative, balanced, positional_need
            # Moderate bias toward top players
            weights = [1.0 / (i + 1) for i in range(len(candidates))]

        # Normalize weights
        weights = [w / sum(weights) for w in weights]

        # Select player
        selected_idx = np.random.choice(len(candidates), p=weights)
        return candidates.iloc[selected_idx]

    def get_pick_context(self, pick_info: dict) -> str:
        """Get contextual information about the pick."""
        vbd = pick_info.get('vbd', 0)
        overall_rank = pick_info.get('overall_rank', 999)

        if vbd > 20:
            return "🔥 (Elite Pick!)"
        elif vbd > 15:
            return "⭐ (Great Value)"
        elif overall_rank <= 10:
            return "👑 (Top 10 Player)"
        elif overall_rank <= 25:
            return "📈 (Solid Pick)"
        else:
            return "📊 (Depth Pick)"

    def display_draft_results_and_grading(self):
        """Display draft results with AI grading and analytics."""
        st.markdown("## 🏆 Draft Complete - AI Analysis & Grading")

        # AI Draft Grade
        user_team = st.session_state.draft_simulator.user_team if st.session_state.draft_simulator else []
        draft_grade = self.calculate_draft_grade(user_team)

        # Prominent draft grade display
        st.markdown(f"""
        <div class="vbd-analysis-container" style="text-align: center; margin: 2rem 0;">
            <h1 style="font-size: 4rem; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                {draft_grade['letter_grade']}
            </h1>
            <h2 style="margin: 0; color: rgba(255,255,255,0.9);">Draft Grade: {draft_grade['score']:.1f}/100</h2>
            <p style="font-size: 1.2rem; margin: 1rem 0; color: rgba(255,255,255,0.8);">{draft_grade['summary']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Detailed analytics tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🏆 Your Team", "📊 Draft Grade Breakdown", "📈 Advanced Analytics", 
            "🔮 Future Suggestions", "📋 Full Draft Board"
        ])

        with tab1:
            self.display_user_team_analysis(user_team, draft_grade)

        with tab2:
            self.display_draft_grade_breakdown(draft_grade)

        with tab3:
            self.display_advanced_analytics(user_team)

        with tab4:
            self.display_future_suggestions(user_team, draft_grade)

        with tab5:
            self.display_full_draft_board()

    def calculate_draft_grade(self, user_team: List[dict]) -> dict:
        """Calculate comprehensive AI draft grade for 12-player roster."""
        if not user_team or len(user_team) != 12:
            return {
                'score': 0,
                'letter_grade': 'F',
                'summary': 'Incomplete draft - 12 players required',
                'breakdown': {}
            }

        # Calculate various grading metrics
        total_vbd = sum(player.get('VBD_Value', 0) for player in user_team)
        avg_vbd = total_vbd / len(user_team) if user_team else 0

        # Position analysis with 12-player roster requirements
        position_counts = {}
        position_vbd = {}
        starter_vbd = 0  # VBD from starting lineup (first 9 picks)
        bench_vbd = 0    # VBD from bench (last 3 picks)

        for idx, player in enumerate(user_team):
            pos = player.get('Position', 'UNKNOWN')
            position_counts[pos] = position_counts.get(pos, 0) + 1
            position_vbd[pos] = position_vbd.get(pos, 0) + player.get('VBD_Value', 0)

            # Separate starter vs bench value
            if idx < 9:  # First 9 picks are starters
                starter_vbd += player.get('VBD_Value', 0)
            else:  # Last 3 picks are bench
                bench_vbd += player.get('VBD_Value', 0)

        # Enhanced scoring components for 12-player format

        # 1. VBD Score (30 points max) - prioritize starter value
        starter_vbd_score = min(25, (starter_vbd / 120) * 25)  # Starters worth more
        bench_vbd_score = min(5, (bench_vbd / 30) * 5)        # Bench depth bonus
        vbd_score = starter_vbd_score + bench_vbd_score

        # 2. Roster Construction Score (25 points max)
        required_positions = {'QB': 1, 'WR': 2, 'RB': 2, 'TE': 1, 'K': 1, 'DEF': 1}
        construction_score = 0

        for pos, required in required_positions.items():
            actual = position_counts.get(pos, 0)
            if actual >= required:
                construction_score += (25 / len(required_positions))
            else:
                construction_score += (actual / required) * (25 / len(required_positions))

        # Bonus for FLEX diversity (having different position types)
        flex_players = user_team[6:7] if len(user_team) > 6 else []  # 7th pick is FLEX
        flex_positions = set()
        for player in flex_players:
            pos = player.get('Position', 'UNKNOWN')
            if pos in ['WR', 'RB', 'TE']:
                flex_positions.add(pos)

        if len(flex_positions) > 0:
            construction_score += 2  # Bonus for proper FLEX usage

        # 3. Value and Strategy Score (25 points max)
        value_picks = sum(1 for player in user_team if player.get('Value_Pick', False))
        early_value_picks = sum(1 for i, player in enumerate(user_team[:6]) if player.get('Value_Pick', False))

        value_strategy_score = min(15, (value_picks / 12) * 30)  # Overall value identification
        early_strategy_score = min(10, (early_value_picks / 6) * 20)  # Early round value
        strategy_score = value_strategy_score + early_strategy_score

        # 4. Draft Order Execution Score (20 points max)
        execution_score = 20

        # Check if positions were drafted in reasonable order
        position_order_check = {
            0: 'QB',     # Round 1: QB
            1: 'WR',     # Round 2: WR1  
            2: 'WR',     # Round 3: WR2
            3: 'RB',     # Round 4: RB1
            4: 'RB',     # Round 5: RB2
            5: 'TE',     # Round 6: TE
            6: ['WR', 'RB', 'TE'],  # Round 7: FLEX
            7: 'K',      # Round 8: K
            8: 'DEF'     # Round 9: DEF
        }

        for pick_idx, expected_pos in position_order_check.items():
            if pick_idx < len(user_team):
                actual_pos = user_team[pick_idx].get('Position', 'UNKNOWN')

                if isinstance(expected_pos, list):
                    if actual_pos not in expected_pos:
                        execution_score -= 2  # Penalty for wrong FLEX position
                else:
                    if actual_pos != expected_pos:
                        execution_score -= 3  # Penalty for wrong position

        # Penalty for drafting K/DEF too early
        for idx in range(7):  # First 7 picks shouldn't be K/DEF
            if idx < len(user_team):
                pos = user_team[idx].get('Position', 'UNKNOWN')
                if pos in ['K', 'DEF']:
                    execution_score -= 5

        execution_score = max(0, execution_score)

        # Calculate final score
        final_score = vbd_score + construction_score + strategy_score + execution_score

        # Letter grade
        if final_score >= 90:
            letter_grade = 'A+'
        elif final_score >= 85:
            letter_grade = 'A'
        elif final_score >= 80:
            letter_grade = 'A-'
        elif final_score >= 75:
            letter_grade = 'B+'
        elif final_score >= 70:
            letter_grade = 'B'
        elif final_score >= 65:
            letter_grade = 'B-'
        elif final_score >= 60:
            letter_grade = 'C+'
        elif final_score >= 55:
            letter_grade = 'C'
        elif final_score >= 50:
            letter_grade = 'C-'
        elif final_score >= 45:
            letter_grade = 'D+'
        elif final_score >= 40:
            letter_grade = 'D'
        else:
            letter_grade = 'F'

        # Generate summary
        if final_score >= 85:
            summary = "🔥 Excellent draft! Outstanding value and team construction."
        elif final_score >= 75:
            summary = "⭐ Very good draft with solid players and good strategy."
        elif final_score >= 65:
            summary = "👍 Good draft with room for improvement in some areas."
        elif final_score >= 55:
            summary = "📊 Average draft, consider improving draft strategy."
        else:
            summary = "⚠️ Below average draft, significant improvements needed."

        return {
            'score': final_score,
            'letter_grade': letter_grade,
            'summary': summary,
            'breakdown': {
                'vbd_score': vbd_score,
                'construction_score': construction_score,
                'strategy_score': strategy_score,
                'execution_score': execution_score,
                'total_vbd': total_vbd,
                'starter_vbd': starter_vbd,
                'bench_vbd': bench_vbd,
                'avg_vbd': avg_vbd,
                'value_picks': value_picks,
                'early_value_picks': early_value_picks
            }
        }

    def display_user_team_analysis(self, user_team: List[dict], draft_grade: dict):
        """Display detailed user team analysis for 12-player roster."""
        st.markdown("### 🏆 Your Final 12-Player Team")

        if not user_team:
            st.info("No players drafted yet.")
            return

        # Team composition with roster slots
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("#### 📋 Starting Lineup")

            # Display starters (first 9 picks) with proper roster slots
            for idx, player in enumerate(user_team[:9]):
                roster_slot = self.get_user_roster_slot(idx + 1)
                pick_round = idx + 1

                # Roster slot styling
                slot_colors = {
                    'QB': '#e74c3c', 'WR': '#f39c12', 'RB': '#3498db', 
                    'TE': '#27ae60', 'FLEX': '#9b59b6', 'K': '#34495e', 'DEF': '#7f8c8d'
                }
                slot_color = slot_colors.get(roster_slot, '#667eea')

                st.markdown(f"""
                <div class="draft-pick" style="border-left: 4px solid {slot_color};">
                    <div style="background: {slot_color}; color: white; padding: 0.5rem; border-radius: 8px; font-weight: 700; min-width: 80px; text-align: center; margin-right: 1rem;">
                        {roster_slot}
                    </div>
                    <div style="flex-grow: 1;">
                        <div style="font-weight: 600; font-size: 1.1rem;">{player['Player_Name']}</div>
                        <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
                            <span class="position-badge pos-{player['Position'].lower()}">{player['Position']}</span>
                            <span class="team-badge">{player.get('Team', 'UNK')}</span>
                            <span style="margin-left: 0.5rem;">VBD: {player.get('VBD_Value', 0):.1f}</span>
                            <span style="margin-left: 0.5rem;">Rank: #{player.get('Overall_Rank', 999)}</span>
                        </div>
                    </div>
                    <div style="text-align: right; color: rgba(255,255,255,0.6);">
                        Round {pick_round}
                        {'<div style="color: #00ff87; font-size: 0.8rem;">💎 VALUE</div>' if player.get('Value_Pick', False) else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Display bench players
            if len(user_team) > 9:
                st.markdown("#### 🪑 Bench Players")

                for idx, player in enumerate(user_team[9:]):
                    bench_round = idx + 10

                    st.markdown(f"""
                    <div class="draft-pick" style="border-left: 4px solid #95a5a6;">
                        <div style="background: #95a5a6; color: white; padding: 0.5rem; border-radius: 8px; font-weight: 700; min-width: 80px; text-align: center; margin-right: 1rem;">
                            BENCH
                        </div>
                        <div style="flex-grow: 1;">
                            <div style="font-weight: 600; font-size: 1.1rem;">{player['Player_Name']}</div>
                            <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
                                <span class="position-badge pos-{player['Position'].lower()}">{player['Position']}</span>
                                <span class="team-badge">{player.get('Team', 'UNK')}</span>
                                <span style="margin-left: 0.5rem;">VBD: {player.get('VBD_Value', 0):.1f}</span>
                                <span style="margin-left: 0.5rem;">Rank: #{player.get('Overall_Rank', 999)}</span>
                            </div>
                        </div>
                        <div style="text-align: right; color: rgba(255,255,255,0.6);">
                            Round {bench_round}
                            {'<div style="color: #00ff87; font-size: 0.8rem;">💎 VALUE</div>' if player.get('Value_Pick', False) else ''}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        with col2:
            st.markdown("#### 📊 12-Player Team Stats")

            # Roster verification
            required_positions = {'QB': 1, 'WR': 2, 'RB': 2, 'TE': 1, 'K': 1, 'DEF': 1}
            position_counts = {}
            for player in user_team:
                pos = player.get('Position', 'UNKNOWN')
                position_counts[pos] = position_counts.get(pos, 0) + 1

            st.markdown("**Roster Check:**")
            for pos, required in required_positions.items():
                actual = position_counts.get(pos, 0)
                status = "✅" if actual >= required else "❌"
                st.markdown(f"{status} **{pos}:** {actual}/{required}")

            # FLEX and Bench analysis
            flex_count = sum(1 for p in user_team if p.get('Position') in ['WR', 'RB', 'TE']) - 5  # Subtract required WR/RB/TE
            st.markdown(f"🔄 **FLEX Options:** {max(0, flex_count)}")
            st.markdown(f"🪑 **Bench Depth:** {len(user_team) - 9}")

            st.markdown("---")

            # Enhanced metrics for 12-player format
            total_vbd = sum(player.get('VBD_Value', 0) for player in user_team)
            starter_vbd = sum(player.get('VBD_Value', 0) for player in user_team[:9])
            bench_vbd = sum(player.get('VBD_Value', 0) for player in user_team[9:])
            value_picks = sum(1 for player in user_team if player.get('Value_Pick', False))

            st.metric("Starter VBD", f"{starter_vbd:.1f}")
            st.metric("Bench VBD", f"{bench_vbd:.1f}")
            st.metric("Total VBD", f"{total_vbd:.1f}")
            st.metric("Value Picks", f"{value_picks}/12")

    def display_draft_grade_breakdown(self, draft_grade: dict):
        """Display detailed breakdown of draft grade."""
        st.markdown("### 📊 AI Draft Grade Breakdown")

        breakdown = draft_grade['breakdown']

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🎯 Scoring Components")

            # Score breakdown chart for 12-player format
            components = ['VBD Score', 'Roster Construction', 'Strategy & Value', 'Draft Execution']
            scores = [
                breakdown['vbd_score'],
                breakdown['construction_score'], 
                breakdown['strategy_score'],
                breakdown['execution_score']
            ]
            max_scores = [30, 25, 25, 20]

            fig_breakdown = go.Figure()

            fig_breakdown.add_trace(go.Bar(
                name='Your Score',
                x=components,
                y=scores,
                marker_color='#667eea'
            ))

            fig_breakdown.add_trace(go.Bar(
                name='Max Possible',
                x=components,
                y=max_scores,
                marker_color='rgba(255,255,255,0.3)'
            ))

            fig_breakdown.update_layout(
                title="Draft Grade Components",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                barmode='overlay'
            )

            st.plotly_chart(fig_breakdown, use_container_width=True)

        with col2:
            st.markdown("#### 📈 Performance Metrics")

            st.metric("VBD Score", f"{breakdown['vbd_score']:.1f}/30")
            st.metric("Roster Construction", f"{breakdown['construction_score']:.1f}/25")
            st.metric("Strategy & Value", f"{breakdown['strategy_score']:.1f}/25")
            st.metric("Draft Execution", f"{breakdown['execution_score']:.1f}/20")

            st.markdown("---")

            st.metric("Starter VBD", f"{breakdown['starter_vbd']:.1f}")
            st.metric("Bench VBD", f"{breakdown['bench_vbd']:.1f}")
            st.metric("Total VBD", f"{breakdown['total_vbd']:.1f}")
            st.metric("Value Picks", f"{breakdown['value_picks']}/12")
            st.metric("Early Value Picks", f"{breakdown['early_value_picks']}/6")

    def display_advanced_analytics(self, user_team: List[dict]):
        """Display advanced analytics for user's team."""
        st.markdown("### 📈 Advanced Team Analytics")

        if not user_team:
            st.info("No team data available for analysis.")
            return

        col1, col2 = st.columns(2)

        with col1:
            # Position VBD breakdown
            position_vbd = {}
            for player in user_team:
                pos = player.get('Position', 'UNKNOWN')
                position_vbd[pos] = position_vbd.get(pos, 0) + player.get('VBD_Value', 0)

            fig_pos_vbd = px.bar(
                x=list(position_vbd.keys()),
                y=list(position_vbd.values()),
                title="VBD Score by Position",
                color=list(position_vbd.values()),
                color_continuous_scale='Viridis'
            )

            fig_pos_vbd.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )

            st.plotly_chart(fig_pos_vbd, use_container_width=True)

        with col2:
            # Draft round efficiency
            round_picks = {}
            round_vbd = {}

            for idx, player in enumerate(user_team):
                round_num = (idx // 10) + 1
                round_picks[round_num] = round_picks.get(round_num, 0) + 1
                round_vbd[round_num] = round_vbd.get(round_num, 0) + player.get('VBD_Value', 0)

            if round_vbd:
                fig_round_eff = px.line(
                    x=list(round_vbd.keys()),
                    y=[round_vbd[r]/round_picks[r] for r in round_vbd.keys()],
                    title="Average VBD by Draft Round",
                    markers=True
                )

                fig_round_eff.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis_title="Round",
                    yaxis_title="Average VBD"
                )

                st.plotly_chart(fig_round_eff, use_container_width=True)

        # Team strengths and weaknesses
        st.markdown("#### 💪 Team Analysis")

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.markdown("##### 🔥 Team Strengths")
            strengths = self.analyze_team_strengths(user_team)
            for strength in strengths:
                st.markdown(f"• {strength}")

        with col_b:
            st.markdown("##### ⚠️ Areas for Improvement")
            weaknesses = self.analyze_team_weaknesses(user_team)
            for weakness in weaknesses:
                st.markdown(f"• {weakness}")

        with col_c:
            st.markdown("##### 🎯 Key Insights")
            insights = self.generate_team_insights(user_team)
            for insight in insights:
                st.markdown(f"• {insight}")

    def analyze_team_strengths(self, user_team: List[dict]) -> List[str]:
        """Analyze team strengths."""
        strengths = []

        # Position analysis
        position_counts = {}
        position_vbd = {}
        for player in user_team:
            pos = player.get('Position', 'UNKNOWN')
            position_counts[pos] = position_counts.get(pos, 0) + 1
            position_vbd[pos] = position_vbd.get(pos, 0) + player.get('VBD_Value', 0)

        # Check for positional strengths
        for pos, vbd_total in position_vbd.items():
            avg_vbd = vbd_total / position_counts[pos]
            if avg_vbd >= 20:
                strengths.append(f"Elite {pos} corps with {avg_vbd:.1f} avg VBD")
            elif avg_vbd >= 10:
                strengths.append(f"Strong {pos} depth with {avg_vbd:.1f} avg VBD")

        # Value pick analysis
        value_picks = sum(1 for player in user_team if player.get('Value_Pick', False))
        if value_picks >= 3:
            strengths.append(f"Excellent value identification ({value_picks} value picks)")
        elif value_picks >= 2:
            strengths.append(f"Good value drafting ({value_picks} value picks)")

        # Total VBD analysis
        total_vbd = sum(player.get('VBD_Value', 0) for player in user_team)
        if total_vbd >= 150:
            strengths.append(f"Outstanding total VBD score ({total_vbd:.1f})")
        elif total_vbd >= 100:
            strengths.append(f"Strong total VBD accumulation ({total_vbd:.1f})")

        return strengths[:5]  # Top 5 strengths

    def analyze_team_weaknesses(self, user_team: List[dict]) -> List[str]:
        """Analyze team weaknesses."""
        weaknesses = []

        # Position analysis
        position_counts = {}
        for player in user_team:
            pos = player.get('Position', 'UNKNOWN')
            position_counts[pos] = position_counts.get(pos, 0) + 1

        # Check for missing positions
        required_positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']
        for pos in required_positions:
            if position_counts.get(pos, 0) == 0:
                weaknesses.append(f"Missing {pos} - need to address via waivers")

        # Check for thin positions
        if position_counts.get('RB', 0) < 2:
            weaknesses.append("Thin at RB - high injury risk position")
        if position_counts.get('WR', 0) < 2:
            weaknesses.append("Limited WR depth - need more pass catchers")

        # Check for early kicker/defense
        for idx, player in enumerate(user_team[:12]):  # First 12 picks
            if player.get('Position') in ['K', 'DEF']:
                weaknesses.append(f"Drafted {player.get('Position')} too early (pick {idx + 1})")

        # Low VBD players
        low_vbd_picks = [p for p in user_team if p.get('VBD_Value', 0) < 0]
        if len(low_vbd_picks) >= 2:
            weaknesses.append(f"{len(low_vbd_picks)} picks with negative VBD")

        return weaknesses[:5]  # Top 5 weaknesses

    def generate_team_insights(self, user_team: List[dict]) -> List[str]:
        """Generate key insights about the team."""
        insights = []

        if not user_team:
            return ["No players drafted"]

        # Highest VBD pick
        best_pick = max(user_team, key=lambda p: p.get('VBD_Value', 0))
        insights.append(f"Best pick: {best_pick['Player_Name']} ({best_pick.get('VBD_Value', 0):.1f} VBD)")

        # Position dominance
        position_vbd = {}
        position_counts = {}
        for player in user_team:
            pos = player.get('Position', 'UNKNOWN')
            position_vbd[pos] = position_vbd.get(pos, 0) + player.get('VBD_Value', 0)
            position_counts[pos] = position_counts.get(pos, 0) + 1

        if position_vbd:
            strongest_pos = max(position_vbd.items(), key=lambda x: x[1])
            insights.append(f"Strongest position: {strongest_pos[0]} ({strongest_pos[1]:.1f} total VBD)")

        # Draft efficiency
        total_vbd = sum(player.get('VBD_Value', 0) for player in user_team)
        picks_made = len(user_team)
        if picks_made > 0:
            efficiency = total_vbd / picks_made
            insights.append(f"Draft efficiency: {efficiency:.1f} VBD per pick")

        return insights

    def display_future_suggestions(self, user_team: List[dict], draft_grade: dict):
        """Display AI-powered future suggestions for 12-player roster."""
        st.markdown("### 🔮 Advanced AI Future Strategy")

        # Analyze roster construction
        position_counts = {}
        position_vbd = {}
        for player in user_team:
            pos = player.get('Position', 'UNKNOWN')
            position_counts[pos] = position_counts.get(pos, 0) + 1
            position_vbd[pos] = position_vbd.get(pos, 0) + player.get('VBD_Value', 0)

        # Advanced roster analysis
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🎯 Waiver Wire Priority Targets")

            # Find undrafted high-value players by position need
            drafted_names = [p['Player_Name'] for p in user_team]
            undrafted = st.session_state.available_players[
                ~st.session_state.available_players['Player_Name'].isin(drafted_names)
            ]

            # Priority based on roster weaknesses
            weak_positions = []

            # Check starting lineup strength
            qb_vbd = position_vbd.get('QB', 0)
            rb_vbd = position_vbd.get('RB', 0) / max(position_counts.get('RB', 1), 2)  # Average RB value
            wr_vbd = position_vbd.get('WR', 0) / max(position_counts.get('WR', 1), 2)  # Average WR value
            te_vbd = position_vbd.get('TE', 0)

            if qb_vbd < 10:
                weak_positions.append(('QB', 'Upgrade starting QB - low VBD score'))
            if rb_vbd < 8:
                weak_positions.append(('RB', 'RB corps needs strengthening'))
            if wr_vbd < 8:
                weak_positions.append(('WR', 'WR depth insufficient'))
            if te_vbd < 6:
                weak_positions.append(('TE', 'TE position needs upgrade'))

            # Show priority waiver targets
            for pos, reason in weak_positions[:3]:
                pos_targets = undrafted[undrafted['Position'] == pos].head(3)
                if not pos_targets.empty:
                    st.markdown(f"**🔥 {pos} Priority:** {reason}")
                    for _, player in pos_targets.iterrows():
                        st.markdown(f"""
                        <div style="padding: 0.6rem; margin: 0.3rem 0; background: rgba(255,68,68,0.1); border-left: 3px solid #ff4444; border-radius: 6px;">
                            <div style="font-weight: 600; font-size: 0.9rem;">{player['Player_Name']} ({player.get('Team', 'UNK')})</div>
                            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.8);">
                                VBD: {player['VBD_Value']:.1f} | Rank: #{player['Overall_Rank']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown("")

        with col2:
            st.markdown("#### 🔄 Advanced Roster Management")

            # Lineup optimization suggestions
            st.markdown("**🎯 Weekly Lineup Strategy:**")

            # Analyze FLEX position
            flex_player = user_team[6] if len(user_team) > 6 else None
            if flex_player:
                flex_pos = flex_player.get('Position', 'UNKNOWN')
                flex_vbd = flex_player.get('VBD_Value', 0)

                if flex_vbd < 8:
                    st.markdown("⚠️ FLEX position weak - consider weekly waiver streaming")
                else:
                    st.markdown(f"✅ Strong FLEX with {flex_player['Player_Name']} ({flex_vbd:.1f} VBD)")

            # Bench utilization
            bench_players = user_team[9:] if len(user_team) > 9 else []
            if bench_players:
                bench_total_vbd = sum(p.get('VBD_Value', 0) for p in bench_players)
                st.markdown(f"🪑 Bench VBD: {bench_total_vbd:.1f}")

                # Best bench player for potential starter
                best_bench = max(bench_players, key=lambda p: p.get('VBD_Value', 0))
                st.markdown(f"💎 Best Bench Asset: {best_bench['Player_Name']} ({best_bench.get('VBD_Value', 0):.1f} VBD)")

            # Bye week analysis
            st.markdown("**📅 Bye Week Management:**")
            bye_weeks = {}
            for player in user_team[:9]:  # Only starters matter for bye weeks
                bye = player.get('Bye_Week', 0)
                if bye > 0:
                    if bye not in bye_weeks:
                        bye_weeks[bye] = []
                    bye_weeks[bye].append(f"{player['Player_Name']} ({player['Position']})")

            # Identify problematic bye weeks
            for week, players in bye_weeks.items():
                if len(players) >= 3:
                    st.markdown(f"🚨 Week {week}: {len(players)} starters on bye")
                elif len(players) == 2:
                    st.markdown(f"⚠️ Week {week}: {len(players)} starters on bye")

        # Advanced trade analysis
        st.markdown("#### 💱 Advanced Trade Opportunities")

        trade_col1, trade_col2 = st.columns(2)

        with trade_col1:
            st.markdown("**📈 Roster Strengths to Trade From:**")

            # Identify position strengths (above average VBD)
            avg_vbd_by_pos = {
                'QB': 12, 'RB': 9, 'WR': 8, 'TE': 7, 'K': 3, 'DEF': 4  # Rough benchmarks
            }

            trade_assets = []
            for pos, threshold in avg_vbd_by_pos.items():
                pos_vbd = position_vbd.get(pos, 0)
                pos_count = position_counts.get(pos, 0)
                if pos_count > 0:
                    avg_pos_vbd = pos_vbd / pos_count
                    if avg_pos_vbd > threshold and pos_count > 1:
                        surplus = pos_count - self.roster_requirements.get(pos, 1)
                        if surplus > 0:
                            trade_assets.append(f"Strong {pos} depth - consider trading for upgrades")

            for asset in trade_assets:
                st.markdown(f"• {asset}")

            if not trade_assets:
                st.markdown("• No obvious trade assets - hold current roster")

        with trade_col2:
            st.markdown("📉 **Areas to Target in Trades:**")

            # Identify weak positions
            upgrade_targets = []

            for pos, threshold in avg_vbd_by_pos.items():
                pos_vbd = position_vbd.get(pos, 0)
                pos_count = position_counts.get(pos, 0)
                if pos_count > 0:
                    avg_pos_vbd = pos_vbd / pos_count
                    if avg_pos_vbd < threshold * 0.8:  # Below 80% of benchmark
                        upgrade_targets.append(f"Upgrade {pos} - current VBD below optimal")

            for target in upgrade_targets:
                st.markdown(f"• {target}")

            if not upgrade_targets:
                st.markdown("• Roster well-balanced - focus on depth")

        # Season-long strategy based on roster construction
        st.markdown("#### 📊 Season-Long Strategy Recommendations")

        strategy_recommendations = []

        # Analyze starting lineup strength
        starter_strength = sum(p.get('VBD_Value', 0) for p in user_team[:9])
        if starter_strength >= 80:
            strategy_recommendations.append("🏆 **Championship Contender**: Strong starting lineup - focus on playoff schedule")
        elif starter_strength >= 60:
            strategy_recommendations.append("📈 **Competitive Team**: Solid foundation - target 1-2 key upgrades")
        else:
            strategy_recommendations.append("🔧 **Rebuilding Mode**: Focus on waiver wire gems and high-upside trades")

        # Position-specific strategies
        if position_counts.get('RB', 0) < 3:
            strategy_recommendations.append("🏃 **RB Strategy**: Prioritize RB handcuffs and waiver wire adds")

        if position_counts.get('WR', 0) >= 4:
            strategy_recommendations.append("📡 **WR Strategy**: Deep WR corps - use for trade leverage")

        if position_counts.get('QB', 0) == 1:
            strategy_recommendations.append("🎯 **QB Strategy**: Monitor QB2 options for bye week/injury insurance")

        # Display recommendations
        for rec in strategy_recommendations:
            st.markdown(rec)

        # Future draft advice
        st.markdown("#### 🎓 Future Draft Improvement Tips")

        draft_advice = []
        breakdown = draft_grade['breakdown']

        if breakdown['execution_score'] < 15:
            draft_advice.append("📋 **Position Order**: Follow QB→WR→WR→RB→RB→TE→FLEX→K→DEF for optimal roster construction")

        if breakdown['strategy_score'] < 20:
            draft_advice.append("💎 **Value Identification**: Focus more on VBD scores rather than name recognition")

        if breakdown['construction_score'] < 20:
            draft_advice.append("🏗️ **Roster Building**: Ensure all required positions filled before drafting bench depth")

        if breakdown['vbd_score'] < 25:
            draft_advice.append("📊 **VBD Focus**: Target higher VBD players, especially in early rounds")

        # General improvement tips
        draft_advice.extend([
            "⏰ **Draft Timing**: Don't reach for positions too early (K/DEF rounds 8-9 only)",
            "🔄 **FLEX Strategy**: Use FLEX for best remaining WR/RB/TE, not positional need",
            "🪑 **Bench Value**: Draft bench players with upside, not just safe floor players"
        ])

        for advice in draft_advice[:6]:
            st.markdown(advice)

    def display_full_draft_board(self):
        """Display the complete draft board."""
        st.markdown("### 📋 Complete Draft Board")

        if st.session_state.draft_results:
            draft_df = pd.DataFrame(st.session_state.draft_results)

            # Group by rounds for better display
            for round_num in range(1, st.session_state.draft_rounds + 1):
                round_picks = draft_df[draft_df['round'] == round_num]

                if not round_picks.empty:
                    with st.expander(f"Round {round_num} ({len(round_picks)} picks)", expanded=(round_num <= 3)):
                        for _, pick in round_picks.iterrows():
                            is_user_pick = "Your Team" in pick['team']
                            team_color = "#667eea" if is_user_pick else "#666"

                            st.markdown(f"""
                            <div class="draft-pick" style="border-left: 4px solid {team_color};">
                                <div class="pick-number">#{pick['pick']}</div>
                                <div style="flex-grow: 1;">
                                    <div style="font-weight: 600; font-size: 1.1rem;">{pick['player']}</div>
                                    <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
                                        <span class="position-badge pos-{pick['position'].lower()}">{pick['position']}</span>
                                        <span class="team-badge">{pick['team_name']}</span>
                                        <span style="margin-left: 0.5rem;">VBD: {pick['vbd']:.1f}</span>
                                        <span style="margin-left: 0.5rem;">Rank: #{pick['overall_rank']}</span>
                                    </div>
                                </div>
                                <div style="text-align: right; color: rgba(255,255,255,0.7);">
                                    {pick['team']}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'players_data' not in st.session_state:
    st.session_state.players_data = pd.DataFrame()
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Rankings'

# Navigation Bar
st.markdown("""
<div class="navbar">
    <h2 style="margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">T3's AI Powered Fantasy Football 2025</h2>
</div>
""", unsafe_allow_html=True)

# Navigation buttons
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    nav_col1, nav_col2 = st.columns(2)
    with nav_col1:
        if st.button("🏆 Player Rankings", use_container_width=True, type="primary" if st.session_state.current_page == 'Rankings' else "secondary"):
            st.session_state.current_page = 'Rankings'
            st.rerun()
    with nav_col2:
        if st.button("🎯 Draft Simulator", use_container_width=True, type="primary" if st.session_state.current_page == 'Draft' else "secondary"):
            st.session_state.current_page = 'Draft'
            st.rerun()

# Initialize analyzer
analyzer = AdvancedFantasyAnalyzer()

# Page routing
if st.session_state.current_page == 'Rankings':
    # RANKINGS PAGE
    st.markdown("## 🏆 Player Rankings")

    # Enhanced file upload section
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "📊 Upload Fantasy Football Excel File",
        type=['xlsx', 'xls'],
        help="Upload your Excel file with VBD Custom columns for advanced fantasy analysis"
    )

    if uploaded_file is not None:
        if st.button("🚀 Calculate Advanced VBD Rankings", type="primary"):
            with st.spinner("🔄 Processing VBD data and training AI models..."):
                try:
                    players_data = analyzer.process_excel_file(uploaded_file)

                    if not players_data.empty:
                        st.session_state.players_data = players_data
                        st.session_state.data_loaded = True
                        st.balloons()
                        st.success(f"✅ Successfully processed {len(players_data)} players with VBD rankings!")

                        # Show AI insights summary
                        with st.expander("🤖 AI Processing Summary"):
                            value_picks = len(players_data[players_data.get('Value_Pick', False) == True])
                            avg_vbd = players_data['VBD_Value'].mean()
                            top_vbd = players_data['VBD_Value'].max()

                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Value Picks Identified", value_picks)
                            with col2:
                                st.metric("Average VBD Score", f"{avg_vbd:.1f}")
                            with col3:
                                st.metric("Highest VBD Score", f"{top_vbd:.1f}")
                    else:
                        st.error("❌ No player data found with VBD values.")

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
            min_vbd = st.slider("📊 Minimum VBD Score", -20.0, 100.0, -20.0, 5.0)

        with col3:
            top_n = st.selectbox("📈 Display Count", [25, 50, 100, 200, "All"])

        with col4:
            search_term = st.text_input("🔍 Search Player", placeholder="Enter player name...")

        st.markdown('</div>', unsafe_allow_html=True)

        # Apply filters
        filtered_data = data.copy()

        if selected_position != 'All Positions':
            filtered_data = filtered_data[filtered_data['Position'] == selected_position]

        filtered_data = filtered_data[filtered_data['VBD_Value'] >= min_vbd]

        if search_term:
            filtered_data = filtered_data[
                filtered_data['Player_Name'].str.contains(search_term, case=False, na=False)
            ]

        # Sort by overall rank (VBD-based)
        filtered_data = filtered_data.sort_values('Overall_Rank', ascending=True)

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
                avg_vbd = filtered_data['VBD_Value'].mean()
                st.metric("Avg VBD Score", f"{avg_vbd:.1f}")
            with col3:
                top_vbd = filtered_data['VBD_Value'].max()
                st.metric("Highest VBD", f"{top_vbd:.1f}")
            with col4:
                positions_count = filtered_data['Position'].nunique()
                st.metric("Positions", positions_count)
            with col5:
                value_picks = len(filtered_data[filtered_data.get('Value_Pick', False) == True])
                st.metric("AI Value Picks", value_picks)

            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("---")

            # Enhanced player display with VBD rankings
            st.markdown("### 🏆 Advanced VBD Rankings")
            st.markdown("*Based on Value Based Drafting with AI-enhanced insights - Click any player for detailed analysis*")

            # Display top 25 players first
            top_25_players = filtered_data.head(25)
            remaining_players = filtered_data.iloc[25:] if len(filtered_data) > 25 else pd.DataFrame()

            # Top 25 players (displayed normally)
            if not top_25_players.empty:
                st.markdown("#### 🥇 Top 25 Players")
                for idx, (_, player) in enumerate(top_25_players.iterrows()):
                    overall_rank = player['Overall_Rank']
                    rank_class = analyzer.get_rank_badge_class(overall_rank)

                    # Enhanced player row
                    player_container = st.container()
                    with player_container:
                        col_rank, col_player, col_team, col_pos, col_vbd, col_round, col_ai, col_news = st.columns([1, 2, 1, 1, 1, 1, 1, 3])

                        with col_rank:
                            st.markdown(f'<div class="rank-badge {rank_class}">#{overall_rank}</div>', 
                                       unsafe_allow_html=True)
                            st.markdown(f"<small>Overall</small>", unsafe_allow_html=True)

                        with col_player:
                            first_name = player.get('First_Name', '').strip()
                            last_name = player.get('Last_Name', '').strip()
                            display_name = f"{first_name} {last_name}".strip() or player.get('Player_Name', 'Unknown')

                            if st.button(f"🏈 {display_name}", key=f"top_player_{idx}", use_container_width=True):
                                st.session_state.selected_player = player

                        with col_team:
                            team = player.get('Team', 'UNK')
                            bye_week = player.get('Bye_Week', 0)
                            st.markdown(f'<div class="team-badge">{team}</div>', unsafe_allow_html=True)
                            if bye_week > 0:
                                st.markdown(f'<div class="bye-week">Bye: {bye_week}</div>', unsafe_allow_html=True)

                        with col_pos:
                            position = player.get('Position', 'UNKNOWN')
                            st.markdown(f'<span class="position-badge pos-{position.lower()}">{position}</span>', 
                                       unsafe_allow_html=True)
                            pos_rank = player.get('Position_Rank', 'N/A')
                            st.markdown(f"<small>#{pos_rank}</small>", unsafe_allow_html=True)

                        with col_vbd:
                            vbd = player.get('VBD_Value', 0)
                            vbd_class = analyzer.get_vbd_class(vbd)
                            st.markdown(f'<div class="vbd-badge {vbd_class}">{vbd:.1f}</div>', 
                                       unsafe_allow_html=True)
                            st.markdown(f"<small>VBD</small>", unsafe_allow_html=True)

                        with col_round:
                            draft_round = player.get('Draft_Round', 'TBD')
                            if 'Round 1' in draft_round or 'Round 2' in draft_round:
                                round_class = 'round-1-2'
                            elif 'Round 3' in draft_round or 'Round 4' in draft_round or 'Round 5' in draft_round:
                                round_class = 'round-3-5'
                            elif 'Rounds 6' in draft_round or 'Round 8' in draft_round or 'Round 9' in draft_round or 'Round 10' in draft_round:
                                round_class = 'round-6-10'
                            elif 'Round 11' in draft_round or 'Round 12' in draft_round or 'Round 13' in draft_round or 'Round 14' in draft_round or 'Round 15' in draft_round:
                                round_class = 'round-11-15'
                            else:
                                round_class = 'round-waiver'

                            st.markdown(f'<div class="draft-round-badge {round_class}">{draft_round}</div>', 
                                       unsafe_allow_html=True)

                        with col_ai:
                            value_pick = player.get('Value_Pick', False)
                            if value_pick:
                                st.markdown('💎 <span style="color: #00ff87; font-weight: bold;">VALUE</span>', unsafe_allow_html=True)
                            else:
                                st.markdown('<span style="color: #666;">---</span>', unsafe_allow_html=True)

                        with col_news:
                            news = str(player.get('News', 'No recent news'))
                            if len(news) > 100:
                                news = news[:100] + "..."
                            st.markdown(f"<div style='font-size: 0.85rem; color: rgba(255,255,255,0.8);'>{news}</div>", unsafe_allow_html=True)

            # Remaining players in scrollable container
            if not remaining_players.empty:
                st.markdown("---")
                st.markdown(f"#### 📋 Remaining Players (Ranks 26-{len(filtered_data)})")

                # Scrollable container for remaining players
                st.markdown("""
                <div style="
                    background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
                    backdrop-filter: blur(15px);
                    border-radius: 16px;
                    padding: 1.5rem;
                    margin: 1rem 0;
                    border: 2px solid rgba(255,255,255,0.2);
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                    max-height: 600px;
                    overflow-y: auto;
                    overflow-x: hidden;
                ">
                """, unsafe_allow_html=True)

                for idx, (_, player) in enumerate(remaining_players.iterrows()):
                    overall_rank = player['Overall_Rank']
                    rank_class = analyzer.get_rank_badge_class(overall_rank)

                    # Enhanced player row
                    player_container = st.container()
                    with player_container:
                        col_rank, col_player, col_team, col_pos, col_vbd, col_round, col_ai, col_news = st.columns([1, 2, 1, 1, 1, 1, 1, 3])

                        with col_rank:
                            st.markdown(f'<div class="rank-badge {rank_class}">#{overall_rank}</div>', 
                                       unsafe_allow_html=True)
                            st.markdown(f"<small>Overall</small>", unsafe_allow_html=True)

                        with col_player:
                            first_name = player.get('First_Name', '').strip()
                            last_name = player.get('Last_Name', '').strip()
                            display_name = f"{first_name} {last_name}".strip() or player.get('Player_Name', 'Unknown')

                            if st.button(f"🏈 {display_name}", key=f"scroll_player_{idx + 25}", use_container_width=True):
                                st.session_state.selected_player = player

                        with col_team:
                            team = player.get('Team', 'UNK')
                            bye_week = player.get('Bye_Week', 0)
                            st.markdown(f'<div class="team-badge">{team}</div>', unsafe_allow_html=True)
                            if bye_week > 0:
                                st.markdown(f'<div class="bye-week">Bye: {bye_week}</div>', unsafe_allow_html=True)

                        with col_pos:
                            position = player.get('Position', 'UNKNOWN')
                            st.markdown(f'<span class="position-badge pos-{position.lower()}">{position}</span>', 
                                       unsafe_allow_html=True)
                            pos_rank = player.get('Position_Rank', 'N/A')
                            st.markdown(f"<small>#{pos_rank}</small>", unsafe_allow_html=True)

                        with col_vbd:
                            vbd = player.get('VBD_Value', 0)
                            vbd_class = analyzer.get_vbd_class(vbd)
                            st.markdown(f'<div class="vbd-badge {vbd_class}">{vbd:.1f}</div>', 
                                       unsafe_allow_html=True)
                            st.markdown(f"<small>VBD</small>", unsafe_allow_html=True)

                        with col_round:
                            draft_round = player.get('Draft_Round', 'TBD')
                            if 'Round 1' in draft_round or 'Round 2' in draft_round:
                                round_class = 'round-1-2'
                            elif 'Round 3' in draft_round or 'Round 4' in draft_round or 'Round 5' in draft_round:
                                round_class = 'round-3-5'
                            elif 'Rounds 6' in draft_round or 'Round 8' in draft_round or 'Round 9' in draft_round or 'Round 10' in draft_round:
                                round_class = 'round-6-10'
                            elif 'Round 11' in draft_round or 'Round 12' in draft_round or 'Round 13' in draft_round or 'Round 14' in draft_round or 'Round 15' in draft_round:
                                round_class = 'round-11-15'
                            else:
                                round_class = 'round-waiver'

                            st.markdown(f'<div class="draft-round-badge {round_class}">{draft_round}</div>', 
                                       unsafe_allow_html=True)

                        with col_ai:
                            value_pick = player.get('Value_Pick', False)
                            if value_pick:
                                st.markdown('💎 <span style="color: #00ff87; font-weight: bold;">VALUE</span>', unsafe_allow_html=True)
                            else:
                                st.markdown('<span style="color: #666;">---</span>', unsafe_allow_html=True)

                        with col_news:
                            news = str(player.get('News', 'No recent news'))
                            if len(news) > 100:
                                news = news[:100] + "..."
                            st.markdown(f"<div style='font-size: 0.85rem; color: rgba(255,255,255,0.8);'>{news}</div>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

            # Display selected player details
            if 'selected_player' in st.session_state:
                st.markdown("---")
                analyzer.render_player_modal(st.session_state.selected_player, data)

    else:
        # Enhanced welcome section
        st.markdown("""
        <div class="advanced-card" style="text-align: center; padding: 3rem;">
            <h3 style="color: #667eea;">🚀 Advanced VBD Fantasy Rankings</h3>
            <p style="font-size: 1.1rem; margin: 1.5rem 0;">Upload your Excel file with VBD Custom columns for AI-powered analysis!</p>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin: 2rem 0;">
                <div class="metric-card">
                    <h4>📊 VBD Analysis</h4>
                    <p>Uses Value Based Drafting scores from your Excel sheets</p>
                </div>
                <div class="metric-card">
                    <h4>🤖 AI Insights</h4>
                    <p>Machine learning identifies value picks and draft strategies</p>
                </div>
                <div class="metric-card">
                    <h4>🎯 Smart Rankings</h4>
                    <p>Position scarcity and draft round logic optimize rankings</p>
                </div>
            </div>

            <div style="text-align: left; max-width: 600px; margin: 2rem auto;">
                <h4>📋 Required VBD Columns:</h4>
                <ul style="font-size: 0.9rem;">
                    <li><strong>QB, RB, WR:</strong> Column X (VBD Custom)</li>
                    <li><strong>TE:</strong> Column S (VBD Custom)</li>
                    <li><strong>K, DEF:</strong> Column L (0 = best, higher = worse)</li>
                    <li><strong>Names:</strong> Column A (First), Column B (Last)</li>
                    <li><strong>Team:</strong> Column C</li>
                    <li><strong>News:</strong> Column Y (automatic detection)</li>
                </ul>
            </div>

            <p><strong>Features:</strong> Advanced AI rankings, value pick identification, draft round optimization</p>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.current_page == 'Draft':
    # REAL-TIME DRAFT SIMULATOR PAGE
    st.markdown("## 🎯 Real-Time Fantasy Draft Simulator")

    if not st.session_state.data_loaded or st.session_state.players_data.empty:
        st.warning("⚠️ Please upload and process player data on the Rankings page first.")
        st.markdown("""
        <div class="advanced-card" style="text-align: center; padding: 2rem;">
            <h3>🎯 AI-Powered Real-Time Draft</h3>
            <p>Experience realistic fantasy football drafts with 9 AI opponents and live timer!</p>
            <p><strong>To get started:</strong> Upload your Excel file on the Rankings page first.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        data = st.session_state.players_data

        # Initialize draft state
        if 'draft_simulator' not in st.session_state:
            st.session_state.draft_simulator = None
        if 'draft_in_progress' not in st.session_state:
            st.session_state.draft_in_progress = False
        if 'draft_results' not in st.session_state:
            st.session_state.draft_results = []
        if 'current_pick_number' not in st.session_state:
            st.session_state.current_pick_number = 1
        if 'available_players' not in st.session_state:
            st.session_state.available_players = pd.DataFrame()
        if 'user_draft_position' not in st.session_state:
            st.session_state.user_draft_position = 5
        if 'draft_rounds' not in st.session_state:
            st.session_state.draft_rounds = 12
        if 'pick_timer_start' not in st.session_state:
            st.session_state.pick_timer_start = None
        if 'waiting_for_user_pick' not in st.session_state:
            st.session_state.waiting_for_user_pick = False
        if 'draft_completed' not in st.session_state:
            st.session_state.draft_completed = False

        if not st.session_state.draft_in_progress:
            # Draft setup phase
            st.markdown('<div class="draft-container">', unsafe_allow_html=True)

            # Draft settings
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown("### 🎮 12-Player Fantasy Draft Configuration")

                draft_col1, draft_col2, draft_col3 = st.columns(3)

                with draft_col1:
                    # Fixed to 12 rounds for the specific roster format
                    st.session_state.draft_rounds = 12
                    st.markdown("**Draft Rounds:** 12 (Fixed)")
                    st.markdown("**Roster Format:** QB, 2WR, 2RB, TE, FLEX, K, DEF, 3 Bench")

                with draft_col2:
                    draft_position = st.selectbox("Your Draft Position", list(range(1, 11)), index=4)
                    st.session_state.user_draft_position = draft_position

                with draft_col3:
                    league_type = st.selectbox("League Type", ["Standard", "PPR", "Half-PPR"], index=1)

            with col2:
                st.markdown("### ⏱️ 12-Player Draft Features")
                st.markdown("""
                **🏈 Roster Format:**
                - 1 QB, 2 WR, 2 RB, 1 TE
                - 1 FLEX (WR/RB/TE), 1 K, 1 DEF
                - 3 Bench players

                **🎮 Live Features:**
                - ⏱️ 60-second pick timer
                - 🤖 Smart AI opponents
                - 📊 Real-time analytics
                - 🏆 Advanced post-draft grading
                """)

            if st.button("🚀 Start Real-Time Draft", type="primary", use_container_width=True):
                # Initialize draft
                st.session_state.draft_simulator = DraftSimulator(data)
                st.session_state.draft_in_progress = True
                st.session_state.draft_results = []
                st.session_state.current_pick_number = 1
                st.session_state.available_players = data.copy().sort_values('Overall_Rank')
                st.session_state.pick_timer_start = datetime.now()
                st.session_state.waiting_for_user_pick = False
                st.session_state.draft_completed = False
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

        elif st.session_state.draft_completed:
            # Draft completed - show results and AI grading
            st.session_state.draft_simulator.display_draft_results_and_grading()

        else:
            # Active draft phase
            st.session_state.draft_simulator.run_real_time_draft()

# Auto-refresh for real-time draft
if st.session_state.get('draft_in_progress', False) and not st.session_state.get('draft_completed', False):
    if not st.session_state.get('waiting_for_user_pick', False):
        # Auto-refresh every 1 second during AI turns
        st.rerun()

# Enhanced footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: rgba(255,255,255,0.6); padding: 2rem;'>
    <p style="font-size: 1.1rem; font-weight: 600;">T3's AI Powered Fantasy Football 2025 | Advanced VBD Analytics</p>
    <p>Value Based Drafting • Machine Learning Insights • Real-Time Draft Simulation</p>
</div>
""", unsafe_allow_html=True)