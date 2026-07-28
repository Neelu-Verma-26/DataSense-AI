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
            missing_values_html = (missing_values.to_frame(name="Missing Values").to_html())

    duplicate_rows = df.duplicated().sum()

    table = df.head().to_html()

    memory = df.memory_usage().sum()

    if memory < (1024 ** 2):
        memory_size = f"{memory / 1024:.2f} KB"
    else:
        memory_size = f"{memory / (1024 ** 2):.2f} MB"

    return {
    "rows": rows,
    "columns": columns,
    "column_names": column_names,
    "missing_values_html": missing_values_html,
    "duplicate_rows": duplicate_rows,
    "table": table,
    "memory_usage": memory_size
}        

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
    plt.figure(figsize=(8,5))
    plt.hist(column_data, bins=20)
    plt.title(f"Histogram of {selected_column}")
    plt.xlabel(selected_column)
    plt.ylabel("Frequency")
    plt.grid(True)
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
    plt.figure(figsize=(8,5))
    plt.boxplot(column_data)
    plt.title(f"Box Plot of {selected_column}")
    plt.ylabel(selected_column)
    plt.grid(True)
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

    plt.figure(figsize=(8,5))
    plt.scatter(x_data, y_data)
    plt.title(f"Scatter Plot of {x_column} vs {y_column}")
    plt.xlabel(x_column)
    plt.ylabel(y_column)
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
    plt.title("Correlation Heatmap")
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
    plt.figure(figsize=(8,5))
    plt.bar(counts.index, counts.values)
    plt.title(f"Bar Chart of {selected_column}")
    plt.xlabel(selected_column)
    plt.ylabel("Count")
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

    plt.figure(figsize=(8,5))
    plt.plot(x_data, y_data)
    plt.title(f"Line Chart of {x_column} vs {y_column}")
    plt.xlabel(x_column)
    plt.ylabel(y_column)
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
    plt.figure(figsize=(8,5))
    plt.pie(counts.values, labels=counts.index,  autopct="%1.1f%%")
    plt.title(f"Pie Chart of {selected_column}")
    plt.axis("equal") 
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

if __name__ == "__main__":
    app.run(debug = True, port=5001)
