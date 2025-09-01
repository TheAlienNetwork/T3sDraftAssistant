import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional, List
import re
import streamlit as st

class DataProcessor:
    """Handles Excel file processing and data standardization for NFL Draft analysis."""
    
    def __init__(self):
        self.position_mappings = {
            'QB': 'Quarterback',
            'RB': 'Running Back',
            'FB': 'Fullback',
            'WR': 'Wide Receiver',
            'TE': 'Tight End',
            'OT': 'Offensive Tackle',
            'OG': 'Offensive Guard',
            'C': 'Center',
            'DE': 'Defensive End',
            'DT': 'Defensive Tackle',
            'NT': 'Nose Tackle',
            'LB': 'Linebacker',
            'MLB': 'Middle Linebacker',
            'OLB': 'Outside Linebacker',
            'CB': 'Cornerback',
            'S': 'Safety',
            'FS': 'Free Safety',
            'SS': 'Strong Safety',
            'K': 'Kicker',
            'P': 'Punter',
            'LS': 'Long Snapper'
        }
        
        self.column_mappings = {
            # Name variations
            'name': ['name', 'player_name', 'player', 'full_name'],
            'position': ['position', 'pos', 'positions'],
            'college': ['college', 'school', 'university'],
            'height': ['height', 'ht', 'hgt'],
            'weight': ['weight', 'wt', 'wgt'],
            'forty_time': ['40_time', '40_yard', 'forty', '40yd', '40_yd'],
            'bench_press': ['bench', 'bench_press', 'bp'],
            'vertical': ['vertical', 'vert', 'vertical_jump', 'vert_jump'],
            'broad_jump': ['broad', 'broad_jump', 'broad_jmp'],
            'three_cone': ['3_cone', 'three_cone', '3cone', 'cone'],
            'shuttle': ['shuttle', '20_shuttle', '20_yard_shuttle', '20yd'],
            'grade': ['grade', 'overall', 'rating', 'score', 'overall_grade']
        }
    
    def process_excel_file(self, uploaded_file) -> Tuple[Dict[str, pd.DataFrame], Optional[pd.DataFrame]]:
        """Process uploaded Excel file and extract all sheets."""
        try:
            # Read all sheets from the Excel file
            excel_data = pd.read_excel(uploaded_file, sheet_name=None, engine='openpyxl')
            
            processed_sheets = {}
            all_players = []
            
            for sheet_name, df in excel_data.items():
                # Skip empty sheets
                if df.empty:
                    continue
                
                # Process individual sheet
                processed_df = self._process_sheet(df, sheet_name)
                
                if processed_df is not None and not processed_df.empty:
                    processed_sheets[sheet_name] = processed_df
                    all_players.append(processed_df)
            
            # Combine all processed data
            if all_players:
                combined_data = pd.concat(all_players, ignore_index=True)
                combined_data = self._clean_combined_data(combined_data)
                return processed_sheets, combined_data
            else:
                return processed_sheets, None
                
        except Exception as e:
            st.error(f"Error processing Excel file: {str(e)}")
            return {}, None
    
    def _process_sheet(self, df: pd.DataFrame, sheet_name: str) -> Optional[pd.DataFrame]:
        """Process individual sheet and standardize column names."""
        try:
            # Create a copy to avoid modifying original
            processed_df = df.copy()
            
            # Clean column names (lowercase, remove spaces, special characters)
            processed_df.columns = [self._clean_column_name(col) for col in processed_df.columns]
            
            # Map columns to standard names
            standardized_df = self._standardize_columns(processed_df)
            
            # Add sheet source
            standardized_df['source_sheet'] = sheet_name
            
            # Clean and validate data
            standardized_df = self._clean_data(standardized_df)
            
            return standardized_df
            
        except Exception as e:
            st.warning(f"Error processing sheet '{sheet_name}': {str(e)}")
            return None
    
    def _clean_column_name(self, col_name: str) -> str:
        """Clean column names for standardization."""
        if pd.isna(col_name):
            return 'unknown_column'
        
        # Convert to string and lowercase
        clean_name = str(col_name).lower()
        
        # Remove special characters and replace with underscore
        clean_name = re.sub(r'[^a-z0-9_]', '_', clean_name)
        
        # Remove multiple underscores
        clean_name = re.sub(r'_+', '_', clean_name)
        
        # Remove leading/trailing underscores
        clean_name = clean_name.strip('_')
        
        return clean_name
    
    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Map columns to standard names using fuzzy matching."""
        standardized_df = pd.DataFrame()
        
        # Get available columns
        available_cols = df.columns.tolist()
        
        for standard_name, possible_names in self.column_mappings.items():
            matched_col = None
            
            # Exact match first
            for possible_name in possible_names:
                if possible_name in available_cols:
                    matched_col = possible_name
                    break
            
            # Fuzzy match if no exact match
            if matched_col is None:
                for col in available_cols:
                    for possible_name in possible_names:
                        if possible_name in col or col in possible_name:
                            matched_col = col
                            break
                    if matched_col:
                        break
            
            # Add column if found
            if matched_col:
                standardized_df[standard_name] = df[matched_col]
        
        # Add any remaining columns that weren't mapped
        for col in available_cols:
            if col not in [val for sublist in self.column_mappings.values() for val in sublist]:
                if col not in standardized_df.columns:
                    standardized_df[col] = df[col]
        
        return standardized_df
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate the data."""
        cleaned_df = df.copy()
        
        # Clean height data (convert to inches)
        if 'height' in cleaned_df.columns:
            cleaned_df['height_inches'] = cleaned_df['height'].apply(self._parse_height)
        
        # Clean weight data
        if 'weight' in cleaned_df.columns:
            cleaned_df['weight'] = pd.to_numeric(cleaned_df['weight'], errors='coerce')
        
        # Clean forty time
        if 'forty_time' in cleaned_df.columns:
            cleaned_df['forty_time'] = pd.to_numeric(cleaned_df['forty_time'], errors='coerce')
        
        # Clean numerical combine metrics
        numeric_cols = ['bench_press', 'vertical', 'broad_jump', 'three_cone', 'shuttle', 'grade']
        for col in numeric_cols:
            if col in cleaned_df.columns:
                cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
        
        # Standardize position names
        if 'position' in cleaned_df.columns:
            cleaned_df['position'] = cleaned_df['position'].apply(self._standardize_position)
        
        # Remove rows with no name
        if 'name' in cleaned_df.columns:
            cleaned_df = cleaned_df.dropna(subset=['name'])
            cleaned_df = cleaned_df[cleaned_df['name'].str.strip() != '']
        
        return cleaned_df
    
    def _parse_height(self, height_str) -> Optional[float]:
        """Parse height string and convert to inches."""
        if pd.isna(height_str):
            return None
        
        height_str = str(height_str).strip()
        
        # Pattern for feet'inches" format (e.g., "6'2\"", "6'2", "6-2")
        pattern1 = re.match(r"(\d+)['\-](\d+)", height_str)
        if pattern1:
            feet, inches = int(pattern1.group(1)), int(pattern1.group(2))
            return feet * 12 + inches
        
        # Pattern for decimal feet (e.g., "6.17")
        pattern2 = re.match(r"(\d+)\.(\d+)", height_str)
        if pattern2:
            feet = int(pattern2.group(1))
            decimal_part = int(pattern2.group(2))
            # Convert decimal to inches (assuming .17 means 2 inches, etc.)
            inches = round(decimal_part * 12 / 100)
            return feet * 12 + inches
        
        # Pattern for just inches
        pattern3 = re.match(r"(\d+)\"?$", height_str)
        if pattern3:
            return int(pattern3.group(1))
        
        return None
    
    def _standardize_position(self, position_str) -> str:
        """Standardize position names."""
        if pd.isna(position_str):
            return 'Unknown'
        
        position_str = str(position_str).strip().upper()
        
        # Direct mapping
        if position_str in self.position_mappings:
            return self.position_mappings[position_str]
        
        # Partial matching
        for abbrev, full_name in self.position_mappings.items():
            if abbrev in position_str:
                return full_name
        
        return position_str.title()
    
    def _clean_combined_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Final cleaning and feature engineering for combined data."""
        cleaned_df = df.copy()
        
        # Remove duplicates (same name and position)
        if 'name' in cleaned_df.columns and 'position' in cleaned_df.columns:
            cleaned_df = cleaned_df.drop_duplicates(subset=['name', 'position'], keep='first')
        
        # Calculate BMI if height and weight available
        if 'height_inches' in cleaned_df.columns and 'weight' in cleaned_df.columns:
            cleaned_df['bmi'] = (cleaned_df['weight'] * 703) / (cleaned_df['height_inches'] ** 2)
        
        # Calculate speed score (if forty time and weight available)
        if 'forty_time' in cleaned_df.columns and 'weight' in cleaned_df.columns:
            cleaned_df['speed_score'] = (cleaned_df['weight'] * 200) / (cleaned_df['forty_time'] ** 4)
        
        # Create position groups
        if 'position' in cleaned_df.columns:
            cleaned_df['position_group'] = cleaned_df['position'].apply(self._get_position_group)
        
        # Fill missing grades with position-based averages
        if 'grade' in cleaned_df.columns and 'position' in cleaned_df.columns:
            for position in cleaned_df['position'].unique():
                pos_mask = cleaned_df['position'] == position
                pos_avg = cleaned_df.loc[pos_mask, 'grade'].mean()
                if not pd.isna(pos_avg):
                    cleaned_df.loc[pos_mask & cleaned_df['grade'].isna(), 'grade'] = pos_avg
        
        return cleaned_df
    
    def _get_position_group(self, position: str) -> str:
        """Group positions into broader categories."""
        if pd.isna(position):
            return 'Unknown'
        
        position = position.upper()
        
        if any(pos in position for pos in ['QB']):
            return 'Quarterback'
        elif any(pos in position for pos in ['RB', 'FB']):
            return 'Running Back'
        elif any(pos in position for pos in ['WR']):
            return 'Wide Receiver'
        elif any(pos in position for pos in ['TE']):
            return 'Tight End'
        elif any(pos in position for pos in ['OT', 'OG', 'C', 'OFFENSIVE']):
            return 'Offensive Line'
        elif any(pos in position for pos in ['DE', 'DT', 'NT']):
            return 'Defensive Line'
        elif any(pos in position for pos in ['LB', 'MLB', 'OLB']):
            return 'Linebacker'
        elif any(pos in position for pos in ['CB', 'S', 'FS', 'SS', 'SAFETY', 'CORNER']):
            return 'Defensive Back'
        elif any(pos in position for pos in ['K', 'P', 'LS']):
            return 'Special Teams'
        else:
            return 'Other'
    
    def get_data_summary(self, df: pd.DataFrame) -> Dict:
        """Generate comprehensive data summary."""
        summary = {
            'total_players': len(df),
            'positions': df['position'].value_counts().to_dict() if 'position' in df.columns else {},
            'position_groups': df['position_group'].value_counts().to_dict() if 'position_group' in df.columns else {},
            'colleges': df['college'].value_counts().head(10).to_dict() if 'college' in df.columns else {},
            'data_completeness': {}
        }
        
        # Calculate data completeness
        for col in df.columns:
            summary['data_completeness'][col] = {
                'count': df[col].notna().sum(),
                'percentage': (df[col].notna().sum() / len(df)) * 100
            }
        
        return summary
