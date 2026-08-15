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
import re
from config.settings import (
    VIDEO_WIDTH,
    VIDEO_HEIGHT,
    VIDEO_FPS
)


class Recorder:

    def __init__(self):

        self.recording = False
        self.writer = None

    def start_recording(
        self,
        sentence
    ):
        """
        Startet eine neue Videoaufnahme.
        """

        folder_name = (
            self.sentence_to_folder_name(
                sentence
            )
        )

        target_folder = os.path.join(
            "dataset",
            folder_name
        )

        os.makedirs(
            target_folder,
            exist_ok=True
        )

        filename = datetime.now().strftime(
            target_folder
        )

        filepath = os.path.join(
            target_folder,
            filename
        )

        self.writer = cv2.VideoWriter(
            filepath,
            cv2.VideoWriter_fourcc(*"mp4v"),
            VIDEO_FPS,
            (
            VIDEO_WIDTH,
            VIDEO_HEIGHT
            )
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
                (
                    VIDEO_WIDTH,
                    VIDEO_HEIGHT
                )
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
    
    def sentence_to_folder_name(
        self,
        sentence
    ):
        """
        Erzeugt einen gültigen Ordnernamen
        aus einem Trainingssatz.
        """

        folder = sentence.lower()

        folder = folder.replace("ä", "ae")
        folder = folder.replace("ö", "oe")
        folder = folder.replace("ü", "ue")
        folder = folder.replace("ß", "ss")

        folder = folder.replace(" ", "_")

        folder = re.sub(
            r"[^a-z0-9_]",
            "",
            folder
        )

        return folder    
    
    def get_next_filename(
        self,
        target_folder
    ):
        """
        Ermittelt die nächste freie Dateinummer.
        """

        existing = []

        for file in os.listdir(target_folder):

            if (
                file.startswith("video_")
                and
                file.endswith(".mp4")
            ):

                try:

                    number = int(
                        file[6:9]
                    )

                    existing.append(number)

                except ValueError:

                    pass

        if not existing:

            return "video_001.mp4"

        next_number = max(existing) + 1

        return (
            f"video_{next_number:03d}.mp4"
        )
    
        