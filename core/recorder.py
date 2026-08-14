# core/recorder.py

"""
Verantwortung:

- Aufnahme von Trainingsvideos
- Speichern der Mundregion

Diese Klasse kennt keine Kamera,
keine MediaPipe-Details und keine KI.

Sie erhält lediglich Mundbilder.
"""

import os
import cv2
from datetime import datetime


class Recorder:

    def __init__(self):

        self.recording = False
        self.writer = None

    def start_recording(
        self,
        width,
        height
    ):
        """
        Startet eine neue Videoaufnahme.
        """

        os.makedirs(
            "dataset/raw",
            exist_ok=True
        )

        filename = datetime.now().strftime(
            "%Y%m%d_%H%M%S.mp4"
        )

        filepath = os.path.join(
            "dataset/raw",
            filename
        )

        self.writer = cv2.VideoWriter(
            filepath,
            cv2.VideoWriter_fourcc(*"mp4v"),
            20,
            (128, 128) #(width, height)
        )

        self.recording = True

        print()
        print("Aufnahme gestartet")
        print(filepath)
        print()

    def write_frame(
        self,
        mouth_roi
    ):
        """
        Speichert einen Frame.
        """

        if self.recording:

            resized = cv2.resize(
                mouth_roi,
                (128, 128)
            )

            self.writer.write(
                resized
            )

    def stop_recording(self):
        """
        Beendet die Aufnahme.
        """

        if self.writer:

            self.writer.release()

        self.writer = None
        self.recording = False

        print()
        print("Aufnahme beendet")
        print()