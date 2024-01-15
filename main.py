from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import google_auth_oauthlib.flow
from PIL import Image
import random

DEVELOPER_KEY = ''
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
client_secrets_file = "client_secret.json"
video_id = 'il_BgisEi6E'
thumbnail_name = 'teste.jpeg'

list_comments = [
    ';)',
    ':)',
    'gostei do video',
    'boaaaaaaaaaaaa'
]

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)


def get_comments(video_id):

    list_comments = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id
    ).execute()

    print(list_comments)

    for comment in list_comments['items']:
        com = comment['snippet']['topLevelComment']['snippet']

        print('{}: {}'.format(com['authorDisplayName'], com['textOriginal']))
        print("-"*100)


def get_video(video_id):
    list_videos = youtube.videos().list(
        id = video_id, 
        part="id,snippet,contentDetails, statistics",
    ).execute()

    results = list_videos.get("items", [])

    for result in results:
        print(result['snippet']['title'])
        print(result['statistics']['likeCount'])


def auth():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)
    return youtube


def set_comment(video_id, comment_text):
    insert_text = youtube.commentThreads().insert(
        part='snippet',
        body={
            'snippet': {
                'videoId': video_id,
                'topLevelComment': {
                    'snippet': {
                        'textOriginal': comment_text
                    }
                }
            }
        }
    )
    insert_text.execute()


if __name__ == "__main__":
    youtube = auth()

    # pegar infos do vídeo
    get_video(video_id)

    # pegar os comentários do vídeo
    get_comments(video_id)

    # comentar um vídeo
    set_comment(video_id, random.choice(list_comments))

    # alterar a thumbnail
    youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(thumbnail_name, mimetype='image/jpeg', resumable=True)
    ).execute()