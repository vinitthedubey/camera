from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Initialize the camera
cap = cv2.VideoCapture(0)  # 0 is the default camera

# Check if the camera is opened correctly
if not cap.isOpened():
    print("Error: Camera not found.")
    exit()

# Function to generate frames for the video stream
def generate():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Encode the frame in JPEG format
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            break
        # Convert the encoded frame to bytes and yield it as part of the HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

# Home route that renders the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to stream video feed
@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
