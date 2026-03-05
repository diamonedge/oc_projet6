echo "[entrypoint.sh] Paramétrage"
bash build_params.sh
#cat params.ini
#pip freeze

echo "[entrypoint.sh] Mot de passe lecteur"
grep "READER_USER_" params.ini

echo "[entrypoint.sh] Lancement injection"
python3 main.py

echo "[entrypoint.sh] Tests"
pytest -q -m mongo
