from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import json

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

def handler(event, context):
    if event['request']['method'] == 'GET':
        return {
            'statusCode': 200,
            'body': json.dumps({
                'status': 'ok',
                'message': 'YouTube Transcriber API is running. Send a POST request with a YouTube URL to get the transcript.',
                'example': {
                    'method': 'POST',
                    'content-type': 'application/json',
                    'body': {
                        'url': 'https://www.youtube.com/watch?v=VIDEO_ID'
                    }
                }
            })
        }
    
    elif event['request']['method'] == 'POST':
        try:
            body = json.loads(event['body'])
            url = body.get('url')
            
            if not url:
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        'success': False,
                        'error': 'URL is required'
                    })
                }

            video_id = get_video_id(url)
            if not video_id:
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        'success': False,
                        'error': 'Invalid YouTube URL'
                    })
                }

            # Get transcript
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Format transcript for response
            formatted_transcript = '\n'.join([entry['text'] for entry in transcript])
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'success': True,
                    'transcript': formatted_transcript,
                    'video_id': video_id
                })
            }
            
        except Exception as e:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'success': False,
                    'error': str(e)
                })
            }
    
    return {
        'statusCode': 405,
        'body': json.dumps({
            'success': False,
            'error': 'Method not allowed'
        })
    }
