import os
import pytest
from pymongo import MongoClient


def _get_collection():
    uri = os.environ["MONGODB_URI"]
    db_name = os.environ["DB_NAME"]
    coll_name = os.environ["COLLECTION_NAME"]
    client = MongoClient(uri)
    return client, client[db_name][coll_name]


def _random_document(coll):
    # obtenir un document au hasard
    docs = list(coll.aggregate([{"$sample": {"size": 1}}]))
    return docs[0] if docs else None


@pytest.mark.mongo
def test_collection_not_empty():
    client, coll = _get_collection()
    try:
        assert coll.estimated_document_count() > 0, "Collection vide = injection absente ou incomplète."
    finally:
        client.close()


@pytest.mark.mongo
def test_random_document_field_count_or_schema():
    client, coll = _get_collection()
    try:
        doc = _random_document(coll)
        assert doc is not None, "Impossible de récupérer un document."

        # On ignore _id (ajouté par MongoDB)
        fields = set(doc.keys()) - {"_id"}

        expected_fields = os.environ.get("EXPECTED_FIELDS")
        expected_count = os.environ.get("EXPECTED_FIELD_COUNT")

        if expected_fields:
            expected = {f.strip() for f in expected_fields.split(",") if f.strip()}
            assert fields == expected, f"Schéma inattendu.\nAttendu: {sorted(expected)}\nReçu: {sorted(fields)}"
        elif expected_count:
            n = int(expected_count)
            assert len(fields) == n, f"Nombre de champs inattendu (hors _id) : {len(fields)} au lieu de {n}."
        else:
            pytest.fail("Définissez EXPECTED_FIELDS ou EXPECTED_FIELD_COUNT.")
    finally:
        client.close()
