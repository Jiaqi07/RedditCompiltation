import praw
from moviepy.video.tools.subtitles import SubtitlesClip
from redvid import Downloader
from moviepy.editor import *
import os
import datetime
from Google import Create_Service
from googleapiclient.http import MediaFileUpload

r = praw.Reddit(client_id="---", client_secret="---",
                user_agent="Jiaqi07")

reddit = Downloader(max_q=True)
redditClips = []
redditDelete = []
redditTitles = []
i = 1

for submission in r.subreddit("VALORANT").top(time_filter="week"):
    if submission.is_video and submission.score > 900 and submission.media["reddit_video"]["duration"] < 60:
        print(str(submission.title) + ': ' + str(submission))

        reddit.max = True
        reddit.url = submission.url
        reddit.download()

        os.rename(reddit.file_name, 'Clip ' + str(i) + '.mp4')
        i += 1

        redditClips.append(VideoFileClip('Clip ' + str(i - 1) + '.mp4'))
        redditDelete.append('Clip ' + str(i - 1) + '.mp4')
        print('Clip ' + str(i - 1) + '.mp4')

        redditTitles.append(str(submission.title) + '.mp4')

video = concatenate_videoclips(redditClips, method='compose')

# for caption in redditTitles:
#     txt_clip = TextClip(caption[0:len(caption) - 3], fontsize=70, color='white').set_position('bottom').set_duration(5)
#     result = CompositeVideoClip([video, txt_clip])  # Overlay text on video
#     video = result
# FIGURE OUT SUBTITLES LATER

video.write_videofile("RedditCompilation.mp4", fps=60)

# YOUTUBE UPLOADER
CLIENT_SECRET_FILE = 'ClientSecretFile.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

upload_date_time = datetime.datetime(2022, 6, 24, 16, 30, 0).isoformat() + '.000Z'

request_body = {
    'snippet': {
        'categoryI': 20,
        'title': 'Best of Reddit - Compilation 1',
        'description': 'All clips were taken from Reddit',
        'tags': ['Valorant', 'Valorant Clips', 'Riot']
    },
    'status': {
        'privacyStatus': 'private',
        'publishAt': upload_date_time,
        'selfDeclaredMadeForKids': False,
    },
    'notifySubscribers': False
}

mediaFile = MediaFileUpload("RedditCompilation.mp4")

response_upload = service.videos().insert(
    part='snippet,status',
    body=request_body,
    media_body=mediaFile
).execute()

service.thumbnails().set(
    videoId=response_upload.get('id'),
    media_body=MediaFileUpload('thumnail.PNG')
).execute()

for x in redditDelete:
    os.remove(x)
