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
        table = df.head().to_html()
        return render_template("index.html", table=table)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug = True, port=5001)
