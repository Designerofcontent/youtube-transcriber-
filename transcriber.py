        import customtkinter as ctk
from youtube_transcript_api import YouTubeTranscriptApi
import json
import re
import os
from urllib.parse import urlparse, parse_qs

class TranscriberApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("YouTube Transcriber")
        self.window.geometry("600x400")
        
        # URL Input
        self.url_label = ctk.CTkLabel(self.window, text="Enter YouTube URL:")
        self.url_label.pack(pady=10)
        
        self.url_entry = ctk.CTkEntry(self.window, width=400)
        self.url_entry.pack(pady=5)
        
        # Buttons
        self.transcribe_button = ctk.CTkButton(self.window, text="Get Transcript", command=self.transcribe)
        self.transcribe_button.pack(pady=20)
        
        # Status
        self.status_label = ctk.CTkLabel(self.window, text="")
        self.status_label.pack(pady=10)

    def get_video_id(self, url):
        """Extract video ID from YouTube URL"""
        parsed_url = urlparse(url)
        if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
            return parse_qs(parsed_url.query)['v'][0]
        elif parsed_url.hostname in ['youtu.be']:
            return parsed_url.path[1:]
        else:
            raise ValueError("Not a valid YouTube URL")

    def transcribe(self):
        try:
            url = self.url_entry.get()
            video_id = self.get_video_id(url)
            
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
            
            self.status_label.configure(text=f"Transcript saved!\nJSON: {json_path}\nText: {text_path}")
            
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = TranscriberApp()
    app.run()
