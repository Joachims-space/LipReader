"""
Verwaltet Trainingssätze
für den LipReader.
"""

import random


class TrainingManager:

    def __init__(self):

        self.sentences = [

            "Bitte Wasser",

            "Bitte Hilfe",

            "Ich habe Schmerzen",

            "Ja",

            "Nein",

            "Danke"
        ]

        self.current_sentence = (
            random.choice(self.sentences)
        )

    def get_current_sentence(self):
        """
        Liefert den aktuell
        anzuzeigenden Satz.
        """

        return self.current_sentence

    def next_sentence(self):
        """
        Wählt einen neuen
        Trainingssatz aus.
        """

        self.current_sentence = (
            random.choice(self.sentences)
        )

        return self.current_sentence