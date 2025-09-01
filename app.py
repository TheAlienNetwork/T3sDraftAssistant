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

                                # Extract additional data
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
        """Extract player names and additional data."""
        # Find player name column (usually first non-empty column)
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
            <h2 style="margin-bottom: 1rem;">🏈 {player_data['Player_Name']}</h2>
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

        # Tabs for detailed analysis
        tab1, tab2, tab3, tab4 = st.tabs(["📊 VBD Analysis", "📰 News & Intel", "🤖 AI Insights", "📈 Comparison"])

        with tab1:
            self.render_vbd_analysis_tab(player_data)

        with tab2:
            self.render_news_tab(player_data)

        with tab3:
            self.render_ai_insights_tab(player_data)

        with tab4:
            self.render_comparison_tab(player_data, all_data)

    def render_vbd_analysis_tab(self, player_data):
        """Render VBD analysis tab."""
        st.markdown("### 📊 Value Based Drafting Analysis")

        col1, col2 = st.columns(2)

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

        # Points breakdown if available
        if 'Points' in player_data and player_data['Points'] > 0:
            st.markdown("#### 🏈 Fantasy Points Projection")
            points = player_data.get('Points', 0)
            st.metric("Projected Fantasy Points", f"{points:.1f}")

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

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'players_data' not in st.session_state:
    st.session_state.players_data = pd.DataFrame()

# Enhanced Hero Header
st.markdown("""
<div class="hero-header">
    <h1 class="hero-title">Fantasy Football 2025</h1>
    <p class="hero-subtitle">🚀 Advanced VBD Rankings with AI Analytics</p>
</div>
""", unsafe_allow_html=True)

# Initialize analyzer
analyzer = AdvancedFantasyAnalyzer()

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
                col_rank, col_player, col_pos, col_vbd, col_round, col_ai, col_news = st.columns([1, 3, 1, 1, 1, 1, 3])

                with col_rank:
                    st.markdown(f'<div class="rank-badge {rank_class}">#{overall_rank}</div>', 
                               unsafe_allow_html=True)
                    st.markdown(f"<small>Overall</small>", unsafe_allow_html=True)

                with col_player:
                    if st.button(f"🏈 {player['Player_Name']}", key=f"player_{idx}", use_container_width=True):
                        st.session_state.selected_player = player

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
                <li><strong>News:</strong> Column Y (automatic detection)</li>
            </ul>
        </div>

        <p><strong>Features:</strong> Advanced AI rankings, value pick identification, draft round optimization</p>
    </div>
    """, unsafe_allow_html=True)

# Enhanced footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: rgba(255,255,255,0.6); padding: 2rem;'>
    <p style="font-size: 1.1rem; font-weight: 600;">Fantasy Football 2025 | Advanced VBD Analytics with AI</p>
    <p>Value Based Drafting • Machine Learning Insights • Position Scarcity Logic</p>
</div>
""", unsafe_allow_html=True)