import urllib.request
import json
import re
import moviepy.editor as mpe
import os


def cut_legs(string):
    x = string.find('?source=fallback')
    return string[0:x]


def replace_url(string):
    x = re.findall('DASH_[0-9]+', string)
    y = x[0][5:]
    return string.replace(y, 'audio')


def combine_audio(vidname, audname, outname, fps=30):
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname, fps=fps)


def validate(url):
    url_split = url.split('/')
    json_url = url[0:-1] + '.json'
    if len(url_split) == 9:
        return json_url
    return False


def download(reddit_url):
    print(
        'Validating URL'
    )
    if validate(reddit_url):
        try:
            # ---------------------------------------------------------------------------
            # Get fallback_url from JSON
            print(
                'Geting fallback_url from JSON'
            )
            get_data = urllib.request.urlopen(validate(reddit_url))
            data = json.loads(get_data.read().decode())
            fallback_url = data[0]["data"]["children"][0]["data"]["secure_media"]
            # ---------------------------------------------------------------------------
            # Check if its video
            print(
                'Checking if its video'
            )
            if fallback_url is None:
                return False
            # ---------------------------------------------------------------------------
            # Get video and audio URL
            print(
                'Downloading fallback_url from JSON'
            )
            video = cut_legs(fallback_url["reddit_video"]["fallback_url"])
            fallback_audio = replace_url(fallback_url["reddit_video"]["fallback_url"])
            audio = cut_legs(fallback_audio)
            # ---------------------------------------------------------------------------
            # Download video and audio
            urllib.request.urlretrieve(video, 'video.mp4')
            urllib.request.urlretrieve(audio, 'audio.mp4')
            # ---------------------------------------------------------------------------
            # Combine audio/video
            print(
                'Combining audio and video'
            )
            combine_audio('video.mp4', 'audio.mp4', (reddit_url.split('/')[7] + '.mp4'))
            # ---------------------------------------------------------------------------
            # Delete unnecessary files
            print(
                'Removing any unnecessary files'
            )
            os.remove('video.mp4')
            os.remove('audio.mp4')
            return True
            # ---------------------------------------------------------------------------
        except Exception as e:
            print(e)
    print('Wrong URL')
    return False


if __name__ == "__main__":
    rdt = input('Pass URL here\n> ')
    if download(rdt):
        print('Download completed!')
    else:
        print('An error has occured!')
