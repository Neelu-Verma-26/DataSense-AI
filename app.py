from flask import Flask, render_template, request

print("Running DataSense AI")

app = Flask(__name__)

@app.route("/")
def welcome():
    return "THIS IS DATASENSE AI"

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        uploaded_file.save("uploads/" + uploaded_file.filename)
        return "File Uploaded Successfully!"
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug = True, port=5001)
