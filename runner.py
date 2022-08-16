import re
from pytube import Playlist, YouTube
import subprocess
import os

YOUTUBE_STREAM_AUDIO = '140' # modify the value to download a different stream
DOWNLOAD_DIR = os.path.expanduser('~/Downloads') 

playlist = Playlist('https://www.youtube.com/playlist?list=PLU8-xwslFxH9NwboeEdiYOwWyZX6uCks9')

# this fixes the empty playlist.videos list
playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
album = playlist.title

print(len(playlist.video_urls))

for url in playlist.video_urls:
    print(url)
i = 0
# physically downloading the audio track
for video in playlist.videos:
    i +=1
    nome = ''.join(e for e in video.title if e.isalnum())
    new_filename=os.path.join(DOWNLOAD_DIR, nome+'.mp3')
    default_filename =os.path.join(DOWNLOAD_DIR, nome+'.mp4')
    author = video.author
    title = video.title
    track = i

    audioStream = video.streams.get_by_itag(YOUTUBE_STREAM_AUDIO)
    audioStream.download(output_path=DOWNLOAD_DIR, filename=default_filename)
    
    cmd = [
    '-i', default_filename,
    '-metadata artist=%s' % author,
    '-metadata album=%s' % album,
    '-metadata title="%s"' % title,
    '-metadata track=%s' %track,
    '-y', new_filename,
    ]
    
    subprocess.run(["ffmpeg" +"".join(" %s" % s for s in cmd)], shell=True)

print('Download Complete')