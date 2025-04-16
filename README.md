# 🧠 AdemoTool — Discord MultiTool

Une interface graphique stylée en **PySide6** pour centraliser plusieurs outils d'OSINT, de spam, de tracking et d'autres utilitaires... 💻⚡


---

## 🚀 Fonctionnalités incluses

| Bouton                  | Description                                         |
|------------------------|-----------------------------------------------------|
| **GithubLookup**       | Recherche d'informations sur un utilisateur GitHub  |
| **CcGen**              | Générateur de cartes de crédit factices             |
| **RaidBot**            | Raid automatisé sur plateformes (usage perso !)     |
| **EventSpammer**       | Spam d'événements automatisé                        |
| **GunsLol UserGen**    | Générateur + checker de users Gunslol               |
| **Webhook Spammer**    | Spam de webhook Discord                             |
| **SearchDatabase**     | Recherche dans des bases de données leaks           |
| **osintTool**          | Outil OSINT avec IP/Numéro/Username Lookup          |
| **MailTracker**        | Vérifie où un mail est enregistré (20+ sites)       |
| **InfoTool**           | Donne les infos système, IP, OS, etc.               |
| **soon...**            | Slots réservés pour les futurs outils               |

---

## 🖼️ Interface

- Interface **PySide6**
- Design **cyberpunk** (néons, ombres, animations, etc.)
- Responsive et lisible
- Effets de survol sur chaque bouton
- Grille dynamique avec couleurs cycliques

---

## 🛠️ Installation

```bash
git clone https://github.com/ademoxx/AdemoMultiTool.git
cd AdemoTool
pip install -r requirements.txt

## 🚀 Fonctionnalités actuelles

- Interface graphique avec effets néon (PySide6 / Qt)
- Boutons personnalisés pour chaque outil
- Exécution indépendante des scripts via `subprocess`
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
