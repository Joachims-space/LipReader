# core/calibration.py

"""
Verantwortung:

- Grundrauschen messen
- Schwellwerte berechnen
- Lippenbewegungen erkennen
"""

import statistics


class Calibration:

    def __init__(self, calibration_frames=300):

        self.calibration_frames = calibration_frames

        self.width_values = []
        self.height_values = []

        self.calibrated = False

        self.width_mean = 0
        self.height_mean = 0

        self.width_threshold = 0
        self.height_threshold = 0
        self.started = False

    def add_measurement(self, width, height):

        """
        Fügt einen Messwert hinzu.
        """

        if self.calibrated:
            return

        self.width_values.append(width)
        self.height_values.append(height)

        if len(self.width_values) >= self.calibration_frames:

            self.width_mean = statistics.mean(self.width_values)
            self.height_mean = statistics.mean(self.height_values)

            self.width_threshold = (
                statistics.stdev(self.width_values) * 3
            )

            self.height_threshold = (
                statistics.stdev(self.height_values) * 3
            )

            self.calibrated = True

            print()
            print("=== Kalibrierung abgeschlossen ===")
            print(
                f"Width Threshold: {self.width_threshold:.6f}"
            )
            print(
                f"Height Threshold: {self.height_threshold:.6f}"
            )
            print()

    def is_calibrated(self):

        return self.calibrated

    def detect_movement(self, width, height):

        """
        Ermittelt, ob eine Lippenbewegung vorliegt.
        """

        if not self.calibrated:
            return False

        width_changed = (

            abs(width - self.width_mean)

            > self.width_threshold
        )

        height_changed = (

            abs(height - self.height_mean)

            > self.height_threshold
        )

        return width_changed or height_changed
    
    def start(self):
        """
        Startet die Kalibrierung.
        """

        self.started = True

        self.width_values = []
        self.height_values = []

        self.calibrated = False    
            
    def is_started(self):

        return self.started        