# search.py

import pymysql
from config import MYSQL_CONFIG
from tabulate import tabulate
from formatter import *

def get_connection():
    """
    Erstellt und gibt eine Verbindung zur MySQL-Datenbank zurück.
    """
    return pymysql.connect(**MYSQL_CONFIG)


def execute_query(query, params=None):
    """
    Führt eine SQL-Abfrage aus und gibt alle Ergebnisse zurück.
    Args:
        query (str): SQL-Abfrage mit Platzhaltern (%s).
        params (tuple | list | None, optional): Parameter für Platzhalter. Standard None.
    Returns:
        list[tuple]: Ergebnisliste, wobei jede Zeile ein Tupel von Werten ist.
    """
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()


def get_search_keyword():
    """
    Fordert den Benutzer auf, ein Schlüsselwort zur Filmsuche einzugeben.
    Leere Eingaben sind nicht erlaubt.
    Returns:
        str: Gibt das Schlüsselwort zurück.
    """
    keyword = input("\nGeben Sie ein Schlüsselwort für die Suche ein: ").strip()
    if not keyword:
        print("Das Feld für das Schlüsselwort darf nicht leer sein!")
        return get_search_keyword()
    return keyword


def search_film_by_title(keyword):
    """
    Suche von Filmen nach Schlüsselwort im Titel oder in der Beschreibung.
    Args:
        keyword (str): Schlüsselwort für die Suche
    Returns:
        List[Row]: Liste der Filme, jede Zeile als Tupel.
        List[str]: Liste der Spaltenüberschriften für die Ausgabe.
    """
    # SQL-Abfrage zur Filmsuche nach Schlüsselwort
    query = """
        SELECT f.title, f.release_year, c.name, f.rating, f.length
        FROM film f
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        WHERE f.title LIKE %s OR f.description LIKE %s
    """
    
    # Alle Ergebnisse der SQL-Abfrage in der Variable results speichern
    results = execute_query(query, ('%' + keyword + '%', '%' + keyword + '%'))

    if not results:
        print("Keine Filme gefunden.")
    else:
        print(f"\nGefundene Filme für das Schlüsselwort {keyword}: insgesamt {len(results)}")

    # Spaltenüberschriften für die paginierte Ausgabe
    columns = ["Titel", "Erscheinungsjahr", "Genre", "Bewertung", "Laufzeit"]
        
    return list(results), columns


def get_all_genres():
    """
    Suche aller einzigartigen Genres.
    Returns:
        List[Row]: Liste der Genres als Tupel.
    """
    # SQL-Abfrage zur Suche eindeutiger Genres
    query = """
        SELECT category_id, name
        FROM category
        ORDER BY name
    """
    results = execute_query(query)

    # Ausgabe der Ergebnisse für den Benutzer
    print("\nFolgende Filmgenres stehen zur Suche zur Verfügung:")
    print("_" * 60)
    for row in results:
        print(f"{row[0]}. {row[1]}")
        
    return list(results)


def get_year_range():
    """
    Liefert das minimale und maximale Erscheinungsjahr der Filme.
    Returns:
        tuple: Tupel (min_year, max_year)
    """
    with pymysql.connect(**MYSQL_CONFIG) as connection:
        with connection.cursor() as cursor:
            # SQL-Abfrage zur Suche nach minimalem und maximalem Jahr
            query = """
                SELECT MIN(release_year) AS min_year, MAX(release_year) AS max_year
                FROM film
            """
            cursor.execute(query)
            
            result = cursor.fetchone()  # Eine Zeile (min_year, max_year)

            # Ausgabe für den Benutzer
            if result:
                min_year, max_year = result
                print(f"\nErscheinungsjahre der Filme: {min_year} — {max_year}")
                print("_" * 60)
                return min_year, max_year
            else:
                return None, None


def get_valid_genre_num(genres):
    """
    Fordert den Benutzer auf, eine Genre-Nummer einzugeben und prüft deren Gültigkeit.
    Args:
        genres (list[tuple[int, str]]): Liste der Genres [(id, name), ...]
    Returns:
        int: Genre-Nummer
        str: Genre-Name
    """
    valid_numbers = [g[0] for g in genres]

    while True:
        try:
            genre_num = int(input("\nGeben Sie die Genre-Nummer ein: "))
            if genre_num not in valid_numbers:
                print(f"Genre mit der Nummer {genre_num} existiert nicht. Bitte erneut versuchen.")
                continue
                
            # Genre-Name in Variable speichern
            genre_name = next(name for (num, name) in genres if num == genre_num)
            
            return genre_num, genre_name
            
        except ValueError:
            print("\nUngültige Eingabe. Bitte geben Sie eine ganze Zahl ein.")


def search_film_by_genre(genre_num):
    """
    Suche von Filmen nach Genre-Nummer.
    Args:
        genre_num (int): Genre-Nummer
    Returns:
        List[Row]: Liste der Filme als Tupel.
        List[str]: Spaltenüberschriften für die Ausgabe.
    """
    query = """
        SELECT f.title, c.name AS genre, f.release_year, f.rating, f.length
        FROM film f
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        WHERE c.category_id = %s                
        ORDER BY f.title
    """
          
    results = execute_query(query, (genre_num,))            

    if not results:
        print("\nKeine Filme gefunden.")
    else:
        print(f"Insgesamt gefundene Filme: {len(results)}")

    columns = ["Titel", "Genre", "Erscheinungsjahr", "Bewertung", "Laufzeit"]        
        
    return list(results), columns


def get_valid_year(min_year, max_year):
    """
    Fordert den Benutzer auf, ein Jahr einzugeben und prüft die Gültigkeit.
    Args:
        min_year (int): Minimales Jahr
        max_year (int): Maximales Jahr
    Returns:
        int: gültiges Jahr
    """
    while True:
        try:
            year = int(input(f"Geben Sie ein Jahr ein ({min_year}–{max_year}): "))
            if not (min_year <= year <= max_year):
                print(f"Das Jahr muss im Bereich {min_year}–{max_year} liegen. Bitte erneut versuchen.")
                continue
            return year
        except ValueError:
            print("\nUngültige Eingabe. Bitte geben Sie eine ganze Zahl ein.")


def search_film_by_genre_and_year(genre_num, year):
    """
    Suche von Filmen nach Genre und spezifischem Erscheinungsjahr.
    Args:
        genre_num (int): Genre-Nummer aus der Tabelle category.
        year (int): Erscheinungsjahr für die Suche.
    Returns:
        List[Row]: Liste der Filme als Tupel.
        List[str]: Spaltenüberschriften für die Ausgabe.
    """
    query = """
        SELECT f.title, f.release_year, c.name, f.rating, f.length
        FROM film f
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        WHERE fc.category_id = %s AND f.release_year = %s
    """
    results = execute_query(query, (genre_num, year)) 

    if not results:
        print("Keine Filme gefunden.")
    else:
        print(f"\nInsgesamt gefundene Filme: {len(results)}")
        
    columns = ["Titel", "Erscheinungsjahr", "Genre", "Bewertung", "Laufzeit"]        
        
    return list(results), columns


def get_valid_year_range(min_year, max_year):
    """
    Fordert den Benutzer auf, einen Jahresbereich einzugeben und prüft die Gültigkeit.
    Args:
        min_year (int): Minimales Jahr
        max_year (int): Maximales Jahr
    Returns:
        tuple: (Startjahr, Endjahr)
    """
    while True:
        try:
            start_year = int(input(f"Geben Sie das Startjahr ein ({min_year}–{max_year}): "))
            end_year = int(input(f"Geben Sie das Endjahr ein ({min_year}–{max_year}): "))

            if not (min_year <= start_year <= max_year and min_year <= end_year <= max_year):
                print(f"Die Jahre müssen im Bereich {min_year}–{max_year} liegen. Bitte erneut versuchen.")
                continue

            if start_year > end_year:
                print("\nDas Startjahr darf nicht größer als das Endjahr sein. Bitte erneut versuchen.")
                continue

            return start_year, end_year
        except ValueError:
            print("\nUngültige Eingabe. Bitte geben Sie ganze Zahlen ein.")


def search_film_by_genre_and_year_range(genre_id, start_year, end_year):
    """
    Suche von Filmen nach Genre und Jahresbereich.
    Args:
        genre_id (int): Genre-Nummer aus der Tabelle category.
        start_year (int): Startjahr des Bereichs.
        end_year (int): Endjahr des Bereichs.
    Returns:
        List[Row]: Liste der Filme als Tupel.
        List[str]: Liste der Spaltenüberschriften für die Ausgabe.
    """
    # SQL-Abfrage zur Suche von Filmen nach Genre und Jahresbereich
    query = """
        SELECT f.title, f.release_year, c.name, f.rating, f.length
        FROM film f
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        WHERE fc.category_id = %s AND f.release_year BETWEEN %s AND %s
    """
    # Alle Ergebnisse der SQL-Abfrage in der Variable results speichern
    results = execute_query(query, (genre_id, start_year, end_year))

    if not results:
        print("Keine Filme gefunden.")
    else:
        print(f"\nInsgesamt gefundene Filme: {len(results)}")
        
    # Spaltenüberschriften für die paginierte Ausgabe
    columns = ["Titel", "Erscheinungsjahr", "Genre", "Bewertung", "Laufzeit"]        
        
    return list(results), columns


def get_search_actor():
    """
    Fordert den Benutzer auf, den Namen eines Schauspielers/einer Schauspielerin für die Suche einzugeben.
    Leere Eingaben sind nicht erlaubt.
    Returns:
        str: Gibt das Schlüsselwort zurück.
    """
    actor = input("\nGeben Sie den Namen des Schauspielers/der Schauspielerin ein: ").strip()
    if not actor:
        print("Das Feld für den Namen darf nicht leer sein!")
        return get_search_actor()
    return actor


def search_film_by_actor(actor):
    """
    Suche von Filmen nach Name eines Schauspielers/einer Schauspielerin (oder einem Teil davon).
    Args:
        actor (str): Schlüsselwort für die Suche
    Returns:
        List[Row]: Liste der Filme als Tupel.
        List[str]: Liste der Spaltenüberschriften für die Ausgabe.
    """
    # SQL-Abfrage zur Suche von Filmen nach Name des Schauspielers/der Schauspielerin
    query = """
        SELECT CONCAT(a.first_name, ' ', a.last_name), f.title, f.release_year, c.name, f.rating, f.length
        FROM film f
        JOIN film_actor fa ON f.film_id = fa.film_id
        JOIN actor a ON fa.actor_id = a.actor_id
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        WHERE CONCAT(a.first_name, ' ', a.last_name) LIKE %s
        ORDER BY a.last_name ASC, a.first_name ASC, f.release_year DESC
    """
            
    # Alle Ergebnisse der SQL-Abfrage in der Variable results speichern
    results = execute_query(query, ('%' + actor + '%',))

    if not results:
        print("Keine Filme gefunden.")
    else:
        print(f"\nInsgesamt gefundene Filme: {len(results)}")
        
    # Spaltenüberschriften für die paginierte Ausgabe
    columns = ["Name des Schauspielers/der Schauspielerin", "Titel", "Erscheinungsjahr", "Genre", "Bewertung", "Laufzeit"]        
        
    return list(results), columns