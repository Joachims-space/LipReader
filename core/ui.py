# core/ui.py

"""
Verantwortung:

- Anzeige des Kamerabildes
- Anzeige der Lippenregion
- Statusmeldungen
- Zeichnen von Markierungen

Diese Klasse enthält die komplette
OpenCV-Darstellung.
"""

import cv2
from config.shortcuts import SHORTCUTS
from config.settings import (
    TARGET_RECORDINGS_PER_SENTENCE
)

class UI:

    def draw_mouth_rectangle(
        self,
        frame,
        xmin,
        ymin,
        xmax,
        ymax
    ):

        cv2.rectangle(
            frame,
            (xmin, ymin),
            (xmax, ymax),
            (0, 255, 0),
            2
        )

    def show_lips(self, mouth_roi):

        if mouth_roi.size > 0:

            cv2.imshow(
                "Lips",
                mouth_roi
            )

    def show_calibration(
        self,
        frame,
        current,
        total
    ):

        cv2.putText(
            frame,
            "BITTE STILL HALTEN",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        cv2.putText(
            frame,
            f"Kalibrierung: {current}/{total}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

    def show_movement(self, frame):

        cv2.putText(
            frame,
            "LIPPENBEWEGUNG",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

    def show_main_window(
        self,
        frame
    ):

        cv2.imshow(
            "LipReader",
            frame
        )
        
    def show_calibration_hint(self, frame):

        cv2.putText(
            frame,
            "Taste C zum Kalibrieren",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 0),
            2
        )        
            
    def show_training_sentence(
        self,
        frame,
        sentence
    ):
        """
        Zeigt den aktuellen Trainingssatz an.
        """

        cv2.putText(
            frame,
            "Trainingssatz:",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            sentence,
            (20, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 0),
            2
        )        
        
        
    def show_shortcuts(
        self,
        frame
    ):
        """
        Zeigt alle verfügbaren
        Tastenkürzel an.
        """

        start_x = 20
        start_y = 260

        for index, (
            key,
            description
        ) in enumerate(
            SHORTCUTS.items()
        ):

            y = start_y + (index * 30)

            cv2.putText(
                frame,
                f"{key}: {description}",
                (start_x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (200, 200, 200),
                2
            )


    def create_windows(self):
        """
        Erstellt die OpenCV-Fenster.

        Das Hauptfenster wird im Vordergrund gehalten.
        """

        cv2.namedWindow(
            "LipReader",
            cv2.WINDOW_NORMAL
        )

        cv2.namedWindow(
            "Lips",
            cv2.WINDOW_NORMAL
        )

        cv2.resizeWindow(
            "LipReader",
            1200,
            800
        )

        cv2.resizeWindow(
            "Lips",
            300,
            300
        )

        cv2.setWindowProperty(
            "LipReader",
            cv2.WND_PROP_TOPMOST,
            1
        )            


    def show_recording_count(
        self,
        frame,
        count,
        target_count=TARGET_RECORDINGS_PER_SENTENCE
    ):
        """
        Zeigt den Trainingsfortschritt an.

        count:
            Vorhandene Trainingsvideos

        target_count:
            Gewünschte Anzahl von Videos
        """

        cv2.putText(
            frame,
            f"Aufnahmen: {count}/{target_count}",
            (20, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        if count < target_count:

            status = (
                "Weitere Trainingsdaten benoetigt"
            )

            color = (0, 255, 255)

        else:

            status = (
                "Genuegend Trainingsdaten vorhanden"
            )

            color = (0, 255, 0)

        cv2.putText(
            frame,
            status,
            (20, 230),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )