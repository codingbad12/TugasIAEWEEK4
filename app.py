from flask import Flask, render_template, request
import requests
import random
import string

app = Flask(__name__)

API_KEY = 'API_KEY'
SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'

# Filter
CATEGORIES = {
    'music': 'music',
    'gaming': 'gaming',
    'tech': 'technology'
}

DURATIONS = {
    'short': 'short',    # <4 menit
    'medium': 'medium',  # 4-20 menit
    'long': 'long'       # >20 menit
}

def get_random_video(category=None, duration=None):
    random_query = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
    
    params = {
        'part': 'snippet',
        'maxResults': 30,
        'order': 'viewCount',
        'type': 'video',
        'key': API_KEY,
        'q': f'{random_query} {CATEGORIES.get(category, "")}',
        'videoDuration': DURATIONS.get(duration, None)  # Duration
    }

    # Hapus parameter yang None/nulls
    params = {k: v for k, v in params.items() if v is not None}
    
    response = requests.get(SEARCH_URL, params=params)
    if response.status_code == 200:
        videos = response.json().get('items', [])
        return random.choice(videos)['id']['videoId'] if videos else None
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    category = request.form.get('category')
    duration = request.form.get('duration')
    
    video_id = get_random_video(category, duration)
    
    return render_template('index.html',
                         video_id=video_id,
                         categories=CATEGORIES,
                         durations=DURATIONS)

if __name__ == '__main__':
    app.run(port=8080)
