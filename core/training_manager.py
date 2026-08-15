"""
Verwaltet Trainingssätze
für den LipReader.

Aufgaben:

- Trainingssätze bereitstellen
- Aktuellen Satz verwalten
- Zum nächsten Satz wechseln
- Zum vorherigen Satz wechseln
- Anzahl vorhandener Aufnahmen ermitteln
"""

import os
import re
from config.training_sentences import TRAINING_SENTENCES

class TrainingManager:

    def __init__(self):

        # Trainingssätze
        #
        # Diese Liste wird später
        # wahrscheinlich noch erweitert.
        #
        self.sentences = TRAINING_SENTENCES

        # Start mit erstem Satz

        self.current_index = 0

        self.current_sentence = (
            self.sentences[self.current_index]
        )

    def get_current_sentence(self):
        """
        Liefert den aktuell
        ausgewählten Trainingssatz.
        """

        return self.current_sentence

    def next_sentence(self):
        """
        Wechselt zum nächsten Satz.
        Nach dem letzten Satz beginnt
        die Liste wieder von vorne.
        """

        self.current_index += 1

        if self.current_index >= len(self.sentences):

            self.current_index = 0

        self.current_sentence = (
            self.sentences[self.current_index]
        )

        return self.current_sentence

    def previous_sentence(self):
        """
        Wechselt zum vorherigen Satz.
        Vor dem ersten Satz wird
        zum letzten Satz gesprungen.
        """

        self.current_index -= 1

        if self.current_index < 0:

            self.current_index = (
                len(self.sentences) - 1
            )

        self.current_sentence = (
            self.sentences[self.current_index]
        )

        return self.current_sentence

    def sentence_to_folder_name(
        self,
        sentence
    ):
        """
        Wandelt einen Satz
        in einen gültigen Ordnernamen um.

        Beispiel:

        "Bitte Wasser"

        wird zu

        "bitte_wasser"
        """

        folder = sentence.lower()

        folder = folder.replace(
            "ä",
            "ae"
        )

        folder = folder.replace(
            "ö",
            "oe"
        )

        folder = folder.replace(
            "ü",
            "ue"
        )

        folder = folder.replace(
            "ß",
            "ss"
        )

        folder = folder.replace(
            " ",
            "_"
        )

        folder = re.sub(
            r"[^a-z0-9_]",
            "",
            folder
        )

        return folder

    def get_recording_count(self):
        """
        Anzahl vorhandener Videos
        für den aktuellen Satz.
        """

        folder_name = (
            self.sentence_to_folder_name(
                self.current_sentence
            )
        )

        target_folder = os.path.join(
            "dataset",
            folder_name
        )

        if not os.path.exists(
            target_folder
        ):
            return 0

        count = 0

        for file in os.listdir(
            target_folder
        ):

            if file.endswith(".mp4"):

                count += 1

        return count
