import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True
) as face_mesh:

    while cap.isOpened():

        success, frame = cap.read()

        if not success:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:

            for landmarks in results.multi_face_landmarks:

                # drawing.draw_landmarks(
                #     frame,
                #     landmarks,
                #     mp_face_mesh.FACEMESH_TESSELATION
                # )
                
                h, w, _ = frame.shape

                mouth_points = [
                    61, 291, 13, 14,
                    78, 308, 82, 312,
                    87, 317
                ]

                x_coords = []
                y_coords = []

                for idx in mouth_points:
                    point = landmarks.landmark[idx]

                    x = int(point.x * w)
                    y = int(point.y * h)

                    x_coords.append(x)
                    y_coords.append(y)

                xmin = min(x_coords) - 20
                xmax = max(x_coords) + 20
                ymin = min(y_coords) - 20
                ymax = max(y_coords) + 20

                cv2.rectangle(
                    frame,
                    (xmin, ymin),
                    (xmax, ymax),
                    (0, 255, 0),
                    2
                )
                
        cv2.imshow("Lip Reader Test", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()