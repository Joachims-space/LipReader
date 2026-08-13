# camera
#     ↓
# face_detector
#     ↓
# mouth_detector
#     ↓
# calibration
#     ↓
# recorder

# main.py

"""
Haupteinstieg des Programms.

Aktuell:
- Kamera starten
- Kamerabild anzeigen

Später:
- Face Detector
- Mouth Detector
- Recorder
- KI-Modell
"""

import cv2
from core.camera import Camera
from core.face_detector import FaceDetector
from core.mouth_detector import MouthDetector

def main():

    camera = Camera()
    face_detector = FaceDetector()
    mouth_detector = MouthDetector()

    while True:

        frame = camera.read_frame()
        landmarks = face_detector.detect(frame)
        if landmarks:

            face_landmarks = landmarks[0]

            mouth_roi, xmin, ymin, xmax, ymax = (
                mouth_detector.extract_mouth_region(
                    frame,
                    face_landmarks
                )
            )
        cv2.rectangle(
            frame,
            (xmin, ymin),
            (xmax, ymax),
            (0, 255, 0),
            2
        )
        if mouth_roi.size > 0:
            cv2.imshow("Lips", mouth_roi)        


        if frame is None:
            break

        cv2.imshow("LipReader", frame)

        key = cv2.waitKey(1)

        if key == 27:
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()