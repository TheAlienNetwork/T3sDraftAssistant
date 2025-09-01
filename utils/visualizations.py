import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class Visualizations:
    """Advanced visualizations for NFL Draft analysis."""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.colors = {
            'primary': '#FF6B35',
            'secondary': '#4ECDC4',
            'accent': '#45B7D1',
            'success': '#96CEB4',
            'warning': '#FFEAA7',
            'danger': '#FF7675',
            'dark': '#2d3436'
        }
    
    def render_comprehensive_overview(self):
        """Render comprehensive overview dashboard."""
        st.markdown("### 📊 Comprehensive Overview")
        
        # Key metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            total_players = len(self.data)
            st.metric("Total Players", total_players)
        
        with col2:
            if 'position' in self.data.columns:
                unique_positions = self.data['position'].nunique()
                st.metric("Positions", unique_positions)
        
        with col3:
            if 'college' in self.data.columns:
                unique_colleges = self.data['college'].nunique()
                st.metric("Colleges", unique_colleges)
        
        with col4:
            if 'grade' in self.data.columns:
                avg_grade = self.data['grade'].mean()
                st.metric("Avg Grade", f"{avg_grade:.1f}")
        
        with col5:
            if 'grade' in self.data.columns:
                grade_std = self.data['grade'].std()
                st.metric("Grade Std Dev", f"{grade_std:.1f}")
        
        # Main visualizations
        row1_col1, row1_col2 = st.columns(2)
        
        with row1_col1:
            # Grade distribution
            if 'grade' in self.data.columns:
                fig_hist = px.histogram(
                    self.data,
                    x='grade',
                    nbins=20,
                    title="Grade Distribution",
                    color_discrete_sequence=[self.colors['primary']]
                )
                
                fig_hist.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis_title="Grade",
                    yaxis_title="Frequency"
                )
                
                st.plotly_chart(fig_hist, use_container_width=True)
        
        with row1_col2:
            # Position distribution
            if 'position_group' in self.data.columns:
                pos_counts = self.data['position_group'].value_counts()
                
                fig_pie = px.pie(
                    values=pos_counts.values,
                    names=pos_counts.index,
                    title="Position Group Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                
                fig_pie.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                
                st.plotly_chart(fig_pie, use_container_width=True)
        
        # Second row
        row2_col1, row2_col2 = st.columns(2)
        
        with row2_col1:
            # Top colleges
            if 'college' in self.data.columns:
                top_colleges = self.data['college'].value_counts().head(10)
                
                fig_college = px.bar(
                    x=top_colleges.values,
                    y=top_colleges.index,
                    orientation='h',
                    title="Top 10 Colleges by Player Count",
                    color=top_colleges.values,
                    color_continuous_scale='Viridis'
                )
                
                fig_college.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis_title="Number of Players",
                    yaxis_title="College"
                )
                
                st.plotly_chart(fig_college, use_container_width=True)
        
        with row2_col2:
            # Physical attributes scatter
            if 'height_inches' in self.data.columns and 'weight' in self.data.columns:
                fig_physical = px.scatter(
                    self.data,
                    x='height_inches',
                    y='weight',
                    color='position_group' if 'position_group' in self.data.columns else None,
                    title="Physical Attributes: Height vs Weight",
                    hover_data=['name'] if 'name' in self.data.columns else None
                )
                
                fig_physical.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis_title="Height (inches)",
                    yaxis_title="Weight (lbs)"
                )
                
                st.plotly_chart(fig_physical, use_container_width=True)
    
    def render_position_analysis(self):
        """Render position-specific analysis."""
        st.markdown("### 🏈 Position Analysis")
        
        if 'position' not in self.data.columns:
            st.error("Position column required for position analysis.")
            return
        
        # Position selector
        positions = sorted(self.data['position'].unique())
        selected_position = st.selectbox("Select Position for Analysis", positions)
        
        position_data = self.data[self.data['position'] == selected_position]
        
        if len(position_data) == 0:
            st.warning(f"No data available for {selected_position}")
            return
        
        # Position metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Players", len(position_data))
        
        with col2:
            if 'grade' in position_data.columns:
                avg_grade = position_data['grade'].mean()
                st.metric("Avg Grade", f"{avg_grade:.2f}")
        
        with col3:
            if 'height_inches' in position_data.columns:
                avg_height = position_data['height_inches'].mean()
                feet = int(avg_height // 12)
                inches = int(avg_height % 12)
                st.metric("Avg Height", f"{feet}'{inches}\"")
        
        with col4:
            if 'weight' in position_data.columns:
                avg_weight = position_data['weight'].mean()
                st.metric("Avg Weight", f"{avg_weight:.0f} lbs")
        
        # Position-specific visualizations
        row1_col1, row1_col2 = st.columns(2)
        
        with row1_col1:
            # Grade distribution for position
            if 'grade' in position_data.columns:
                fig_grade = px.histogram(
                    position_data,
                    x='grade',
                    nbins=15,
                    title=f"Grade Distribution - {selected_position}",
                    color_discrete_sequence=[self.colors['secondary']]
                )
                
                # Add vertical line for position average
                avg_grade = position_data['grade'].mean()
                fig_grade.add_vline(
                    x=avg_grade,
                    line_dash="dash",
                    line_color="white",
                    annotation_text=f"Avg: {avg_grade:.1f}"
                )
                
                fig_grade.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                
                st.plotly_chart(fig_grade, use_container_width=True)
        
        with row1_col2:
            # Top colleges for this position
            if 'college' in position_data.columns:
                top_colleges = position_data['college'].value_counts().head(8)
                
                fig_college = px.bar(
                    x=top_colleges.index,
                    y=top_colleges.values,
                    title=f"Top Colleges - {selected_position}",
                    color=top_colleges.values,
                    color_continuous_scale='Plasma'
                )
                
                fig_college.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis_title="College",
                    yaxis_title="Number of Players"
                )
                
                st.plotly_chart(fig_college, use_container_width=True)
        
        # Combine metrics analysis
        combine_cols = ['forty_time', 'bench_press', 'vertical', 'broad_jump', 'three_cone', 'shuttle']
        available_combine = [col for col in combine_cols if col in position_data.columns]
        
        if available_combine:
            st.markdown("#### 🏃‍♂️ Combine Performance Analysis")
            
            # Box plots for combine metrics
            fig_combine = make_subplots(
                rows=2, cols=3,
                subplot_titles=[col.replace('_', ' ').title() for col in available_combine[:6]]
            )
            
            for i, col in enumerate(available_combine[:6]):
                row = (i // 3) + 1
                col_pos = (i % 3) + 1
                
                fig_combine.add_trace(
                    go.Box(
                        y=position_data[col].dropna(),
                        name=col.replace('_', ' ').title(),
                        boxpoints='outliers',
                        marker_color=self.colors['accent']
                    ),
                    row=row, col=col_pos
                )
            
            fig_combine.update_layout(
                title=f"Combine Metrics Distribution - {selected_position}",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=False,
                height=600
            )
            
            st.plotly_chart(fig_combine, use_container_width=True)
        
        # Top performers table
        if 'grade' in position_data.columns:
            st.markdown("#### 🌟 Top Performers")
            
            top_performers = position_data.nlargest(10, 'grade')
            display_cols = ['name', 'college', 'grade']
            
            # Add available combine metrics
            for col in ['height_inches', 'weight', 'forty_time', 'vertical']:
                if col in top_performers.columns:
                    display_cols.append(col)
            
            st.dataframe(
                top_performers[display_cols].round(2),
                use_container_width=True
            )
    
    def render_combine_metrics(self):
        """Render combine metrics analysis."""
        st.markdown("### 🏃‍♂️ Combine Metrics Analysis")
        
        combine_cols = ['forty_time', 'bench_press', 'vertical', 'broad_jump', 'three_cone', 'shuttle']
        available_combine = [col for col in combine_cols if col in self.data.columns]
        
        if not available_combine:
            st.error("No combine metrics found in the data.")
            return
        
        # Metric selector
        selected_metrics = st.multiselect(
            "Select Combine Metrics for Analysis",
            available_combine,
            default=available_combine[:4] if len(available_combine) >= 4 else available_combine
        )
        
        if not selected_metrics:
            st.warning("Please select at least one combine metric.")
            return
        
        # Summary statistics
        st.markdown("#### 📊 Summary Statistics")
        
        summary_stats = self.data[selected_metrics].describe().round(3)
        st.dataframe(summary_stats, use_container_width=True)
        
        # Distribution plots
        st.markdown("#### 📈 Metric Distributions")
        
        cols_per_row = 2
        num_metrics = len(selected_metrics)
        num_rows = (num_metrics + cols_per_row - 1) // cols_per_row
        
        for row in range(num_rows):
            columns = st.columns(cols_per_row)
            
            for col_idx in range(cols_per_row):
                metric_idx = row * cols_per_row + col_idx
                if metric_idx < num_metrics:
                    metric = selected_metrics[metric_idx]
                    
                    with columns[col_idx]:
                        fig_dist = px.histogram(
                            self.data,
                            x=metric,
                            nbins=20,
                            title=f"{metric.replace('_', ' ').title()} Distribution",
                            color_discrete_sequence=[self.colors['accent']]
                        )
                        
                        # Add mean line
                        mean_val = self.data[metric].mean()
                        fig_dist.add_vline(
                            x=mean_val,
                            line_dash="dash",
                            line_color="white",
                            annotation_text=f"Mean: {mean_val:.2f}"
                        )
                        
                        fig_dist.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='white'),
                            height=400
                        )
                        
                        st.plotly_chart(fig_dist, use_container_width=True)
        
        # Position comparison
        if 'position_group' in self.data.columns:
            st.markdown("#### 🏈 Position Group Comparisons")
            
            selected_metric = st.selectbox(
                "Select Metric for Position Comparison",
                selected_metrics
            )
            
            # Box plot by position
            fig_box = px.box(
                self.data,
                x='position_group',
                y=selected_metric,
                title=f"{selected_metric.replace('_', ' ').title()} by Position Group",
                color='position_group',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig_box.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_title="Position Group",
                yaxis_title=selected_metric.replace('_', ' ').title()
            )
            
            st.plotly_chart(fig_box, use_container_width=True)
        
        # Performance percentiles
        st.markdown("#### 🎯 Performance Percentiles")
        
        percentiles = [10, 25, 50, 75, 90]
        percentile_data = []
        
        for metric in selected_metrics:
            metric_percentiles = self.data[metric].quantile([p/100 for p in percentiles])
            for i, p in enumerate(percentiles):
                percentile_data.append({
                    'Metric': metric.replace('_', ' ').title(),
                    'Percentile': f"{p}th",
                    'Value': metric_percentiles.iloc[i]
                })
        
        percentile_df = pd.DataFrame(percentile_data)
        percentile_pivot = percentile_df.pivot(index='Metric', columns='Percentile', values='Value')
        
        st.dataframe(percentile_pivot.round(3), use_container_width=True)
    
    def render_statistical_correlations(self):
        """Render statistical correlation analysis."""
        st.markdown("### 🔗 Statistical Correlations")
        
        # Get numeric columns
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) < 2:
            st.error("Need at least 2 numeric columns for correlation analysis.")
            return
        
        # Correlation matrix
        correlation_data = self.data[numeric_cols].corr()
        
        # Heatmap
        fig_heatmap = px.imshow(
            correlation_data.values,
            x=correlation_data.columns,
            y=correlation_data.index,
            color_continuous_scale='RdBu',
            aspect='auto',
            title="Correlation Matrix Heatmap",
            zmin=-1,
            zmax=1
        )
        
        fig_heatmap.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=600
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Strong correlations
        st.markdown("#### 🔍 Strong Correlations")
        
        strong_corr = []
        for i in range(len(correlation_data.columns)):
            for j in range(i+1, len(correlation_data.columns)):
                corr_val = correlation_data.iloc[i, j]
                if abs(corr_val) > 0.3:  # Threshold for "strong" correlation
                    strong_corr.append({
                        'Variable 1': correlation_data.columns[i],
                        'Variable 2': correlation_data.columns[j],
                        'Correlation': corr_val,
                        'Strength': 'Strong' if abs(corr_val) > 0.7 else 'Moderate'
                    })
        
        if strong_corr:
            strong_corr_df = pd.DataFrame(strong_corr).sort_values('Correlation', key=abs, ascending=False)
            st.dataframe(strong_corr_df.round(3), use_container_width=True)
        else:
            st.info("No strong correlations found (threshold: |r| > 0.3)")
        
        # Scatter plot for selected correlation
        if strong_corr:
            st.markdown("#### 📊 Correlation Visualization")
            
            col1, col2 = st.columns([3, 1])
            
            with col2:
                # Select variables for scatter plot
                var1 = st.selectbox("Select X Variable", numeric_cols)
                var2 = st.selectbox("Select Y Variable", [col for col in numeric_cols if col != var1])
            
            with col1:
                # Create scatter plot
                fig_scatter = px.scatter(
                    self.data,
                    x=var1,
                    y=var2,
                    color='position_group' if 'position_group' in self.data.columns else None,
                    title=f"Correlation: {var1.title()} vs {var2.title()}",
                    hover_data=['name'] if 'name' in self.data.columns else None,
                    trendline="ols"
                )
                
                # Calculate correlation
                corr_val = self.data[var1].corr(self.data[var2])
                
                fig_scatter.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    title=f"Correlation: {var1.title()} vs {var2.title()} (r = {corr_val:.3f})"
                )
                
                st.plotly_chart(fig_scatter, use_container_width=True)
    
    def render_performance_trends(self):
        """Render performance trends analysis."""
        st.markdown("### 📈 Performance Trends")
        
        if 'grade' not in self.data.columns:
            st.error("Grade column required for performance trends analysis.")
            return
        
        # Grade trends by position
        if 'position_group' in self.data.columns:
            st.markdown("#### 🏈 Performance by Position Group")
            
            position_stats = self.data.groupby('position_group')['grade'].agg([
                'count', 'mean', 'std', 'min', 'max'
            ]).round(2)
            
            position_stats.columns = ['Count', 'Mean Grade', 'Std Dev', 'Min Grade', 'Max Grade']
            st.dataframe(position_stats, use_container_width=True)
            
            # Position performance chart
            fig_pos = px.box(
                self.data,
                x='position_group',
                y='grade',
                title="Grade Distribution by Position Group",
                color='position_group',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig_pos.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_title="Position Group",
                yaxis_title="Grade"
            )
            
            st.plotly_chart(fig_pos, use_container_width=True)
        
        # College performance analysis
        if 'college' in self.data.columns:
            st.markdown("#### 🎓 College Performance Analysis")
            
            # Top colleges by average grade (minimum 3 players)
            college_stats = self.data.groupby('college').agg({
                'grade': ['count', 'mean', 'std']
            }).round(2)
            
            college_stats.columns = ['Player Count', 'Avg Grade', 'Grade Std Dev']
            
            # Filter colleges with at least 3 players
            top_colleges = college_stats[college_stats['Player Count'] >= 3].sort_values('Avg Grade', ascending=False).head(15)
            
            if not top_colleges.empty:
                fig_college = px.bar(
                    x=top_colleges.index,
                    y=top_colleges['Avg Grade'],
                    title="Top Colleges by Average Grade (Min 3 Players)",
                    color=top_colleges['Avg Grade'],
                    color_continuous_scale='Viridis'
                )
                
                fig_college.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis_title="College",
                    yaxis_title="Average Grade"
                )
                
                st.plotly_chart(fig_college, use_container_width=True)
                
                st.dataframe(top_colleges, use_container_width=True)
        
        # Physical attributes vs performance
        physical_cols = ['height_inches', 'weight', 'bmi']
        available_physical = [col for col in physical_cols if col in self.data.columns]
        
        if available_physical:
            st.markdown("#### 💪 Physical Attributes vs Performance")
            
            selected_physical = st.selectbox(
                "Select Physical Attribute",
                available_physical
            )
            
            # Create bins for the physical attribute
            n_bins = 5
            self.data[f'{selected_physical}_bin'] = pd.cut(
                self.data[selected_physical],
                bins=n_bins,
                labels=[f'Bin {i+1}' for i in range(n_bins)]
            )
            
            # Performance by physical attribute bins
            physical_performance = self.data.groupby(f'{selected_physical}_bin')['grade'].agg([
                'count', 'mean', 'std'
            ]).round(2)
            
            physical_performance.columns = ['Count', 'Mean Grade', 'Std Dev']
            
            fig_physical = px.bar(
                x=physical_performance.index,
                y=physical_performance['Mean Grade'],
                title=f"Performance by {selected_physical.replace('_', ' ').title()} Range",
                color=physical_performance['Mean Grade'],
                color_continuous_scale='Plasma'
            )
            
            fig_physical.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_title=f"{selected_physical.replace('_', ' ').title()} Range",
                yaxis_title="Average Grade"
            )
            
            st.plotly_chart(fig_physical, use_container_width=True)
