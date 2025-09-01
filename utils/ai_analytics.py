import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class AIAnalytics:
    """Advanced AI analytics for NFL Draft analysis."""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.scaler = StandardScaler()
        self.features = self._get_numeric_features()
        
    def _get_numeric_features(self) -> list:
        """Get numeric features for analysis."""
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns.tolist()
        # Remove target variables and irrelevant columns
        exclude_cols = ['grade', 'overall', 'rating', 'source_sheet']
        return [col for col in numeric_cols if col not in exclude_cols]
    
    def render_performance_predictions(self):
        """Render performance prediction analysis."""
        st.markdown("### 🎯 Performance Predictions")
        
        col1, col2 = st.columns([2, 1])
        
        with col2:
            st.markdown("#### Model Configuration")
            
            # Target variable selection
            target_options = ['grade', 'overall', 'rating']
            available_targets = [col for col in target_options if col in self.data.columns]
            
            if not available_targets:
                st.error("No target variable (grade/overall/rating) found in data.")
                return
            
            target_var = st.selectbox("Select Target Variable", available_targets)
            
            # Feature selection
            st.markdown("##### Feature Selection")
            selected_features = st.multiselect(
                "Select Features for Prediction",
                self.features,
                default=self.features[:5] if len(self.features) >= 5 else self.features
            )
            
            if len(selected_features) < 2:
                st.warning("Please select at least 2 features for prediction.")
                return
        
        with col1:
            # Prepare data for modeling
            model_data = self.data[selected_features + [target_var]].dropna()
            
            if len(model_data) < 10:
                st.error("Insufficient data for modeling. Need at least 10 complete records.")
                return
            
            X = model_data[selected_features]
            y = model_data[target_var]
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Train model
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # Predictions
            y_pred = model.predict(X_test)
            
            # Metrics
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Display metrics
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("R² Score", f"{r2:.3f}")
            with col_b:
                st.metric("RMSE", f"{np.sqrt(mse):.3f}")
            with col_c:
                st.metric("Training Samples", len(X_train))
            
            # Prediction vs Actual plot
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=y_test,
                y=y_pred,
                mode='markers',
                name='Predictions',
                marker=dict(color='#FF6B35', size=8, opacity=0.7)
            ))
            
            # Perfect prediction line
            min_val, max_val = min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())
            fig.add_trace(go.Scatter(
                x=[min_val, max_val],
                y=[min_val, max_val],
                mode='lines',
                name='Perfect Prediction',
                line=dict(color='white', dash='dash')
            ))
            
            fig.update_layout(
                title="Predicted vs Actual Performance",
                xaxis_title=f"Actual {target_var.title()}",
                yaxis_title=f"Predicted {target_var.title()}",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig, width='stretch')
            
            # Feature importance
            feature_importance = pd.DataFrame({
                'feature': selected_features,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=True)
            
            fig_importance = px.bar(
                feature_importance,
                x='importance',
                y='feature',
                orientation='h',
                title="Feature Importance in Prediction Model",
                color='importance',
                color_continuous_scale='Viridis'
            )
            
            fig_importance.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_importance, width='stretch')
    
    def render_risk_assessment(self):
        """Render risk assessment analysis."""
        st.markdown("### ⚠️ Risk Assessment Analysis")
        
        if 'grade' not in self.data.columns:
            st.error("Grade column required for risk assessment.")
            return
        
        # Create risk categories based on grade distribution
        grade_percentiles = self.data['grade'].quantile([0.25, 0.5, 0.75])
        
        def categorize_risk(grade):
            if pd.isna(grade):
                return 'Unknown'
            elif grade >= grade_percentiles[0.75]:
                return 'Low Risk'
            elif grade >= grade_percentiles[0.5]:
                return 'Medium Risk'
            elif grade >= grade_percentiles[0.25]:
                return 'High Risk'
            else:
                return 'Very High Risk'
        
        self.data['risk_category'] = self.data['grade'].apply(categorize_risk)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk distribution
            risk_counts = self.data['risk_category'].value_counts()
            
            fig_pie = px.pie(
                values=risk_counts.values,
                names=risk_counts.index,
                title="Risk Distribution Across All Players",
                color_discrete_map={
                    'Low Risk': '#28a745',
                    'Medium Risk': '#ffc107',
                    'High Risk': '#fd7e14',
                    'Very High Risk': '#dc3545',
                    'Unknown': '#6c757d'
                }
            )
            
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_pie, width='stretch')
        
        with col2:
            # Risk by position
            if 'position_group' in self.data.columns:
                risk_by_pos = pd.crosstab(
                    self.data['position_group'],
                    self.data['risk_category'],
                    normalize='index'
                ) * 100
                
                fig_heatmap = px.imshow(
                    risk_by_pos.values,
                    x=risk_by_pos.columns,
                    y=risk_by_pos.index,
                    title="Risk Distribution by Position Group (%)",
                    color_continuous_scale='RdYlGn_r',
                    aspect='auto'
                )
                
                fig_heatmap.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                
                st.plotly_chart(fig_heatmap, width='stretch')
        
        # Risk factors analysis
        st.markdown("#### 🔍 Risk Factors Analysis")
        
        # Identify key risk factors using correlation with grade
        risk_features = []
        for feature in self.features:
            if feature in self.data.columns:
                correlation = self.data[feature].corr(self.data['grade'])
                if not pd.isna(correlation):
                    risk_features.append({
                        'feature': feature,
                        'correlation': correlation,
                        'risk_impact': 'Positive' if correlation > 0 else 'Negative'
                    })
        
        risk_df = pd.DataFrame(risk_features).sort_values('correlation', key=abs, ascending=False)
        
        if not risk_df.empty:
            # Top risk factors chart
            top_risk = risk_df.head(10)
            
            fig_risk = px.bar(
                top_risk,
                x='correlation',
                y='feature',
                orientation='h',
                title="Top Risk Factors (Correlation with Grade)",
                color='correlation',
                color_continuous_scale='RdYlGn'
            )
            
            fig_risk.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_risk, width='stretch')
    
    def render_clustering_analysis(self):
        """Render player clustering analysis."""
        st.markdown("### 🎯 Player Clustering Analysis")
        
        # Prepare data for clustering
        cluster_features = [f for f in self.features if f in self.data.columns]
        
        if len(cluster_features) < 2:
            st.error("Need at least 2 numeric features for clustering analysis.")
            return
        
        cluster_data = self.data[cluster_features].dropna()
        
        if len(cluster_data) < 10:
            st.error("Insufficient data for clustering. Need at least 10 complete records.")
            return
        
        col1, col2 = st.columns([3, 1])
        
        with col2:
            st.markdown("#### Clustering Configuration")
            
            # Number of clusters
            n_clusters = st.slider("Number of Clusters", 2, 8, 4)
            
            # Feature selection for clustering
            selected_cluster_features = st.multiselect(
                "Select Features for Clustering",
                cluster_features,
                default=cluster_features[:4] if len(cluster_features) >= 4 else cluster_features
            )
            
            if len(selected_cluster_features) < 2:
                st.warning("Please select at least 2 features for clustering.")
                return
        
        with col1:
            # Perform clustering
            cluster_subset = cluster_data[selected_cluster_features]
            
            # Scale features
            scaled_features = self.scaler.fit_transform(cluster_subset)
            
            # K-means clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(scaled_features)
            
            # Add clusters to data
            cluster_subset['cluster'] = clusters
            
            # Create visualization based on available features
            if len(selected_cluster_features) >= 2:
                feature_x = selected_cluster_features[0]
                feature_y = selected_cluster_features[1]
                
                fig_scatter = px.scatter(
                    cluster_subset,
                    x=feature_x,
                    y=feature_y,
                    color='cluster',
                    title=f"Player Clusters: {feature_x.title()} vs {feature_y.title()}",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                
                fig_scatter.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                
                st.plotly_chart(fig_scatter, width='stretch')
            
            # Cluster analysis
            st.markdown("#### 📊 Cluster Analysis")
            
            cluster_stats = []
            for i in range(n_clusters):
                cluster_mask = clusters == i
                cluster_players = cluster_subset[cluster_mask]
                
                stats_dict = {
                    'Cluster': f'Cluster {i+1}',
                    'Players': len(cluster_players),
                    'Percentage': f"{(len(cluster_players)/len(cluster_subset))*100:.1f}%"
                }
                
                # Add mean values for each feature
                for feature in selected_cluster_features:
                    stats_dict[f'Avg {feature.title()}'] = f"{cluster_players[feature].mean():.2f}"
                
                cluster_stats.append(stats_dict)
            
            cluster_stats_df = pd.DataFrame(cluster_stats)
            st.dataframe(cluster_stats_df, width='stretch')
            
            # Cluster characteristics
            fig_radar = go.Figure()
            
            # Normalize features for radar chart
            normalized_data = pd.DataFrame(scaled_features, columns=selected_cluster_features)
            normalized_data['cluster'] = clusters
            
            for i in range(n_clusters):
                cluster_means = normalized_data[normalized_data['cluster'] == i][selected_cluster_features].mean()
                
                fig_radar.add_trace(go.Scatterpolar(
                    r=cluster_means.values.tolist() + [cluster_means.values[0]],
                    theta=cluster_means.index.tolist() + [cluster_means.index[0]],
                    fill='toself',
                    name=f'Cluster {i+1}'
                ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[-2, 2]
                    )),
                title="Cluster Characteristics (Normalized)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_radar, width='stretch')
    
    def render_market_value_analysis(self):
        """Render market value analysis."""
        st.markdown("### 💰 Market Value Analysis")
        
        if 'grade' not in self.data.columns:
            st.error("Grade column required for market value analysis.")
            return
        
        # Create value tiers based on grade
        value_percentiles = self.data['grade'].quantile([0.2, 0.4, 0.6, 0.8])
        
        def categorize_value(grade):
            if pd.isna(grade):
                return 'Unknown'
            elif grade >= value_percentiles[0.8]:
                return 'Elite'
            elif grade >= value_percentiles[0.6]:
                return 'High Value'
            elif grade >= value_percentiles[0.4]:
                return 'Medium Value'
            elif grade >= value_percentiles[0.2]:
                return 'Low Value'
            else:
                return 'Minimal Value'
        
        self.data['value_tier'] = self.data['grade'].apply(categorize_value)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Value distribution
            value_counts = self.data['value_tier'].value_counts()
            
            fig_value = px.bar(
                x=value_counts.index,
                y=value_counts.values,
                title="Market Value Distribution",
                color=value_counts.values,
                color_continuous_scale='Viridis'
            )
            
            fig_value.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_title="Value Tier",
                yaxis_title="Number of Players"
            )
            
            st.plotly_chart(fig_value, width='stretch')
        
        with col2:
            # Value by position
            if 'position_group' in self.data.columns:
                value_by_pos = self.data.groupby(['position_group', 'value_tier']).size().unstack(fill_value=0)
                
                fig_stack = px.bar(
                    value_by_pos,
                    title="Value Distribution by Position Group",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                
                fig_stack.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis_title="Position Group",
                    yaxis_title="Number of Players"
                )
                
                st.plotly_chart(fig_stack, width='stretch')
        
        # Value efficiency analysis
        st.markdown("#### 📈 Value Efficiency Metrics")
        
        if 'position_group' in self.data.columns:
            efficiency_metrics = []
            
            for pos_group in self.data['position_group'].unique():
                pos_data = self.data[self.data['position_group'] == pos_group]
                
                if len(pos_data) > 0:
                    elite_pct = (pos_data['value_tier'] == 'Elite').mean() * 100
                    avg_grade = pos_data['grade'].mean()
                    grade_std = pos_data['grade'].std()
                    
                    efficiency_metrics.append({
                        'Position Group': pos_group,
                        'Elite %': f"{elite_pct:.1f}%",
                        'Avg Grade': f"{avg_grade:.2f}",
                        'Grade Std Dev': f"{grade_std:.2f}",
                        'Players': len(pos_data)
                    })
            
            efficiency_df = pd.DataFrame(efficiency_metrics)
            st.dataframe(efficiency_df, width='stretch')
        
        # Undervalued/Overvalued players
        if len(self.features) > 0:
            st.markdown("#### 💎 Value Opportunities")
            
            # Simple value model based on combine metrics
            feature_cols = [f for f in self.features if f in self.data.columns][:5]
            
            if len(feature_cols) >= 2:
                model_data = self.data[feature_cols + ['grade']].dropna()
                
                if len(model_data) >= 10:
                    X = model_data[feature_cols]
                    y = model_data['grade']
                    
                    # Train simple model
                    model = RandomForestRegressor(n_estimators=50, random_state=42)
                    model.fit(X, y)
                    
                    # Predict expected grades
                    predicted_grades = model.predict(X)
                    
                    # Calculate value difference
                    model_data['predicted_grade'] = predicted_grades
                    model_data['value_diff'] = model_data['grade'] - model_data['predicted_grade']
                    
                    # Find undervalued players (actual grade < predicted grade)
                    undervalued = model_data.nlargest(10, 'value_diff')[['predicted_grade', 'grade', 'value_diff']]
                    overvalued = model_data.nsmallest(10, 'value_diff')[['predicted_grade', 'grade', 'value_diff']]
                    
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        st.markdown("##### 📈 Most Undervalued")
                        st.dataframe(undervalued.round(2), width='stretch')
                    
                    with col_b:
                        st.markdown("##### 📉 Most Overvalued")
                        st.dataframe(overvalued.round(2), width='stretch')
