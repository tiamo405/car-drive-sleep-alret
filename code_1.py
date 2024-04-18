import cv2          
from functools import wraps
#from pygame import mixer
import time

lastsave = 0


def counter(func):
    @wraps(func)
    def tmp(*args, **kwargs):
        tmp.count += 1
        global lastsave
        if time.time() - lastsave > 3:
            # this is in seconds, so 5 minutes = 300 seconds
            lastsave = time.time()
            tmp.count = 0
        return func(*args, **kwargs)
    tmp.count = 0
    return tmp

#loading the xml files
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')             #for the face

eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')                              #for the eye

cap = cv2.VideoCapture(0) #0 for default cam and 1 for external cam
frame_width = int(cap.get(3)) 
frame_height = int(cap.get(4)) 
   
size = (frame_width, frame_height) 
   
# Below VideoWriter object will create 
# a frame of above defined The output  
# is stored in 'filename.avi' file. 
output = cv2.VideoWriter('filename.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         10, size) 

@counter
def closed():       
  print ("Eye Closed")


def openeye():
  print ("Eye is Open")

#fumnction for alarm sound
'''
def sound():
    mixer.init()
    mixer.music.load('alarm.mp3')                            #loading the audio for alarm
    mixer.music.play()
'''

while 1:
    ret, img = cap.read()   #reading the videofeed
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #conversion to grayscale
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) #harcasscade

    #drawing rectangles around the face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

        #detecting eyes
        eyes = eye_cascade.detectMultiScale(roi_gray)


        #if eyes detected draw rectangle and declare eye open else closed
        if eyes is not ():
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                openeye()
        else:
           closed()
           if closed.count == 3:             #checking condition
                print ("driver is sleeping") 
               #sound()                      #sound the alarm
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 255, 0), 2)
                cv2.putText(roi_color, 'Nham Mat', (50,50), cv2.FONT_HERSHEY_SIMPLEX , 1, (255,255,0), 2, cv2.LINE_AA)
    output.write(roi_color)

    #show the frame window
    cv2.imshow('img', roi_color)
    k = cv2.waitKey(30) & 0xff

#free the camera and destroy the window
cap.release()
output.release()
cv2.destroyAllWindows()