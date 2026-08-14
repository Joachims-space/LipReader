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