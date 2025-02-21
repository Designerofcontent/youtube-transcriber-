const functions = require('firebase-functions');
const fetch = require('node-fetch');

exports.api = functions.https.onRequest(async (request, response) => {
  response.set('Access-Control-Allow-Origin', '*');
  response.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  response.set('Access-Control-Allow-Headers', 'Content-Type');

  if (request.method === 'OPTIONS') {
    response.status(204).send('');
    return;
  }

  try {
    const { url } = request.body;
    if (!url) {
      return response.status(400).json({ error: 'URL is required' });
    }

    // Extract video ID
    const videoIdMatch = url.match(/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/);
    if (!videoIdMatch) {
      return response.status(400).json({ error: 'Invalid YouTube URL' });
    }

    const videoId = videoIdMatch[1];
    
    try {
      // Try to get captions directly
      const captionsUrl = `https://www.youtube.com/api/timedtext?lang=en&v=${videoId}`;
      const captionsResponse = await fetch(captionsUrl);
      const captionsText = await captionsResponse.text();
      
      if (!captionsText || captionsText.trim() === '') {
        throw new Error('No captions available');
      }

      // Parse XML
      const lines = captionsText.match(/<text[^>]*>(.*?)<\/text>/g);
      if (!lines) {
        throw new Error('No captions found');
      }

      const transcript = lines
        .map(line => {
          const text = line.match(/<text[^>]*>(.*?)<\/text>/)[1];
          return decodeURIComponent(text.replace(/&#39;/g, "'").replace(/&quot;/g, '"'));
        })
        .join('\n');

      return response.json({ transcript });
    } catch (error) {
      console.error('Caption Error:', error);
      return response.status(400).json({
        error: 'Could not get transcript. Make sure the video exists and has captions enabled.'
      });
    }
  } catch (error) {
    console.error('Server Error:', error);
    return response.status(500).json({ error: 'Server error' });
  }
});
