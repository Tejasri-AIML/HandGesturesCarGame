import cv2
import mediapipe as mp


# ---------------------------------------------------------
# 1. Initialize MediaPipe
# ---------------------------------------------------------

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


# ---------------------------------------------------------
# 2. Open Webcam
# ---------------------------------------------------------

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Could not open webcam.")
    exit()


# ---------------------------------------------------------
# 3. Function to Detect Gesture
# ---------------------------------------------------------

def detect_gesture(landmarks):
    """
    Detect a simple hand gesture using landmark positions.
    """

    # Get important fingertip landmarks
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    little_tip = landmarks[20]

    # Get finger joint landmarks
    index_pip = landmarks[6]
    middle_pip = landmarks[10]
    ring_pip = landmarks[14]
    little_pip = landmarks[18]


    # -----------------------------------------------------
    # Determine whether fingers are UP
    # -----------------------------------------------------

    index_up = index_tip.y < index_pip.y
    middle_up = middle_tip.y < middle_pip.y
    ring_up = ring_tip.y < ring_pip.y
    little_up = little_tip.y < little_pip.y


    # -----------------------------------------------------
    # Count raised fingers
    # -----------------------------------------------------

    fingers_up = sum([
        index_up,
        middle_up,
        ring_up,
        little_up
    ])


    # -----------------------------------------------------
    # Recognize gestures
    # -----------------------------------------------------

    # ✋ Four fingers raised
    if fingers_up == 4:
        return "OPEN PALM"


    # ✊ No fingers raised
    elif fingers_up == 0:
        return "FIST"


    # ☝️ Only index finger raised
    elif fingers_up == 1 and index_up:
        return "INDEX"


    # ✌️ Index + middle fingers raised
    elif fingers_up == 2 and index_up and middle_up:
        return "TWO FINGERS"


    # Otherwise
    else:
        return "UNKNOWN"


# ---------------------------------------------------------
# 4. Main Loop
# ---------------------------------------------------------

while True:

    success, frame = camera.read()

    if not success:
        print("Could not read camera frame.")
        break


    # Mirror camera
    frame = cv2.flip(frame, 1)


    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    # Detect hand
    results = hands.process(rgb_frame)


    gesture = "NO HAND"


    # -----------------------------------------------------
    # 5. Process Detected Hand
    # -----------------------------------------------------

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # Draw landmarks
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )


            # Convert landmarks into a list
            landmarks = hand_landmarks.landmark


            # Detect gesture
            gesture = detect_gesture(landmarks)


    # -----------------------------------------------------
    # 6. Display Gesture on Screen
    # -----------------------------------------------------

    cv2.putText(
        frame,
        f"Gesture: {gesture}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )


    # Show camera
    cv2.imshow(
        "Phase 3 - Gesture Recognition",
        frame
    )


    # -----------------------------------------------------
    # 7. Quit
    # -----------------------------------------------------

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ---------------------------------------------------------
# 8. Release Resources
# ---------------------------------------------------------

camera.release()
cv2.destroyAllWindows()
hands.close()

print("Gesture recognition stopped.")

