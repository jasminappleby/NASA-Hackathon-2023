from flask import Flask, render_template, request, send_file
import cv2
import numpy as np
import pandas as pd
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the uploaded image
        uploaded_image = request.files["image"]

        if uploaded_image:
            # Read the uploaded image using OpenCV
            image_data = np.fromstring(uploaded_image.read(), np.uint8)
            image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

            # Convert the image to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Create a histogram of pixel values
            hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256])

            # Flatten the histogram data for display
            hist_values = hist.flatten()

            # Create a Pandas DataFrame for the pixel values
            pixel_values = pd.DataFrame(data={'Pixel Value': np.arange(256), 'Frequency': hist_values})

            # Save the pixel values to a CSV file
            pixel_values.to_csv('pixel_values.csv', index=False)

            return render_template("index.html", hist=hist_values, show_download=True)
    
    return render_template("index.html", hist=None, show_download=False)

@app.route("/download")
def download():
    return send_file('pixel_values.csv', as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

