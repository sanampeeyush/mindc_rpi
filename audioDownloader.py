from logge import generate_log as logger
logger('audio downloader file started')
from datetime import datetime
import requests

def get_audio():
    now = datetime.now()
    date = now.strftime("%d-%m-%Y")
    print(date)

    base_url = 'http://159.89.173.79:8000/media/audio_files/'
    path = '/home/pi/media/'
    count = 0
    attempt = 0
    success = True
    while success and count < 10 and attempt < 1:
        attempt += 1
        count = 0
        for i in range(1,11):
            ind = str(i).zfill(2)
            audio_file_url = f'{date}-{ind}.mp3'; audio_file = f'{ind}.mp3'
            print(audio_file)
            try:
                print(base_url+audio_file_url);resp = requests.get(base_url + audio_file_url)
                if resp.status_code == 200:
                    with open(path+audio_file,'wb') as f:
                        f.write(resp.content)
                        count += 1
                else:
                    print('File download failed')
                    continue
            except Exception as e:
                print('Network Error', e)
                logger(str(e))
    if count == 10:
        return True
    else:
        return False

if __name__ == '__main__':
    get_audio()
