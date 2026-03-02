PARAMS_FILE="params.ini"
echo "[DEFAULT]" > $PARAMS_FILE
echo "MongoDbUri = mongodb://${MONGODB_USER}:${MONGODB_PASSWORD}@${MONGODB_HOST}:27017/" >> $PARAMS_FILE
echo "Db_name = ${MONGODB_DBNAME}" >> $PARAMS_FILE
echo "Collection_Name = ${MONGODB_COLLECTION_NAME}" >> $PARAMS_FILE
echo "TempDir = ${PYTHON_TEMP_DIR}" >> $PARAMS_FILE
echo "BatchSize = ${PYTHON_BATCH_SIZE}" >> $PARAMS_FILE
