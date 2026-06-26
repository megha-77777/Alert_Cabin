import time
from scipy.spatial import distance

YAWN_THRESHOLD = 0.065
YAWN_TIME_LIMIT = 1.5

yawn_start = None

def process_yawn(lm, current_time):
    global yawn_start

    top = lm[13]
    bottom = lm[14]

    mouth_dist = distance.euclidean(
        (top.x, top.y),
        (bottom.x, bottom.y)
    )

    face_height = distance.euclidean(
        (lm[10].x, lm[10].y),
        (lm[152].x, lm[152].y)
    )

    mouth_ratio = mouth_dist / face_height

    status = "ACTIVE"
    score = 0

    if mouth_ratio > YAWN_THRESHOLD:
        if yawn_start is None:
            yawn_start = current_time

        if current_time - yawn_start > YAWN_TIME_LIMIT:
            status = "YAWNING"
            score = 1
    else:
        yawn_start = None

    return mouth_ratio, status, score
