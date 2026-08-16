#!/usr/bin/env python3

"""
VS Code Extension Alert

Analyse les extensions installées dans VS Code
et les compare à une base locale d'extensions connues comme
dépréciées, archivées, renommées ou non maintenues.

Scans extensions installed in VS Code
and compares them against a local database of extensions known
to be deprecated, archived, renamed or unmaintained.

Aucune dépendance Python externe.
No external Python dependency.
"""

from pathlib import Path
import json
import shutil
import subprocess
import sys


# =========================================================
# CONFIGURATION → CONFIGURATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
ALERTS_FILE = BASE_DIR / "extensions.json"


# =========================================================
# STATUTS → STATUSES
# =========================================================

STATUSES = {
    "deprecated": "DEPRECATED / DÉPRÉCIÉE",
    "unmaintained": "UNMAINTAINED / NON MAINTENUE",
    "archived": "ARCHIVED / ARCHIVÉE",
    "renamed": "RENAMED / RENOMMÉE",
    "inactive": "INACTIVE / INACTIVE",
}


# =========================================================
# CHARGEMENT DE LA BASE → DATABASE LOADING
# =========================================================

def load_alert_database():
    """
    Charge extensions.json.
    Load extensions.json.
    """

    if not ALERTS_FILE.is_file():
        return None

    try:
        with ALERTS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

    except (json.JSONDecodeError, OSError):
        return None

    if not isinstance(data, dict):
        return None

    if not isinstance(data.get("extensions"), list):
        return None

    return data


# =========================================================
# DÉTECTION DE VS CODE → VS CODE DETECTION
# =========================================================

def find_vscode_cli():
    """
    Recherche la commande VS Code dans le PATH.
    Find the VS Code command in PATH.
    """

    return shutil.which("code")


# =========================================================
# EXTENSIONS INSTALLÉES → INSTALLED EXTENSIONS
# =========================================================

def get_installed_extensions(code_command):
    """
    Retourne les extensions VS Code installées avec leur version.
    Return installed VS Code extensions with their version.
    """

    try:
        result = subprocess.run(
            [
                code_command,
                "--list-extensions",
                "--show-versions"
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True
        )

    except (subprocess.CalledProcessError, OSError):
        return None

    extensions = {}

    for line in result.stdout.splitlines():

        line = line.strip()

        if not line:
            continue

        if "@" in line:
            extension_id, version = line.rsplit("@", 1)
        else:
            extension_id = line
            version = "unknown"

        normalized_id = extension_id.lower()

        extensions[normalized_id] = {
            "id": extension_id,
            "version": version
        }

    return extensions


# =========================================================
# INDEX DES ALERTES → ALERT INDEX
# =========================================================

def build_alert_index(database):
    """
    Construit l'index des extensions connues.
    Build the known extension alert index.
    """

    alerts = {}

    for extension in database.get("extensions", []):

        extension_id = extension.get("id")

        if not extension_id:
            continue

        alerts[extension_id.lower()] = extension

    return alerts


# =========================================================
# ANALYSE → ANALYSIS
# =========================================================

def scan_extensions(installed_extensions, alert_index):
    """
    Recherche les extensions installées présentes dans la base.
    Find installed extensions present in the alert database.
    """

    matches = []

    for extension_id, installed in installed_extensions.items():

        alert = alert_index.get(extension_id)

        if alert is None:
            continue

        matches.append({
            "installed": installed,
            "alert": alert
        })

    return matches


# =========================================================
# TEXTE BILINGUE → BILINGUAL TEXT
# =========================================================

def bilingual_value(value):
    """
    Retourne les textes anglais et français.
    Return English and French text.
    """

    if not isinstance(value, dict):
        return value or "", ""

    return (
        value.get("en", ""),
        value.get("fr", "")
    )


# =========================================================
# STATUT → STATUS
# =========================================================

def bilingual_status(status):
    """
    Retourne le statut bilingue.
    Return bilingual status.
    """

    return STATUSES.get(
        status.lower(),
        status.upper()
    )


# =========================================================
# RAPPORT → REPORT
# =========================================================

def print_report(database, installed_extensions, matches):
    """
    Affiche le rapport bilingue.
    Display the bilingual report.
    """

    print()
    print("=" * 64)
    print("VS CODE EXTENSION ALERT / ALERTE EXTENSIONS VS CODE")
    print("=" * 64)

    database_info = database.get("database", {})

    database_name = database_info.get(
        "name",
        "VS Code Extension Alert Database"
    )

    database_updated = database_info.get(
        "updated",
        "unknown"
    )

    print()
    print(f"Alert database / Base d'alertes: {database_name}")
    print(f"Database updated / Base mise à jour: {database_updated}")

    print()
    print("Scanning installed extensions...")
    print("Analyse des extensions installées...")
    print()

    if not matches:

        print("[OK] No known alert found.")
        print("     Aucune alerte connue détectée.")

    else:

        for match in matches:

            installed = match["installed"]
            alert = match["alert"]

            status = bilingual_status(
                alert.get("status", "unknown")
            )

            reason_en, reason_fr = bilingual_value(
                alert.get("reason")
            )

            replacement_en, replacement_fr = bilingual_value(
                alert.get("replacement")
            )

            source = alert.get("source", "")

            print(
                f"[!] {installed['id']} "
                f"{installed['version']}"
            )

            print(f"    Status / Statut: {status}")

            if reason_en or reason_fr:
                print()

                if reason_en:
                    print("    Reason:")
                    print(f"    {reason_en}")

                if reason_fr:
                    print("    Raison :")
                    print(f"    {reason_fr}")

            if replacement_en or replacement_fr:
                print()

                if (
                    replacement_en
                    and replacement_fr
                    and replacement_en == replacement_fr
                ):
                    print(
                        "    Suggested replacement / "
                        f"Remplacement suggéré: {replacement_en}"
                    )

                else:

                    if replacement_en:
                        print(
                            "    Suggested replacement: "
                            f"{replacement_en}"
                        )

                    if replacement_fr:
                        print(
                            "    Remplacement suggéré : "
                            f"{replacement_fr}"
                        )

            if source:
                print()
                print(f"    Source: {source}")

            print()

    print("-" * 64)

    print(
        "Extensions scanned / Extensions analysées: "
        f"{len(installed_extensions)}"
    )

    print(
        "Alerts found / Alertes trouvées: "
        f"{len(matches)}"
    )

    print("-" * 64)

    if matches:
        print()
        print(
            "Review flagged extensions before continuing to use them."
        )
        print(
            "Vérifiez les extensions signalées avant de continuer à les utiliser."
        )

    print()


# =========================================================
# EXÉCUTION PRINCIPALE → MAIN
# =========================================================

def main():
    """
    Lance l'analyse des extensions.
    Run the extension alert detector.
    """

    # Recherche VS Code → Find VS Code
    code_command = find_vscode_cli()

    if code_command is None:
        print(
            "VS Code CLI not found / "
            "Commande VS Code introuvable."
        )
        print(
            "Make sure the 'code' command is available in PATH. / "
            "Vérifiez que la commande 'code' est disponible dans le PATH."
        )
        sys.exit(1)

    # Charge la base locale → Load local database
    database = load_alert_database()

    if database is None:

        if not ALERTS_FILE.exists():
            print(
                "Extension database not found / "
                f"Base d'extensions introuvable: {ALERTS_FILE}"
            )

        else:
            print(
                "Invalid extension database / "
                f"Base d'extensions invalide: {ALERTS_FILE}"
            )

        sys.exit(1)

    # Récupère les extensions → Get extensions
    installed_extensions = get_installed_extensions(
        code_command
    )

    if installed_extensions is None:
        print(
            "Unable to read VS Code extensions. / "
            "Impossible de lire les extensions VS Code."
        )
        sys.exit(1)

    # Prépare les alertes → Prepare alerts
    alert_index = build_alert_index(database)

    # Recherche les correspondances → Find matches
    matches = scan_extensions(
        installed_extensions,
        alert_index
    )

    # Affiche le rapport → Display report
    print_report(
        database,
        installed_extensions,
        matches
    )


if __name__ == "__main__":
    main()
