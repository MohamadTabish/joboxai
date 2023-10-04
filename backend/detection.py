import time
import audio
import head_pose
import matplotlib.pyplot as plt
import numpy as np
import threading as th
import cv2

PLOT_LENGTH = 200

GLOBAL_CHEAT = 0
PERCENTAGE_CHEAT = 0
CHEAT_THRESH = 0.4
XDATA = list(range(200))
YDATA = [0] * 200
NO_FACE_CHEAT = 0

def avg(current, previous):
    if previous > 1:
        return 0.65
    if current == 0:
        if previous < 0.01:
            return 0.01
        return previous / 1.01
    if previous == 0:
        return current
    return 1 * previous + 0.1 * current

def process():
    global GLOBAL_CHEAT, PERCENTAGE_CHEAT, CHEAT_THRESH, NO_FACE_CHEAT
    if NO_FACE_CHEAT == 1 or head_pose.NO_FACE_CHEAT == 1:
        PERCENTAGE_CHEAT = avg(0.9, PERCENTAGE_CHEAT)  # Increase cheat level when face is not detected or camera feed is blank
        print("Face Not Detected (Cheating)")
    elif GLOBAL_CHEAT == 0:
        if head_pose.X_AXIS_CHEAT == 0:
            if head_pose.Y_AXIS_CHEAT == 0:
                if audio.AUDIO_CHEAT == 0:
                    PERCENTAGE_CHEAT = avg(0, PERCENTAGE_CHEAT)
                else:
                    PERCENTAGE_CHEAT = avg(0.2, PERCENTAGE_CHEAT)
            else:
                if audio.AUDIO_CHEAT == 0:
                    PERCENTAGE_CHEAT = avg(0.2, PERCENTAGE_CHEAT)
                else:
                    PERCENTAGE_CHEAT = avg(0.4, PERCENTAGE_CHEAT)
        else:
            if head_pose.Y_AXIS_CHEAT == 0:
                if audio.AUDIO_CHEAT == 0:
                    PERCENTAGE_CHEAT = avg(0.1, PERCENTAGE_CHEAT)
                else:
                    PERCENTAGE_CHEAT = avg(0.4, PERCENTAGE_CHEAT)
            else:
                if audio.AUDIO_CHEAT == 0:
                    PERCENTAGE_CHEAT = avg(0.15, PERCENTAGE_CHEAT)
                else:
                    PERCENTAGE_CHEAT = avg(0.25, PERCENTAGE_CHEAT)
    else:
        if head_pose.X_AXIS_CHEAT == 0:
            if head_pose.Y_AXIS_CHEAT == 0:
                if audio.AUDIO_CHEAT == 0:
                    PERCENTAGE_CHEAT = avg(0, PERCENTAGE_CHEAT)
                else:
                    PERCENTAGE_CHEAT = avg(0.55, PERCENTAGE_CHEAT)
            else:
                if audio.AUDIO_CHEAT == 0:
                    PERCENTAGE_CHEAT = avg(0.55, PERCENTAGE_CHEAT)
                else:
                    PERCENTAGE_CHEAT = avg(0.85, PERCENTAGE_CHEAT)
        else:
            if head_pose.Y_AXIS_CHEAT == 0:
                if audio.AUDIO_CHEAT == 0:
                    PERCENTAGE_CHEAT = avg(0.6, PERCENTAGE_CHEAT)
                else:
                    PERCENTAGE_CHEAT = avg(0.85, PERCENTAGE_CHEAT)
            else:
                if audio.AUDIO_CHEAT == 0:
                    PERCENTAGE_CHEAT = avg(0.5, PERCENTAGE_CHEAT)
                else:
                    PERCENTAGE_CHEAT = avg(0.85, PERCENTAGE_CHEAT)

    if PERCENTAGE_CHEAT > CHEAT_THRESH :
        GLOBAL_CHEAT = 1
        print("CHEATING..!!")
        if head_pose.X_AXIS_CHEAT == 1:
            print("Reason: Head Pose - Looking Right or Left")
        elif head_pose.Y_AXIS_CHEAT == 1:
            print("Reason: Head Pose - Looking Down")
        elif audio.AUDIO_CHEAT == 1:
            print("Reason: Audio - Suspicious Sound")
    else:
        GLOBAL_CHEAT = 0
    print("Cheat percent:", PERCENTAGE_CHEAT, "GLOBAL_CHEAT:", GLOBAL_CHEAT)

def run_detection():
    global XDATA, YDATA
    plt.show()
    axes = plt.gca()
    axes.set_xlim(0, 200)
    axes.set_ylim(0, 1)
    line, = axes.plot(XDATA, YDATA, 'r-')
    plt.title("Suspicious Behaviour Detection")
    plt.xlabel("Time")
    plt.ylabel("Cheat Probability")
    i = 0
    while True:
        YDATA.pop(0)
        YDATA.append(PERCENTAGE_CHEAT)
        line.set_xdata(XDATA)
        line.set_ydata(YDATA)
        plt.draw()
        plt.pause(1e-17)
        time.sleep(1 / 20)
        process()

def main():
    t1 = th.Thread(target=head_pose.pose)
    t1.start()
    t2 = th.Thread(target=run_detection)
    t2.start()

    # Check camera state
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Camera is switched off")
        head_pose.NO_FACE_CHEAT = 1
    else:
        ret, frame = camera.read()
        if not ret or cv2.countNonZero(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)) == 0:
            print("Camera Feed Blank (Cheating)")
            head_pose.NO_FACE_CHEAT = 1

    camera.release()

    t1.join()
    t2.join()

if __name__ == "_main_":
    main()