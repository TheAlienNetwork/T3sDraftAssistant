import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

class PlayerAnalysis:
    """Individual player analysis component."""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.colors = {
            'primary': '#FF6B35',
            'secondary': '#4ECDC4',
            'accent': '#45B7D1',
            'success': '#96CEB4',
            'warning': '#FFEAA7',
            'danger': '#FF7675'
        }
    
    def render(self):
        """Render the player analysis interface."""
        st.markdown("## 👤 Individual Player Analysis")
        
        if 'name' not in self.data.columns:
            st.error("Player name column required for individual analysis.")
            return
        
        # Player selection
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Search and filter
            search_term = st.text_input("🔍 Search Player", placeholder="Enter player name...")
            
            # Filter data based on search
            if search_term:
                filtered_data = self.data[
                    self.data['name'].str.contains(search_term, case=False, na=False)
                ]
            else:
                filtered_data = self.data
            
            if len(filtered_data) == 0:
                st.warning("No players found matching the search criteria.")
                return
            
            # Player selector
            players = filtered_data['name'].unique()
            selected_player = st.selectbox("Select Player", sorted(players))
        
        with col2:
            # Additional filters
            if 'position' in self.data.columns:
                # Clean positions and handle mixed types
                unique_positions = [str(pos) for pos in self.data['position'].unique() if pd.notna(pos) and str(pos) != 'nan']
                positions = ['All'] + sorted(unique_positions)
                selected_position = st.selectbox("Filter by Position", positions)
                
                if selected_position != 'All':
                    filtered_data = filtered_data[filtered_data['position'] == selected_position]
                    if len(filtered_data) == 0:
                        st.warning(f"No players found for position {selected_position}")
                        return
        
        # Get selected player data
        player_data = self.data[self.data['name'] == selected_player].iloc[0]
        
        # Player profile header
        self._render_player_header(player_data)
        
        # Tabs for different analysis views
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Player Profile", 
            "📈 Performance Metrics", 
            "⚖️ Comparisons", 
            "🎯 Projections",
            "📋 Detailed Stats"
        ])
        
        with tab1:
            self._render_player_profile(player_data)
        
        with tab2:
            self._render_performance_metrics(player_data)
        
        with tab3:
            self._render_player_comparisons(player_data)
        
        with tab4:
            self._render_player_projections(player_data)
        
        with tab5:
            self._render_detailed_stats(player_data)
    
    def _render_player_header(self, player_data):
        """Render player header with key information."""
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f"### {player_data['name']}")
            if 'position' in player_data:
                st.markdown(f"**Position:** {player_data['position']}")
        
        with col2:
            if 'college' in player_data:
                st.markdown(f"**College:** {player_data['college']}")
        
        with col3:
            if 'height_inches' in player_data and not pd.isna(player_data['height_inches']):
                feet = int(player_data['height_inches'] // 12)
                inches = int(player_data['height_inches'] % 12)
                st.markdown(f"**Height:** {feet}'{inches}\"")
        
        with col4:
            if 'weight' in player_data and not pd.isna(player_data['weight']):
                st.markdown(f"**Weight:** {player_data['weight']:.0f} lbs")
        
        with col5:
            if 'grade' in player_data and not pd.isna(player_data['grade']):
                st.markdown(f"**Grade:** {player_data['grade']:.1f}")
        
        st.markdown("---")
    
    def _render_player_profile(self, player_data):
        """Render comprehensive player profile."""
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📋 Basic Information")
            
            info_data = []
            info_fields = {
                'name': 'Name',
                'position': 'Position',
                'position_group': 'Position Group',
                'college': 'College',
                'height_inches': 'Height (inches)',
                'weight': 'Weight (lbs)',
                'bmi': 'BMI',
                'grade': 'Overall Grade'
            }
            
            for field, label in info_fields.items():
                if field in player_data and not pd.isna(player_data[field]):
                    if field == 'height_inches':
                        feet = int(player_data[field] // 12)
                        inches = int(player_data[field] % 12)
                        value = f"{feet}'{inches}\" ({player_data[field]:.1f}\")"
                    elif field in ['weight', 'bmi', 'grade']:
                        value = f"{player_data[field]:.1f}"
                    else:
                        value = str(player_data[field])
                    
                    info_data.append({'Attribute': label, 'Value': value})
            
            if info_data:
                info_df = pd.DataFrame(info_data)
                st.dataframe(info_df, width='stretch', hide_index=True)
        
        with col2:
            st.markdown("#### 🏃‍♂️ Combine Metrics")
            
            combine_fields = {
                'forty_time': '40-Yard Dash',
                'bench_press': 'Bench Press',
                'vertical': 'Vertical Jump',
                'broad_jump': 'Broad Jump',
                'three_cone': '3-Cone Drill',
                'shuttle': '20-Yard Shuttle'
            }
            
            combine_data = []
            for field, label in combine_fields.items():
                if field in player_data and not pd.isna(player_data[field]):
                    combine_data.append({
                        'Metric': label,
                        'Value': f"{player_data[field]:.2f}",
                        'Raw_Value': player_data[field]
                    })
            
            if combine_data:
                combine_df = pd.DataFrame(combine_data)
                st.dataframe(combine_df[['Metric', 'Value']], width='stretch', hide_index=True)
                
                # Radar chart for combine metrics
                if len(combine_data) >= 3:
                    fig_radar = go.Figure()
                    
                    fig_radar.add_trace(go.Scatterpolar(
                        r=[item['Raw_Value'] for item in combine_data],
                        theta=[item['Metric'] for item in combine_data],
                        fill='toself',
                        name=player_data['name'],
                        line_color=self.colors['primary']
                    ))
                    
                    fig_radar.update_layout(
                        polar=dict(
                            radialaxis=dict(visible=True)
                        ),
                        title="Combine Performance Profile",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white')
                    )
                    
                    st.plotly_chart(fig_radar, width='stretch')
            else:
                st.info("No combine metrics available for this player.")
    
    def _render_performance_metrics(self, player_data):
        """Render performance metrics analysis."""
        st.markdown("#### 📊 Performance Analysis")
        
        if 'position' not in player_data or 'grade' not in player_data:
            st.warning("Position and grade information required for performance analysis.")
            return
        
        # Position-based analysis
        position_data = self.data[self.data['position'] == player_data['position']]
        
        if len(position_data) < 2:
            st.warning("Insufficient data for position-based analysis.")
            return
        
        # Calculate percentiles
        metrics = ['grade']
        combine_metrics = ['forty_time', 'bench_press', 'vertical', 'broad_jump', 'three_cone', 'shuttle']
        physical_metrics = ['height_inches', 'weight', 'bmi']
        
        all_metrics = metrics + [m for m in combine_metrics + physical_metrics if m in self.data.columns]
        
        percentile_data = []
        for metric in all_metrics:
            if metric in player_data and not pd.isna(player_data[metric]):
                player_value = player_data[metric]
                position_values = position_data[metric].dropna()
                
                if len(position_values) > 1:
                    percentile = (position_values < player_value).mean() * 100
                    percentile_data.append({
                        'Metric': metric.replace('_', ' ').title(),
                        'Player Value': f"{player_value:.2f}",
                        'Position Avg': f"{position_values.mean():.2f}",
                        'Percentile': f"{percentile:.1f}%",
                        'Raw_Percentile': percentile
                    })
        
        if percentile_data:
            col1, col2 = st.columns(2)
            
            with col1:
                # Percentile table
                percentile_df = pd.DataFrame(percentile_data)
                st.dataframe(
                    percentile_df[['Metric', 'Player Value', 'Position Avg', 'Percentile']],
                    width='stretch',
                    hide_index=True
                )
            
            with col2:
                # Percentile visualization
                fig_percentile = px.bar(
                    percentile_df,
                    x='Raw_Percentile',
                    y='Metric',
                    orientation='h',
                    title=f"Percentile Rankings vs {player_data['position']}",
                    color='Raw_Percentile',
                    color_continuous_scale='RdYlGn'
                )
                
                fig_percentile.add_vline(
                    x=50,
                    line_dash="dash",
                    line_color="white",
                    annotation_text="Average"
                )
                
                fig_percentile.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis_title="Percentile",
                    yaxis_title="Metric"
                )
                
                st.plotly_chart(fig_percentile, width='stretch')
        
        # Strengths and weaknesses
        if percentile_data:
            st.markdown("#### 💪 Strengths & Weaknesses")
            
            col_str, col_weak = st.columns(2)
            
            # Sort by percentile
            sorted_metrics = sorted(percentile_data, key=lambda x: x['Raw_Percentile'], reverse=True)
            
            with col_str:
                st.markdown("##### 🎯 Strengths (Top 3)")
                for i, metric in enumerate(sorted_metrics[:3]):
                    st.success(f"**{metric['Metric']}**: {metric['Percentile']} percentile")
            
            with col_weak:
                st.markdown("##### ⚠️ Areas for Improvement (Bottom 3)")
                for i, metric in enumerate(sorted_metrics[-3:]):
                    st.warning(f"**{metric['Metric']}**: {metric['Percentile']} percentile")
    
    def _render_player_comparisons(self, player_data):
        """Render player comparison analysis."""
        st.markdown("#### ⚖️ Player Comparisons")
        
        if 'position' not in player_data:
            st.warning("Position information required for comparisons.")
            return
        
        # Similar players selection
        position_players = self.data[
            (self.data['position'] == player_data['position']) & 
            (self.data['name'] != player_data['name'])
        ]
        
        if len(position_players) == 0:
            st.warning(f"No other {player_data['position']} players found for comparison.")
            return
        
        # Select comparison players
        comparison_players = st.multiselect(
            "Select Players for Comparison",
            position_players['name'].tolist(),
            default=position_players['name'].tolist()[:3]
        )
        
        if not comparison_players:
            st.info("Select players to compare with.")
            return
        
        # Prepare comparison data
        comparison_data = self.data[
            self.data['name'].isin([player_data['name']] + comparison_players)
        ].copy()
        
        # Metrics for comparison
        compare_metrics = ['grade']
        combine_metrics = ['forty_time', 'bench_press', 'vertical', 'broad_jump', 'three_cone', 'shuttle']
        physical_metrics = ['height_inches', 'weight', 'bmi']
        
        available_metrics = [m for m in compare_metrics + combine_metrics + physical_metrics 
                           if m in comparison_data.columns]
        
        if len(available_metrics) < 2:
            st.warning("Insufficient metrics for comparison.")
            return
        
        # Comparison table
        st.markdown("##### 📋 Comparison Table")
        
        display_cols = ['name'] + available_metrics
        comparison_display = comparison_data[display_cols].round(2)
        
        # Highlight the selected player
        def highlight_player(row):
            if row['name'] == player_data['name']:
                return ['background-color: #FF6B35; color: white'] * len(row)
            return [''] * len(row)
        
        st.dataframe(
            comparison_display.style.apply(highlight_player, axis=1),
            width='stretch',
            hide_index=True
        )
        
        # Radar chart comparison
        if len(available_metrics) >= 3:
            st.markdown("##### 📊 Multi-Metric Comparison")
            
            # Normalize metrics for radar chart
            normalized_data = comparison_data[available_metrics].copy()
            for col in available_metrics:
                col_min = normalized_data[col].min()
                col_max = normalized_data[col].max()
                if col_max > col_min:
                    normalized_data[col] = (normalized_data[col] - col_min) / (col_max - col_min)
                else:
                    normalized_data[col] = 0.5
            
            fig_radar_comp = go.Figure()
            
            colors = [self.colors['primary'], self.colors['secondary'], 
                     self.colors['accent'], self.colors['success'], self.colors['warning']]
            
            for i, (_, row) in enumerate(comparison_data.iterrows()):
                player_name = row['name']
                norm_values = normalized_data.iloc[i]
                
                fig_radar_comp.add_trace(go.Scatterpolar(
                    r=norm_values.tolist() + [norm_values.iloc[0]],
                    theta=[m.replace('_', ' ').title() for m in available_metrics] + [available_metrics[0].replace('_', ' ').title()],
                    fill='toself' if player_name == player_data['name'] else None,
                    name=player_name,
                    line_color=colors[i % len(colors)]
                ))
            
            fig_radar_comp.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )),
                title="Player Comparison (Normalized Metrics)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_radar_comp, width='stretch')
    
    def _render_player_projections(self, player_data):
        """Render player projection analysis."""
        st.markdown("#### 🎯 Performance Projections")
        
        # This would typically involve more sophisticated modeling
        # For now, we'll provide position-based projections
        
        if 'position' not in player_data or 'grade' not in player_data:
            st.warning("Position and grade information required for projections.")
            return
        
        position_data = self.data[self.data['position'] == player_data['position']]
        
        if len(position_data) < 5:
            st.warning("Insufficient position data for meaningful projections.")
            return
        
        # Simple projection based on position statistics
        position_stats = position_data['grade'].describe()
        player_grade = player_data['grade']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 📊 Position Context")
            
            context_data = [
                {'Metric': 'Player Grade', 'Value': f"{player_grade:.2f}"},
                {'Metric': 'Position Average', 'Value': f"{position_stats['mean']:.2f}"},
                {'Metric': 'Position Median', 'Value': f"{position_stats['50%']:.2f}"},
                {'Metric': 'Position Max', 'Value': f"{position_stats['max']:.2f}"},
                {'Metric': 'Position Min', 'Value': f"{position_stats['min']:.2f}"}
            ]
            
            context_df = pd.DataFrame(context_data)
            st.dataframe(context_df, width='stretch', hide_index=True)
        
        with col2:
            st.markdown("##### 🎯 Projection Categories")
            
            # Categorize player based on grade
            if player_grade >= position_stats['75%']:
                category = "Elite Prospect"
                description = "Top 25% of position. High NFL potential."
                color = "success"
            elif player_grade >= position_stats['50%']:
                category = "Above Average"
                description = "Above median. Solid NFL potential."
                color = "info"
            elif player_grade >= position_stats['25%']:
                category = "Average Prospect"
                description = "Around average. Development needed."
                color = "warning"
            else:
                category = "Below Average"
                description = "Below average. Significant development needed."
                color = "error"
            
            if color == "success":
                st.success(f"**{category}**\n\n{description}")
            elif color == "info":
                st.info(f"**{category}**\n\n{description}")
            elif color == "warning":
                st.warning(f"**{category}**\n\n{description}")
            else:
                st.error(f"**{category}**\n\n{description}")
        
        # Grade distribution with player position
        st.markdown("##### 📈 Grade Distribution Analysis")
        
        fig_dist = px.histogram(
            position_data,
            x='grade',
            nbins=20,
            title=f"Grade Distribution - {player_data['position']}",
            color_discrete_sequence=[self.colors['secondary']]
        )
        
        # Add player's grade as vertical line
        fig_dist.add_vline(
            x=player_grade,
            line_dash="solid",
            line_color=self.colors['primary'],
            line_width=3,
            annotation_text=f"{player_data['name']}: {player_grade:.1f}"
        )
        
        # Add percentile lines
        fig_dist.add_vline(
            x=position_stats['25%'],
            line_dash="dash",
            line_color="gray",
            annotation_text="25th %ile"
        )
        
        fig_dist.add_vline(
            x=position_stats['75%'],
            line_dash="dash",
            line_color="gray",
            annotation_text="75th %ile"
        )
        
        fig_dist.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_dist, width='stretch')
    
    def _render_detailed_stats(self, player_data):
        """Render detailed player statistics."""
        st.markdown("#### 📋 Complete Player Statistics")
        
        # All available data for the player
        player_df = pd.DataFrame({
            'Attribute': player_data.index,
            'Value': player_data.values
        })
        
        # Clean up the display
        player_df = player_df[player_df['Value'].notna()]
        player_df['Value'] = player_df['Value'].astype(str)
        
        # Categorize attributes
        basic_info = ['name', 'position', 'position_group', 'college', 'source_sheet']
        physical = ['height', 'height_inches', 'weight', 'bmi']
        combine = ['forty_time', 'bench_press', 'vertical', 'broad_jump', 'three_cone', 'shuttle']
        performance = ['grade', 'overall', 'rating', 'speed_score']
        
        categories = {
            'Basic Information': basic_info,
            'Physical Attributes': physical,
            'Combine Metrics': combine,
            'Performance Scores': performance
        }
        
        for category, attrs in categories.items():
            category_data = player_df[player_df['Attribute'].isin(attrs)]
            
            if not category_data.empty:
                st.markdown(f"##### {category}")
                st.dataframe(category_data, width='stretch', hide_index=True)
                st.markdown("")
        
        # Show any remaining attributes
        used_attrs = [attr for attrs in categories.values() for attr in attrs]
        remaining_data = player_df[~player_df['Attribute'].isin(used_attrs)]
        
        if not remaining_data.empty:
            st.markdown("##### Other Attributes")
            st.dataframe(remaining_data, width='stretch', hide_index=True)
