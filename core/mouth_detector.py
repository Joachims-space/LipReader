# core/mouth_detector.py

"""
Verantwortung:

- Lippenregion bestimmen
- Mundrechteck berechnen
- Mundbild ausschneiden

Diese Klasse kennt die MediaPipe-Landmarken
des Mundes.
"""


class MouthDetector:

    def __init__(self):

        # Landmarken des Mundbereichs
        
        # 61  = linker Mundwinkel
        # 291 = rechter Mundwinkel
        # 13 = Oberlippe Mitte
        # 14 = Unterlippe Mitte
        # Weitere Lippenpunkte Ober- und Unterlippe
        # 78, 308,
        # 82, 312,
        # 87, 317

        self.mouth_points = [
            61, 291,
            13, 14,
            78, 308,
            82, 312,
            87, 317
        ]

    def extract_mouth_region(self, frame, landmarks):

        """
        Ermittelt die Mundregion.

        Parameter:
            frame      OpenCV Bild
            landmarks  MediaPipe Landmarken

        Rückgabe:
            mouth_roi
            xmin
            ymin
            xmax
            ymax
        """

        h, w, _ = frame.shape

        x_coords = []
        y_coords = []

        for idx in self.mouth_points:

            point = landmarks.landmark[idx]

            x = int(point.x * w)
            y = int(point.y * h)

            x_coords.append(x)
            y_coords.append(y)

        xmin = min(x_coords) - 20
        xmax = max(x_coords) + 20

        ymin = min(y_coords) - 20
        ymax = max(y_coords) + 20

        mouth_roi = frame[ymin:ymax, xmin:xmax]

        return mouth_roi, xmin, ymin, xmax, ymax