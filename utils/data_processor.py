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
        try:
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
                            if possible_name in str(col).lower() or str(col).lower() in possible_name:
                                matched_col = col
                                break
                        if matched_col:
                            break
                
                # Add column if found and it's a single column
                if matched_col and matched_col in df.columns:
                    try:
                        # Ensure we're only copying series data, not complex objects
                        column_data = df[matched_col].copy()
                        if isinstance(column_data, pd.Series):
                            standardized_df[standard_name] = column_data
                    except Exception as e:
                        st.warning(f"Error mapping column '{matched_col}' to '{standard_name}': {str(e)}")
                        continue
            
            # Add any remaining columns that weren't mapped
            mapped_cols = set()
            for possible_names in self.column_mappings.values():
                mapped_cols.update(possible_names)
            
            for col in available_cols:
                if col not in mapped_cols and col not in standardized_df.columns:
                    try:
                        # Only add if it's a proper series
                        column_data = df[col].copy()
                        if isinstance(column_data, pd.Series):
                            # Clean column name for consistency
                            clean_col_name = self._clean_column_name(str(col))
                            standardized_df[clean_col_name] = column_data
                    except Exception as e:
                        st.warning(f"Error adding unmapped column '{col}': {str(e)}")
                        continue
            
            return standardized_df
            
        except Exception as e:
            st.error(f"Error in column standardization: {str(e)}")
            return df.copy()  # Return original if standardization fails
    
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
            # Convert to string first, then apply string operations
            cleaned_df['name'] = cleaned_df['name'].astype(str)
            cleaned_df = cleaned_df[cleaned_df['name'].str.strip() != '']
            cleaned_df = cleaned_df[cleaned_df['name'].str.strip() != 'nan']
        
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
    
    def _generate_ai_grades(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate AI-based grades for players based on available statistics."""
        result_df = df.copy()
        
        # Check if grade column exists and has missing values
        needs_grades = False
        if 'grade' not in result_df.columns:
            result_df['grade'] = np.nan
            needs_grades = True
        else:
            needs_grades = result_df['grade'].isna().any()
        
        if not needs_grades:
            return result_df
        
        # Get numeric features for grade calculation
        numeric_features = []
        feature_weights = {}
        
        # Define feature importance weights based on NFL scouting
        if 'forty_time' in result_df.columns:
            numeric_features.append('forty_time')
            feature_weights['forty_time'] = -0.3  # Lower is better
        
        if 'height_inches' in result_df.columns:
            numeric_features.append('height_inches')
            feature_weights['height_inches'] = 0.15
        
        if 'weight' in result_df.columns:
            numeric_features.append('weight')
            feature_weights['weight'] = 0.1
        
        if 'vertical' in result_df.columns:
            numeric_features.append('vertical')
            feature_weights['vertical'] = 0.2
        
        if 'broad_jump' in result_df.columns:
            numeric_features.append('broad_jump')
            feature_weights['broad_jump'] = 0.15
        
        if 'bench_press' in result_df.columns:
            numeric_features.append('bench_press')
            feature_weights['bench_press'] = 0.1
        
        if 'three_cone' in result_df.columns:
            numeric_features.append('three_cone')
            feature_weights['three_cone'] = -0.15  # Lower is better
        
        if 'shuttle' in result_df.columns:
            numeric_features.append('shuttle')
            feature_weights['shuttle'] = -0.1  # Lower is better
        
        if 'bmi' in result_df.columns:
            numeric_features.append('bmi')
            feature_weights['bmi'] = -0.05  # Moderate BMI preferred
        
        if 'speed_score' in result_df.columns:
            numeric_features.append('speed_score')
            feature_weights['speed_score'] = 0.25
        
        # Calculate grades for each position group
        if 'position_group' in result_df.columns and len(numeric_features) > 0:
            for pos_group in result_df['position_group'].unique():
                if pd.isna(pos_group):
                    continue
                
                pos_mask = result_df['position_group'] == pos_group
                pos_data = result_df[pos_mask].copy()
                
                # Calculate weighted score for this position group
                scores = []
                for idx, row in pos_data.iterrows():
                    score = 50  # Base score
                    total_weight = 0
                    
                    for feature in numeric_features:
                        if feature in pos_data.columns and pd.notna(row[feature]):
                            # Normalize feature value within position group
                            feature_values = pos_data[feature].dropna()
                            if len(feature_values) > 1:
                                feature_std = feature_values.std()
                                feature_mean = feature_values.mean()
                                
                                if feature_std > 0:
                                    normalized_value = (row[feature] - feature_mean) / feature_std
                                    weight = feature_weights.get(feature, 0.1)
                                    score += normalized_value * weight * 10
                                    total_weight += abs(weight)
                    
                    # Apply position-specific adjustments
                    score = self._apply_position_adjustments(score, pos_group, row)
                    
                    # Ensure score is within reasonable bounds (0-100)
                    score = max(0, min(100, score))
                    scores.append(score)
                
                # Update grades for this position group where missing
                missing_mask = pos_mask & result_df['grade'].isna()
                if missing_mask.any():
                    result_df.loc[missing_mask, 'grade'] = scores[:missing_mask.sum()]
        
        # Fill any remaining missing grades with global average
        if result_df['grade'].isna().any():
            global_avg = result_df['grade'].mean()
            if pd.isna(global_avg):
                global_avg = 50  # Default fallback
            result_df['grade'] = result_df['grade'].fillna(global_avg)
        
        return result_df
    
    def _apply_position_adjustments(self, base_score: float, position_group: str, player_data: pd.Series) -> float:
        """Apply position-specific adjustments to the base score."""
        score = base_score
        
        # Position-specific adjustments
        if position_group == 'Quarterback':
            # QBs need good arm strength and accuracy (harder to measure from combine)
            score += 5  # Slight bonus for the premium position
        
        elif position_group == 'Running Back':
            # RBs benefit more from speed and agility
            if 'forty_time' in player_data and pd.notna(player_data['forty_time']):
                if player_data['forty_time'] < 4.5:
                    score += 8
                elif player_data['forty_time'] < 4.6:
                    score += 4
        
        elif position_group == 'Wide Receiver':
            # WRs need speed and jumping ability
            if 'vertical' in player_data and pd.notna(player_data['vertical']):
                if player_data['vertical'] > 35:
                    score += 6
            if 'forty_time' in player_data and pd.notna(player_data['forty_time']):
                if player_data['forty_time'] < 4.4:
                    score += 10
                elif player_data['forty_time'] < 4.5:
                    score += 5
        
        elif position_group == 'Defensive Line':
            # DL needs size and strength
            if 'bench_press' in player_data and pd.notna(player_data['bench_press']):
                if player_data['bench_press'] > 25:
                    score += 6
            if 'weight' in player_data and pd.notna(player_data['weight']):
                if player_data['weight'] > 280:
                    score += 4
        
        elif position_group == 'Linebacker':
            # LBs need balance of size, speed, and agility
            if 'three_cone' in player_data and pd.notna(player_data['three_cone']):
                if player_data['three_cone'] < 7.0:
                    score += 5
        
        elif position_group == 'Defensive Back':
            # DBs need speed and agility
            if 'forty_time' in player_data and pd.notna(player_data['forty_time']):
                if player_data['forty_time'] < 4.4:
                    score += 8
            if 'three_cone' in player_data and pd.notna(player_data['three_cone']):
                if player_data['three_cone'] < 6.8:
                    score += 5
        
        elif position_group == 'Offensive Line':
            # OL needs size and functional strength
            if 'weight' in player_data and pd.notna(player_data['weight']):
                if player_data['weight'] > 300:
                    score += 6
            if 'bench_press' in player_data and pd.notna(player_data['bench_press']):
                if player_data['bench_press'] > 30:
                    score += 5
        
        return score
    
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
        
        # Generate AI-based grades if missing
        cleaned_df = self._generate_ai_grades(cleaned_df)
        
        # Clean position data to handle mixed types
        if 'position' in cleaned_df.columns:
            cleaned_df['position'] = cleaned_df['position'].fillna('Unknown').astype(str)
        
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
