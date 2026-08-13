# core/face_detector.py

"""
Verantwortung:
- MediaPipe initialisieren
- Gesichtslandmarken erkennen

Der Rest der Anwendung muss nicht wissen,
wie MediaPipe funktioniert.
"""

import cv2
import mediapipe as mp


class FaceDetector:

    def __init__(self):
        """
        Initialisiert MediaPipe Face Mesh.
        """

        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True
        )

    def detect(self, frame):
        """
        Erkennt Gesichtslandmarken.

        Args:
            frame: OpenCV Bild

        Returns:
            MediaPipe Landmarken oder None
        """

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.face_mesh.process(rgb)

        if results.multi_face_landmarks:
            return results.multi_face_landmarks

        return None