from playsound import playsound
import threading

def audio(num):
    path = '/home/robit/VS_workspace/capstone/audios/'
    # path = './'
    audio_name = path + 'audio_' + str(num) + '.wav'
    try:
        threading.Thread(target=playsound, args=(audio_name,), daemon=False).start()
    except:
        pass

if __name__ == '__main__':
    audio(1) 