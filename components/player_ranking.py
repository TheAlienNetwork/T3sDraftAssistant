import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from typing import List, Dict

class PlayerRanking:
    """Comprehensive player ranking component with advanced filtering and modern UI."""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.colors = {
            'primary': '#FF6B35',
            'secondary': '#4ECDC4',
            'accent': '#45B7D1',
            'success': '#96CEB4',
            'warning': '#FFEAA7',
            'danger': '#FF7675',
            'elite': '#28a745',
            'high': '#17a2b8',
            'medium': '#ffc107',
            'low': '#dc3545'
        }
        
        # Position group colors
        self.position_colors = {
            'Quarterback': '#FF6B35',
            'Running Back': '#4ECDC4',
            'Wide Receiver': '#45B7D1',
            'Tight End': '#96CEB4',
            'Offensive Line': '#8B4513',
            'Defensive Line': '#DC143C',
            'Linebacker': '#FF4500',
            'Defensive Back': '#4169E1',
            'Special Teams': '#708090'
        }
    
    def render(self):
        """Render the comprehensive player ranking interface."""
        st.markdown("## 🏆 Comprehensive Player Rankings")
        
        if 'grade' not in self.data.columns:
            st.error("Grade information required for player rankings.")
            return
        
        # Enhanced filters sidebar
        with st.sidebar:
            st.markdown("### 🔧 Ranking Filters")
            
            # Position filtering
            all_positions = ['All Positions'] + sorted(self.data['position_group'].unique()) if 'position_group' in self.data.columns else ['All Positions']
            selected_position = st.selectbox("📍 Position Group", all_positions)
            
            if 'position' in self.data.columns:
                if selected_position != 'All Positions' and 'position_group' in self.data.columns:
                    specific_positions = ['All'] + sorted(self.data[self.data['position_group'] == selected_position]['position'].unique())
                else:
                    specific_positions = ['All'] + sorted(self.data['position'].unique())
                selected_specific_position = st.selectbox("🎯 Specific Position", specific_positions)
            
            # Grade range filter
            if 'grade' in self.data.columns:
                min_grade = float(self.data['grade'].min())
                max_grade = float(self.data['grade'].max())
                grade_range = st.slider(
                    "📊 Grade Range", 
                    min_grade, max_grade, 
                    (min_grade, max_grade),
                    step=0.1
                )
            
            # College filter
            if 'college' in self.data.columns:
                all_colleges = ['All Colleges'] + sorted(self.data['college'].dropna().unique())
                selected_college = st.selectbox("🎓 College", all_colleges)
            
            # Number of players to show
            num_players = st.selectbox("📋 Players to Display", [25, 50, 100, 200, 500, "All"])
        
        # Apply filters
        filtered_data = self._apply_filters(
            selected_position, 
            selected_specific_position if 'position' in self.data.columns else None,
            grade_range if 'grade' in self.data.columns else None,
            selected_college if 'college' in self.data.columns else None
        )
        
        if filtered_data.empty:
            st.warning("No players match the selected filters.")
            return
        
        # Main content tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🏆 Player Rankings", 
            "📊 Statistical Overview", 
            "🎯 Position Breakdown",
            "📈 Performance Analysis", 
            "💎 Prospect Tiers"
        ])
        
        with tab1:
            self._render_player_rankings(filtered_data, num_players)
        
        with tab2:
            self._render_statistical_overview(filtered_data)
        
        with tab3:
            self._render_position_breakdown(filtered_data)
        
        with tab4:
            self._render_performance_analysis(filtered_data)
        
        with tab5:
            self._render_prospect_tiers(filtered_data)
    
    def _apply_filters(self, position_group, specific_position, grade_range, college):
        """Apply all selected filters to the data."""
        filtered_data = self.data.copy()
        
        # Position group filter
        if position_group != 'All Positions' and 'position_group' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['position_group'] == position_group]
        
        # Specific position filter
        if specific_position and specific_position != 'All' and 'position' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['position'] == specific_position]
        
        # Grade range filter
        if grade_range and 'grade' in filtered_data.columns:
            filtered_data = filtered_data[
                (filtered_data['grade'] >= grade_range[0]) & 
                (filtered_data['grade'] <= grade_range[1])
            ]
        
        # College filter
        if college and college != 'All Colleges' and 'college' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['college'] == college]
        
        return filtered_data
    
    def _get_grade_badge_class(self, grade):
        """Get CSS class for grade badge based on grade value."""
        if pd.isna(grade):
            return 'low'
        elif grade >= 8.5:
            return 'elite'
        elif grade >= 7.5:
            return 'high'
        elif grade >= 6.5:
            return 'medium'
        else:
            return 'low'
    
    def _render_grade_badge(self, grade, player_name):
        """Render a colorful grade badge."""
        if pd.isna(grade):
            badge_class = 'low'
            grade_text = 'N/A'
        else:
            badge_class = self._get_grade_badge_class(grade)
            grade_text = f"{grade:.1f}"
        
        badge_color = self.colors[badge_class]
        
        return f"""
        <div style="
            display: inline-block;
            background: linear-gradient(135deg, {badge_color}, {badge_color}aa);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9rem;
            margin: 0.2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            text-align: center;
            min-width: 50px;
        ">
            {grade_text}
        </div>
        """
    
    def _render_position_badge(self, position_group):
        """Render a colorful position badge."""
        if pd.isna(position_group):
            position_group = 'Unknown'
        
        color = self.position_colors.get(position_group, self.colors['secondary'])
        
        return f"""
        <div style="
            display: inline-block;
            background: linear-gradient(135deg, {color}, {color}aa);
            color: white;
            padding: 0.2rem 0.6rem;
            border-radius: 15px;
            font-weight: 500;
            font-size: 0.8rem;
            margin: 0.1rem;
            box-shadow: 0 1px 5px rgba(0,0,0,0.2);
        ">
            {position_group}
        </div>
        """
    
    def _render_player_rankings(self, data, num_players):
        """Render the main player rankings table with modern styling."""
        st.markdown("### 🏆 Player Rankings")
        
        # Sort by grade
        sorted_data = data.sort_values('grade', ascending=False) if 'grade' in data.columns else data
        
        # Limit number of players
        if num_players != "All":
            sorted_data = sorted_data.head(num_players)
        
        # Summary metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("📊 Total Players", len(sorted_data))
        
        with col2:
            if 'grade' in sorted_data.columns:
                avg_grade = sorted_data['grade'].mean()
                st.metric("📈 Avg Grade", f"{avg_grade:.2f}")
        
        with col3:
            if 'position_group' in sorted_data.columns:
                unique_positions = sorted_data['position_group'].nunique()
                st.metric("🎯 Position Groups", unique_positions)
        
        with col4:
            if 'college' in sorted_data.columns:
                unique_colleges = sorted_data['college'].nunique()
                st.metric("🎓 Colleges", unique_colleges)
        
        with col5:
            if 'grade' in sorted_data.columns:
                top_grade = sorted_data['grade'].max()
                st.metric("⭐ Top Grade", f"{top_grade:.1f}")
        
        st.markdown("---")
        
        # Enhanced rankings table
        st.markdown("#### 📋 Rankings Table")
        
        # Create enhanced display data
        display_data = []
        for idx, (_, player) in enumerate(sorted_data.iterrows(), 1):
            player_info = {
                'Rank': f"#{idx}",
                'Player': player.get('name', 'Unknown'),
                'Position': player.get('position', 'Unknown'),
                'College': player.get('college', 'Unknown'),
                'Grade': player.get('grade', 0),
                'Grade_Badge': self._render_grade_badge(player.get('grade'), player.get('name', '')),
                'Position_Badge': self._render_position_badge(player.get('position_group', ''))
            }
            
            # Add combine metrics if available
            combine_metrics = ['forty_time', 'bench_press', 'vertical', 'broad_jump']
            for metric in combine_metrics:
                if metric in player and not pd.isna(player[metric]):
                    player_info[metric.replace('_', ' ').title()] = f"{player[metric]:.2f}"
                else:
                    player_info[metric.replace('_', ' ').title()] = '-'
            
            display_data.append(player_info)
        
        if display_data:
            # Create the table with badges
            for i, player_data in enumerate(display_data):
                if i % 10 == 0:  # Add spacing every 10 players
                    st.markdown("---")
                
                col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 2, 2, 1.5, 1.5])
                
                with col1:
                    # Rank with special styling for top 10
                    rank_num = i + 1
                    if rank_num <= 3:
                        st.markdown(f"<h3 style='color: gold; text-align: center;'>{player_data['Rank']}</h3>", unsafe_allow_html=True)
                    elif rank_num <= 10:
                        st.markdown(f"<h4 style='color: silver; text-align: center;'>{player_data['Rank']}</h4>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='text-align: center; font-weight: bold;'>{player_data['Rank']}</p>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"**{player_data['Player']}**")
                    st.markdown(f"*{player_data['College']}*")
                
                with col3:
                    st.markdown(player_data['Position_Badge'], unsafe_allow_html=True)
                    st.markdown(f"{player_data['Position']}")
                
                with col4:
                    st.markdown(player_data['Grade_Badge'], unsafe_allow_html=True)
                
                with col5:
                    if 'Forty Time' in player_data and player_data['Forty Time'] != '-':
                        st.markdown(f"**40:** {player_data['Forty Time']}")
                    if 'Vertical' in player_data and player_data['Vertical'] != '-':
                        st.markdown(f"**Vert:** {player_data['Vertical']}")
                
                with col6:
                    if 'Bench Press' in player_data and player_data['Bench Press'] != '-':
                        st.markdown(f"**Bench:** {player_data['Bench Press']}")
                    if 'Broad Jump' in player_data and player_data['Broad Jump'] != '-':
                        st.markdown(f"**Broad:** {player_data['Broad Jump']}")
        
        # Download rankings
        if st.button("📥 Download Rankings as CSV"):
            csv_data = sorted_data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"nfl_draft_rankings_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    def _render_statistical_overview(self, data):
        """Render statistical overview with advanced charts."""
        st.markdown("### 📊 Statistical Overview")
        
        if 'grade' not in data.columns:
            st.warning("Grade data required for statistical analysis.")
            return
        
        # Grade distribution
        col1, col2 = st.columns(2)
        
        with col1:
            fig_hist = px.histogram(
                data,
                x='grade',
                nbins=25,
                title="Grade Distribution",
                color_discrete_sequence=[self.colors['primary']]
            )
            
            # Add mean line
            mean_grade = data['grade'].mean()
            fig_hist.add_vline(
                x=mean_grade,
                line_dash="dash",
                line_color="white",
                annotation_text=f"Mean: {mean_grade:.2f}"
            )
            
            fig_hist.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_hist, width='stretch')
        
        with col2:
            # Grade tiers pie chart
            grade_tiers = []
            for _, row in data.iterrows():
                grade = row.get('grade', 0)
                if pd.isna(grade):
                    tier = 'Ungraded'
                elif grade >= 8.5:
                    tier = 'Elite (8.5+)'
                elif grade >= 7.5:
                    tier = 'High (7.5-8.4)'
                elif grade >= 6.5:
                    tier = 'Medium (6.5-7.4)'
                else:
                    tier = 'Low (<6.5)'
                grade_tiers.append(tier)
            
            tier_counts = pd.Series(grade_tiers).value_counts()
            
            fig_pie = px.pie(
                values=tier_counts.values,
                names=tier_counts.index,
                title="Player Distribution by Grade Tier",
                color_discrete_sequence=[
                    self.colors['elite'],
                    self.colors['high'],
                    self.colors['medium'],
                    self.colors['low'],
                    '#666666'
                ]
            )
            
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_pie, width='stretch')
        
        # Position vs Grade analysis
        if 'position_group' in data.columns:
            st.markdown("#### 📈 Grade Analysis by Position")
            
            fig_box = px.box(
                data,
                x='position_group',
                y='grade',
                title="Grade Distribution by Position Group",
                color='position_group',
                color_discrete_map=self.position_colors
            )
            
            fig_box.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_title="Position Group",
                yaxis_title="Grade"
            )
            
            st.plotly_chart(fig_box, width='stretch')
    
    def _render_position_breakdown(self, data):
        """Render detailed position breakdown."""
        st.markdown("### 🎯 Position Breakdown")
        
        if 'position_group' not in data.columns:
            st.warning("Position group data required for breakdown analysis.")
            return
        
        # Position summary table
        position_stats = data.groupby('position_group').agg({
            'grade': ['count', 'mean', 'std', 'max', 'min'],
            'name': 'count'
        }).round(2)
        
        position_stats.columns = ['Count', 'Avg Grade', 'Std Dev', 'Max Grade', 'Min Grade', 'Total']
        position_stats = position_stats[['Count', 'Avg Grade', 'Std Dev', 'Max Grade', 'Min Grade']]
        position_stats = position_stats.sort_values('Avg Grade', ascending=False)
        
        st.dataframe(position_stats, width='stretch')
        
        # Position depth chart
        col1, col2 = st.columns(2)
        
        with col1:
            fig_depth = px.bar(
                x=position_stats.index,
                y=position_stats['Count'],
                title="Player Count by Position",
                color=position_stats['Count'],
                color_continuous_scale='Viridis'
            )
            
            fig_depth.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_title="Position Group",
                yaxis_title="Number of Players"
            )
            
            st.plotly_chart(fig_depth, width='stretch')
        
        with col2:
            # Average grade by position
            fig_avg = px.bar(
                x=position_stats.index,
                y=position_stats['Avg Grade'],
                title="Average Grade by Position",
                color=position_stats['Avg Grade'],
                color_continuous_scale='RdYlGn'
            )
            
            fig_avg.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_title="Position Group",
                yaxis_title="Average Grade"
            )
            
            st.plotly_chart(fig_avg, width='stretch')
    
    def _render_performance_analysis(self, data):
        """Render performance analysis with combine metrics."""
        st.markdown("### 📈 Performance Analysis")
        
        # Combine metrics analysis
        combine_metrics = ['forty_time', 'bench_press', 'vertical', 'broad_jump', 'three_cone', 'shuttle']
        available_metrics = [col for col in combine_metrics if col in data.columns]
        
        if available_metrics:
            st.markdown("#### 🏃‍♂️ Combine Performance")
            
            # Create correlation matrix
            if len(available_metrics) > 1:
                corr_data = data[available_metrics + ['grade']].corr()
                
                fig_corr = px.imshow(
                    corr_data.values,
                    x=corr_data.columns,
                    y=corr_data.index,
                    color_continuous_scale='RdBu',
                    title="Performance Metrics Correlation Matrix",
                    zmin=-1,
                    zmax=1
                )
                
                fig_corr.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                
                st.plotly_chart(fig_corr, width='stretch')
            
            # Performance vs Grade scatter plots
            if len(available_metrics) >= 2:
                selected_metric = st.selectbox("Select Metric for Grade Correlation", available_metrics)
                
                fig_scatter = px.scatter(
                    data,
                    x=selected_metric,
                    y='grade',
                    color='position_group' if 'position_group' in data.columns else None,
                    title=f"Grade vs {selected_metric.replace('_', ' ').title()}",
                    hover_data=['name'] if 'name' in data.columns else None,
                    trendline="ols"
                )
                
                fig_scatter.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                
                st.plotly_chart(fig_scatter, width='stretch')
    
    def _render_prospect_tiers(self, data):
        """Render prospect tier analysis."""
        st.markdown("### 💎 Prospect Tiers")
        
        if 'grade' not in data.columns:
            st.warning("Grade data required for tier analysis.")
            return
        
        # Define tiers
        tiers = {
            'Elite Prospects (8.5+)': data[data['grade'] >= 8.5],
            'High-Quality Prospects (7.5-8.4)': data[(data['grade'] >= 7.5) & (data['grade'] < 8.5)],
            'Solid Prospects (6.5-7.4)': data[(data['grade'] >= 6.5) & (data['grade'] < 7.5)],
            'Developmental Prospects (5.5-6.4)': data[(data['grade'] >= 5.5) & (data['grade'] < 6.5)],
            'Late Round/UDFA (<5.5)': data[data['grade'] < 5.5]
        }
        
        # Tier analysis
        for tier_name, tier_data in tiers.items():
            if not tier_data.empty:
                with st.expander(f"{tier_name} ({len(tier_data)} players)"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Players", len(tier_data))
                        if 'position_group' in tier_data.columns:
                            most_common_pos = tier_data['position_group'].value_counts().index[0]
                            st.metric("Top Position", most_common_pos)
                    
                    with col2:
                        avg_grade = tier_data['grade'].mean()
                        st.metric("Avg Grade", f"{avg_grade:.2f}")
                        if 'college' in tier_data.columns:
                            most_common_college = tier_data['college'].value_counts().index[0]
                            st.metric("Top College", most_common_college)
                    
                    with col3:
                        grade_range = f"{tier_data['grade'].min():.1f} - {tier_data['grade'].max():.1f}"
                        st.metric("Grade Range", grade_range)
                    
                    # Top players in tier
                    if len(tier_data) > 0:
                        st.markdown("**Top Players:**")
                        top_tier_players = tier_data.nlargest(min(10, len(tier_data)), 'grade')
                        
                        for _, player in top_tier_players.iterrows():
                            col_a, col_b, col_c, col_d = st.columns([3, 2, 1, 1])
                            
                            with col_a:
                                st.markdown(f"**{player.get('name', 'Unknown')}**")
                            
                            with col_b:
                                st.markdown(self._render_position_badge(player.get('position_group', '')), unsafe_allow_html=True)
                            
                            with col_c:
                                st.markdown(self._render_grade_badge(player.get('grade'), player.get('name', '')), unsafe_allow_html=True)
                            
                            with col_d:
                                st.markdown(f"*{player.get('college', 'Unknown')}*")