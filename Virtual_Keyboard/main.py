import cv2
import HandTracking as ht
from time import sleep
from pynput.keyboard import Controller
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = ht.handDetector(detectionCon=0.8)
keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]
    ]
result = ''
keyboard = Controller()
def draw(butList, frame):
    for button in butList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(frame, button.pos, (x+w, y+h), (255,0,255), cv2.FILLED)
        cv2.putText(frame, button.text, (x+15, y+70), cv2.FONT_HERSHEY_PLAIN, 5, (255,255,255), 4)
    return frame

class Button():
    def __init__(self, pos, text, size=[85,85]):
        self.pos = pos
        self.size = size
        self.text = text

butList = []
for j in range(len(keys)):
    for i,key in enumerate(keys[j]):
        butList.append(Button([100*i+50,100*j+50], key))

while True: 
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = detector.findHands(frame)
    lmlist, bbox = detector.findPositions(frame)
    frame = draw(butList, frame)

    if lmlist:
        for button in butList:
            x, y = button.pos
            w,h = button.size
            if x < lmlist[8][0] < x+w and y < lmlist[8][1] < y+h:
                cv2.rectangle(frame, button.pos, (x+w, y+h), (175,0,175), cv2.FILLED)
                cv2.putText(frame, button.text, (x+15, y+70), cv2.FONT_HERSHEY_PLAIN, 5, (255,255,255), 4)
                l,_,_ =  detector.findDistances(8,12,frame, draw=False)
                if l < 30:
                    cv2.rectangle(frame, button.pos, (x+w, y+h), (0,255,0), cv2.FILLED)
                    cv2.putText(frame, button.text, (x+15, y+70), cv2.FONT_HERSHEY_PLAIN, 5, (255,255,255), 4)
                    result += button.text
                    keyboard.press(button.text)
                    sleep(0.2)
    cv2.rectangle(frame, (50, 350), (700, 450), (175,0,175), cv2.FILLED)
    cv2.putText(frame, result, (60,425), cv2.FONT_HERSHEY_PLAIN, 5, (255,255,255), 4)


    cv2.imshow("Virtual KeyBoard", frame)
    k = cv2.waitKey(10)
    if k == ord('q'):
        break
cv2.destroyAllWindows()
cap.release()