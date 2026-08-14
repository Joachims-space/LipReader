# LipReader Architektur


# Datei: calibration.py

Verantwortung:

- Grundrauschen messen
- Schwellwerte berechnen
- Lippenbewegungen erkennen


## Klasse: Calibration

Keine Dokumentation vorhanden.


### Methoden

- __init__
- add_measurement
- is_calibrated
- detect_movement
- start
- is_started



# Datei: camera.py

Verantwortung:
- Webcam öffnen
- Bilder lesen
- Webcam schließen

Diese Klasse kapselt OpenCV.
Der Rest des Programms muss nicht wissen,
wie die Kamera technisch funktioniert.


## Klasse: Camera

Keine Dokumentation vorhanden.


### Methoden

- __init__
- read_frame
- release



# Datei: face_detector.py

Verantwortung:
- MediaPipe initialisieren
- Gesichtslandmarken erkennen

Der Rest der Anwendung muss nicht wissen,
wie MediaPipe funktioniert.


## Klasse: FaceDetector

Keine Dokumentation vorhanden.


### Methoden

- __init__
- detect



# Datei: mouth_detector.py

Verantwortung:

- Lippenregion bestimmen
- Mundrechteck berechnen
- Mundbild ausschneiden

Diese Klasse kennt die MediaPipe-Landmarken
des Mundes.


## Klasse: MouthDetector

Keine Dokumentation vorhanden.


### Methoden

- __init__
- extract_mouth_region
- get_mouth_measurements



# Datei: recorder.py

Verantwortung:

- Aufnahme von Trainingsvideos
- Speichern der Mundregion

Diese Klasse kennt keine Kamera,
keine MediaPipe-Details und keine KI.

Sie erhält lediglich Mundbilder.


## Klasse: Recorder

Keine Dokumentation vorhanden.


### Methoden

- __init__
- start_recording
- write_frame
- stop_recording
- sentence_to_folder_name
- get_next_filename



# Datei: training_manager.py

Verwaltet Trainingssätze
für den LipReader.

Aufgaben:

- Trainingssätze bereitstellen
- Aktuellen Satz verwalten
- Zum nächsten Satz wechseln
- Zum vorherigen Satz wechseln
- Anzahl vorhandener Aufnahmen ermitteln


## Klasse: TrainingManager

Keine Dokumentation vorhanden.


### Methoden

- __init__
- get_current_sentence
- next_sentence
- previous_sentence
- sentence_to_folder_name
- get_recording_count



# Datei: ui.py

Verantwortung:

- Anzeige des Kamerabildes
- Anzeige der Lippenregion
- Statusmeldungen
- Zeichnen von Markierungen

Diese Klasse enthält die komplette
OpenCV-Darstellung.


## Klasse: UI

Keine Dokumentation vorhanden.


### Methoden

- draw_mouth_rectangle
- show_lips
- show_calibration
- show_movement
- show_main_window
- show_calibration_hint
- show_training_sentence
- show_shortcuts
- create_windows
- show_recording_count
- show_recording_count



# Datei: main.py

Haupteinstieg des Programms.

Aktuell:
- Kamera starten
- Kamerabild anzeigen

Später:
- Face Detector
- Mouth Detector
- Recorder
- KI-Modell



# Projektstruktur

```text
├── backend
│   ├── tests
│   ├── main.py
│   └── requirements.txt
├── config
│   ├── dataflow.py
│   ├── settings.py
│   └── shortcuts.py
├── core
│   ├── calibration.py
│   ├── camera.py
│   ├── face_detector.py
│   ├── mouth_detector.py
│   ├── recorder.py
│   ├── training_manager.py
│   └── ui.py
├── dataset
│   ├── bitte_hilfe
│   ├── bitte_wasser
│   └── raw
├── docs
│   └── architecture.md
├── frontend
│   ├── app.js
│   ├── index.html
│   └── style.css
├── models
├── tests
│   └── test_mediapipe.py
├── tools
│   └── generate_architecture.py
├── .gitignore
├── git_howto.txt
├── main.py
├── README.md
└── requirements.txt
```

# Trainingssätze

- Bitte Wasser
- Bitte Hilfe
- Ich habe Schmerzen
- Ja
- Nein
- Danke

# Tastenkürzel

- C: Kalibrieren
- R: Aufnahme Start/Stop
- N: Nächster Trainingssatz
- P: Vorheriger Trainingssatz
- ESC: Programm beenden

# Datenfluss

```text
Camera
↓
FaceDetector
↓
MouthDetector
↓
Calibration
↓
TrainingManager
↓
Recorder
↓
UI
```