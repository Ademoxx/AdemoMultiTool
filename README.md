# 🧠 AdemoTool - Python Multitool GUI [#FREE]

**AdemoTool** est un *launcher multitool* codé en Python avec PySide6, pensé pour centraliser plusieurs scripts en une seule interface graphique stylisée et rapide. Que ce soit pour des tests, des outils dev, ou des automations diverses, ce hub t'offre une UX fluide dans une ambiance cyberpunk.

![interface-preview](https://imgur.com/a/dGjeeqg)<!-- Ajoute une image si tu veux -->

---

## 🎯 Objectif

Créer un **multi-outil extensible** avec une interface simple, esthétique et pratique pour exécuter n’importe quel script Python sans passer par la ligne de commande.

---

## 🚀 Fonctionnalités actuelles

- Interface graphique avec effets néon (PySide6 / Qt)
- Boutons personnalisés pour chaque outil
- Exécution indépendante des scripts via `subprocess`
- Design dark mode / cyberpunk
- Facilement extensible (ajout de modules simple)

---

## 📦 Modules intégrés (démo actuelle)

| Nom du module               | Script exécuté                 |
|----------------------------|--------------------------------|
| GithubLookup               | `scripts/option1.py`           |
| CcGen                      | `scripts/ccgen.py`             |
| RaidBot                    | `scripts/raid.py`              |
| EventSpammer               | `scripts/event.py`             |
| GunsLol UserGen&Check      | `scripts/Gunslol.py`           |
| WebHook Spammer            | `scripts/spammer.py`           |
| InfoTool                   | `scripts/info.py`              |
| *...et des emplacements "soon" pour en rajouter* |

---

## 🛠️ Installation

### Prérequis

- Python 3.8 ou plus
- PySide6

### Lancer le tool

```bash
git clone https://github.com/Ademoxx/AdemoMultiTool
cd AdemoMultiTool
pip install -r requirements.txt
python interface.py
