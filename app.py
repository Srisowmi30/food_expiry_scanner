from flask import Flask, render_template, request
import easyocr
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

reader = easyocr.Reader(['en'])

@app.route("/", methods=["GET", "POST"])
def index():
    expiry_text = None
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded"
        file = request.files["file"]
        if file.filename == "":
            return "No file selected"

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Run OCR
        results = reader.readtext(filepath)

        # Extract detected text
        texts = [res[1] for res in results]
        expiry_text = " | ".join(texts)

    return render_template("index.html", expiry_text=expiry_text)

if __name__ == "__main__":
    app.run(debug=True)
