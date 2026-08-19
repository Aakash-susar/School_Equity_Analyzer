#School Equity & Resource Allocation Analyzer

## Problem Statement
Educational inequality persists across schools due to uneven resource allocation, socioeconomic differences, and systemic factors. This project aims to analyze disparities and recommend resource allocation strategies to promote equity.

## Objectives
- Quantify equity across schools via an `Equity Score` metric.
- Cluster schools by need and resource levels using unsupervised learning.
- Predict key outcomes (e.g., test scores) with regression models.
- Provide actionable recommendations for resource reallocation.

## Dataset Overview
A Kaggle dataset will be used containing school-level features such as enrollment, demographics, funding, test scores, and other socioeconomic indicators.

## Project Workflow
1. Business understanding
2. Data loading and cleaning
3. Exploratory data analysis (EDA)
4. Feature engineering
5. Compute Equity Score
6. School clustering and segmentation
7. Regression analysis for key outcomes
8. Recommendation engine and simulation
9. Save models for dashboard use

## Tech Stack
- Python, Pandas, NumPy
- Scikit-Learn (clustering, regression)
- Joblib (model persistence)
- Jupyter (notebook-driven development)
- Streamlit (interactive dashboard)
- Matplotlib, Seaborn, Plotly (visualizations)


## Project Structure
- `data/`: Raw and processed datasets
- `notebooks/`: Jupyter notebook containing all analysis and modeling
- `models/`: Saved trained models
- `dashboard/`: Streamlit app for visualization and simulation
- `reports/`: Analysis reports and exportable artifacts
