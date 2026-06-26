import cv2
import mediapipe as mp
import time

from eye import process_eyes
from yawn import process_yawn
from alarm import init_alarm, start_alarm, stop_alarm

# -----------------------
# INIT
# -----------------------
init_alarm()

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

cap = cv2.VideoCapture(0)

score = 0

# -----------------------
# LOOP
# -----------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    status = "ACTIVE"
    current_time = time.time()

    if results.multi_face_landmarks:
        lm = results.multi_face_landmarks[0].landmark

        # ---------------- EYE MODULE ----------------
        ear, eye_time, eye_status, eye_score = process_eyes(
            lm, w, h, LEFT_EYE, RIGHT_EYE, current_time
        )

        # ---------------- YAWN MODULE ----------------
        mouth_ratio, yawn_status, yawn_score = process_yawn(lm, current_time)

        # ---------------- SCORE ----------------
        score += eye_score + yawn_score
        score = max(0, score - 0.2)

        # ---------------- STATUS ----------------
        if eye_status == "EYES CLOSED":
            status = "SLEEPY"
        if yawn_status == "YAWNING":
            status = "YAWNING"

        # ---------------- ALARM ----------------
        if score > 15:
            status = "DROWSY ALERT!"
            start_alarm()
        else:
            stop_alarm()

        # ---------------- UI ----------------
        cv2.putText(frame, f"EAR: {ear:.2f}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        cv2.putText(frame, f"Score: {int(score)}", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        cv2.putText(frame, f"Eye Time: {eye_time:.1f}s", (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 0), 2)

        cv2.putText(frame, status, (20, 160),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow("Driver Monitor", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# -----------------------
# CLEANUP
# -----------------------
stop_alarm()
cap.release()
cv2.destroyAllWindows()
face_mesh.close()
