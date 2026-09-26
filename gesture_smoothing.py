import cv2
import mediapipe as mp
from collections import deque

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
# STEP 2: Open webcam
# --------------------------------------------------

camera = cv2.VideoCapture(0)

# --------------------------------------------------
# STEP 3: Store recent directions
# --------------------------------------------------

# We will remember the last 7 directions
direction_history = deque(maxlen=7)


# --------------------------------------------------
# STEP 4: Find hand direction
# --------------------------------------------------

def get_hand_direction(landmarks):

    # Important palm landmarks
    wrist = landmarks[0]
    index_mcp = landmarks[5]
    middle_mcp = landmarks[9]
    ring_mcp = landmarks[13]
    pinky_mcp = landmarks[17]

    # Calculate average X position of the palm
    palm_x = (
        wrist.x +
        index_mcp.x +
        middle_mcp.x +
        ring_mcp.x +
        pinky_mcp.x
    ) / 5

    # Divide camera into three zones

    if palm_x < 0.35:
        direction = "LEFT"

    elif palm_x > 0.65:
        direction = "RIGHT"

    else:
        direction = "CENTER"

    return direction, palm_x


# --------------------------------------------------
# STEP 5: Smooth the direction
# --------------------------------------------------

def get_stable_direction():

    if len(direction_history) == 0:
        return "NO HAND"

    # Count how many times each direction appears
    left_count = direction_history.count("LEFT")
    center_count = direction_history.count("CENTER")
    right_count = direction_history.count("RIGHT")

    # Find the direction with the highest count
    counts = {
        "LEFT": left_count,
        "CENTER": center_count,
        "RIGHT": right_count
    }

    stable_direction = max(counts, key=counts.get)

    return stable_direction


# --------------------------------------------------
# STEP 6: Main webcam loop
# --------------------------------------------------

while True:

    success, frame = camera.read()

    if not success:
        print("Could not access the camera.")
        break

    # Mirror the camera
    frame = cv2.flip(frame, 1)

    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # Detect hand
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # Draw hand landmarks
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Find current direction
            direction, palm_x = get_hand_direction(
                hand_landmarks.landmark
            )

            # Add current direction to history
            direction_history.append(direction)

            # Get stable direction
            stable_direction = get_stable_direction()

            # Display X position
            cv2.putText(
                frame,
                f"X Position: {palm_x:.2f}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

            # Display current direction
            cv2.putText(
                frame,
                f"Current: {direction}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

            # Display stable direction
            cv2.putText(
                frame,
                f"Stable: {stable_direction}",
                (20, 125),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.1,
                (0, 255, 0),
                3
            )

    else:
        # No hand detected
        direction_history.clear()

        cv2.putText(
            frame,
            "NO HAND",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.1,
            (0, 0, 255),
            3
        )

    # Show webcam
    cv2.imshow(
        "Gesture Smoothing",
        frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# --------------------------------------------------
# STEP 7: Close everything
# --------------------------------------------------

camera.release()
cv2.destroyAllWindows()