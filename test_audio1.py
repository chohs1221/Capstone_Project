from playsound import playsound
import threading

def audio(num):
    audio_name = '/home/robit/VS_workspace/capstone/audios/audio_' + str(num) + '.wav'
    try:
        threading.Thread(target=playsound, args=(audio_name,), daemon=False).start()
    except:
        pass
for i in range(2):
    audio(i)