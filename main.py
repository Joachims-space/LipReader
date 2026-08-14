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
from core.training_manager import TrainingManager

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
    ui.create_windows()
    # Recorder initialisieren
    recorder = Recorder()
    
    training_manager = TrainingManager()

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
            if (
                calibration.is_started()
                and
                not calibration.is_calibrated()
            ):

                calibration.add_measurement(
                    mouth_width,
                    mouth_height
                )

                current = len(
                    calibration.width_values
                )

                total = calibration.calibration_frames

                ui.show_calibration(
                    frame,
                    current,
                    total
                )   
                
            if not calibration.is_started():

                ui.show_calibration_hint(
                    frame
                )
                            
            ui.draw_mouth_rectangle(
                frame,
                xmin,
                ymin,
                xmax,
                ymax
            )
            
            ui.show_training_sentence(
                frame,
                training_manager.get_current_sentence()
            )          
            
            recording_count = (
                training_manager.get_recording_count()
            )

            ui.show_recording_count(
                frame,
                recording_count
            )
            
        if mouth_roi is not None and mouth_roi.size > 0:
            ui.show_lips(mouth_roi)     
            
            recorder.write_frame(
                mouth_roi
            )
    
            
        ui.show_shortcuts(
            frame
        )    
        
        ui.show_main_window(frame)




        key = cv2.waitKey(1) & 0xFF

        # Kalibrierung starten
        if key == ord("c"):

            calibration.start()

            print()
            print("Kalibrierung gestartet")
            print()


        # Nächsten Trainingssatz auswählen
        if key == ord("n"):

            sentence = (
                training_manager.next_sentence()
            )

            print()
            print(
                f"Trainingssatz: {sentence}"
            )
            print()


        # Vorherigen Trainingssatz auswählen
        if key == ord("p"):

            sentence = (
                training_manager.previous_sentence()
            )

            print()
            print(
                f"Trainingssatz: {sentence}"
            )
            print()


        # Aufnahme starten / stoppen
        if key == ord("r"):

            if not recorder.recording:

                if (
                    mouth_roi is not None
                    and
                    mouth_roi.size > 0
                ):

                    recorder.start_recording(
                        training_manager.get_current_sentence()
                    )

            else:

                recorder.stop_recording()





        if key == 27:
            break

    recorder.stop_recording()    
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()