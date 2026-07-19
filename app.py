from flask import Flask, render_template, request, session
import pandas as pd

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

    return rows, columns, column_names, missing_values_html, duplicate_rows, table         

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

        rows, columns, column_names, missing_values_html, duplicate_rows, table = generate_dataset_report(df)

        return render_template("index.html",
                                table=table,
                                rows=rows,
                                columns=columns,
                                column_names=column_names,
                                missing_values = missing_values_html,
                                duplicate_rows = duplicate_rows)
    
    return render_template("index.html")

@app.route("/remove_duplicates", methods = ["POST"])
def remove_duplicates():
    file_path = session.get("file_path")
    
    df = pd.read_csv(file_path)

    df.drop_duplicates(inplace=True)

    df.to_csv(file_path, index=False)

    rows, columns, column_names, missing_values_html, duplicate_rows, table = generate_dataset_report(df)

    return render_template("index.html",
                                table=table,
                                rows=rows,
                                columns=columns,
                                column_names=column_names,
                                missing_values = missing_values_html,
                                duplicate_rows = duplicate_rows)

@app.route("/remove_missing_rows", methods = ["POST"])
def remove_missing_rows():
    file_path = session.get("file_path")

    if file_path is None:
        return "Please upload a file first."

    df = pd.read_csv(file_path)

    df.dropna(inplace=True)

    df.to_csv(file_path, index = False)

    rows, columns, column_names, missing_values_html, duplicate_rows, table = generate_dataset_report(df)

    return render_template("index.html",
                           table=table,
                           rows=rows,
                           columns=columns,
                           column_names=column_names,
                           missing_values = missing_values_html,
                           duplicate_rows = duplicate_rows)

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

    rows, columns, column_names, missing_values_html, duplicate_rows, table = generate_dataset_report(df)

    return render_template("index.html",
                            table=table, 
                            rows=rows,
                            columns=columns,
                            column_names=column_names,
                            missing_values = missing_values_html,
                            duplicate_rows = duplicate_rows)

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

    rows, columns, column_names, missing_values_html, duplicate_rows, table = generate_dataset_report(df)

    return render_template("index.html",
                            table=table, 
                            rows=rows,
                            columns=columns,
                            column_names=column_names,
                            missing_values = missing_values_html,
                            duplicate_rows = duplicate_rows)

@app.route("/fill_mode", methods = ["POST"])
def fill_mode():
    file_path = session.get("file_path")
    if file_path is None:
          return "Please upload a file first"
     
    df = pd.read_csv(file_path)

    for column in df.columns:
        mode_value = df[column].mode()
        if not mode_value.empty:
            df[column] = df[column].fillna(mode_value[0], inplace=True)

    df.to_csv(file_path, index=False)

    rows, columns, column_names, missing_values_html, duplicate_rows, table = generate_dataset_report(df)

    return render_template("index.html",
                            table=table, 
                            rows=rows,
                            columns=columns,
                            column_names=column_names,
                            missing_values = missing_values_html,
                            duplicate_rows = duplicate_rows)

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

    rows, columns, column_names, missing_values_html, duplicate_rows, table = generate_dataset_report(df)

    return render_template("index.html",
                            table=table, 
                            rows=rows,
                            columns=columns,
                            column_names=column_names,
                            missing_values = missing_values_html,
                            duplicate_rows = duplicate_rows,
                            
                            mean_html=mean_html,
                            median_html=median_html,
                            mode_html=mode_html,
                            min_html=min_html,
                            max_html=max_html,
                            std_html=std_html,
                            variance_html=variance_html)


if __name__ == "__main__":
    app.run(debug = True, port=5001)
