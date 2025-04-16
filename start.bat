@echo off
echo Installation des dépendances en cours...
pip install -r requirements.txt

echo Lancement de l'interface...
python interface.py

pause
