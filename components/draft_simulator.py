import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from typing import List, Dict
import random

class DraftSimulator:
    """NFL Draft simulation component."""
    
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
        
        # NFL teams for simulation
        self.nfl_teams = [
            'Arizona Cardinals', 'Atlanta Falcons', 'Baltimore Ravens', 'Buffalo Bills',
            'Carolina Panthers', 'Chicago Bears', 'Cincinnati Bengals', 'Cleveland Browns',
            'Dallas Cowboys', 'Denver Broncos', 'Detroit Lions', 'Green Bay Packers',
            'Houston Texans', 'Indianapolis Colts', 'Jacksonville Jaguars', 'Kansas City Chiefs',
            'Las Vegas Raiders', 'Los Angeles Chargers', 'Los Angeles Rams', 'Miami Dolphins',
            'Minnesota Vikings', 'New England Patriots', 'New Orleans Saints', 'New York Giants',
            'New York Jets', 'Philadelphia Eagles', 'Pittsburgh Steelers', 'San Francisco 49ers',
            'Seattle Seahawks', 'Tampa Bay Buccaneers', 'Tennessee Titans', 'Washington Commanders'
        ]
        
        # Position needs (simplified for simulation)
        self.position_needs = {
            'Quarterback': 0.1,
            'Running Back': 0.15,
            'Wide Receiver': 0.2,
            'Tight End': 0.1,
            'Offensive Line': 0.2,
            'Defensive Line': 0.15,
            'Linebacker': 0.15,
            'Defensive Back': 0.2,
            'Special Teams': 0.05
        }
    
    def render(self):
        """Render the draft simulator interface."""
        st.markdown("## 🏈 NFL Draft Simulator")
        
        if 'grade' not in self.data.columns:
            st.error("Grade column required for draft simulation.")
            return
        
        # Simulation configuration
        col1, col2 = st.columns([3, 1])
        
        with col2:
            st.markdown("### Simulation Settings")
            
            # Draft rounds
            num_rounds = st.slider("Number of Rounds", 1, 7, 3)
            
            # Simulation type
            sim_type = st.selectbox(
                "Simulation Type",
                ["Best Available", "Positional Needs", "Mixed Strategy"]
            )
            
            # Number of simulations
            num_sims = st.selectbox("Number of Simulations", [1, 5, 10, 25])
            
            # Position weights (if using positional needs)
            if sim_type in ["Positional Needs", "Mixed Strategy"]:
                st.markdown("#### Position Weights")
                position_weights = {}
                
                if 'position_group' in self.data.columns:
                    for pos in self.data['position_group'].unique():
                        if pd.notna(pos):
                            default_weight = self.position_needs.get(pos, 0.1)
                            position_weights[pos] = st.slider(
                                f"{pos}", 0.0, 1.0, default_weight, 0.05
                            )
            
            # Run simulation button
            run_simulation = st.button("🚀 Run Simulation", type="primary")
        
        with col1:
            if run_simulation:
                self._run_draft_simulation(num_rounds, sim_type, num_sims, position_weights if sim_type != "Best Available" else None)
            else:
                self._show_simulation_overview()
    
    def _show_simulation_overview(self):
        """Show simulation overview and available players."""
        st.markdown("### 📊 Draft Pool Overview")
        
        # Key statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_players = len(self.data)
            st.metric("Total Players", total_players)
        
        with col2:
            if 'position_group' in self.data.columns:
                position_groups = self.data['position_group'].nunique()
                st.metric("Position Groups", position_groups)
        
        with col3:
            avg_grade = self.data['grade'].mean()
            st.metric("Average Grade", f"{avg_grade:.2f}")
        
        with col4:
            top_grade = self.data['grade'].max()
            st.metric("Top Grade", f"{top_grade:.2f}")
        
        # Grade distribution
        fig_grade_dist = px.histogram(
            self.data,
            x='grade',
            nbins=30,
            title="Grade Distribution of Available Players",
            color_discrete_sequence=[self.colors['primary']]
        )
        
        fig_grade_dist.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis_title="Grade",
            yaxis_title="Number of Players"
        )
        
        st.plotly_chart(fig_grade_dist, use_container_width=True)
        
        # Position breakdown
        if 'position_group' in self.data.columns:
            col_a, col_b = st.columns(2)
            
            with col_a:
                pos_counts = self.data['position_group'].value_counts()
                
                fig_pos = px.bar(
                    x=pos_counts.index,
                    y=pos_counts.values,
                    title="Players by Position Group",
                    color=pos_counts.values,
                    color_continuous_scale='Viridis'
                )
                
                fig_pos.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis_title="Position Group",
                    yaxis_title="Number of Players"
                )
                
                st.plotly_chart(fig_pos, use_container_width=True)
            
            with col_b:
                # Top prospects by position
                st.markdown("#### 🌟 Top Prospects by Position")
                
                selected_pos = st.selectbox(
                    "Select Position Group",
                    sorted(self.data['position_group'].unique())
                )
                
                pos_data = self.data[self.data['position_group'] == selected_pos]
                top_prospects = pos_data.nlargest(10, 'grade')
                
                display_cols = ['name', 'position', 'college', 'grade']
                if 'position' not in top_prospects.columns:
                    display_cols.remove('position')
                if 'college' not in top_prospects.columns:
                    display_cols.remove('college')
                
                st.dataframe(
                    top_prospects[display_cols].round(2),
                    use_container_width=True,
                    hide_index=True
                )
    
    def _run_draft_simulation(self, num_rounds: int, sim_type: str, num_sims: int, position_weights: Dict = None):
        """Run the draft simulation."""
        st.markdown("### 🎯 Simulation Results")
        
        # Prepare draft eligible players (top performers)
        eligible_players = self.data.nlargest(min(len(self.data), 32 * num_rounds), 'grade').copy()
        eligible_players = eligible_players.reset_index(drop=True)
        
        # Run multiple simulations
        all_results = []
        
        for sim_num in range(num_sims):
            simulation_result = self._simulate_single_draft(
                eligible_players, num_rounds, sim_type, position_weights
            )
            simulation_result['simulation'] = sim_num + 1
            all_results.append(simulation_result)
        
        # Combine results
        combined_results = pd.concat(all_results, ignore_index=True)
        
        # Display results
        if num_sims == 1:
            self._display_single_simulation(combined_results)
        else:
            self._display_multiple_simulations(combined_results, num_sims)
    
    def _simulate_single_draft(self, players: pd.DataFrame, num_rounds: int, sim_type: str, position_weights: Dict = None) -> pd.DataFrame:
        """Simulate a single draft."""
        available_players = players.copy()
        draft_results = []
        
        for round_num in range(1, num_rounds + 1):
            for pick_num in range(1, 33):  # 32 teams
                overall_pick = (round_num - 1) * 32 + pick_num
                team = self.nfl_teams[(pick_num - 1) % len(self.nfl_teams)]
                
                if len(available_players) == 0:
                    break
                
                # Select player based on strategy
                if sim_type == "Best Available":
                    selected_player = self._select_best_available(available_players)
                elif sim_type == "Positional Needs":
                    selected_player = self._select_by_position_need(available_players, position_weights)
                else:  # Mixed Strategy
                    if random.random() < 0.7:  # 70% best available, 30% positional need
                        selected_player = self._select_best_available(available_players)
                    else:
                        selected_player = self._select_by_position_need(available_players, position_weights)
                
                if selected_player is not None:
                    draft_results.append({
                        'round': round_num,
                        'pick': pick_num,
                        'overall': overall_pick,
                        'team': team,
                        'player': selected_player['name'],
                        'position': selected_player.get('position', 'Unknown'),
                        'position_group': selected_player.get('position_group', 'Unknown'),
                        'college': selected_player.get('college', 'Unknown'),
                        'grade': selected_player['grade']
                    })
                    
                    # Remove selected player
                    available_players = available_players[
                        available_players['name'] != selected_player['name']
                    ].reset_index(drop=True)
        
        return pd.DataFrame(draft_results)
    
    def _select_best_available(self, players: pd.DataFrame) -> Dict:
        """Select the best available player."""
        if len(players) == 0:
            return None
        
        best_player = players.iloc[0]  # Players should already be sorted by grade
        return best_player.to_dict()
    
    def _select_by_position_need(self, players: pd.DataFrame, position_weights: Dict) -> Dict:
        """Select player based on positional needs."""
        if len(players) == 0 or not position_weights:
            return self._select_best_available(players)
        
        # Calculate weighted scores
        players_copy = players.copy()
        players_copy['weighted_score'] = 0
        
        for pos_group, weight in position_weights.items():
            if 'position_group' in players_copy.columns:
                mask = players_copy['position_group'] == pos_group
                players_copy.loc[mask, 'weighted_score'] = players_copy.loc[mask, 'grade'] * (1 + weight)
            else:
                # Fallback to grade only
                players_copy['weighted_score'] = players_copy['grade']
        
        # Add some randomness to avoid always picking the same player
        randomness = np.random.normal(0, 0.1, len(players_copy))
        players_copy['final_score'] = players_copy['weighted_score'] + randomness
        
        best_player = players_copy.loc[players_copy['final_score'].idxmax()]
        return best_player.to_dict()
    
    def _display_single_simulation(self, results: pd.DataFrame):
        """Display results of a single simulation."""
        # Draft board
        st.markdown("#### 📋 Draft Board")
        
        # Format the results for display
        display_results = results.copy()
        display_results['Pick'] = display_results.apply(
            lambda row: f"R{row['round']} P{row['pick']} ({row['overall']})", axis=1
        )
        
        display_cols = ['Pick', 'team', 'player', 'position', 'college', 'grade']
        available_cols = [col for col in display_cols if col in display_results.columns]
        
        st.dataframe(
            display_results[available_cols].round(2),
            use_container_width=True,
            hide_index=True
        )
        
        # Analysis charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Draft by position
            if 'position_group' in results.columns:
                pos_counts = results['position_group'].value_counts()
                
                fig_pos = px.pie(
                    values=pos_counts.values,
                    names=pos_counts.index,
                    title="Draft Picks by Position Group",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                
                fig_pos.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                
                st.plotly_chart(fig_pos, use_container_width=True)
        
        with col2:
            # Grade by round
            avg_grade_by_round = results.groupby('round')['grade'].mean()
            
            fig_grade = px.bar(
                x=avg_grade_by_round.index,
                y=avg_grade_by_round.values,
                title="Average Grade by Round",
                color=avg_grade_by_round.values,
                color_continuous_scale='Viridis'
            )
            
            fig_grade.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_title="Round",
                yaxis_title="Average Grade"
            )
            
            st.plotly_chart(fig_grade, use_container_width=True)
        
        # Round-by-round breakdown
        st.markdown("#### 🔄 Round-by-Round Analysis")
        
        for round_num in sorted(results['round'].unique()):
            round_data = results[results['round'] == round_num]
            
            with st.expander(f"Round {round_num} ({len(round_data)} picks)"):
                round_stats = {
                    'Avg Grade': round_data['grade'].mean(),
                    'Best Pick': round_data.loc[round_data['grade'].idxmax(), 'player'],
                    'Top College': round_data['college'].value_counts().index[0] if 'college' in round_data.columns else 'N/A',
                    'Top Position': round_data['position_group'].value_counts().index[0] if 'position_group' in round_data.columns else 'N/A'
                }
                
                stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
                
                with stat_col1:
                    st.metric("Avg Grade", f"{round_stats['Avg Grade']:.2f}")
                with stat_col2:
                    st.metric("Best Pick", round_stats['Best Pick'])
                with stat_col3:
                    st.metric("Top College", round_stats['Top College'])
                with stat_col4:
                    st.metric("Top Position", round_stats['Top Position'])
                
                # Round picks table
                round_display = round_data[['pick', 'team', 'player', 'position', 'grade']].copy()
                st.dataframe(round_display.round(2), use_container_width=True, hide_index=True)
    
    def _display_multiple_simulations(self, results: pd.DataFrame, num_sims: int):
        """Display results of multiple simulations."""
        st.markdown(f"#### 📊 Analysis of {num_sims} Simulations")
        
        # Overall statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_picks = len(results)
            st.metric("Total Picks", total_picks)
        
        with col2:
            avg_grade = results['grade'].mean()
            st.metric("Avg Grade", f"{avg_grade:.2f}")
        
        with col3:
            unique_players = results['player'].nunique()
            st.metric("Unique Players Drafted", unique_players)
        
        with col4:
            if 'position_group' in results.columns:
                position_diversity = results['position_group'].nunique()
                st.metric("Position Groups", position_diversity)
        
        # Draft frequency analysis
        st.markdown("#### 📈 Draft Frequency Analysis")
        
        # Most frequently drafted players
        player_frequency = results['player'].value_counts().head(20)
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            fig_freq = px.bar(
                x=player_frequency.values,
                y=player_frequency.index,
                orientation='h',
                title="Most Frequently Drafted Players",
                color=player_frequency.values,
                color_continuous_scale='Plasma'
            )
            
            fig_freq.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_title="Times Drafted",
                yaxis_title="Player"
            )
            
            st.plotly_chart(fig_freq, use_container_width=True)
        
        with col_b:
            # Position frequency
            if 'position_group' in results.columns:
                pos_frequency = results['position_group'].value_counts()
                
                fig_pos_freq = px.pie(
                    values=pos_frequency.values,
                    names=pos_frequency.index,
                    title="Position Group Draft Frequency",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                
                fig_pos_freq.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                
                st.plotly_chart(fig_pos_freq, use_container_width=True)
        
        # Average draft position
        st.markdown("#### 📍 Average Draft Position")
        
        avg_draft_pos = results.groupby('player').agg({
            'overall': ['mean', 'std', 'count'],
            'grade': 'first'
        }).round(2)
        
        avg_draft_pos.columns = ['Avg Pick', 'Std Dev', 'Times Drafted', 'Grade']
        avg_draft_pos = avg_draft_pos[avg_draft_pos['Times Drafted'] >= max(1, num_sims * 0.2)]  # Show players drafted in at least 20% of sims
        avg_draft_pos = avg_draft_pos.sort_values('Avg Pick').head(30)
        
        st.dataframe(avg_draft_pos, use_container_width=True)
        
        # Round analysis
        st.markdown("#### 🔄 Round-by-Round Simulation Analysis")
        
        round_analysis = results.groupby(['round', 'simulation'])['grade'].mean().reset_index()
        
        fig_round_trends = px.box(
            round_analysis,
            x='round',
            y='grade',
            title="Grade Distribution by Round Across Simulations"
        )
        
        fig_round_trends.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis_title="Round",
            yaxis_title="Average Grade"
        )
        
        st.plotly_chart(fig_round_trends, use_container_width=True)
