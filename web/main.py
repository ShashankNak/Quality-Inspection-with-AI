from flask import Flask, request, jsonify,render_template
import os
from inspect_video import InspectVideo


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_inspection")
def video_inspection():
    return render_template("/sections/products/video_inspection.html")

@app.route("/sample_inspection")
def sample_inspection():
    return render_template("/sections/products/sample_inspection.html")

ALLOWED_EXTENSIONS = ['mp4']
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['mp4']



@app.route("/predictVideo", methods=["POST"])
def predictvideo():
    inspect = InspectVideo()
    if 'video' not in request.files:
        return "No file part"
    video = request.files['video']
    if video.filename == '':
        return "No selected file"
    if allowed_file(video.filename):
        url = "web/static/input/"
        print("storing...")
        print(os.listdir(url))

        s = request.form['model']
        print(s)

        print(video.filename)

        input_video_path = url + video.filename
        output_video_path = "web/static/output/" + video.filename

        if not inspect.checklabel(url,video.filename,s.lower()):
            return None

        # Check if both input and output videos already exist
        if os.path.exists(input_video_path) and os.path.exists(output_video_path):
            print("Both input and output videos exist. Returning output video.")
            return jsonify({"output_video_url": "static/output/" + video.filename})


        # If only input video exists, save it and return
        if os.path.exists(input_video_path):
            print("Only input video exists. Saving input video.")
            return jsonify(inspect.inspectVideo(url, video.filename, s.lower()))

        # Save input video and return
        video.save(input_video_path)
        print("Input video saved.")
        return jsonify(inspect.inspectVideo(url, video.filename, s.lower()))


    
    
if __name__ == "__main__":
    app.run(debug=True)


