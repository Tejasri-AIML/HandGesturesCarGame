import cv2
import mediapipe as mp

# --------------------------------------------------
# STEP 1: Setup MediaPipe
# --------------------------------------------------

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# --------------------------------------------------
# STEP 2: Open the webcam
# --------------------------------------------------

camera = cv2.VideoCapture(0)

# --------------------------------------------------
# STEP 3: Function to find hand direction
# --------------------------------------------------

def get_hand_direction(landmarks):

    # Get important palm landmarks
    wrist = landmarks[0]
    index_mcp = landmarks[5]
    middle_mcp = landmarks[9]
    ring_mcp = landmarks[13]
    pinky_mcp = landmarks[17]

    # Calculate the average X position of the palm
    palm_x = (
        wrist.x +
        index_mcp.x +
        middle_mcp.x +
        ring_mcp.x +
        pinky_mcp.x
    ) / 5

    # Divide the camera into 3 zones
    if palm_x < 0.35:
        direction = "LEFT"

    elif palm_x > 0.65:
        direction = "RIGHT"

    else:
        direction = "CENTER"

    return direction, palm_x


# --------------------------------------------------
# STEP 4: Main webcam loop
# --------------------------------------------------

while True:

    success, frame = camera.read()

    if not success:
        print("Could not access the camera.")
        break

    # Flip the camera so it behaves like a mirror
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hand
    results = hands.process(rgb_frame)

    direction = "NO HAND"

    # --------------------------------------------------
    # STEP 5: If a hand is detected
    # --------------------------------------------------

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # Draw the 21 hand landmarks
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Get direction
            direction, palm_x = get_hand_direction(
                hand_landmarks.landmark
            )

            # Display X coordinate
            cv2.putText(
                frame,
                f"X Position: {palm_x:.2f}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

    # --------------------------------------------------
    # STEP 6: Display direction
    # --------------------------------------------------

    cv2.putText(
        frame,
        f"Direction: {direction}",
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 255, 0),
        3
    )

    # Show camera
    cv2.imshow("Hand Direction Detection", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# --------------------------------------------------
# STEP 7: Close everything
# --------------------------------------------------

camera.release()
cv2.destroyAllWindows()