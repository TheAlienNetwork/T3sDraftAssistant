import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, List

class TeamAnalysis:
    """Team analysis component for NFL Draft evaluation."""
    
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
        
        # NFL teams with their typical positional needs (simplified model)
        self.nfl_teams = {
            'Arizona Cardinals': {'primary_needs': ['Offensive Line', 'Linebacker'], 'secondary_needs': ['Defensive Back', 'Wide Receiver']},
            'Atlanta Falcons': {'primary_needs': ['Defensive Line', 'Offensive Line'], 'secondary_needs': ['Linebacker', 'Running Back']},
            'Baltimore Ravens': {'primary_needs': ['Wide Receiver', 'Offensive Line'], 'secondary_needs': ['Defensive Back', 'Linebacker']},
            'Buffalo Bills': {'primary_needs': ['Defensive Line', 'Wide Receiver'], 'secondary_needs': ['Offensive Line', 'Running Back']},
            'Carolina Panthers': {'primary_needs': ['Quarterback', 'Offensive Line'], 'secondary_needs': ['Defensive Line', 'Wide Receiver']},
            'Chicago Bears': {'primary_needs': ['Offensive Line', 'Wide Receiver'], 'secondary_needs': ['Defensive Back', 'Tight End']},
            'Cincinnati Bengals': {'primary_needs': ['Defensive Line', 'Offensive Line'], 'secondary_needs': ['Linebacker', 'Running Back']},
            'Cleveland Browns': {'primary_needs': ['Wide Receiver', 'Defensive Back'], 'secondary_needs': ['Offensive Line', 'Tight End']},
            'Dallas Cowboys': {'primary_needs': ['Defensive Line', 'Running Back'], 'secondary_needs': ['Linebacker', 'Offensive Line']},
            'Denver Broncos': {'primary_needs': ['Offensive Line', 'Wide Receiver'], 'secondary_needs': ['Defensive Line', 'Linebacker']},
            'Detroit Lions': {'primary_needs': ['Defensive Back', 'Linebacker'], 'secondary_needs': ['Offensive Line', 'Defensive Line']},
            'Green Bay Packers': {'primary_needs': ['Defensive Line', 'Linebacker'], 'secondary_needs': ['Wide Receiver', 'Offensive Line']},
            'Houston Texans': {'primary_needs': ['Defensive Back', 'Wide Receiver'], 'secondary_needs': ['Offensive Line', 'Linebacker']},
            'Indianapolis Colts': {'primary_needs': ['Defensive Line', 'Wide Receiver'], 'secondary_needs': ['Offensive Line', 'Defensive Back']},
            'Jacksonville Jaguars': {'primary_needs': ['Offensive Line', 'Linebacker'], 'secondary_needs': ['Wide Receiver', 'Defensive Line']},
            'Kansas City Chiefs': {'primary_needs': ['Defensive Line', 'Wide Receiver'], 'secondary_needs': ['Offensive Line', 'Linebacker']},
            'Las Vegas Raiders': {'primary_needs': ['Quarterback', 'Defensive Line'], 'secondary_needs': ['Offensive Line', 'Linebacker']},
            'Los Angeles Chargers': {'primary_needs': ['Offensive Line', 'Linebacker'], 'secondary_needs': ['Wide Receiver', 'Defensive Line']},
            'Los Angeles Rams': {'primary_needs': ['Offensive Line', 'Linebacker'], 'secondary_needs': ['Wide Receiver', 'Defensive Back']},
            'Miami Dolphins': {'primary_needs': ['Offensive Line', 'Linebacker'], 'secondary_needs': ['Running Back', 'Defensive Line']},
            'Minnesota Vikings': {'primary_needs': ['Quarterback', 'Defensive Line'], 'secondary_needs': ['Offensive Line', 'Linebacker']},
            'New England Patriots': {'primary_needs': ['Quarterback', 'Wide Receiver'], 'secondary_needs': ['Offensive Line', 'Defensive Back']},
            'New Orleans Saints': {'primary_needs': ['Quarterback', 'Offensive Line'], 'secondary_needs': ['Wide Receiver', 'Linebacker']},
            'New York Giants': {'primary_needs': ['Quarterback', 'Offensive Line'], 'secondary_needs': ['Wide Receiver', 'Defensive Line']},
            'New York Jets': {'primary_needs': ['Offensive Line', 'Wide Receiver'], 'secondary_needs': ['Defensive Back', 'Linebacker']},
            'Philadelphia Eagles': {'primary_needs': ['Wide Receiver', 'Defensive Back'], 'secondary_needs': ['Linebacker', 'Offensive Line']},
            'Pittsburgh Steelers': {'primary_needs': ['Quarterback', 'Offensive Line'], 'secondary_needs': ['Wide Receiver', 'Defensive Back']},
            'San Francisco 49ers': {'primary_needs': ['Wide Receiver', 'Defensive Back'], 'secondary_needs': ['Offensive Line', 'Linebacker']},
            'Seattle Seahawks': {'primary_needs': ['Offensive Line', 'Linebacker'], 'secondary_needs': ['Defensive Line', 'Wide Receiver']},
            'Tampa Bay Buccaneers': {'primary_needs': ['Quarterback', 'Offensive Line'], 'secondary_needs': ['Wide Receiver', 'Defensive Back']},
            'Tennessee Titans': {'primary_needs': ['Quarterback', 'Wide Receiver'], 'secondary_needs': ['Offensive Line', 'Defensive Line']},
            'Washington Commanders': {'primary_needs': ['Quarterback', 'Wide Receiver'], 'secondary_needs': ['Offensive Line', 'Linebacker']}
        }
        
        # Position value tiers for different team strategies
        self.position_value_tiers = {
            'Premium': ['Quarterback', 'Defensive Back', 'Wide Receiver'],
            'High Value': ['Offensive Line', 'Defensive Line', 'Linebacker'],
            'Skill Position': ['Running Back', 'Tight End'],
            'Specialist': ['Special Teams']
        }
    
    def render(self):
        """Render the team analysis interface."""
        st.markdown("## 🏈 Team Analysis & Fit Evaluation")
        
        if 'position_group' not in self.data.columns:
            st.error("Position group information required for team analysis.")
            return
        
        # Main analysis tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🎯 Team Fit Analysis", 
            "📊 Positional Value", 
            "🔄 Team Needs Matrix", 
            "💎 Value Opportunities",
            "📈 Draft Strategy"
        ])
        
        with tab1:
            self._render_team_fit_analysis()
        
        with tab2:
            self._render_positional_value()
        
        with tab3:
            self._render_team_needs_matrix()
        
        with tab4:
            self._render_value_opportunities()
        
        with tab5:
            self._render_draft_strategy()
    
    def _render_team_fit_analysis(self):
        """Render team fit analysis."""
        st.markdown("### 🎯 Team Fit Analysis")
        
        # Team selection
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_team = st.selectbox(
                "Select NFL Team for Analysis",
                sorted(self.nfl_teams.keys())
            )
        
        with col2:
            # Analysis depth
            analysis_depth = st.selectbox(
                "Analysis Depth",
                ["Top 50 Players", "Top 100 Players", "All Players"]
            )
            
            if analysis_depth == "Top 50 Players":
                analysis_data = self.data.nlargest(50, 'grade')
            elif analysis_depth == "Top 100 Players":
                analysis_data = self.data.nlargest(100, 'grade')
            else:
                analysis_data = self.data
        
        # Get team needs
        team_needs = self.nfl_teams[selected_team]
        primary_needs = team_needs['primary_needs']
        secondary_needs = team_needs['secondary_needs']
        
        # Team fit scoring
        fit_scores = self._calculate_team_fit_scores(analysis_data, primary_needs, secondary_needs)
        
        # Display team needs
        st.markdown("#### 📋 Team Needs Assessment")
        
        need_col1, need_col2 = st.columns(2)
        
        with need_col1:
            st.markdown("##### 🔴 Primary Needs")
            for need in primary_needs:
                st.markdown(f"• **{need}**")
        
        with need_col2:
            st.markdown("##### 🟡 Secondary Needs")
            for need in secondary_needs:
                st.markdown(f"• **{need}**")
        
        # Top fits for this team
        st.markdown("#### 🌟 Best Fits for Team")
        
        if not fit_scores.empty:
            top_fits = fit_scores.head(20)
            
            # Fit score visualization
            fig_fit = px.bar(
                top_fits,
                x='team_fit_score',
                y='name',
                orientation='h',
                title=f"Top 20 Player Fits for {selected_team}",
                color='team_fit_score',
                color_continuous_scale='RdYlGn',
                hover_data=['position_group', 'grade', 'need_priority']
            )
            
            fig_fit.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_title="Team Fit Score",
                yaxis_title="Player",
                height=600
            )
            
            st.plotly_chart(fig_fit, use_container_width=True)
            
            # Detailed fit table
            display_cols = ['name', 'position_group', 'grade', 'team_fit_score', 'need_priority', 'value_score']
            if 'college' in top_fits.columns:
                display_cols.insert(2, 'college')
            
            st.dataframe(
                top_fits[display_cols].round(2),
                use_container_width=True,
                hide_index=True
            )
        
        # Position group analysis for team
        st.markdown("#### 📊 Available Players by Team Needs")
        
        needs_analysis = []
        all_needs = primary_needs + secondary_needs
        
        for need in all_needs:
            need_players = analysis_data[analysis_data['position_group'] == need]
            
            if len(need_players) > 0:
                needs_analysis.append({
                    'Position Group': need,
                    'Priority': 'Primary' if need in primary_needs else 'Secondary',
                    'Available Players': len(need_players),
                    'Top Grade': need_players['grade'].max(),
                    'Avg Grade': need_players['grade'].mean(),
                    'Top Player': need_players.loc[need_players['grade'].idxmax(), 'name']
                })
        
        if needs_analysis:
            needs_df = pd.DataFrame(needs_analysis)
            
            # Needs summary chart
            fig_needs = px.bar(
                needs_df,
                x='Position Group',
                y='Available Players',
                color='Priority',
                title="Available Players by Team Need Priority",
                color_discrete_map={'Primary': self.colors['danger'], 'Secondary': self.colors['warning']}
            )
            
            fig_needs.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_needs, use_container_width=True)
            
            st.dataframe(needs_df.round(2), use_container_width=True, hide_index=True)
    
    def _calculate_team_fit_scores(self, data: pd.DataFrame, primary_needs: List, secondary_needs: List) -> pd.DataFrame:
        """Calculate team fit scores for players."""
        scored_data = data.copy()
        
        # Initialize scores
        scored_data['need_priority'] = 'Not a Need'
        scored_data['need_multiplier'] = 1.0
        scored_data['team_fit_score'] = 0.0
        scored_data['value_score'] = 0.0
        
        # Assign need priorities and multipliers
        primary_mask = scored_data['position_group'].isin(primary_needs)
        secondary_mask = scored_data['position_group'].isin(secondary_needs)
        
        scored_data.loc[primary_mask, 'need_priority'] = 'Primary Need'
        scored_data.loc[primary_mask, 'need_multiplier'] = 2.0
        
        scored_data.loc[secondary_mask, 'need_priority'] = 'Secondary Need'
        scored_data.loc[secondary_mask, 'need_multiplier'] = 1.5
        
        # Calculate team fit score (grade * need multiplier)
        scored_data['team_fit_score'] = scored_data['grade'] * scored_data['need_multiplier']
        
        # Calculate value score (considering both grade and need)
        max_grade = scored_data['grade'].max()
        scored_data['value_score'] = (scored_data['grade'] / max_grade) * scored_data['need_multiplier'] * 100
        
        return scored_data.sort_values('team_fit_score', ascending=False)
    
    def _render_positional_value(self):
        """Render positional value analysis."""
        st.markdown("### 📊 Positional Value Analysis")
        
        # Overall positional value
        col1, col2 = st.columns(2)
        
        with col1:
            # Average grade by position
            if 'position_group' in self.data.columns:
                pos_value = self.data.groupby('position_group').agg({
                    'grade': ['count', 'mean', 'std', 'max'],
                    'name': 'count'
                }).round(2)
                
                pos_value.columns = ['Player Count', 'Avg Grade', 'Grade Std Dev', 'Max Grade', 'Total Players']
                pos_value = pos_value[['Player Count', 'Avg Grade', 'Grade Std Dev', 'Max Grade']]
                pos_value = pos_value.sort_values('Avg Grade', ascending=False)
                
                fig_pos_value = px.bar(
                    x=pos_value.index,
                    y=pos_value['Avg Grade'],
                    title="Average Grade by Position Group",
                    color=pos_value['Avg Grade'],
                    color_continuous_scale='Viridis'
                )
                
                fig_pos_value.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis_title="Position Group",
                    yaxis_title="Average Grade"
                )
                
                st.plotly_chart(fig_pos_value, use_container_width=True)
        
        with col2:
            # Position depth analysis
            depth_analysis = []
            
            for pos_group in self.data['position_group'].unique():
                if pd.notna(pos_group):
                    pos_data = self.data[self.data['position_group'] == pos_group]
                    
                    # Calculate depth metrics
                    top_tier = len(pos_data[pos_data['grade'] >= pos_data['grade'].quantile(0.8)])
                    mid_tier = len(pos_data[(pos_data['grade'] >= pos_data['grade'].quantile(0.4)) & 
                                           (pos_data['grade'] < pos_data['grade'].quantile(0.8))])
                    low_tier = len(pos_data[pos_data['grade'] < pos_data['grade'].quantile(0.4)])
                    
                    depth_analysis.append({
                        'Position': pos_group,
                        'Top Tier': top_tier,
                        'Mid Tier': mid_tier,
                        'Low Tier': low_tier,
                        'Total': len(pos_data),
                        'Depth Score': (top_tier * 3 + mid_tier * 2 + low_tier) / len(pos_data)
                    })
            
            depth_df = pd.DataFrame(depth_analysis).sort_values('Depth Score', ascending=False)
            
            fig_depth = px.bar(
                depth_df,
                x='Position',
                y=['Top Tier', 'Mid Tier', 'Low Tier'],
                title="Position Depth Analysis",
                color_discrete_sequence=[self.colors['success'], self.colors['warning'], self.colors['danger']]
            )
            
            fig_depth.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_title="Position Group",
                yaxis_title="Number of Players"
            )
            
            st.plotly_chart(fig_depth, use_container_width=True)
        
        # Position value tables
        st.markdown("#### 📋 Detailed Position Analysis")
        
        tab_premium, tab_high, tab_skill, tab_specialist = st.tabs([
            "Premium Positions", "High Value", "Skill Positions", "Specialists"
        ])
        
        with tab_premium:
            self._render_position_tier_analysis('Premium')
        
        with tab_high:
            self._render_position_tier_analysis('High Value')
        
        with tab_skill:
            self._render_position_tier_analysis('Skill Position')
        
        with tab_specialist:
            self._render_position_tier_analysis('Specialist')
    
    def _render_position_tier_analysis(self, tier: str):
        """Render analysis for a specific position tier."""
        tier_positions = self.position_value_tiers[tier]
        tier_data = self.data[self.data['position_group'].isin(tier_positions)]
        
        if len(tier_data) == 0:
            st.warning(f"No players found in {tier} positions.")
            return
        
        # Tier summary
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Players", len(tier_data))
        
        with col2:
            avg_grade = tier_data['grade'].mean()
            st.metric("Average Grade", f"{avg_grade:.2f}")
        
        with col3:
            top_grade = tier_data['grade'].max()
            st.metric("Top Grade", f"{top_grade:.2f}")
        
        with col4:
            positions = tier_data['position_group'].nunique()
            st.metric("Position Groups", positions)
        
        # Top players in tier
        top_tier_players = tier_data.nlargest(15, 'grade')
        
        display_cols = ['name', 'position_group', 'grade']
        if 'college' in top_tier_players.columns:
            display_cols.insert(2, 'college')
        
        st.markdown(f"##### 🌟 Top {tier} Players")
        st.dataframe(
            top_tier_players[display_cols].round(2),
            use_container_width=True,
            hide_index=True
        )
    
    def _render_team_needs_matrix(self):
        """Render team needs matrix analysis."""
        st.markdown("### 🔄 Team Needs Matrix")
        
        # Create needs matrix
        needs_matrix = []
        
        for team, needs_info in self.nfl_teams.items():
            team_row = {'Team': team}
            
            # Initialize all positions as 0
            for pos_group in self.data['position_group'].unique():
                if pd.notna(pos_group):
                    team_row[pos_group] = 0
            
            # Set primary needs as 2, secondary as 1
            for need in needs_info['primary_needs']:
                if need in team_row:
                    team_row[need] = 2
            
            for need in needs_info['secondary_needs']:
                if need in team_row:
                    team_row[need] = 1
            
            needs_matrix.append(team_row)
        
        needs_df = pd.DataFrame(needs_matrix).set_index('Team')
        
        # Heatmap of team needs
        fig_heatmap = px.imshow(
            needs_df.values,
            x=needs_df.columns,
            y=needs_df.index,
            color_continuous_scale='RdYlGn',
            title="Team Needs Matrix (2=Primary, 1=Secondary, 0=No Need)",
            aspect='auto'
        )
        
        fig_heatmap.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=800
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Position demand analysis
        st.markdown("#### 📈 Position Demand Across League")
        
        position_demand = {}
        for pos in needs_df.columns:
            primary_demand = (needs_df[pos] == 2).sum()
            secondary_demand = (needs_df[pos] == 1).sum()
            total_demand = primary_demand * 2 + secondary_demand
            
            position_demand[pos] = {
                'Primary Needs': primary_demand,
                'Secondary Needs': secondary_demand,
                'Total Demand Score': total_demand,
                'Available Players': len(self.data[self.data['position_group'] == pos])
            }
        
        demand_df = pd.DataFrame(position_demand).T.sort_values('Total Demand Score', ascending=False)
        
        # Demand vs supply chart
        fig_supply_demand = go.Figure()
        
        fig_supply_demand.add_trace(go.Bar(
            name='Total Demand Score',
            x=demand_df.index,
            y=demand_df['Total Demand Score'],
            yaxis='y',
            marker_color=self.colors['primary']
        ))
        
        fig_supply_demand.add_trace(go.Scatter(
            name='Available Players',
            x=demand_df.index,
            y=demand_df['Available Players'],
            yaxis='y2',
            mode='lines+markers',
            line=dict(color=self.colors['secondary'], width=3),
            marker=dict(size=8)
        ))
        
        fig_supply_demand.update_layout(
            title='Position Demand vs Available Players',
            xaxis_title='Position Group',
            yaxis=dict(title='Demand Score', side='left'),
            yaxis2=dict(title='Available Players', side='right', overlaying='y'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_supply_demand, use_container_width=True)
        
        st.dataframe(demand_df.round(2), use_container_width=True)
    
    def _render_value_opportunities(self):
        """Render value opportunities analysis."""
        st.markdown("### 💎 Value Opportunities")
        
        # Calculate value opportunities based on supply/demand
        opportunities = []
        
        for pos_group in self.data['position_group'].unique():
            if pd.notna(pos_group):
                pos_data = self.data[self.data['position_group'] == pos_group]
                
                if len(pos_data) > 0:
                    # Calculate demand score
                    primary_needs = sum(1 for team_data in self.nfl_teams.values() 
                                      if pos_group in team_data['primary_needs'])
                    secondary_needs = sum(1 for team_data in self.nfl_teams.values() 
                                        if pos_group in team_data['secondary_needs'])
                    demand_score = primary_needs * 2 + secondary_needs
                    
                    # Calculate supply metrics
                    supply_count = len(pos_data)
                    avg_grade = pos_data['grade'].mean()
                    top_grade = pos_data['grade'].max()
                    
                    # Value opportunity score (high demand, limited quality supply = high opportunity)
                    if supply_count > 0:
                        opportunity_score = (demand_score * avg_grade) / supply_count
                    else:
                        opportunity_score = 0
                    
                    opportunities.append({
                        'Position Group': pos_group,
                        'Demand Score': demand_score,
                        'Available Players': supply_count,
                        'Avg Grade': avg_grade,
                        'Top Grade': top_grade,
                        'Opportunity Score': opportunity_score,
                        'Value Rating': self._get_value_rating(demand_score, supply_count, avg_grade)
                    })
        
        opp_df = pd.DataFrame(opportunities).sort_values('Opportunity Score', ascending=False)
        
        # Opportunity visualization
        col1, col2 = st.columns(2)
        
        with col1:
            # Opportunity score chart
            fig_opp = px.bar(
                opp_df.head(10),
                x='Position Group',
                y='Opportunity Score',
                title="Top Value Opportunities",
                color='Opportunity Score',
                color_continuous_scale='Plasma'
            )
            
            fig_opp.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_opp, use_container_width=True)
        
        with col2:
            # Value rating distribution
            rating_counts = opp_df['Value Rating'].value_counts()
            
            fig_rating = px.pie(
                values=rating_counts.values,
                names=rating_counts.index,
                title="Value Rating Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig_rating.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_rating, use_container_width=True)
        
        # Detailed opportunities table
        st.markdown("#### 📊 Detailed Value Analysis")
        st.dataframe(opp_df.round(2), use_container_width=True, hide_index=True)
        
        # Specific player recommendations
        st.markdown("#### 🎯 High-Value Player Recommendations")
        
        # Get high-value players from top opportunity positions
        top_opp_positions = opp_df.head(5)['Position Group'].tolist()
        
        for pos in top_opp_positions:
            pos_players = self.data[self.data['position_group'] == pos].nlargest(5, 'grade')
            
            if len(pos_players) > 0:
                with st.expander(f"🏆 Top {pos} Prospects"):
                    display_cols = ['name', 'grade']
                    if 'college' in pos_players.columns:
                        display_cols.insert(1, 'college')
                    
                    st.dataframe(
                        pos_players[display_cols].round(2),
                        use_container_width=True,
                        hide_index=True
                    )
    
    def _get_value_rating(self, demand_score: float, supply_count: int, avg_grade: float) -> str:
        """Calculate value rating based on supply/demand dynamics."""
        if demand_score >= 10 and supply_count <= 15 and avg_grade >= 7.0:
            return "Exceptional Value"
        elif demand_score >= 8 and supply_count <= 20 and avg_grade >= 6.5:
            return "High Value"
        elif demand_score >= 6 and supply_count <= 25 and avg_grade >= 6.0:
            return "Good Value"
        elif demand_score >= 4 and supply_count <= 30:
            return "Moderate Value"
        else:
            return "Limited Value"
    
    def _render_draft_strategy(self):
        """Render draft strategy recommendations."""
        st.markdown("### 📈 Draft Strategy Recommendations")
        
        # Strategy selection
        strategy_type = st.selectbox(
            "Select Draft Strategy Focus",
            ["Best Player Available", "Team Needs", "Value-Based", "Position Scarcity"]
        )
        
        if strategy_type == "Best Player Available":
            self._render_bpa_strategy()
        elif strategy_type == "Team Needs":
            self._render_needs_strategy()
        elif strategy_type == "Value-Based":
            self._render_value_strategy()
        else:
            self._render_scarcity_strategy()
    
    def _render_bpa_strategy(self):
        """Render Best Player Available strategy."""
        st.markdown("#### 🏆 Best Player Available Strategy")
        
        st.markdown("""
        **Philosophy:** Draft the highest-graded player regardless of position or need.
        
        **Advantages:**
        - Maximizes talent acquisition
        - Builds depth across roster
        - Takes advantage of unexpected value
        
        **Considerations:**
        - May not address immediate needs
        - Could create positional imbalances
        """)
        
        # Top BPA candidates by round equivalent
        bpa_rounds = {
            "Round 1 Talent (Grades 8.0+)": self.data[self.data['grade'] >= 8.0],
            "Round 2-3 Talent (Grades 7.0-7.9)": self.data[(self.data['grade'] >= 7.0) & (self.data['grade'] < 8.0)],
            "Round 4-7 Talent (Grades 6.0-6.9)": self.data[(self.data['grade'] >= 6.0) & (self.data['grade'] < 7.0)]
        }
        
        for round_name, round_data in bpa_rounds.items():
            if len(round_data) > 0:
                with st.expander(f"📋 {round_name} ({len(round_data)} players)"):
                    top_players = round_data.nlargest(15, 'grade')
                    
                    display_cols = ['name', 'position_group', 'grade']
                    if 'college' in top_players.columns:
                        display_cols.insert(2, 'college')
                    
                    st.dataframe(
                        top_players[display_cols].round(2),
                        use_container_width=True,
                        hide_index=True
                    )
    
    def _render_needs_strategy(self):
        """Render team needs-based strategy."""
        st.markdown("#### 🎯 Team Needs Strategy")
        
        # Team selection for needs analysis
        selected_team = st.selectbox(
            "Select Team for Needs-Based Strategy",
            sorted(self.nfl_teams.keys()),
            key="needs_team"
        )
        
        team_needs = self.nfl_teams[selected_team]
        
        st.markdown(f"""
        **Strategy for {selected_team}:**
        
        **Primary Needs:** {', '.join(team_needs['primary_needs'])}
        
        **Secondary Needs:** {', '.join(team_needs['secondary_needs'])}
        """)
        
        # Needs-based recommendations
        for i, need in enumerate(team_needs['primary_needs']):
            need_players = self.data[self.data['position_group'] == need].nlargest(10, 'grade')
            
            if len(need_players) > 0:
                st.markdown(f"##### 🔴 Primary Need: {need}")
                
                display_cols = ['name', 'grade']
                if 'college' in need_players.columns:
                    display_cols.insert(1, 'college')
                
                st.dataframe(
                    need_players[display_cols].round(2),
                    use_container_width=True,
                    hide_index=True
                )
    
    def _render_value_strategy(self):
        """Render value-based strategy."""
        st.markdown("#### 💰 Value-Based Strategy")
        
        st.markdown("""
        **Philosophy:** Target players who provide the best combination of talent and positional value.
        
        **Key Metrics:**
        - Player grade relative to position
        - Positional scarcity
        - Team need multiplier
        """)
        
        # Calculate value scores
        value_analysis = []
        
        for _, player in self.data.iterrows():
            pos_group = player['position_group']
            player_grade = player['grade']
            
            # Position average and scarcity
            pos_data = self.data[self.data['position_group'] == pos_group]
            pos_avg = pos_data['grade'].mean()
            pos_count = len(pos_data)
            
            # Value metrics
            grade_diff = player_grade - pos_avg
            scarcity_bonus = max(0, (50 - pos_count) / 50)  # Bonus for scarce positions
            
            value_score = player_grade + grade_diff + scarcity_bonus
            
            value_analysis.append({
                'name': player['name'],
                'position_group': pos_group,
                'grade': player_grade,
                'position_avg': pos_avg,
                'grade_diff': grade_diff,
                'scarcity_bonus': scarcity_bonus,
                'value_score': value_score
            })
        
        value_df = pd.DataFrame(value_analysis).sort_values('value_score', ascending=False)
        
        # Top value picks
        st.markdown("#### 🎯 Top Value Selections")
        
        top_value = value_df.head(25)
        
        display_cols = ['name', 'position_group', 'grade', 'value_score', 'grade_diff', 'scarcity_bonus']
        st.dataframe(
            top_value[display_cols].round(3),
            use_container_width=True,
            hide_index=True
        )
    
    def _render_scarcity_strategy(self):
        """Render position scarcity strategy."""
        st.markdown("#### 🔒 Position Scarcity Strategy")
        
        st.markdown("""
        **Philosophy:** Prioritize positions with limited high-quality depth in the draft class.
        
        **Focus Areas:**
        - Positions with few elite prospects
        - High-demand positions
        - Premium positions with depth concerns
        """)
        
        # Calculate scarcity metrics
        scarcity_analysis = []
        
        for pos_group in self.data['position_group'].unique():
            if pd.notna(pos_group):
                pos_data = self.data[self.data['position_group'] == pos_group]
                
                if len(pos_data) > 0:
                    # Scarcity metrics
                    total_players = len(pos_data)
                    elite_players = len(pos_data[pos_data['grade'] >= 7.5])
                    solid_players = len(pos_data[pos_data['grade'] >= 6.5])
                    
                    # Demand calculation
                    primary_needs = sum(1 for team_data in self.nfl_teams.values() 
                                      if pos_group in team_data['primary_needs'])
                    
                    # Scarcity score
                    if total_players > 0:
                        elite_ratio = elite_players / total_players
                        demand_ratio = primary_needs / 32  # 32 teams
                        scarcity_score = (demand_ratio * 100) / max(elite_ratio * 100, 1)
                    else:
                        scarcity_score = 0
                    
                    scarcity_analysis.append({
                        'Position Group': pos_group,
                        'Total Players': total_players,
                        'Elite Players': elite_players,
                        'Solid Players': solid_players,
                        'Teams with Primary Need': primary_needs,
                        'Scarcity Score': scarcity_score
                    })
        
        scarcity_df = pd.DataFrame(scarcity_analysis).sort_values('Scarcity Score', ascending=False)
        
        # Scarcity visualization
        fig_scarcity = px.bar(
            scarcity_df.head(10),
            x='Position Group',
            y='Scarcity Score',
            title="Position Scarcity Rankings",
            color='Scarcity Score',
            color_continuous_scale='Reds'
        )
        
        fig_scarcity.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_scarcity, use_container_width=True)
        
        # Scarcity table
        st.dataframe(scarcity_df.round(2), use_container_width=True, hide_index=True)
        
        # Scarcity-based recommendations
        st.markdown("#### 🚨 Scarcity Alerts")
        
        high_scarcity = scarcity_df[scarcity_df['Scarcity Score'] >= scarcity_df['Scarcity Score'].quantile(0.7)]
        
        for _, pos_info in high_scarcity.iterrows():
            pos_group = pos_info['Position Group']
            pos_players = self.data[self.data['position_group'] == pos_group].nlargest(5, 'grade')
            
            if len(pos_players) > 0:
                with st.expander(f"⚠️ {pos_group} - High Scarcity Alert"):
                    st.markdown(f"""
                    **Scarcity Score:** {pos_info['Scarcity Score']:.1f}
                    
                    **Available Elite Players:** {pos_info['Elite Players']}
                    
                    **Teams with Primary Need:** {pos_info['Teams with Primary Need']}
                    """)
                    
                    display_cols = ['name', 'grade']
                    if 'college' in pos_players.columns:
                        display_cols.insert(1, 'college')
                    
                    st.dataframe(
                        pos_players[display_cols].round(2),
                        use_container_width=True,
                        hide_index=True
                    )
