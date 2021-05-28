from playsound import playsound
import threading
for i in range(3):
    threading.Thread(target=playsound, args=('./audios/cartout.wav',), daemon=False).start()
    print("{}out".format(i))
    threading.Thread(target=playsound, args=('./audios/cartin.wav',), daemon=False).start()
    print("{}in".format(i))
