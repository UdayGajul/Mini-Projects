from flask import Flask, render_template, request, jsonify
import os
import cv2
import numpy as np
from sklearn.cluster import KMeans

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def extract_top_colors(image_path, num_colors=10):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    pixels = img.reshape((-1, 3))

    kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
    kmeans.fit(pixels)

    colors = kmeans.cluster_centers_.astype(int)

    counts = np.bincount(kmeans.labels_)
    percentages = counts / counts.sum()

    color_data = sorted(
        [(colors[i].tolist(), float(percentages[i])) for i in range(len(colors))],
        key=lambda x: x[1],
        reverse=True,
    )

    return color_data


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    colors = extract_top_colors(filepath)

    return jsonify(colors)


if __name__ == "__main__":
    app.run(debug=True)
