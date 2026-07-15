from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/")
def welcome():
    return "THIS IS DATASENSE AI"

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        file_path = "uploads/" + uploaded_file.filename

        uploaded_file.save(file_path)
        df = pd.read_csv(file_path)

        missing_values = df.isnull().sum()
        missing_values = missing_values[missing_values > 0]
        if missing_values.empty:
            missing_values_html = "<p>No Missing Values found</p>"

        duplicate_rows = df.duplicated().sum()
    
        rows = df.shape[0]
        columns = df.shape[1]
        column_names = list(df.columns)

        table = df.head().to_html()
        return render_template("index.html",
                                table=table,
                                rows=rows,
                                columns=columns,
                                column_names=column_names,
                                missing_values = missing_values_html,
                                duplicate_rows = duplicate_rows)
    
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug = True, port=5001)
