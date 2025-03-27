from flask import Flask, render_template
import requests
import random

app = Flask(__name__)

API_KEY = 'API_KEY' 
SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'

def get_random_video():
    params = {
        'part': 'snippet',
        'maxResults': 50,
        'order': 'viewCount',
        'type': 'video',
        'key': API_KEY
    }
    response = requests.get(SEARCH_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        videos = data['items']
        random_video = random.choice(videos)
        video_id = random_video['id']['videoId']
        title = random_video['snippet']['title']
        return title, f'https://www.youtube.com/watch?v={video_id}'
    return None, None

@app.route('/')
def index():
    video_title, video_url = get_random_video()
    return render_template('index.html', video_title=video_title, video_url=video_url)

if __name__ == '__main__':
    app.run(port=8080)
