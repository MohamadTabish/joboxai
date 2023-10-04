import time
from audio import sound
from head_pose import pose
from detection import run_detection

if __name__ == "__main__":
    head_pose_thread = pose()
    audio_thread = sound()

    head_pose_thread.start()
    audio_thread.start()

    head_pose_thread.join()
    audio_thread.join()
