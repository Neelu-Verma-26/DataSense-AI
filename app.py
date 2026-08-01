from flask import Flask, render_template, request, session, send_file
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)
app.secret_key =  "datasense_ai_secret_key"

def generate_dataset_report(df):
    rows = df.shape[0]
    columns = df.shape[1]
    column_names = list(df.columns)
    
    missing_values = df.isnull().sum()
    missing_values = missing_values[missing_values > 0]
    if missing_values.empty:
            missing_values_html = "<p>No Missing Values found</p>"
    else:
            missing_values_html = (missing_values.to_frame(name="Missing Values").to_html(
    classes="table table-striped table-hover table-bordered",
    index=False))

    duplicate_rows = df.duplicated().sum()
    if duplicate_rows == 0:
        duplicate_status = "🟢 Excellent"
        duplicate_message = "No duplicate rows found."

    else:
        duplicate_status = "🟡 Warning"
        duplicate_message = f"{duplicate_rows} duplicate rows found."

    table = df.head().to_html(
        classes="table table-striped table-hover table-bordered",
        index=False
    )

    memory = df.memory_usage().sum()

    if memory < (1024 ** 2):
        memory_size = f"{memory / 1024:.2f} KB"
    else:
        memory_size = f"{memory / (1024 ** 2):.2f} MB"

    numeric_df = df.select_dtypes(include="number")
    numeric_columns = numeric_df.shape[1]

    categorical_df = df.select_dtypes(include="object")
    categorical_columns = categorical_df.shape[1]

    column_types = df.dtypes
    column_types_html = column_types.to_frame(name="Data Type").to_html(
    classes="table table-striped table-hover table-bordered",
    index=False
)

    unique_values = df.nunique()
    unique_values_html = unique_values.to_frame(name="Unique Values").to_html(
    classes="table table-striped table-hover table-bordered",
    index=False
)
    constant_columns = unique_values[unique_values == 1].index.tolist()

    missing_percentage = (missing_values / rows) * 100
    missing_percentage_html = missing_percentage.to_frame(name="Missing Percentage (%)").to_html(
    classes="table table-striped table-hover table-bordered",
    index=False
)

    total_missing = missing_values.sum()
    overall_missing_percentage = (total_missing / (rows * columns)) * 100
    duplicate_percentage = (duplicate_rows/rows)*100

    quality_score = 100-overall_missing_percentage-duplicate_percentage
    quality_score = max(quality_score,0)
    quality_score = round(quality_score, 2)

    overall_missing_percentage = round(overall_missing_percentage, 2)
    if overall_missing_percentage==0:
        missing_status = "🟢 Excellent"
        missing_message= "No missing values found"
    elif overall_missing_percentage <= 10:
        missing_status = "🟡 Warning"
        missing_message = f"{overall_missing_percentage}% missing values detected."
    else:
        missing_status = "🔴 Poor"
        missing_message =  f"{overall_missing_percentage}% missing values detected."

    correlation_matrix = df.corr(numeric_only=True)
    highly_correlated = []
    for i in range(len(correlation_matrix.columns)):
        for j in range(i + 1, len(correlation_matrix.columns)):
            if abs(correlation_matrix.iloc[i, j]) >= 0.80:
                col1 = correlation_matrix.columns[i]
                col2 = correlation_matrix.columns[j]
                corr_value = correlation_matrix.iloc[i, j]
                highly_correlated.append(
                    f"{col1} ↔ {col2} ({corr_value:.2f})"
                )

    health_issues = []

    if overall_missing_percentage > 0:
        health_issues.append("Missing values detected")

    if duplicate_rows > 0:
        health_issues.append("Duplicate rows detected")

    if len(constant_columns) > 0:
        health_issues.append("Constant columns detected")

    if len(highly_correlated) > 0:
        health_issues.append("Highly correlated columns detected")

    if len(health_issues) == 0:
        dataset_health = "🟢 Excellent"
        health_message = "No major data quality issues detected."
    elif len(health_issues) <= 2:
        dataset_health = "🟡 Moderate"
        health_message = "Some data quality issues need attention."
    else:
        dataset_health = "🔴 Poor"
        health_message = "Multiple data quality issues detected."

    if quality_score >= 90:
        dataset_condition = "Dataset is in excellent condition."

    elif quality_score >= 70:
        dataset_condition = "Dataset is in good condition but needs minor cleaning."

    else:
        dataset_condition = "Dataset requires significant preprocessing before analysis."

    dataset_overview = (
        f"Dataset contains {rows} rows and {columns} columns. "
        f"It has {numeric_columns} numeric columns and "
        f"{categorical_columns} categorical columns. "
        f"Dataset quality score is {quality_score}%. "
        f"{dataset_condition}"
    )

    recommendations = []

    if overall_missing_percentage > 0:
        recommendations.append(
            "Fill or remove missing values."
        )

    if duplicate_rows > 0:
        recommendations.append(
            "Remove duplicate rows."
        )

    if len(constant_columns) > 0:
        recommendations.append(
            "Remove constant columns."
        )

    if len(highly_correlated) > 0:
        recommendations.append(
            "Consider removing highly correlated features."
        )

    if categorical_columns > 0:
        recommendations.append(
            "Encode categorical columns before training."
        )

    target_keywords = [
    "target",
    "label",
    "class",
    "price",
    "salary",
    "income",
    "churn",
    "survived",
    "purchased",
    "output"
    ]

    target_column = None

    for column in column_names:
        if column.lower() in target_keywords:
            target_column = column
            break

    ml_readiness_score = quality_score
    if ml_readiness_score >= 90:
        ml_readiness_message = "✅ Ready for Machine Learning."

    elif ml_readiness_score >= 70:
        ml_readiness_message = "⚠️ Minor preprocessing recommended."

    else:
        ml_readiness_message = "❌ Significant preprocessing required."

    return {
    "rows": rows,
    "columns": columns,
    "column_names": column_names,
    "missing_values_html": missing_values_html,
    "duplicate_rows": duplicate_rows,
    "table": table,
    "memory_usage": memory_size,
    "numeric_columns": numeric_columns, 
    "categorical_columns": categorical_columns,
    "column_types_html": column_types_html,
    "unique_values_html":unique_values_html,
    "missing_percentage_html": missing_percentage_html,
    "quality_score": quality_score,
    "missing_status": missing_status,
    "missing_message": missing_message,
    "duplicate_status": duplicate_status,
    "duplicate_message": duplicate_message,
    "constant_columns": constant_columns,
    "highly_correlated": highly_correlated,
    "dataset_health": dataset_health,
    "health_message": health_message,
    "health_issues": health_issues,
    "dataset_overview": dataset_overview,
    "recommendations": recommendations,
    "target_column": target_column,
    "ml_readiness_score": ml_readiness_score,
    "ml_readiness_message": ml_readiness_message}        

@app.route("/")
def welcome():
    return "THIS IS DATASENSE AI"

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        file_path = "uploads/" + uploaded_file.filename

        session["file_path"] = file_path

        uploaded_file.save(file_path)
        df = pd.read_csv(file_path)

        report = generate_dataset_report(df)

        return render_template("index.html",
                                report=report)
    
    return render_template("index.html", report=None)

@app.route("/remove_duplicates", methods = ["POST"])
def remove_duplicates():
    file_path = session.get("file_path")
    
    df = pd.read_csv(file_path)

    df.drop_duplicates(inplace=True)

    df.to_csv(file_path, index=False)

    report = generate_dataset_report(df)

    return render_template("index.html",
                            report = report)

@app.route("/remove_missing_rows", methods = ["POST"])
def remove_missing_rows():
    file_path = session.get("file_path")

    if file_path is None:
        return "Please upload a file first."

    df = pd.read_csv(file_path)

    df.dropna(inplace=True)

    df.to_csv(file_path, index = False)

    report = generate_dataset_report(df)

    return render_template("index.html",
                           report=report)

@app.route("/fill_mean", methods = ["POST"])
def fill_mean():
    file_path = session.get("file_path")
    if file_path is None:
          return "Please upload a file first."
    
    df = pd.read_csv(file_path)

    numeric_df = df.select_dtypes(include="number")
    for column in numeric_df.columns:
         df[column] = df[column].fillna(df[column].mean())

    df.to_csv(file_path, index=False)

    report = generate_dataset_report(df)

    return render_template("index.html",
                            report= report)

@app.route("/fill_median",methods= ["POST"])
def fill_median():
    file_path = session.get("file_path")
    if file_path is None:
          return "Please upload a file first"
     
    df = pd.read_csv(file_path)

    numeric_df = df.select_dtypes(include="number")
    for column in numeric_df.columns:
         df[column] = df[column].fillna(df[column].median())

    df.to_csv(file_path, index=False)

    report = generate_dataset_report(df)

    return render_template("index.html",
                            report=report)

@app.route("/fill_mode", methods = ["POST"])
def fill_mode():
    file_path = session.get("file_path")
    if file_path is None:
          return "Please upload a file first"
     
    df = pd.read_csv(file_path)

    for column in df.columns:
        mode_value = df[column].mode()
        if not mode_value.empty:
            df[column] = df[column].fillna(mode_value[0])

    df.to_csv(file_path, index=False)

    report = generate_dataset_report(df)

    return render_template("index.html",
                            report=report)

@app.route("/show_statistics", methods=["POST"])
def show_statistics():
    file_path = session.get("file_path")
    if file_path is None:
          return "Please upload a file first"
     
    df = pd.read_csv(file_path)

    numeric_df = df.select_dtypes(include="number")
    mean_values = numeric_df.mean()
    median_values = numeric_df.median()
    mode_values = numeric_df.mode()
    min_values = numeric_df.min()
    max_values = numeric_df.max()
    std_values = numeric_df.std()
    variance_values = numeric_df.var()

    mean_html = mean_values.to_frame(name="Mean").to_html(classes="table table-bordered")
    median_html = median_values.to_frame(name="Median").to_html(classes="table table-bordered")
    mode_html = mode_values.to_html(classes="table table-bordered")
    min_html = min_values.to_frame(name="Min").to_html(classes="table table-bordered")
    max_html = max_values.to_frame(name="Max").to_html(classes="table table-bordered")
    std_html = std_values.to_frame(name="Standard Deviation").to_html(classes="table table-bordered")
    variance_html = variance_values.to_frame(name="Variance").to_html(classes="table table-bordered")

    report = generate_dataset_report(df)

    return render_template("index.html",
                            report=report,
                            
                            mean_html=mean_html,
                            median_html=median_html,
                            mode_html=mode_html,
                            min_html=min_html,
                            max_html=max_html,
                            std_html=std_html,
                            variance_html=variance_html)

@app.route("/show_histogram", methods=["POST"])
def show_histogram():
    selected_column = request.form.get("column")
    file_path = session.get("file_path")
    if file_path is None:
          return "Please upload a file first"
    
    df = pd.read_csv(file_path)

    column_data = df[selected_column]
    plt.figure(figsize=(10,6))
    plt.hist(column_data, bins=20)
    plt.title(f"Histogram of {selected_column}", fontsize=16)
    plt.xlabel(selected_column, fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("static/histogram.png")
    plt.close()

    report = generate_dataset_report(df)

    return render_template("index.html",
                            report=report,
                            histogram_image="histogram.png")

@app.route("/show_boxplot", methods=["POST"])
def show_boxplot():
    selected_column = request.form.get("column")
    file_path = session.get("file_path")
    if file_path is None:
          return "Please upload a file first"
    
    df = pd.read_csv(file_path)
    column_data = df[selected_column]
    plt.figure(figsize=(10,6))
    plt.boxplot(column_data)
    plt.title(f"Box Plot of {selected_column}", fontsize=16)
    plt.ylabel(selected_column, fontsize=12)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("static/boxplot.png")
    plt.close()

    report = generate_dataset_report(df)

    return render_template("index.html",
                            report=report,
                            boxplot_image="boxplot.png")

@app.route("/show_scatter", methods=["POST"])
def show_scatter():
    x_column = request.form.get("x_column")
    y_column = request.form.get("y_column")
    file_path = session.get("file_path")
    if file_path is None:
        return "Please upload a file first"
    
    df = pd.read_csv(file_path)

    report = generate_dataset_report(df)

    if not pd.api.types.is_numeric_dtype(df[x_column]) or not pd.api.types.is_numeric_dtype(df[y_column]):
        return render_template(
            "index.html",
            report = report,
            histogram_image=None,
            boxplot_image=None,
            scatter_image=None
        )

    x_data = df[x_column]
    y_data = df[y_column]

    plt.figure(figsize=(10,6))
    plt.scatter(x_data, y_data)
    plt.title(f"Scatter Plot of {x_column} vs {y_column}", fontsize=16)
    plt.xlabel(x_column, fontsize=12)
    plt.ylabel(y_column, fontsize=12)
    plt.tight_layout()
    plt.savefig("static/scatter.png")
    plt.close()

    return render_template("index.html",
                           report = report,
                           scatter_image= "scatter.png",
                           histogram_image=None,
                           boxplot_image=None)

@app.route("/show_heatmap", methods=["POST"])
def show_heatmap():
    file_path = session.get("file_path")
    if file_path is None:
        return "Please upload a file first"
    df= pd.read_csv(file_path)

    report = generate_dataset_report(df)
    
    numeric_df =  df.select_dtypes(include="number")
    if numeric_df.empty:
         return render_template("index.html",
                                error="Dataset does not contain numeric columns.",
                                report = report,
                                histogram_image=None,
                                boxplot_image=None,
                                scatter_image=None,
                                heatmap_image = None)
    
    correlation_matrix = numeric_df.corr()
    plt.figure(figsize=(10,8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
    plt.tight_layout()
    plt.title("Correlation Heatmap", fontsize=16)
    plt.tight_layout()
    plt.savefig("static/heatmap.png")
    plt.close()

    return render_template("index.html",
                            report=report,
                            histogram_image=None,
                            boxplot_image=None,
                            scatter_image=None,
                            heatmap_image = "heatmap.png")

@app.route("/show_barchart",methods=["POST"])
def show_barchart():
    file_path = session.get("file_path")
    if file_path is None:
        return "Please upload a file first"
    df= pd.read_csv(file_path)
    
    report = generate_dataset_report(df)

    selected_column = request.form["bar_column"]

    counts = df[selected_column].value_counts()
    plt.figure(figsize=(10,6))
    plt.bar(counts.index, counts.values)
    plt.title(f"Bar Chart of {selected_column}", fontsize=16)
    plt.xlabel(selected_column, fontsize=12)
    plt.ylabel("Count", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/barchart.png")
    plt.close()

    return render_template("index.html",
                            report=report,
                            histogram_image=None,
                            boxplot_image=None,
                            scatter_image=None,
                            heatmap_image = None,
                            selected_bar_column=selected_column,
                            barchart_image = "barchart.png")

@app.route("/show_linechart", methods=["POST"])
def show_linechart():
    x_column = request.form.get("x_column")
    y_column = request.form.get("y_column")
    file_path = session.get("file_path")
    if file_path is None:
        return "Please upload a file first"
    
    df = pd.read_csv(file_path)

    report = generate_dataset_report(df)

    if not pd.api.types.is_numeric_dtype(df[y_column]):
        return render_template(
            "index.html",
            line_error="Please select a numeric column for the Y-axis.",
            report=report,
            histogram_image=None,
            boxplot_image=None,
            scatter_image=None,
            heatmap_image = None,
            barchart_image = None,
            linechart_image = None)

    x_data = df[x_column]
    y_data = df[y_column]

    plt.figure(figsize=(10,6))
    plt.plot(x_data, y_data)
    plt.title(f"Line Chart of {x_column} vs {y_column}", fontsize=16)
    plt.xlabel(x_column, fontsize=12)
    plt.ylabel(y_column, fontsize=12)
    plt.tight_layout()
    plt.savefig("static/linechart.png")
    plt.close()

    return render_template("index.html",
                           report=report,
                           histogram_image=None,
                           boxplot_image=None,
                           scatter_image=None,
                           heatmap_image = None,
                           barchart_image = None,
                           linechart_image = "linechart.png")

@app.route("/show_piechart",methods=["POST"])
def show_piechart():
    file_path = session.get("file_path")
    if file_path is None:
        return "Please upload a file first"
    df= pd.read_csv(file_path)
    
    report = generate_dataset_report(df)

    selected_column = request.form["pie_column"]

    if df[selected_column].nunique() > 10:
        return render_template(
            "index.html",
            report=report,
            selected_pie_column=selected_column,
            pie_error="Pie chart is suitable only for columns with 10 or fewer unique values.",
            histogram_image=None,
            boxplot_image=None,
            scatter_image=None,
            heatmap_image=None,
            barchart_image=None,
            linechart_image=None,
            piechart_image=None
        )

    counts = df[selected_column].value_counts(dropna=False)
    plt.figure(figsize=(10,6))
    plt.pie(counts.values, labels=counts.index,  autopct="%1.1f%%")
    plt.title(f"Pie Chart of {selected_column}", fontsize=16)
    plt.axis("equal") 
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/piechart.png")
    plt.close()

    return render_template("index.html",
                            report=report,
                            histogram_image=None,
                            boxplot_image=None,
                            scatter_image=None,
                            heatmap_image = None,
                            barchart_image = None,
                            linechart_image = None,
                            selected_pie_column=selected_column,
                            pie_error=None,
                            piechart_image = "piechart.png")

@app.route("/download_csv")
def download_csv():
    file_path = session.get("file_path")
    if file_path is None:
        return "Please upload a file first"

    return send_file(file_path, as_attachment=True)

@app.route("/download_report")
def download_report():

    df = pd.read_csv(session["file_path"])

    report = generate_dataset_report(df)

    report_path = "analysis_report.txt"

    with open(report_path, "w", encoding="utf-8") as file:

        file.write("========== DATASENSE AI REPORT ==========\n\n")

        file.write("----- Dataset Summary -----\n")
        file.write(f"Rows: {report['rows']}\n")
        file.write(f"Columns: {report['columns']}\n")
        file.write(f"Memory Usage: {report['memory_usage']}\n")
        file.write(f"Numeric Columns: {report['numeric_columns']}\n")
        file.write(f"Categorical Columns: {report['categorical_columns']}\n\n")

        file.write("----- Dataset Quality -----\n")
        file.write(f"Quality Score: {report['quality_score']}%\n")
        file.write(f"Missing Status: {report['missing_status']}\n")
        file.write(f"Duplicate Status: {report['duplicate_status']}\n")
        file.write(f"Dataset Health: {report['dataset_health']}\n\n")

        file.write("----- Machine Learning -----\n")
        file.write(f"ML Readiness Score: {report['ml_readiness_score']}%\n")
        file.write(f"{report['ml_readiness_message']}\n")
        file.write(f"Suggested Target Column: {report['target_column']}\n\n")

        file.write("----- Dataset Overview -----\n")
        file.write(f"{report['dataset_overview']}\n\n")

        file.write("----- Recommendations -----\n")
        if report["recommendations"]:
            for recommendation in report["recommendations"]:
                file.write(f"• {recommendation}\n")
        else:
            file.write("No recommendations.\n")

        file.write("\n----- Constant Columns -----\n")
        if report["constant_columns"]:
            for column in report["constant_columns"]:
                file.write(f"• {column}\n")
        else:
            file.write("None\n")

        file.write("\n----- Highly Correlated Columns -----\n")
        if report["highly_correlated"]:
            for pair in report["highly_correlated"]:
                file.write(f"• {pair}\n")
        else:
            file.write("None\n")

        file.write("\n----- Health Issues -----\n")
        if report["health_issues"]:
            for issue in report["health_issues"]:
                file.write(f"• {issue}\n")
        else:
            file.write("No issues detected.\n")

        file.write("\n========================================\n")
        file.write("Generated by DataSense AI\n")

    return send_file(
        report_path,
        as_attachment=True,
        download_name="DataSense_AI_Report.txt"
    )

if __name__ == "__main__":
    app.run(debug = True, port=5001)
