from __future__ import annotations
from typing import Dict, Iterable, List, Optional
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import BulkWriteError, PyMongoError, CollectionInvalid
import kagglehub, os, csv ,configparser

def download_data(temp_dir:str) -> str:
    os.environ["KAGGLEHUB_CACHE"]=temp_dir
    path = kagglehub.dataset_download("prasad22/healthcare-dataset")
    return path+"/"+"healthcare_dataset.csv"

def ensure_db_and_collection(uri: str, db_name: str, collection_name: str) -> None:
    print(uri)
    client = MongoClient(uri)

    try:
        db = client[db_name]

        existing = set(db.list_collection_names())
        if collection_name in existing:
            print(f"Collection déjà existante: {db_name}.{collection_name}")
            return

        db.create_collection(collection_name)
        print(f"Collection créée: {db_name}.{collection_name}")

    except CollectionInvalid:
        # Rare course condition : quelqu'un l'a créée entre le check et la création
        print(f"Collection déjà existante (race): {db_name}.{collection_name}")
    except PyMongoError as e:
        raise SystemExit(f"Erreur MongoDB: {e}") from e
    finally:
        client.close()

def batched(iterable: Iterable[Dict], batch_size: int) -> Iterable[List[Dict]]:
    """Regroupe un itérable de documents en listes de taille batch_size."""
    batch: List[Dict] = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def csv_rows_as_documents(
    file_path: str,
    delimiter: str = ",",
    encoding: str = "utf-8",
) -> Iterable[Dict]:
    """Lit un CSV et produit un dict par ligne (en supprimant les lignes vides)."""
    with open(file_path, "r", encoding=encoding, newline="") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            # Nettoyage minimal : retirer les champs vides (optionnel)
            doc = {k: v for k, v in row.items() if k is not None and v not in (None, "")}
            if doc:  # ignore lignes vides
                yield doc


def insert_file_in_batches(
    mongo_uri: str,
    db_name: str,
    collection_name: str,
    file_path: str,
    batch_size: int = 1000,
    ordered: bool = False,
    delimiter: str = ",",
    encoding: str = "utf-8",
) -> int:
    """
    Insère un fichier CSV dans MongoDB par lots.
    - ordered=False : continue même si une insertion échoue dans le lot (meilleur débit).
    Retourne le nombre de documents insérés (approximation si erreurs partielles).
    """
    if batch_size <= 0:
        raise ValueError("batch_size doit être > 0")

    client = MongoClient(mongo_uri)
    inserted_total = 0

    try:
        collection: Collection = client[db_name][collection_name]
        docs_iter = csv_rows_as_documents(file_path, delimiter=delimiter, encoding=encoding)

        for batch in batched(docs_iter, batch_size):
            try:
                result = collection.insert_many(batch, ordered=ordered)
                inserted_total += len(result.inserted_ids)
            except BulkWriteError as e:
                # Cas typique : violation d'un index unique, etc.
                # Avec ordered=False, MongoDB insère ce qu'il peut.
                details = e.details or {}
                inserted = details.get("nInserted")
                if isinstance(inserted, int):
                    inserted_total += inserted
                else:
                    # fallback : on ne peut pas être certain du nombre inséré
                    pass
            except PyMongoError as e:
                raise RuntimeError(f"Erreur MongoDB lors de insert_many: {e}") from e

        return inserted_total

    finally:
        client.close()


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('params.ini')
    print("ETAPE 1 - connexion")
    data_file_path=download_data(config['DEFAULT']['TempDir'])
    ensure_db_and_collection(config['DEFAULT']['MongoDbUri'], config['DEFAULT']['Db_name'], config['DEFAULT']['Collection_Name'])

    print("ETAPE 2 - INJECTION")
    n = insert_file_in_batches(
        mongo_uri=config['DEFAULT']['MongoDbUri'],
        db_name=config['DEFAULT']['Db_name'],
        collection_name=config['DEFAULT']['Collection_Name'],
        file_path=data_file_path,
        batch_size=int(config['DEFAULT']['BatchSize']),
        ordered=False,
        delimiter=",",
    )
    print(f"Fin étape 2 - documents injectés : {n}")


