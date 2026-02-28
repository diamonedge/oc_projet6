touch params.ini
echo "[DEFAULT]" > params.ini
echo "MongoDbUri = mongodb://${MONGODB_USER}:${MONGODB_PASSWORD}@${MONGODB_HOST}:27017/" >> params.ini
echo "Db_name = ${MONGODB_DBNAME}" >> params.ini
echo "Collection_Name = ${MONGODB_COLLECTION_NAME}" >> params.ini
echo "TempDir = ${PYTHON_TEMP_DIR}" >> params.ini
echo "BatchSize = ${PYTHON_BATCH_SIZE}" >> params.ini
pip3 install -r requirements.txt
python3 main.py
