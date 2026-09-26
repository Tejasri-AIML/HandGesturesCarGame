import cv2
import mediapipe as mp


# ---------------------------------------------------------
# 1. Initialize MediaPipe Hands
# ---------------------------------------------------------

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


# Create the hand detection model
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


# ---------------------------------------------------------
# 2. Open the Webcam
# ---------------------------------------------------------

camera = cv2.VideoCapture(0)

# Check whether the camera opened successfully
if not camera.isOpened():
    print("Error: Could not open webcam.")
    exit()


print("Webcam started successfully.")
print("Show your hand in front of the camera.")
print("Press 'q' to quit.")


# ---------------------------------------------------------
# 3. Main Camera Loop
# ---------------------------------------------------------

while True:

    # Read one frame from the webcam
    success, frame = camera.read()

    # If the frame could not be read, stop the program
    if not success:
        print("Error: Could not read camera frame.")
        break


    # -----------------------------------------------------
    # 4. Flip the Image
    # -----------------------------------------------------

    # Flip horizontally so the camera behaves like a mirror
    frame = cv2.flip(frame, 1)


    # -----------------------------------------------------
    # 5. Convert BGR → RGB
    # -----------------------------------------------------

    # OpenCV uses BGR format.
    # MediaPipe expects RGB format.
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


    # -----------------------------------------------------
    # 6. Detect the Hand
    # -----------------------------------------------------

    results = hands.process(rgb_frame)


    # -----------------------------------------------------
    # 7. Draw Hand Landmarks
    # -----------------------------------------------------

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # Draw the 21 hand landmarks
            # and the connections between them
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )


    # -----------------------------------------------------
    # 8. Display the Camera
    # -----------------------------------------------------

    cv2.imshow(
        "Phase 1 - Hand Gesture Detection",
        frame
    )


    # -----------------------------------------------------
    # 9. Quit When 'q' Is Pressed
    # -----------------------------------------------------

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# ---------------------------------------------------------
# 10. Release Resources
# ---------------------------------------------------------

camera.release()
cv2.destroyAllWindows()
hands.close()

print("Program stopped.")
