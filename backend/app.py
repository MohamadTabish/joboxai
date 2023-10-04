from flask import Flask, request, jsonify
import audio, head_pose, detection
import threading as th

app = Flask(__name__)

@app.route('/start_detection', methods=['POST'])
def start_detection():
    data = request.get_json()
    # Process the data received from the client
    # You can access the video stream using data['streamData']

    # Example response
    response_data = {'message': 'Data received and processed successfully'}
    return jsonify(response_data)

if __name__ == '__main__':
    # Start audio, head pose, and detection threads
    head_pose_thread = th.Thread(target=head_pose.pose)
    audio_thread = th.Thread(target=audio.sound)
    detection_thread = th.Thread(target=detection.run_detection)

    # head_pose_thread.start()
    # audio_thread.start()
    # detection_thread.start()

    # Run the Flask app
    app.run(host='127.0.0.1', port=5000, debug=True)

    # Wait for threads to finish
    head_pose_thread.join()
    audio_thread.join()
    detection_thread.join()
