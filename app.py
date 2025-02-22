from flask import Flask, render_template, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = Flask(__name__)

def extract_video_id(youtube_url):
    """Extracts the video ID from a YouTube URL"""
    pattern = r"(?:v=|youtu\.be/|/v/|/embed/|/watch\?v=|/shorts/)([\w-]{11})"
    match = re.search(pattern, youtube_url)
    return match.group(1) if match else None

@app.route('/', methods=['GET', 'POST'])
def index():
    transcript = ""
    error = ""

    if request.method == 'POST':
        youtube_url = request.form['youtube_url']
        video_id = extract_video_id(youtube_url)

        if not video_id:
            error = "Invalid YouTube URL. Please try again."
        else:
            try:
                transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
                transcript = "\n".join([entry['text'] for entry in transcript_data])
            except Exception as e:
                error = f"Error fetching transcript: {str(e)}"

    return render_template('index.html', transcript=transcript, error=error)

@app.route('/api/transcript', methods=['POST'])
def get_transcript():
    data = request.get_json()
    youtube_url = data.get('youtube_url')
    
    if not youtube_url:
        return jsonify({'error': 'No URL provided'}), 400
        
    video_id = extract_video_id(youtube_url)
    
    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL'}), 400
        
    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        return jsonify({
            'transcript': transcript_data,
            'text': "\n".join([entry['text'] for entry in transcript_data])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
