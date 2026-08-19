<p align="center">
  <img src="docs/images/checker.png"
       alt="Dependency Security Checker, analyse locale des packages Python et extensions VS Code pour détecter les éléments connus comme dépréciés, archivés ou non maintenus"
       aria-label="Dependency Security Checker, analyse locale des dépendances Python et extensions VS Code"
       width="1200">
</p>

> 🇫🇷 Français | [🇬🇧 English](./README.md)

![Dependency Alerts](https://img.shields.io/badge/Dependency-Alerts-red?style=flat-square)
![VS Code Extension Alerts](https://img.shields.io/badge/VS%20Code-Extension%20Alerts-007ACC?style=flat-square&logo=visualstudiocode&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-lightgreen.svg)
![Offline First](https://img.shields.io/badge/Mode-Offline%20First-0095b1?style=flat)
[![YouTube](https://img.shields.io/badge/YouTube-@Palks__Studio-FF0000?style=flat&logo=youtube&logoColor=white)](https://www.youtube.com/@Palks_Studio)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-@Palks__Studio-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/palks-studio/)

<p align="center">
  <a href="https://palks-studio.com">
    <img src="https://img.shields.io/badge/Palks%20Studio-Website-0095b1?style=for-the-badge" />
  </a>
</p>

# Dependency Security Checker, Open Source

Un outil local et open source pour repérer rapidement des dépendances Python et des extensions VS Code connues comme dépréciées, archivées, renommées, inactives ou non maintenues.

Le projet fonctionne à partir de bases d'alertes locales et ne nécessite aucun service externe.

---

## Structure

```text
dependency-security-checker/
│
├── checker.py                     → Vérificateur d'alertes des packages Python
├── extension.py                   → Vérificateur d'alertes des extensions VS Code
├── alerts.json                    → Base d'alertes des packages Python
├── extensions.json                → Base d'alertes des extensions VS Code
├── LICENSE.md                     → Licence MIT
├── README.md                      → Documentation anglaise
├── README_FR.md                   → Documentation française
│
└── docs/
    ├── images/
    │   ├── checker.png            → Aperçu du projet
    │   └── Palks_Studio.png       → Logo Palks Studio
    └── videos/
        └── checker.mp4            → Démonstrations des checkers
```

---

## Pourquoi cet outil ?

Avec le temps, un environnement de développement peut accumuler de nombreux packages Python et extensions VS Code.

Certains projets finissent par être abandonnés, archivés, renommés ou officiellement dépréciés, sans que l'utilisateur s'en rende forcément compte.

Dependency Security Checker permet d'effectuer une vérification rapide de l'environnement installé et de signaler les éléments connus présents dans ses bases d'alertes.

L'objectif n'est pas de décider à la place de l'utilisateur, mais de lui donner une information qu'il pourra ensuite vérifier et analyser.

---

## Fonctionnalités

Le projet contient actuellement deux outils indépendants.

### Packages Python

`checker.py` analyse les packages installés dans l'environnement Python actif et les compare à la base locale `alerts.json`.

Pour chaque correspondance connue, le rapport peut afficher :

- le package détecté  
- sa version installée  
- son statut  
- la raison de l'alerte  
- un remplacement suggéré lorsqu'il existe  
- la source utilisée pour documenter l'alerte

### Extensions VS Code

`extension.py` analyse les extensions installées dans VS Code et les compare à la base locale `extensions.json`.

Le script récupère également la version installée de chaque extension.

Lorsqu'une extension connue est détectée, le rapport indique son statut, la raison de l'alerte, une éventuelle alternative et la source correspondante.

---

## Statuts

Les bases peuvent actuellement signaler plusieurs situations :

- `deprecated` : projet déprécié  
- `unmaintained` : projet non maintenu  
- `archived` : projet archivé  
- `renamed` : projet renommé ou déplacé  
- `inactive` : projet inactif

Une alerte ne signifie pas nécessairement qu'un package ou une extension présente une vulnérabilité de sécurité.

Elle indique qu'un élément installé correspond à une entrée connue dans la base du projet et mérite éventuellement une vérification.

---

## Utilisation

Clonez ou téléchargez le projet, puis ouvrez un terminal dans son dossier.

### Vérifier les packages Python

```bash
python checker.py
```

Le script analyse l'environnement Python depuis lequel il est exécuté.

Pour analyser un environnement virtuel particulier, activez d'abord cet environnement puis lancez le script.

Exemple :

```bash
python checker.py
```

Si aucune correspondance connue n'est trouvée :

```text
[OK] No known alert found.
     Aucune alerte connue détectée.
```

Si un package présent dans la base est détecté, une alerte similaire à celle-ci est affichée :

```text
[!] package-name 1.0.0
    Status / Statut: DEPRECATED / DÉPRÉCIÉ

    Reason:
    ...

    Raison :
    ...

    Suggested replacement / Remplacement suggéré: ...

    Source: ...
```

### Vérifier les extensions VS Code

```bash
python extension.py
```

VS Code doit être installé et la commande `code` doit être accessible depuis le terminal.

Le script récupère les extensions installées et leurs versions, puis les compare à `extensions.json`.

Si aucune correspondance connue n'est détectée :

```text
[OK] No known alert found.
     Aucune alerte connue détectée.
```

---

## Bases d'alertes

Le projet utilise deux fichiers locaux :

```text
alerts.json
extensions.json
```

`alerts.json` contient les alertes concernant les packages Python.

`extensions.json` contient les alertes concernant les extensions VS Code.

Chaque entrée peut contenir un statut, une explication en français et en anglais, un remplacement éventuel et une source permettant de vérifier l'information.

Les bases sont amenées à évoluer au fil des nouvelles dépréciations, migrations et archives identifiées.

---

## Fonctionnement local

Dependency Security Checker fonctionne localement.

Les scripts n'envoient pas la liste de vos packages ou extensions vers un serveur externe et aucune API distante n'est nécessaire pour effectuer l'analyse.

Les comparaisons sont réalisées avec les fichiers JSON présents dans le projet.

---

## Aucune modification automatique

L'outil fonctionne en lecture seule.

Il ne :

- désinstalle aucun package  
- supprime aucune extension  
- désactive aucune extension  
- met à jour aucune dépendance  
- installe aucun remplacement  
- modifie aucun projet

Il affiche uniquement les alertes correspondant aux bases locales.

La décision de conserver, remplacer, mettre à jour ou supprimer un élément appartient à l'utilisateur.

---

## Prérequis

Pour l'analyse Python :

```text
Python 3
```

Aucune dépendance Python externe n'est nécessaire.

Pour l'analyse des extensions :

```text
Python 3
Visual Studio Code
Commande "code" disponible dans le PATH
```

---

## Limites

Les bases d'alertes ne prétendent pas être exhaustives.

L'absence d'alerte ne signifie pas qu'un package ou une extension est maintenu, sécurisé ou exempt de vulnérabilité.

Inversement, la présence d'une alerte ne signifie pas nécessairement que l'élément est dangereux.

L'outil constitue un premier niveau d'information destiné à attirer l'attention sur des dépendances connues comme dépréciées, archivées, renommées, inactives ou non maintenues.

Les sources indiquées dans les alertes permettent d'effectuer une vérification complémentaire.

---

## Contribution

Les contributions sont les bienvenues, notamment pour :

- signaler une dépendance dépréciée ou abandonnée  
- signaler une extension VS Code dépréciée ou abandonnée  
- corriger une information existante  
- ajouter ou améliorer une source  
- proposer une amélioration du checker

Toute nouvelle alerte devrait idéalement être accompagnée d'une source publique permettant de vérifier son statut.

---

## Licence

Ce projet est distribué sous licence MIT.

© Palks Studio — voir LICENSE.md  
- https://palks-studio.com
