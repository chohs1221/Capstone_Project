from playsound import playsound
for i in range(3):
    playsound("./audios/cartout.wav")
    print("{}out".format(i))
    playsound("./audios/cartin.wav")
    print("{}in".format(i))
