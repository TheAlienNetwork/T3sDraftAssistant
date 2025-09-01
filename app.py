
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

            # Comparison metrics
            col1, col2, col3 = st.columns(3)

            with col1:
                higher_ranked = len(position_data[position_data['Position_Rank'] < player_rank])
                st.metric("Players Ranked Higher", higher_ranked)

            with col2:
                lower_ranked = len(position_data[position_data['Position_Rank'] > player_rank])
                st.metric("Players Ranked Lower", lower_ranked)

            with col3:
                percentile = ((len(position_data) - player_rank + 1) / len(position_data)) * 100
                st.metric("Percentile Rank", f"{percentile:.0f}%")

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

    def get_pick_order(self, pick_number: int) -> int:
        """Get the team index for snake draft."""
        round_num = ((pick_number - 1) // 10) + 1
        pick_in_round = ((pick_number - 1) % 10) + 1

        if round_num % 2 == 1:  # Odd rounds go 1-10
            return pick_in_round - 1
        else:  # Even rounds go 10-1
            return 9 - (pick_in_round - 1)

    def ai_draft_pick(self, team_index: int, available_players: pd.DataFrame) -> dict:
        """AI logic for drafting players."""
        # Ensure team_index is within valid range for AI teams (0-8)
        if team_index < 0 or team_index >= 9:
            team_index = 0
        
        team_roster = self.ai_teams[team_index]
        
        # Count positions on roster
        position_counts = {}
        for player in team_roster:
            pos = player.get('Position', 'UNKNOWN')
            position_counts[pos] = position_counts.get(pos, 0) + 1

        # AI draft strategy based on round and team needs
        round_num = ((self.current_pick - 1) // 10) + 1

        # Early rounds (1-3): Best available with slight position preference
        if round_num <= 3:
            # Prefer RB/WR in early rounds, avoid K/DEF
            exclude_positions = ['K', 'DEF']
            if round_num >= 3 and position_counts.get('QB', 0) == 0:
                # Might grab QB in round 3
                pass
            
            candidates = available_players[~available_players['Position'].isin(exclude_positions)]
            if len(candidates) == 0:
                candidates = available_players

        # Mid rounds (4-10): Fill needs
        elif round_num <= 10:
            needed_positions = []
            
            if position_counts.get('QB', 0) == 0 and round_num >= 6:
                needed_positions.append('QB')
            if position_counts.get('TE', 0) == 0 and round_num >= 7:
                needed_positions.append('TE')
            
            # Avoid K/DEF until very late
            exclude_positions = ['K', 'DEF'] if round_num < 9 else []
            
            if needed_positions:
                candidates = available_players[
                    (available_players['Position'].isin(needed_positions)) &
                    (~available_players['Position'].isin(exclude_positions))
                ]
                if len(candidates) == 0:
                    candidates = available_players[~available_players['Position'].isin(exclude_positions)]
            else:
                candidates = available_players[~available_players['Position'].isin(exclude_positions)]

        # Late rounds (11+): Fill remaining needs, K/DEF
        else:
            needed_positions = []
            
            if position_counts.get('K', 0) == 0:
                needed_positions.append('K')
            if position_counts.get('DEF', 0) == 0:
                needed_positions.append('DEF')
            if position_counts.get('QB', 0) == 0:
                needed_positions.append('QB')
            if position_counts.get('TE', 0) == 0:
                needed_positions.append('TE')

            if needed_positions:
                candidates = available_players[available_players['Position'].isin(needed_positions)]
                if len(candidates) == 0:
                    candidates = available_players
            else:
                candidates = available_players

        # Add some randomness to make it realistic (top 3-5 players in filtered list)
        top_candidates = candidates.head(min(5, len(candidates)))
        if len(top_candidates) == 0:
            return None

        # Weight selection towards higher ranked players
        weights = [1.0 / (i + 1) for i in range(len(top_candidates))]
        weights = [w / sum(weights) for w in weights]

        selected_idx = np.random.choice(len(top_candidates), p=weights)
        return top_candidates.iloc[selected_idx].to_dict()

    def simulate_draft(self, user_picks: List[int]) -> List[dict]:
        """Simulate a full draft."""
        draft_results = []
        available_players = self.players_data.copy().sort_values('Overall_Rank')

        for pick_num in range(1, 161):  # 16 rounds, 10 teams
            team_index = self.get_pick_order(pick_num)
            
            if team_index == 0 and pick_num in user_picks:
                # User's turn - they'll select manually
                continue
            else:
                # AI pick
                if len(available_players) > 0:
                    # Correctly map team_index to AI teams (team 0 is user, teams 1-9 map to ai_teams 0-8)
                    ai_team_index = team_index - 1 if team_index > 0 else 8
                    ai_pick = self.ai_draft_pick(ai_team_index, available_players)
                    if ai_pick:
                        draft_results.append({
                            'pick': pick_num,
                            'round': ((pick_num - 1) // 10) + 1,
                            'team': f"Team {team_index + 1}" if team_index < 9 else "Your Team",
                            'player': ai_pick['Player_Name'],
                            'position': ai_pick['Position'],
                            'team_name': ai_pick.get('Team', 'Unknown'),
                            'vbd': ai_pick.get('VBD_Value', 0),
                            'overall_rank': ai_pick.get('Overall_Rank', 999)
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
        
        # Enhanced Draft Header
        st.markdown(f"""
        <div class="draft-container" style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); text-align: center; padding: 2rem; margin-bottom: 1rem; border-radius: 20px; box-shadow: 0 15px 35px rgba(30,60,114,0.3);">
            <h1 style="margin: 0; font-size: 2.5rem; background: linear-gradient(135deg, #00ff87 0%, #60efff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🏈 LIVE FANTASY DRAFT</h1>
            <h2 style="margin: 0.5rem 0; color: #ffffff;">Round {round_num} | Pick {pick_in_round} | Overall #{current_pick}</h2>
            <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem;">
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

    def get_remaining_time(self):
        """Get remaining time for current pick."""
        if st.session_state.pick_timer_start:
            elapsed = (datetime.now() - st.session_state.pick_timer_start).total_seconds()
            return max(0, 60 - elapsed)
        return 60

    def render_user_draft_interface(self, current_pick, remaining_time):
        """Render enhanced user draft interface with AI suggestions and full player board."""
        # Timer and urgency indicator
        timer_color = "#ff4444" if remaining_time < 10 else "#ffaa00" if remaining_time < 30 else "#44ff44"
        urgency_class = "timer-urgent" if remaining_time < 10 else ""
        
        st.markdown(f"""
        <div class="user-turn-banner {urgency_class}" style="text-align: center; padding: 2rem; margin: 1rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px;">
            <h1 style="margin: 0; font-size: 2.5rem;">🎯 YOUR TURN TO PICK!</h1>
            <div style="display: flex; justify-content: center; align-items: center; gap: 2rem; margin-top: 1rem;">
                <div style="font-size: 2rem; color: {timer_color};">⏱️ {remaining_time:.0f}s</div>
                <div>Pick #{current_pick} | Make your selection below</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Three-column layout: AI Suggestions | Player Board | Team Rosters
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            self.render_ai_suggestions()
            self.render_my_team()
            
        with col2:
            self.render_draft_board(is_user_turn=True)
            
        with col3:
            self.render_draft_progress()
            self.render_recent_picks()
    
    def render_ai_draft_interface(self, team_index, current_pick):
        """Render interface during AI turns."""
        team_name = f"AI Team {team_index + 1}"
        
        st.markdown(f"""
        <div class="ai-turn-banner" style="text-align: center; padding: 1.5rem; margin: 1rem 0; background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%); border-radius: 15px;">
            <h2 style="margin: 0;">🤖 {team_name} is selecting...</h2>
            <div style="margin-top: 1rem;">
                <div class="thinking-dots">Analyzing available players</div>
                <div style="margin-top: 0.5rem; font-size: 0.9rem; color: rgba(255,255,255,0.7);">Pick #{current_pick} | AI making strategic choice</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Two-column layout during AI turns
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self.render_draft_board(is_user_turn=False)
            
        with col2:
            self.render_draft_progress()
            self.render_recent_picks()
            self.render_my_team()

    def render_ai_suggestions(self):
        """Render AI-suggested players for the user in a clean format."""
        with st.container():
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(102,126,234,0.15) 0%, rgba(118,75,162,0.15) 100%); 
                       border-radius: 12px; padding: 1.5rem; margin: 1rem 0; 
                       border: 2px solid rgba(102,126,234,0.3); box-shadow: 0 8px 25px rgba(102,126,234,0.1);">
                <h3 style="margin-top: 0; color: #667eea; font-size: 1.2rem;">🤖 AI RECOMMENDATIONS</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Get AI suggestions based on user's current team and draft position
            suggestions = self.get_ai_suggestions_for_user()
            
            if suggestions:
                st.markdown("**Top Suggestions for Your Pick:**")
                
                for i, player in enumerate(suggestions[:5]):
                    suggestion_type = player.get('suggestion_type', 'VALUE')
                    reason = player.get('reason', 'Strong pick at this position')
                    
                    # Create suggestion card with Streamlit components
                    sug_cols = st.columns([3, 1])
                    
                    with sug_cols[0]:
                        # Suggestion type indicator
                        type_colors = {
                            'NEED': '🔥',
                            'VALUE': '💎', 
                            'BPA': '⭐'
                        }
                        type_icon = type_colors.get(suggestion_type, '⭐')
                        
                        st.markdown(f"{type_icon} **{player['Player_Name']}** ({player['Position']})")
                        st.markdown(f"<small style='color: rgba(255,255,255,0.8);'>{suggestion_type}: {reason}</small>", unsafe_allow_html=True)
                        st.markdown(f"<small>#{player['Overall_Rank']} Overall | VBD: {player['VBD_Value']:.1f}</small>", unsafe_allow_html=True)
                    
                    with sug_cols[1]:
                        if st.button(f"📝 DRAFT", key=f"ai_suggestion_{i}", type="primary", use_container_width=True):
                            self.make_user_pick(player)
                            st.rerun()
                    
                    if i < len(suggestions) - 1:
                        st.markdown("<hr style='margin: 0.5rem 0; border: 1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='text-align: center; color: rgba(255,255,255,0.5); padding: 1rem;'>Analyzing available players...</div>", unsafe_allow_html=True)

    def render_draft_board(self, is_user_turn=False):
        """Render the complete draft board with all available players in a clean table format."""
        st.markdown("### 📋 DRAFT BOARD")
        
        # Filters in a container
        with st.container():
            filter_col1, filter_col2 = st.columns([1, 1])
            
            with filter_col1:
                positions = ['ALL'] + sorted(st.session_state.available_players['Position'].unique())
                selected_pos = st.selectbox("Position", positions, key="pos_filter")
            
            with filter_col2:
                search_term = st.text_input("🔍 Search Players", placeholder="Player name...", key="board_search")
        
        # Filter players
        filtered_players = st.session_state.available_players.copy()
        if selected_pos != 'ALL':
            filtered_players = filtered_players[filtered_players['Position'] == selected_pos]
        if search_term:
            filtered_players = filtered_players[
                filtered_players['Player_Name'].str.contains(search_term, case=False, na=False)
            ]
        
        # Sort by overall rank and limit results
        filtered_players = filtered_players.sort_values('Overall_Rank').head(30)
        
        # Player table container
        with st.container():
            st.markdown("""<div style="background: rgba(255,255,255,0.05); border-radius: 10px; padding: 1rem; margin: 1rem 0;">""")
            
            # Table header
            header_cols = st.columns([1, 3, 1, 1, 1, 2])
            with header_cols[0]:
                st.markdown("**Rank**")
            with header_cols[1]:
                st.markdown("**Player**")
            with header_cols[2]:
                st.markdown("**Pos**")
            with header_cols[3]:
                st.markdown("**Team**")
            with header_cols[4]:
                st.markdown("**VBD**")
            with header_cols[5]:
                st.markdown("**Action**")
            
            st.markdown("---")
            
            # Player rows
            for idx, (_, player) in enumerate(filtered_players.iterrows()):
                self.render_player_table_row(player, idx, is_user_turn)
            
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
            st.markdown(f"**{player['Player_Name']}**")
            
        with row_cols[2]:
            st.markdown(f"<span style='background: {pos_color}; color: white; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem;'>{player['Position']}</span>", unsafe_allow_html=True)
            
        with row_cols[3]:
            st.markdown(f"{player.get('Team', 'UNK')}")
            
        with row_cols[4]:
            vbd_val = player.get('VBD_Value', 0)
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
                if st.button(f"📝 DRAFT", key=f"draft_player_{idx}", type="primary", use_container_width=True):
                    self.make_user_pick(player)
                    st.rerun()
            else:
                st.markdown("<div style='text-align: center; padding: 0.5rem; background: rgba(255,255,255,0.1); border-radius: 6px; font-size: 0.8rem;'>Available</div>", unsafe_allow_html=True)
        
        # Add subtle divider
        if idx < 29:  # Don't add divider after last row
            st.markdown("<hr style='margin: 0.5rem 0; border: 1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

    def render_my_team(self):
        """Render current user team roster in a clean container."""
        with st.container():
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                       border-radius: 12px; padding: 1.5rem; margin: 1rem 0; 
                       box-shadow: 0 8px 25px rgba(102,126,234,0.3);">
                <h3 style="margin-top: 0; color: white; font-size: 1.2rem;">🎯 MY TEAM</h3>
            </div>
            """, unsafe_allow_html=True)
            
            user_picks = [pick for pick in st.session_state.draft_results if pick['team'] == 'Your Team']
            
            if user_picks:
                # Organize by position
                pos_groups = {}
                for pick in user_picks:
                    pos = pick['position']
                    if pos not in pos_groups:
                        pos_groups[pos] = []
                    pos_groups[pos].append(pick)
                
                # Display by position groups
                for pos in ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']:
                    if pos in pos_groups:
                        pos_colors = {
                            'QB': '#e74c3c', 'RB': '#3498db', 'WR': '#f39c12', 
                            'TE': '#27ae60', 'K': '#9b59b6', 'DEF': '#34495e'
                        }
                        pos_color = pos_colors.get(pos, '#666')
                        
                        st.markdown(f"**{pos}**")
                        for pick in pos_groups[pos]:
                            team_cols = st.columns([2, 1, 1])
                            
                            with team_cols[0]:
                                st.markdown(f"• **{pick['player']}**")
                            
                            with team_cols[1]:
                                st.markdown(f"R{pick['round']}.{pick['pick'] - (pick['round']-1)*10}")
                            
                            with team_cols[2]:
                                st.markdown(f"VBD: {pick['vbd']:.1f}")
                        
                        st.markdown("")
            else:
                st.markdown("<div style='text-align: center; color: rgba(255,255,255,0.5); padding: 2rem;'>No picks yet - your draft picks will appear here</div>", unsafe_allow_html=True)

    def render_recent_picks(self):
        """Render recent draft picks in a clean container."""
        with st.container():
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%); 
                       border-radius: 12px; padding: 1.5rem; margin: 1rem 0; 
                       border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h3 style="margin-top: 0; color: #667eea; font-size: 1.2rem;">📋 RECENT PICKS</h3>
            </div>
            """, unsafe_allow_html=True)
            
            recent_picks = st.session_state.draft_results[-10:] if st.session_state.draft_results else []
            
            if recent_picks:
                # Create a scrollable container for recent picks
                with st.container():
                    for i, pick_info in enumerate(reversed(recent_picks)):
                        team_color = "#667eea" if "Your Team" in pick_info['team'] else "#555"
                        is_user_pick = "Your Team" in pick_info['team']
                        
                        # Position color
                        pos_colors = {
                            'QB': '#e74c3c', 'RB': '#3498db', 'WR': '#f39c12', 
                            'TE': '#27ae60', 'K': '#9b59b6', 'DEF': '#34495e'
                        }
                        pos_color = pos_colors.get(pick_info['position'], '#666')
                        
                        # Pick display with better styling
                        pick_cols = st.columns([1, 3, 1])
                        
                        with pick_cols[0]:
                            st.markdown(f"<div style='text-align: center; font-weight: bold; color: {team_color};'>#{pick_info['pick']}</div>", unsafe_allow_html=True)
                        
                        with pick_cols[1]:
                            user_indicator = "🎯 " if is_user_pick else ""
                            st.markdown(f"**{user_indicator}{pick_info['player']}**")
                            st.markdown(f"<small style='color: rgba(255,255,255,0.7);'>{pick_info['team']}</small>", unsafe_allow_html=True)
                        
                        with pick_cols[2]:
                            st.markdown(f"<span style='background: {pos_color}; color: white; padding: 0.2rem 0.4rem; border-radius: 4px; font-size: 0.7rem;'>{pick_info['position']}</span>", unsafe_allow_html=True)
                        
                        if i < len(recent_picks) - 1:
                            st.markdown("<hr style='margin: 0.3rem 0; border: 1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='text-align: center; color: rgba(255,255,255,0.5); padding: 2rem;'>No picks yet</div>", unsafe_allow_html=True)

    def render_draft_progress(self):
        """Render draft progress and statistics."""
        current_pick = st.session_state.current_pick_number
        max_picks = st.session_state.draft_rounds * 10
        progress = (current_pick - 1) / max_picks
        
        st.markdown("""
        <div class="advanced-card" style="margin-bottom: 1rem;">
            <h3 style="margin-top: 0;">📊 DRAFT PROGRESS</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.progress(progress)
        
        st.markdown(f"""
        <div style="text-align: center; padding: 0.5rem;">
            <div style="font-size: 1.2rem; font-weight: 600;">{current_pick - 1} / {max_picks}</div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">Picks Completed</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Position breakdown
        if st.session_state.draft_results:
            pos_counts = {}
            for pick in st.session_state.draft_results:
                pos = pick['position']
                pos_counts[pos] = pos_counts.get(pos, 0) + 1
            
            st.markdown("**Positions Drafted:**")
            for pos, count in sorted(pos_counts.items()):
                st.markdown(f"• {pos}: {count}")

    def get_ai_suggestions_for_user(self):
        """Generate AI suggestions based on user's team composition and draft strategy."""
        user_picks = [pick for pick in st.session_state.draft_results if pick['team'] == 'Your Team']
        available = st.session_state.available_players.copy()
        
        # Analyze user's current roster
        user_positions = {}
        for pick in user_picks:
            pos = pick['position']
            user_positions[pos] = user_positions.get(pos, 0) + 1
        
        suggestions = []
        current_round = ((st.session_state.current_pick_number - 1) // 10) + 1
        
        # Best Player Available (BPA)
        bpa = available.head(1).iloc[0] if len(available) > 0 else None
        if bpa is not None:
            suggestions.append({
                **bpa.to_dict(),
                'suggestion_type': 'BPA',
                'reason': 'Highest ranked available player'
            })
        
        # Position of Need
        needed_positions = []
        if user_positions.get('QB', 0) == 0 and current_round >= 4:
            needed_positions.append('QB')
        if user_positions.get('RB', 0) < 2 and current_round <= 8:
            needed_positions.append('RB')
        if user_positions.get('WR', 0) < 2 and current_round <= 10:
            needed_positions.append('WR')
        if user_positions.get('TE', 0) == 0 and current_round >= 6:
            needed_positions.append('TE')
        
        for pos in needed_positions[:2]:
            pos_players = available[available['Position'] == pos]
            if len(pos_players) > 0:
                best_pos = pos_players.iloc[0]
                suggestions.append({
                    **best_pos.to_dict(),
                    'suggestion_type': 'NEED',
                    'reason': f'Fill {pos} position need'
                })
        
        # Value Picks (high VBD relative to rank)
        value_threshold = available['VBD_Value'].quantile(0.75) if len(available) > 20 else 0
        value_picks = available[available['VBD_Value'] >= value_threshold].head(3)
        
        for _, player in value_picks.iterrows():
            if len(suggestions) < 5:
                suggestions.append({
                    **player.to_dict(),
                    'suggestion_type': 'VALUE',
                    'reason': 'High value based on VBD analysis'
                })
        
        return suggestions[:5]

    def handle_user_pick(self):
        """Handle when it's the user's turn to pick."""
        # Check if timer expired
        if st.session_state.pick_timer_start:
            elapsed = (datetime.now() - st.session_state.pick_timer_start).total_seconds()
            if elapsed >= 60:
                # Auto-pick best available player
                if len(st.session_state.available_players) > 0:
                    best_player = st.session_state.available_players.iloc[0]
                    st.warning(f"⏰ Time expired! Auto-drafted {best_player['Player_Name']}")
                    self.make_user_pick(best_player)
                    st.rerun()

    def make_user_pick(self, player_row):
        """Process user's player selection."""
        # Add pick to results
        pick_info = {
            'pick': st.session_state.current_pick_number,
            'round': ((st.session_state.current_pick_number - 1) // 10) + 1,
            'team': 'Your Team',
            'player': player_row['Player_Name'],
            'position': player_row['Position'],
            'team_name': player_row.get('Team', 'Unknown'),
            'vbd': player_row.get('VBD_Value', 0),
            'overall_rank': player_row.get('Overall_Rank', 999)
        }
        
        st.session_state.draft_results.append(pick_info)
        
        # Remove player from available
        st.session_state.available_players = st.session_state.available_players[
            st.session_state.available_players['Player_Name'] != player_row['Player_Name']
        ]
        
        # Add to user team
        if st.session_state.draft_simulator:
            st.session_state.draft_simulator.user_team.append(player_row.to_dict())
        
        # Move to next pick
        st.session_state.current_pick_number += 1
        st.session_state.waiting_for_user_pick = False
        st.session_state.pick_timer_start = datetime.now()

    def handle_ai_pick(self):
        """Handle AI picks with timer."""
        # Check if we need to make an AI pick
        if st.session_state.pick_timer_start:
            elapsed = (datetime.now() - st.session_state.pick_timer_start).total_seconds()
            
            # AI picks after 3-8 seconds (random timing)
            ai_pick_time = random.uniform(3, 8)
            
            if elapsed >= ai_pick_time and not st.session_state.waiting_for_user_pick:
                # Make AI pick
                simulator = st.session_state.draft_simulator
                team_index = simulator.get_pick_order(st.session_state.current_pick_number)
                
                if len(st.session_state.available_players) > 0:
                    ai_team_index = team_index - 1 if team_index > 0 else 8
                    ai_pick = simulator.ai_draft_pick(ai_team_index, st.session_state.available_players)
                    
                    if ai_pick:
                        pick_info = {
                            'pick': st.session_state.current_pick_number,
                            'round': ((st.session_state.current_pick_number - 1) // 10) + 1,
                            'team': f'AI Team {team_index + 1}',
                            'player': ai_pick['Player_Name'],
                            'position': ai_pick['Position'],
                            'team_name': ai_pick.get('Team', 'Unknown'),
                            'vbd': ai_pick.get('VBD_Value', 0),
                            'overall_rank': ai_pick.get('Overall_Rank', 999)
                        }
                        
                        st.session_state.draft_results.append(pick_info)
                        
                        # Remove player from available
                        st.session_state.available_players = st.session_state.available_players[
                            st.session_state.available_players['Player_Name'] != ai_pick['Player_Name']
                        ]
                        
                        # Add to AI team
                        if ai_team_index < 9:
                            simulator.ai_teams[ai_team_index].append(ai_pick)
                        
                        # Move to next pick
                        st.session_state.current_pick_number += 1
                        st.session_state.pick_timer_start = datetime.now()
                        
                        st.rerun()
        
        # Auto-refresh every 1 second during AI picks
        if not st.session_state.waiting_for_user_pick:
            st.rerun()

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
        """Calculate comprehensive AI draft grade."""
        if not user_team:
            return {
                'score': 0,
                'letter_grade': 'F',
                'summary': 'No players drafted',
                'breakdown': {}
            }

        # Calculate various grading metrics
        total_vbd = sum(player.get('VBD_Value', 0) for player in user_team)
        avg_vbd = total_vbd / len(user_team) if user_team else 0
        
        # Position analysis
        position_counts = {}
        position_vbd = {}
        for player in user_team:
            pos = player.get('Position', 'UNKNOWN')
            position_counts[pos] = position_counts.get(pos, 0) + 1
            position_vbd[pos] = position_vbd.get(pos, 0) + player.get('VBD_Value', 0)

        # Scoring components
        vbd_score = min(35, (total_vbd / 100) * 35)  # 35 points max for VBD
        
        # Position balance score (25 points max)
        ideal_positions = {'QB': 1, 'RB': 2, 'WR': 2, 'TE': 1, 'K': 1, 'DEF': 1}
        balance_score = 0
        for pos, ideal_count in ideal_positions.items():
            actual_count = position_counts.get(pos, 0)
            if actual_count >= ideal_count:
                balance_score += (25 / len(ideal_positions))
            else:
                balance_score += (actual_count / ideal_count) * (25 / len(ideal_positions))

        # Value picks score (20 points max)
        value_picks = sum(1 for player in user_team if player.get('Value_Pick', False))
        value_score = min(20, (value_picks / max(1, len(user_team))) * 40)

        # Draft timing score (20 points max)
        timing_score = 20  # Base score, deduct for bad picks
        for player in user_team:
            pos = player.get('Position', 'UNKNOWN')
            overall_rank = player.get('Overall_Rank', 999)
            
            # Penalize reaching for players or bad timing
            if pos in ['K', 'DEF'] and overall_rank < 150:
                timing_score -= 5  # Penalty for drafting K/DEF too early
            elif pos == 'QB' and overall_rank > 50 and len([p for p in user_team if p.get('Position') == 'QB']) == 1:
                timing_score -= 3  # Penalty for waiting too long on QB

        timing_score = max(0, timing_score)

        # Calculate final score
        final_score = vbd_score + balance_score + value_score + timing_score

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
                'balance_score': balance_score,
                'value_score': value_score,
                'timing_score': timing_score,
                'total_vbd': total_vbd,
                'avg_vbd': avg_vbd,
                'value_picks': value_picks
            }
        }

    def display_user_team_analysis(self, user_team: List[dict], draft_grade: dict):
        """Display detailed user team analysis."""
        st.markdown("### 🏆 Your Final Team")
        
        if not user_team:
            st.info("No players drafted yet.")
            return

        # Team composition
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### 📋 Roster Breakdown")
            
            for idx, player in enumerate(user_team):
                pick_round = ((idx) // 10) + 1 if idx < len(user_team) else 1
                
                st.markdown(f"""
                <div class="draft-pick" style="border-left: 4px solid #667eea;">
                    <div class="pick-number">R{pick_round}</div>
                    <div style="flex-grow: 1;">
                        <div style="font-weight: 600; font-size: 1.1rem;">{player['Player_Name']}</div>
                        <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
                            <span class="position-badge pos-{player['Position'].lower()}">{player['Position']}</span>
                            <span class="team-badge">{player.get('Team', 'UNK')}</span>
                            <span style="margin-left: 0.5rem;">VBD: {player.get('VBD_Value', 0):.1f}</span>
                            <span style="margin-left: 0.5rem;">Rank: #{player.get('Overall_Rank', 999)}</span>
                        </div>
                    </div>
                    {'<div style="color: #00ff87;">💎 VALUE</div>' if player.get('Value_Pick', False) else ''}
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown("#### 📊 Team Stats")
            
            # Position counts
            position_counts = {}
            for player in user_team:
                pos = player.get('Position', 'UNKNOWN')
                position_counts[pos] = position_counts.get(pos, 0) + 1

            for pos, count in position_counts.items():
                st.markdown(f"**{pos}:** {count} players")

            st.markdown("---")
            
            # Key metrics
            total_vbd = sum(player.get('VBD_Value', 0) for player in user_team)
            value_picks = sum(1 for player in user_team if player.get('Value_Pick', False))
            
            st.metric("Total VBD Score", f"{total_vbd:.1f}")
            st.metric("Value Picks", value_picks)
            st.metric("Team Size", len(user_team))

    def display_draft_grade_breakdown(self, draft_grade: dict):
        """Display detailed breakdown of draft grade."""
        st.markdown("### 📊 AI Draft Grade Breakdown")
        
        breakdown = draft_grade['breakdown']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Scoring Components")
            
            # Score breakdown chart
            components = ['VBD Score', 'Position Balance', 'Value Picks', 'Draft Timing']
            scores = [
                breakdown['vbd_score'],
                breakdown['balance_score'], 
                breakdown['value_score'],
                breakdown['timing_score']
            ]
            max_scores = [35, 25, 20, 20]
            
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
            
            st.metric("VBD Score", f"{breakdown['vbd_score']:.1f}/35")
            st.metric("Position Balance", f"{breakdown['balance_score']:.1f}/25")
            st.metric("Value Identification", f"{breakdown['value_score']:.1f}/20")
            st.metric("Draft Timing", f"{breakdown['timing_score']:.1f}/20")
            
            st.markdown("---")
            
            st.metric("Total VBD Accumulated", f"{breakdown['total_vbd']:.1f}")
            st.metric("Average VBD per Player", f"{breakdown['avg_vbd']:.1f}")
            st.metric("Value Picks Found", breakdown['value_picks'])

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
        """Display AI-powered future suggestions."""
        st.markdown("### 🔮 AI Future Suggestions")
        
        # Waiver wire targets
        st.markdown("#### 🎯 Waiver Wire Targets")
        
        # Find undrafted high-value players
        drafted_names = [p['Player_Name'] for p in user_team]
        undrafted = st.session_state.available_players[
            ~st.session_state.available_players['Player_Name'].isin(drafted_names)
        ].head(10)
        
        if not undrafted.empty:
            for _, player in undrafted.iterrows():
                st.markdown(f"""
                <div style="padding: 0.8rem; margin: 0.5rem 0; background: rgba(0,255,135,0.1); border-left: 3px solid #00ff87; border-radius: 8px;">
                    <div style="font-weight: 600;">{player['Player_Name']} ({player.get('Team', 'UNK')})</div>
                    <div style="font-size: 0.9rem; color: rgba(255,255,255,0.8);">
                        <span class="position-badge pos-{player['Position'].lower()}" style="font-size: 0.7rem; padding: 0.2rem 0.4rem;">{player['Position']}</span>
                        VBD: {player['VBD_Value']:.1f} | Rank: #{player['Overall_Rank']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Trade targets
        st.markdown("#### 🔄 Trade Opportunities")
        
        position_counts = {}
        for player in user_team:
            pos = player.get('Position', 'UNKNOWN')
            position_counts[pos] = position_counts.get(pos, 0) + 1

        trade_suggestions = []
        
        # Suggest trades based on roster construction
        if position_counts.get('RB', 0) >= 4:
            trade_suggestions.append("Consider trading RB depth for WR/TE upgrades")
        if position_counts.get('WR', 0) >= 5:
            trade_suggestions.append("Package WRs to upgrade at RB or elite TE")
        if position_counts.get('QB', 0) >= 2:
            trade_suggestions.append("Trade backup QB for skill position depth")

        for suggestion in trade_suggestions:
            st.markdown(f"• {suggestion}")

        # Season management tips
        st.markdown("#### 📅 Season Management Strategy")
        
        management_tips = [
            "Monitor bye weeks for optimal lineup management",
            "Track injury reports for handcuff opportunities", 
            "Stream defenses based on matchups",
            "Consider quarterback streaming if you went late at the position",
            "Watch for breakout candidates on waivers",
            "Plan ahead for playoff schedule strength"
        ]
        
        for tip in management_tips[:4]:
            st.markdown(f"• {tip}")

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

            for idx, (_, player) in enumerate(filtered_data.iterrows()):
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
                        
                        if st.button(f"🏈 {display_name}", key=f"player_{idx}", use_container_width=True):
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
            st.session_state.draft_rounds = 16
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
                st.markdown("### 🎮 Real-Time Draft Configuration")
                
                draft_col1, draft_col2, draft_col3 = st.columns(3)
                
                with draft_col1:
                    num_rounds = st.selectbox("Draft Rounds", [10, 12, 15, 16], index=3)
                    st.session_state.draft_rounds = num_rounds
                
                with draft_col2:
                    draft_position = st.selectbox("Your Draft Position", list(range(1, 11)), index=4)
                    st.session_state.user_draft_position = draft_position
                
                with draft_col3:
                    league_type = st.selectbox("League Type", ["Standard", "PPR", "Half-PPR"], index=1)

            with col2:
                st.markdown("### ⏱️ Real-Time Features")
                st.markdown("""
                **Live Draft Features:**
                - ⏱️ 60-second timer per pick
                - 🎯 User player selection
                - 🤖 Smart AI opponents
                - 📊 Live draft analytics
                - 🏆 Post-draft AI grading
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
