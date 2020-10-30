import cv2

def spl():
    cap = cv2.VideoCapture(r'Crowd-Activity-All.avi')
    start, end = 7658,7738
    print "Here"
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('3_test3.avi',fourcc, 30.0, (320, 240))
    cap.set(cv2.CAP_PROP_POS_FRAMES , start)
    while end-start>0:
        print "loop"
        ret, frame = cap.read()
        frame = cv2.resize(frame,(320, 240))
        out.write(frame)
        #cv2.imshow('frame', frame)
        #cv2.waitKey(1)
        start+=1
    cap.release()
    out.release()
    cv2.destroyAllWindows()

spl()
