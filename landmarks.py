import cv2
import mediapipe as mp


# ---------------------------------------------------------
# 1. Initialize MediaPipe Hands
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


print("Camera started.")
print("Show your hand.")
print("Press Q to quit.")


# ---------------------------------------------------------
# 3. Main Loop
# ---------------------------------------------------------

while True:

    success, frame = camera.read()

    if not success:
        print("Could not read camera frame.")
        break

    # Mirror the camera
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hand
    results = hands.process(rgb_frame)


    # -----------------------------------------------------
    # 4. Get Hand Landmarks
    # -----------------------------------------------------

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # Draw the hand
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )


            # -------------------------------------------------
            # 5. Get Wrist Coordinates
            # -------------------------------------------------

            wrist = hand_landmarks.landmark[0]

            wrist_x = wrist.x
            wrist_y = wrist.y

            print(
                f"Wrist -> X: {wrist_x:.2f}, "
                f"Y: {wrist_y:.2f}"
            )


            # -------------------------------------------------
            # 6. Get Index Finger Tip
            # -------------------------------------------------

            index_finger = hand_landmarks.landmark[8]

            index_x = index_finger.x
            index_y = index_finger.y

            print(
                f"Index Finger -> X: {index_x:.2f}, "
                f"Y: {index_y:.2f}"
            )

            print("------------------------")


    # -----------------------------------------------------
    # 7. Display Camera
    # -----------------------------------------------------

    cv2.imshow(
        "Phase 2 - Hand Landmarks",
        frame
    )


    # -----------------------------------------------------
    # 8. Quit
    # -----------------------------------------------------

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ---------------------------------------------------------
# 9. Release Resources
# ---------------------------------------------------------

camera.release()
cv2.destroyAllWindows()
hands.close()

print("Program stopped.")
