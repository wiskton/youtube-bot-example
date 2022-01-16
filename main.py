from googleapiclient.discovery import build
import google_auth_oauthlib.flow
import random

DEVELOPER_KEY = ''
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
client_secrets_file = "client_secret.json"

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


get_video('J0ZYt6zNTOM')
get_comments('J0ZYt6zNTOM')

# comentar um vídeo

def auth():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)
    return youtube

youtube = auth()

list_comments = [
    ';)',
    ':)',
    'gostei do video',
    'boaaaaaaaaaaaa'
]

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

set_comment('J0ZYt6zNTOM', random.choice(list_comments))