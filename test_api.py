import requests
import json

url = 'https://youtube-to-text.vercel.app/api'  # Updated URL to use /api endpoint
data = {
    'url': 'https://www.youtube.com/watch?v=oiHMUEy-kpl'
}

response = requests.post(url, json=data)
print(f"Status Code: {response.status_code}")
print("Response:")
try:
    print(json.dumps(response.json(), indent=2))
except:
    print(response.text)
