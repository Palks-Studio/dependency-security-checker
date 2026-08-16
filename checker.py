#!/usr/bin/env python3

"""
Python Dependency Alert

Analyse les packages installés dans l'environnement Python actif
et les compare à une base locale de packages connus comme
dépréciés, archivés, renommés ou non maintenus.

Scans packages installed in the active Python environment
and compares them against a local database of packages known
to be deprecated, archived, renamed or unmaintained.

Aucune dépendance externe.
No external dependency.
"""

from pathlib import Path
from importlib.metadata import distributions
import json
import sys


# =========================================================
# CONFIGURATION → CONFIGURATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
ALERTS_FILE = BASE_DIR / "alerts.json"


# =========================================================
# STATUTS → STATUSES
# =========================================================

STATUSES = {
    "deprecated": "DEPRECATED / DÉPRÉCIÉ",
    "unmaintained": "UNMAINTAINED / NON MAINTENU",
    "archived": "ARCHIVED / ARCHIVÉ",
    "renamed": "RENAMED / RENOMMÉ",
    "inactive": "INACTIVE / INACTIF",
}


# =========================================================
# CHARGEMENT DE LA BASE → DATABASE LOADING
# =========================================================

def load_alert_database():
    """Load alerts.json."""

    if not ALERTS_FILE.is_file():
        return None

    try:
        with ALERTS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

    except (json.JSONDecodeError, OSError):
        return None

    if not isinstance(data, dict):
        return None

    if not isinstance(data.get("packages"), list):
        return None

    return data


# =========================================================
# NORMALISATION DES NOMS → PACKAGE NAME NORMALIZATION
# =========================================================

def normalize_package_name(name):
    """
    Normalise le nom d'un package Python.
    Normalize a Python package name.

    Exemple → Example:
    my_package
    my-package
    my.package

    deviennent → become:
    my-package
    """

    return name.lower().replace("_", "-").replace(".", "-")


# =========================================================
# PACKAGES INSTALLÉS → INSTALLED PACKAGES
# =========================================================

def get_installed_packages():
    """
    Retourne les packages installés dans l'environnement Python actif.
    Return packages installed in the active Python environment.
    """

    packages = {}

    for distribution in distributions():

        name = distribution.metadata.get("Name")

        if not name:
            continue

        normalized_name = normalize_package_name(name)

        packages[normalized_name] = {
            "name": name,
            "version": distribution.version
        }

    return packages


# =========================================================
# INDEX DES ALERTES → ALERT INDEX
# =========================================================

def build_alert_index(database):
    """
    Construit un index des packages présents dans la base d'alertes.
    Build an index of packages present in the alert database.
    """

    alerts = {}

    for package in database.get("packages", []):

        name = package.get("name")

        if not name:
            continue

        normalized_name = normalize_package_name(name)
        alerts[normalized_name] = package

    return alerts


# =========================================================
# ANALYSE → ANALYSIS
# =========================================================

def scan_packages(installed_packages, alert_index):
    """
    Recherche les packages installés présents dans la base d'alertes.
    Find installed packages present in the alert database.
    """

    matches = []

    for normalized_name, installed in installed_packages.items():

        alert = alert_index.get(normalized_name)

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
    Retourne les versions anglaise et française d'un champ.
    Return the English and French versions of a field.
    """

    if not isinstance(value, dict):
        return value or "", ""

    english = value.get("en", "")
    french = value.get("fr", "")

    return english, french


# =========================================================
# STATUT → STATUS
# =========================================================

def bilingual_status(status):
    """
    Retourne le statut en anglais et en français.
    Return the status in English and French.
    """

    return STATUSES.get(
        status.lower(),
        status.upper()
    )


# =========================================================
# RAPPORT → REPORT
# =========================================================

def print_report(database, installed_packages, matches):
    """
    Affiche le rapport bilingue.
    Display the bilingual report.
    """

    print()
    print("=" * 64)
    print("PYTHON DEPENDENCY ALERT / ALERTE DÉPENDANCES PYTHON")
    print("=" * 64)

    print()
    print(f"Python environment / Environnement Python: {sys.executable}")

    database_info = database.get("database", {})

    database_name = database_info.get(
        "name",
        "Python Dependency Alert Database"
    )

    database_updated = database_info.get(
        "updated",
        "unknown"
    )

    print(f"Alert database / Base d'alertes: {database_name}")
    print(f"Database updated / Base mise à jour: {database_updated}")

    print()
    print("Scanning installed packages...")
    print("Analyse des packages installés...")
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

            print(f"[!] {installed['name']} {installed['version']}")
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
                        "    Suggested replacement / Remplacement suggéré: "
                        f"{replacement_en}"
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
        "Packages scanned / Packages analysés: "
        f"{len(installed_packages)}"
    )

    print(
        "Alerts found / Alertes trouvées: "
        f"{len(matches)}"
    )

    print("-" * 64)

    if matches:
        print()
        print(
            "Review flagged dependencies before continuing to use them."
        )
        print(
            "Vérifiez les dépendances signalées avant de continuer à les utiliser."
        )

    print()


# =========================================================
# EXÉCUTION PRINCIPALE → MAIN
# =========================================================

def main():
    """
    Lance l'analyse des dépendances.
    Run the dependency alert checker.
    """

    # Charge la base locale → Load local database
    database = load_alert_database()

    if database is None:

        if not ALERTS_FILE.exists():
            print(
                "Alert database not found / "
                f"Base d'alertes introuvable: {ALERTS_FILE}"
            )

        else:
            print(
                "Invalid alert database / "
                f"Base d'alertes invalide: {ALERTS_FILE}"
            )

        sys.exit(1)

    # Récupère les packages installés → Get installed packages
    installed_packages = get_installed_packages()

    # Prépare la base d'alertes → Prepare alert database
    alert_index = build_alert_index(database)

    # Recherche les correspondances → Find matching alerts
    matches = scan_packages(
        installed_packages,
        alert_index
    )

    # Affiche le rapport → Display report
    print_report(
        database,
        installed_packages,
        matches
    )


if __name__ == "__main__":
    main()
