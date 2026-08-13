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
from core.calibration import Calibration
from core.recorder import Recorder
from core.ui import UI


def main():

    # Kamera initialisieren
    camera = Camera()
    # Face Mesh initialisieren
    face_detector = FaceDetector()
    # Munderkennung initialisieren
    mouth_detector = MouthDetector()
    # Kalibrierung initialisieren
    calibration = Calibration()
    # UI initialisieren
    ui = UI()
    # Recorder initialisieren
    recorder = Recorder()

    while True:

        frame = camera.read_frame()
        if frame is None:
            break
        mouth_roi = None

        # Gesicht erkennen
        landmarks = face_detector.detect(frame)
        if landmarks:
            # Aktuell unterstützen wir genau ein Gesicht
            face_landmarks = landmarks[0]
            
            # Mundbereich bestimmen
            mouth_roi, xmin, ymin, xmax, ymax = (
                mouth_detector.extract_mouth_region(
                    frame,
                    face_landmarks
                )
            )
            
            # Mundmaße bestimmen
            mouth_width, mouth_height = (
                mouth_detector.get_mouth_measurements(
                    face_landmarks
                )
            )
            
            # Kalibrierung durchführen
            if not calibration.is_calibrated():
                calibration.add_measurement(
                    mouth_width,
                    mouth_height
                )            
            
            # Mundbereich markieren
            # cv2.rectangle(
            #     frame,
            #     (xmin, ymin),
            #     (xmax, ymax),
            #     (0, 255, 0),
            #     2
            # )
            
            ui.draw_mouth_rectangle(
                frame,
                xmin,
                ymin,
                xmax,
                ymax
            )
            
        if mouth_roi is not None and mouth_roi.size > 0:
            ui.show_lips(mouth_roi)     


        if frame is None:
            break

        cv2.imshow("LipReader", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("r"):

            if not recorder.recording:

                if mouth_roi is not None and mouth_roi.size > 0:

                    height, width = mouth_roi.shape[:2]

                    recorder.start_recording(
                        width,
                        height
                    )

            else:

                recorder.stop_recording()




        if key == 27:
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()