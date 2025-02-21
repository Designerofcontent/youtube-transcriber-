from youtube_transcript_api import YouTubeTranscriptApi
import json
import os
from urllib.parse import urlparse, parse_qs
import sys

def get_video_id(url):
    """Extract video ID from YouTube URL"""
    parsed_url = urlparse(url)
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        return parse_qs(parsed_url.query)['v'][0]
    elif parsed_url.hostname in ['youtu.be']:
        return parsed_url.path[1:]
    else:
        raise ValueError("Not a valid YouTube URL")

def get_transcript(url):
    try:
        video_id = get_video_id(url)
        
        # Get transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Create output directory if it doesn't exist
        if not os.path.exists('transcripts'):
            os.makedirs('transcripts')
        
        # Save as JSON
        json_path = f'transcripts/{video_id}_transcript.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(transcript, f, ensure_ascii=False, indent=2)
        
        # Save as raw text
        text_path = f'transcripts/{video_id}_transcript.txt'
        with open(text_path, 'w', encoding='utf-8') as f:
            for entry in transcript:
                f.write(f"{entry['text']}\n")
        
        print(f"Success! Transcript saved to:")
        print(f"JSON: {json_path}")
        print(f"Text: {text_path}")
        
        return json_path, text_path
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return None, None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python transcriber_cli.py <youtube_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    get_transcript(url)
