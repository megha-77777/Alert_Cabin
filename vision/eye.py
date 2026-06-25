import time
from utils import eye_aspect_ratio

EAR_THRESHOLD = 0.18
CLOSED_SECONDS_LIMIT = 3
FRAME_CHECK = 10

closed_frames = 0
closed_start = None

def process_eyes(lm, w, h, LEFT_EYE, RIGHT_EYE, current_time):
    global closed_frames, closed_start

    left_eye = [(int(lm[i].x * w), int(lm[i].y * h)) for i in LEFT_EYE]
    right_eye = [(int(lm[i].x * w), int(lm[i].y * h)) for i in RIGHT_EYE]

    ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0

    eye_closed_duration = 0
    status = "ACTIVE"
    score = 0

    if ear < EAR_THRESHOLD:
        closed_frames += 1
        if closed_start is None:
            closed_start = current_time
        eye_closed_duration = current_time - closed_start
    else:
        closed_frames = 0
        closed_start = None
        eye_closed_duration = 0

    if closed_frames > FRAME_CHECK and eye_closed_duration > CLOSED_SECONDS_LIMIT:
        status = "EYES CLOSED"
        score = 1

    return ear, eye_closed_duration, status, score
