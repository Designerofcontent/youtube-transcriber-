from flask import Flask, render_template, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import json
import os

app = Flask(__name__)

def get_video_id(url):
    """Extract video ID from YouTube URL"""
    try:
        parsed_url = urlparse(url)
        if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
            return parse_qs(parsed_url.query)['v'][0]
        elif parsed_url.hostname in ['youtu.be']:
            return parsed_url.path[1:]
        else:
            raise ValueError("Not a valid YouTube URL")
    except:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_transcript', methods=['POST'])
def get_transcript():
    try:
        url = request.form['url']
        video_id = get_video_id(url)
        
        if not video_id:
            return jsonify({'error': 'Invalid YouTube URL'})

        # Get transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Create output directory if it doesn't exist
        if not os.path.exists('transcripts'):
            os.makedirs('transcripts')
        
        # Save as JSON
        json_path = f'transcripts/{video_id}_transcript.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(transcript, f, ensure_ascii=False, indent=2)
        
        # Save as text
        text_path = f'transcripts/{video_id}_transcript.txt'
        with open(text_path, 'w', encoding='utf-8') as f:
            for entry in transcript:
                f.write(f"{entry['text']}\n")

        # Format transcript for display
        formatted_transcript = '\n'.join([entry['text'] for entry in transcript])
        
        return jsonify({
            'success': True,
            'transcript': formatted_transcript,
            'json_path': json_path,
            'text_path': text_path
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
