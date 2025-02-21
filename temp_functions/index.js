const functions = require('firebase-functions');
const admin = require('firebase-admin');
const { YoutubeTranscript } = require('youtube-transcript');
const cors = require('cors')({ origin: true });

admin.initializeApp();

exports.api = functions.https.onRequest((req, res) => {
  return cors(req, res, async () => {
    if (!req.body || !req.body.url) {
      return res.status(400).json({ error: 'URL is required' });
    }

    const url = req.body.url;
    let videoId;

    try {
      const urlObj = new URL(url);
      if (urlObj.hostname === 'youtu.be') {
        videoId = urlObj.pathname.substring(1);
      } else if (urlObj.hostname.includes('youtube.com')) {
        videoId = urlObj.searchParams.get('v');
      }

      if (!videoId) {
        throw new Error('Could not extract video ID');
      }

      const transcript = await YoutubeTranscript.fetchTranscript(videoId);
      const text = transcript.map(item => item.text).join('\n');
      return res.json({ transcript: text });
    } catch (error) {
      console.error('Error:', error);
      return res.status(400).json({ 
        error: 'Could not get transcript. Make sure the video exists and has captions enabled.'
      });
    }
  });
});
