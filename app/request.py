import urllib.request, json
from .models import Videos

def get_videos():
    get_videos_url = 'https://youtube-videos.p.rapidapi.com/mp4'
    get_videos_data = urllib.request.urlopen(get_videos_url)
    get_videos_response = json.loads(get_videos_data.read())

    url = get_videos_response.get('url')

    new_videos = Videos(url)
    return new_videos