# Overview

This is a 2025 NFL Draft Assistant application built with Streamlit that provides advanced AI analytics and statistical breakdown for NFL draft prospects. The application features multiple analysis components including individual player analysis, draft simulation, team analysis, and comprehensive data visualizations. It processes Excel data files containing player statistics and combines them with AI-powered analytics to provide insights for NFL draft evaluation.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The application uses Streamlit as the primary web framework, providing an interactive dashboard interface. The frontend is organized into modular components:
- **Main Application (app.py)**: Central entry point that orchestrates all components and handles page configuration
- **Component-Based Architecture**: Separate modules for player analysis, draft simulation, and team analysis
- **Custom Styling**: CSS-based theming with a modern dark theme using custom color variables
- **Responsive Layout**: Wide layout configuration with sidebar navigation and multi-column displays

## Backend Architecture
The backend follows a utility-based architecture with clear separation of concerns:
- **Data Processing Layer**: Handles Excel file upload, data standardization, and column mapping
- **AI Analytics Engine**: Implements machine learning models using scikit-learn for performance predictions and clustering
- **Visualization Engine**: Creates interactive charts and graphs using Plotly and Plotly Express
- **Component System**: Modular components that can be independently developed and maintained

## Data Processing Pipeline
The system implements a robust data processing pipeline:
- **File Upload Handling**: Streamlit file uploader for Excel files
- **Data Standardization**: Automatic column mapping and position normalization
- **Feature Engineering**: Extraction of numeric features for machine learning analysis
- **Session State Management**: Persistent data storage across user interactions

## Machine Learning Integration
The application incorporates several ML capabilities:
- **Performance Prediction**: Random Forest models for predicting player grades and ratings
- **Clustering Analysis**: K-means clustering for player grouping and comparison
- **Statistical Analysis**: Correlation analysis and feature importance calculation
- **Model Evaluation**: R² scores and mean squared error metrics for model validation

## Visualization Strategy
The visualization system provides comprehensive data exploration:
- **Interactive Dashboards**: Multi-panel layouts with dynamic filtering
- **Statistical Charts**: Distribution plots, correlation heatmaps, and performance metrics
- **Comparative Analysis**: Player comparison tools and team-based analytics
- **Real-time Updates**: Dynamic chart updates based on user selections

# External Dependencies

## Core Framework Dependencies
- **Streamlit**: Web application framework for the user interface
- **Pandas**: Data manipulation and analysis library
- **NumPy**: Numerical computing library for statistical operations

## Visualization Libraries
- **Plotly Express**: High-level plotting library for interactive charts
- **Plotly Graph Objects**: Low-level plotting for custom visualizations
- **Seaborn**: Statistical data visualization (used in utils/visualizations.py)

## Machine Learning Libraries
- **Scikit-learn**: Machine learning library providing:
  - RandomForestRegressor and RandomForestClassifier for predictions
  - KMeans for clustering analysis
  - StandardScaler for feature normalization
  - Train-test split and evaluation metrics
- **SciPy**: Scientific computing library for statistical functions

## Data Processing Dependencies
- **Pandas Excel Engine**: For reading and processing Excel files containing draft data
- **Regular Expressions (re)**: For data cleaning and standardization

## UI/UX Dependencies
- **Custom CSS**: Local stylesheet (assets/styles.css) for theming and responsive design
- **Base64 Encoding**: For handling file downloads and data export functionality

## Session Management
- **Streamlit Session State**: For maintaining data persistence across user interactions and page reloads

The application is designed to work with Excel files as the primary data source, with no external database dependencies. All data processing and analysis occurs in-memory using the loaded datasets.