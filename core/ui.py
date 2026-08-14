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
        
        
    def show_shortcuts(self, frame):
        """
        Zeigt die verfügbaren Tastenkürzel an.
        """

        shortcuts = [

            "C  Kalibrieren",

            "R  Aufnahme Start/Stop",

            "N  Naechster Satz",

            "P  Vorheriger Satz",

            "ESC Beenden"
        ]

        start_x = 20
        start_y = 250

        for index, text in enumerate(shortcuts):

            y = start_y + (index * 30)

            cv2.putText(
                frame,
                text,
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
        count
    ):
        """
        Zeigt die Anzahl der bisher
        vorhandenen Trainingsaufnahmen an.
        """

        cv2.putText(
            frame,
            f"Aufnahmen: {count}",
            (20, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )        