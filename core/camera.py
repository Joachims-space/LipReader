# core/camera.py

"""
Verantwortung:
- Webcam öffnen
- Bilder lesen
- Webcam schließen

Diese Klasse kapselt OpenCV.
Der Rest des Programms muss nicht wissen,
wie die Kamera technisch funktioniert.
"""

import cv2


class Camera:

    def __init__(self):
        """
        Öffnet die Standard-Webcam.
        """
        self.cap = cv2.VideoCapture(0)

    def read_frame(self):
        """
        Liest ein Bild von der Webcam.

        Returns:
            frame oder None
        """
        success, frame = self.cap.read()

        if success:
            return frame

        return None

    def release(self):
        """
        Gibt die Webcam frei.
        """
        self.cap.release()