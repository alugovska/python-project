# log_reader.py

from config import MONGO_CONFIG
from pymongo import MongoClient
from collections import Counter
from datetime import datetime
from tabulate import tabulate


# Wörterbuch für Suchtypen
SEARCH_TYPE_LABELS = {
    "keyword": "Suche nach Schüsselwort",
    "genre": "Suche nach Genre",
    "genre_year": "Suche nach Genre und Jahr",
    "genre_year_range": "Suche nach Genre und Jahresbereich",
    "actor": "Suche nach Schauspieler/in",
}

def show_popular_queries(limit=5):
    """
    Zeigt die Statistik der häufigsten Suchanfragen in Tabellenform an.
    
    Args:
        limit (int, optional): Anzahl der beliebtesten Suchtypen, die angezeigt werden sollen. Standardmäßig 5.
    Returns:
        None: Die Funktion druckt die Tabelle auf den Bildschirm.
        Für jeden Suchtyp wird dessen Bezeichnung, die Gesamtanzahl
        und die Top-3 Werte der Suchparameter (falls vorhanden) angezeigt.
    """
    mongo_client = MongoClient(MONGO_CONFIG['uri'])
    collection = mongo_client[MONGO_CONFIG['database']][MONGO_CONFIG['collection']]

    docs = list(collection.find())
    queries = [doc.get("search_type") for doc in docs if doc.get("search_type")]
    counter = Counter(queries)
    top = counter.most_common(limit)

    if not top:
        print("\nEs gibt bisher keine Suchanfragen.")
        return

    table = []
    for i, (query_type, count) in enumerate(top, 1):
        label = SEARCH_TYPE_LABELS.get(query_type, query_type)  # ersetzt den Namen aus dem Wörterbuch

        # Extrahieren der Parameter für diesen Suchtyp
        params_list = [
            doc.get("params", {})
            for doc in docs
            if doc.get("search_type") == query_type and isinstance(doc.get("params"), dict)
        ]

        # Ermittlung der Top-Werte für jeden Parameter
        params_str = []
        for key in params_list[0].keys() if params_list else []:
            values = [p.get(key) for p in params_list if key in p]
            if values:
                sub_counter = Counter(values).most_common(3)
                sub_label = ", ".join(f"{val} ({cnt})" for val, cnt in sub_counter)
                params_str.append(f"{key}: {sub_label}")
               
        table.append([i, label, count, "\n".join(params_str)])

    # Ausgabe der Ergebnisse als Tabelle
    print("\nBeliebteste Suchanfragen nach Parametern:")
    print(tabulate(table, headers=["Nr.", "Suchtyp", "Anzahl", "Top-Parameter"], tablefmt="grid"))


def show_last_unique_queries(limit=5):
    """
    Zeigt die letzten eindeutigen Suchanfragen aus dem Log an.
    
    Args:
        limit (int, optional): Anzahl der eindeutigen Anfragen, die angezeigt werden sollen. Standardmäßig 5.
    Returns:
        None: Die Funktion druckt die Tabelle auf den Bildschirm.
    """
    mongo_client = MongoClient(MONGO_CONFIG['uri'])
    collection = mongo_client[MONGO_CONFIG['database']][MONGO_CONFIG['collection']]

    # Abruf der letzten Einträge nach Zeitstempel (standardmäßig 5)
    docs = list(collection.find().sort("timestamp", -1))

    # Nur eindeutige Kombinationen von search_type+params in Reihenfolge ihres Auftretens auswählen
    seen = set()
    unique_queries = []
    for doc in docs:
        search_type = doc.get("search_type")
        params = doc.get("params", {})
        ts = doc.get("timestamp")
        
        if isinstance(params, str):  # falls versehentlich ein String, überspringen
            params = {}
        key = (search_type, tuple(sorted(params.items())))
        if key not in seen:
            seen.add(key)
            unique_queries.append((search_type, params, ts))
        if len(unique_queries) >= limit:
            break

    if not unique_queries:
        print("\nEs gibt bisher keine eindeutigen Suchanfragen.")
        return

    # Erstellung der Ergebnistabelle
    table = []
    for i, (stype, params, ts) in enumerate(unique_queries, 1):
        label = SEARCH_TYPE_LABELS.get(stype, stype)
        params_str = ", ".join(f"{k}: {v}" for k, v in params.items()) if params else "-"
        ts_str = datetime.fromisoformat(str(ts)).strftime("%Y-%m-%d %H:%M:%S") if ts else "-"
        table.append([i, label, params_str, ts_str])

    print("\nLetzte eindeutige Suchanfragen:")
    print(tabulate(table, headers=["Nr.", "Suchtyp", "Parameter", "Zeit"], tablefmt="grid"))
