from scipy.spatial import distance
import time
import cv2

# ---------------- MATH ----------------
def euclidean(p1, p2):
    return distance.euclidean(p1, p2)


def eye_aspect_ratio(eye):
    A = euclidean(eye[1], eye[5])
    B = euclidean(eye[2], eye[4])
    C = euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

# ---------------- TIME ----------------
def now():
    return time.time()


def elapsed(start):
    return time.time() - start

# ---------------- VIDEO ----------------
def flip_frame(frame):
    return cv2.flip(frame, 1)
