# 🚀 DataSense AI

An AI-powered Data Quality & Model Monitoring Platform built with Flask and Python.

DataSense AI is a web-based application that enables users to upload CSV datasets, analyze data quality, clean missing and duplicate values, generate statistical insights, visualize data, and download cleaned datasets and analysis reports through an interactive dashboard.

## ✨ Features

- 📂 Upload CSV datasets
- 👀 Preview uploaded datasets
- 📊 Dataset summary (rows, columns, memory usage, data types)
- 🩺 Dataset health analysis
- 📈 Dataset quality score
- 🤖 Machine Learning readiness score
- 💡 Smart data cleaning recommendations
- 🎯 Suggested target column for machine learning
- 🔍 Detect missing values and duplicate rows
- 📉 Calculate missing value percentage
- 🧹 Remove duplicate rows
- 🧹 Remove missing rows
- 🔧 Fill missing values using Mean, Median, or Mode
- 📋 Display column names and data types
- 📌 Show unique values for each column
- 📐 Statistical analysis (Mean, Median, Mode, Min, Max, Standard Deviation, Variance)
- 📊 Generate visualizations:
  - Histogram
  - Box Plot
  - Scatter Plot
  - Correlation Heatmap
  - Bar Chart
  - Line Chart
  - Pie Chart
- 📥 Download cleaned dataset
- 📄 Download analysis report
- 🎨 Responsive Bootstrap dashboard

## 🛠️ Tech Stack

### Backend
- Python
- Flask

### Data Processing
- Pandas
- NumPy

### Data Visualization
- Matplotlib

### Frontend
- HTML
- CSS
- Bootstrap 5
- Jinja2

### Development Tools
- Git
- GitHub
- VS Code

## 📂 Project Structure

```text
DataSense-AI/
│
├── app.py
├── config.py
├── logger.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── database/
├── logs/
├── models/
├── reports/
├── services/
├── uploads/
├── utils/
├── static/
└── templates/
```

## ⚙️ Installation

1. Clone the repository

```bash
git clone https://github.com/Neelu-Verma-26/DataSense-AI.git
```

2. Navigate to the project directory

```bash
cd DataSense-AI
```

3. Create a virtual environment

```bash
python -m venv venv
```

4. Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

5. Install dependencies

```bash
pip install -r requirements.txt
```

6. Run the application

```bash
python app.py
```

7. Open your browser and visit

```
http://127.0.0.1:5001
```

## 🚀 Future Enhancements

The current release (**Version 0.1**) focuses on data quality analysis, cleaning, visualization, and reporting.

Future versions of DataSense AI will include:

- 🔐 User Authentication (Login & Registration)
- 📂 Dataset History Management
- 🗄 Database Integration (SQLite/PostgreSQL)
- 🤖 Machine Learning Model Training
- 📊 Automatic Model Comparison
- 🎯 Prediction on New Datasets
- 📈 Interactive Dashboard with Sidebar Navigation
- 📄 PDF Report Generation
- 🐳 Docker Support
- ☁️ Cloud Deployment

## 👩‍💻 Author

**Neelu Verma**

B.Tech CSE (AI & ML)

GitHub: https://github.com/Neelu-Verma-26

## 📸 Screenshots

### Home Page

> *(Add screenshot here after deployment)*

### Dataset Analysis Dashboard

> *(Add screenshot here after deployment)*

### Data Cleaning

> *(Add screenshot here after deployment)*

### Data Visualization

> *(Add screenshot here after deployment)*

### Analysis Report

> *(Add screenshot here after deployment)*