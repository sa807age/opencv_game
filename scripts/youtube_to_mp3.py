from pytube import YouTube
import os
from pathlib import Path


def youtube2mp3 (url,outdir):
    # url input from user
    yt = YouTube(url)

    # Extract audio with 160kbps quality from video
    video = yt.streams.filter(abr='160kbps').last()

    # Download the file
    out_file = video.download(output_path=outdir)
    base, ext = os.path.splitext(out_file)
    new_file = Path(f'{base}.mp3')
    os.rename(out_file, new_file)
    # Check success of download
    if new_file.exists():
        print(f'{yt.title} has been successfully downloaded.')
    else:
        print(f'ERROR: {yt.title}could not be downloaded!')


output_dir = sounds_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'sounds'))
sound_name = ''
youtube2mp3('https://www.youtube.com/watch?v=gCGp0tSr2tA', os.path.join(output_dir))
