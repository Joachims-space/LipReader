"""
Erzeugt automatisch die Datei

docs/architecture.md

aus den Python-Dateien des Projekts.
"""
from pathlib import Path
import ast
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
# Projektwurzel zum Python-Pfad hinzufügen,
# damit Imports wie
# from config.shortcuts import SHORTCUTS
# funktionieren.
sys.path.insert(
    0,
    str(PROJECT_ROOT)
)
from config.shortcuts import SHORTCUTS
from config.dataflow import DATAFLOW

OUTPUT_DIR = PROJECT_ROOT / "docs"
OUTPUT_FILE = OUTPUT_DIR / "architecture.md"


def get_docstring(node):

    doc = ast.get_docstring(node)

    if doc is None:
        return "Keine Dokumentation vorhanden."

    return doc.strip()


def analyze_file(file_path):

    source = file_path.read_text(
        encoding="utf-8"
    )

    tree = ast.parse(source)

    result = {
        "docstring": get_docstring(tree),
        "classes": []
    }

    for node in tree.body:

        if isinstance(node, ast.ClassDef):

            class_info = {
                "name": node.name,
                "docstring": get_docstring(node),
                "methods": []
            }

            for item in node.body:

                if isinstance(
                    item,
                    ast.FunctionDef
                ):

                    class_info["methods"].append(
                        item.name
                    )

            result["classes"].append(
                class_info
            )

    return result


def add_dataflow(lines):
    """
    Fügt den Datenfluss der Anwendung
    zur Dokumentation hinzu.
    """

    lines.append("\n# Datenfluss\n")

    lines.append("```text")

    for index, component in enumerate(
        DATAFLOW
    ):

        lines.append(component)

        if index < len(DATAFLOW) - 1:

            lines.append("↓")

    lines.append("```")


def add_shortcuts(lines):

    lines.append("\n# Tastenkürzel\n")

    for key, description in SHORTCUTS.items():

        lines.append(
            f"- {key}: {description}"
        )


def build_markdown():

    lines = []

    lines.append("# LipReader Architektur\n")

    python_files = []

    core_path = PROJECT_ROOT / "core"

    if core_path.exists():

        python_files.extend(
            sorted(core_path.glob("*.py"))
        )

    main_file = PROJECT_ROOT / "main.py"

    if main_file.exists():

        python_files.append(main_file)

    for file_path in python_files:

        lines.append(
            f"\n# Datei: {file_path.name}\n"
        )

        analysis = analyze_file(
            file_path
        )

        lines.append(
            analysis["docstring"]
        )

        lines.append("\n")

        for cls in analysis["classes"]:

            lines.append(
                f"## Klasse: {cls['name']}\n"
            )

            lines.append(
                cls["docstring"]
            )

            lines.append("\n")

            lines.append(
                "### Methoden\n"
            )

            for method in cls["methods"]:

                lines.append(
                    f"- {method}"
                )

            lines.append("\n")


    add_project_structure(lines)

    add_training_sentences(lines)

    add_shortcuts(lines)

    add_dataflow(lines)

    return "\n".join(lines)


def add_dataflow(lines):
    """
    Fügt den Datenfluss des Systems
    zur Dokumentation hinzu.
    """

    lines.append("\n# Datenfluss\n")

    try:

        from config.dataflow import DATAFLOW

        lines.append("```text")

        for i, component in enumerate(DATAFLOW):

            lines.append(component)

            if i < len(DATAFLOW) - 1:
                lines.append("↓")

        lines.append("```")

    except Exception as ex:

        lines.append(
            f"Fehler beim Laden des Datenflusses: {ex}"
        )


def add_project_structure(lines):
    """
    Fügt einen Projektstrukturbaum
    zur Dokumentation hinzu.
    """

    lines.append("\n# Projektstruktur\n")

    lines.append("```text")

    build_tree(
        PROJECT_ROOT,
        lines,
        "",
        ignore_dirs={
            ".git",
            "__pycache__",
            ".venv",
            ".pytest_cache",
            ".mypy_cache"
        }
    )

    lines.append("```")


def build_tree(
    path,
    lines,
    prefix,
    ignore_dirs
):
    """
    Erzeugt rekursiv einen
    Verzeichnisbaum.
    """

    entries = sorted(
        path.iterdir(),
        key=lambda p: (
            p.is_file(),
            p.name.lower()
        )
    )

    entries = [

        entry

        for entry in entries

        if entry.name not in ignore_dirs
    ]

    total = len(entries)

    for index, entry in enumerate(entries):

        is_last = (
            index == total - 1
        )

        branch = (
            "└── "
            if is_last
            else "├── "
        )

        lines.append(
            prefix + branch + entry.name
        )

        if entry.is_dir():

            extension = (
                "    "
                if is_last
                else "│   "
            )

            build_tree(
                entry,
                lines,
                prefix + extension,
                ignore_dirs
            )


def main():

    OUTPUT_DIR.mkdir(
        exist_ok=True
    )

    markdown = build_markdown()

    OUTPUT_FILE.write_text(
        markdown,
        encoding="utf-8"
    )

    print(
        f"Architektur erzeugt: {OUTPUT_FILE}"
    )

def add_training_sentences(lines):

    lines.append("\n# Trainingssätze\n")

    try:

        from core.training_manager import (
            TrainingManager
        )

        manager = TrainingManager()

        for sentence in manager.sentences:

            lines.append(
                f"- {sentence}"
            )

    except Exception as ex:

        lines.append(
            f"Fehler: {ex}"
        )

def add_shortcuts(lines):

    lines.append("\n# Tastenkürzel\n")

    try:

        from config.shortcuts import (
            SHORTCUTS
        )

        for key, description in (
            SHORTCUTS.items()
        ):

            lines.append(
                f"- {key}: {description}"
            )

    except Exception as ex:

        lines.append(
            f"Fehler: {ex}"
        )
        
if __name__ == "__main__":
    main()