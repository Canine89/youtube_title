import os
import google_auth_oauthlib.flow
import googleapiclient.discovery

# API 키 또는 OAuth 2.0 인증 정보 설정
API_KEY = 'asdasdfdfs-jsnsadfdsfafdsfsdafdsfads8rE'  # 자신의 API 키로 교체
# CLIENT_SECRETS_FILE = 'client_secret.json'  # 자신의 인증 정보 파일로 교체

# YouTube API 클라이언트 생성
def create_youtube_client(api_key=None):
    api_service_name = 'youtube'
    api_version = 'v3'

    if api_key:
        youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, ['https://www.googleapis.com/auth/youtube.readonly']
        )
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    return youtube

# 채널의 모든 동영상 제목 가져오기
def get_all_video_titles(channel_id, api_key=None):
    youtube = create_youtube_client(api_key)
    
    # 플레이리스트 ID 가져오기
    playlists = youtube.channels().list(part='contentDetails', id=channel_id).execute()
    playlist_id = playlists['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    video_titles = []
    next_page_token = None

    while True:
        playlist_items = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,  # 가져올 최대 동영상 수 (기본값: 5, 최대: 50)
            pageToken=next_page_token
        ).execute()

        video_titles.extend(item['snippet']['title'] for item in playlist_items['items'])

        next_page_token = playlist_items.get('nextPageToken')
        if not next_page_token:
            break

    return video_titles

# 채널 ID를 얻는 방법: https://support.google.com/youtube/answer/3250431?hl=en
channel_id = 'Uasdffadsdfasdsfafdsaafsdg'  # 예시 채널 ID, 자신의 채널 ID로 교체

# 동영상 제목 가져오기
video_titles = get_all_video_titles(channel_id, API_KEY)

# 결과 출력
for i, title in enumerate(video_titles, start=1):
    print(f"{i}. {title}")
