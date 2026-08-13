import cv2
import mediapipe as mp
import statistics

mp_face_mesh = mp.solutions.face_mesh
drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
calibration_frames = 300

width_values = []
height_values = []

calibrated = False
threshold_width = 0
threshold_height = 0

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

                left_corner = landmarks.landmark[61]
                right_corner = landmarks.landmark[291]

                upper_lip = landmarks.landmark[13]
                lower_lip = landmarks.landmark[14]

                mouth_width = abs(right_corner.x - left_corner.x)
                mouth_height = abs(lower_lip.y - upper_lip.y)

                if not calibrated:

                    width_values.append(mouth_width)
                    height_values.append(mouth_height)

                    cv2.putText(
                        frame,
                        f"Kalibrierung: {len(width_values)}/{calibration_frames}",
                        (20, 120),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2
                    )

                    if len(width_values) >= calibration_frames:

                        width_std = statistics.stdev(width_values)
                        height_std = statistics.stdev(height_values)

                        threshold_width = width_std * 3
                        threshold_height = height_std * 3

                        calibrated = True

                        print()
                        print("=== Kalibrierung abgeschlossen ===")
                        print(f"Threshold Width : {threshold_width:.6f}")
                        print(f"Threshold Height: {threshold_height:.6f}")
                        print()

                else:

                    movement_detected = (
                        abs(mouth_width - statistics.mean(width_values))
                        > threshold_width
                        or
                        abs(mouth_height - statistics.mean(height_values))
                        > threshold_height
                    )

                    if movement_detected:

                        cv2.putText(
                            frame,
                            "LIPPENBEWEGUNG",
                            (20, 120),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 255, 255),
                            2
                        )
                        
        
                cv2.rectangle(
                    frame,
                    (xmin, ymin),
                    (xmax, ymax),
                    (0, 255, 0),
                    2
                )
                
                cv2.putText(
                    frame,
                    f"W:{mouth_width:.3f}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"H:{mouth_height:.3f}",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )
                
                mouth_roi = frame[ymin:ymax, xmin:xmax]
                if mouth_roi.size > 0:
                    cv2.imshow("Lips", mouth_roi)
    
        cv2.imshow("Lip Reader Test", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()