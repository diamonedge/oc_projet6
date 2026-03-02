echo "[Entry_point.sh] Paramétrage"
bash build_params.sh
#cat params.ini
#pip freeze

echo "[Entry_point.sh] Lancement injection"
python3 main.py

echo "[Entry_point.sh] Tests"
pytest -q -m mongo
