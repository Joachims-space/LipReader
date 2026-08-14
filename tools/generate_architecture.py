"""
Erzeugt automatisch die Datei

docs/architecture.md

aus den Python-Dateien des Projekts.
"""

from pathlib import Path
import ast


PROJECT_ROOT = Path(__file__).resolve().parent.parent

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

    return "\n".join(lines)


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


if __name__ == "__main__":
    main()