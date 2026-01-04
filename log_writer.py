# log_writer.py

from config import MONGO_CONFIG
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime


def log_search_query(search_type: str, params: dict, results_count: int):
    """
    Protokolliert Suchanfragen in MongoDB zur Sammlung von Statistiken.
    
    Args:
        search_type (str): Suchtyp (z. B. "keyword", "genre", "actor", "year").
        params (dict): Suchparameter (z. B. {"keyword": "matrix"}).
        results_count (int): Anzahl der gefundenen Ergebnisse.
    """
    
    # Einrichtung der Verbindung zu MongoDB
    try:
        mongo_client = MongoClient(MONGO_CONFIG['uri'])
        searches_collection = mongo_client[MONGO_CONFIG['database']][MONGO_CONFIG['collection']]

        log_entry = {
            "timestamp": datetime.now(),
            "search_type": search_type,
            "params": params,
            "results_count": results_count
        }

        searches_collection.insert_one(log_entry)
        
    except ConnectionFailure as e:
        print(f"Fehler beim Schreiben des Logs: {e}")
    finally:
        mongo_client.close()