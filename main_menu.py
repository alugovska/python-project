# main_menu.py

from search import *
from log_reader import *
from log_writer import *
from formatter import *


def main_menu():
    print_header()  # Kopfzeile ausgeben
    while True:
        print("\nHAUPTMENÜ:")
        print("1. Suche nach Schüsselwort")
        print("2. Suche nach Genre und Jahresbereich")
        print("3. Suche nach Schauspieler/in")
        print("4. Beliebteste Suchanfragen anzeigen")
        print("0. Beenden")

        choice = input("\nWählen Sie einen Menüpunkt (1, 2, 3, 4 oder 0): ")

        if choice == '1':
            # Suche nach Stichwort
            keyword = get_search_keyword()
            films, columns = search_film_by_title(keyword)  
            print_rows_paginated(films, columns)
            log_type = "keyword" 
            params = {"keyword": keyword}
            results_count = len(films)
            log_search_query(log_type, params, results_count) 

        
        elif choice == '2':
            # Suche nach Genre und Jahresbereich
            genres = get_all_genres() 
            min_year, max_year = get_year_range() 
            while True:
                print("\nFilmsuchmodus:")
                print("1. Nur nach Genre suchen")
                print("2. Nach Genre und Jahr/Jahresbereich suchen")
                print("0. Beenden")

                sub_choice = input("\nWählen Sie einen Untermenüpunkt (1, 2 oder 0): ")

                if sub_choice == '1':
                    genre_num, genre_name = get_valid_genre_num(genres)  # gültige Genre-Nummer und Name
                    films, columns = search_film_by_genre(genre_num)
                    print_rows_paginated(films, columns)
                    log_type = "genre" 
                    params = {"genre": genre_name}
                    results_count = len(films)
                    log_search_query(log_type, params, results_count)                     
                                                        

                elif sub_choice == '2':
                    genre_num, genre_name = get_valid_genre_num(genres)
                    while True:
                        print("\nFilmsuchmodus:")
                        print("1. Nach einem Jahr suchen")
                        print("2. Nach einem Jahresbereich suchen")
                        print("0. Beenden")
                        
                        year_choice = input("\nWählen Sie einen Untermenüpunkt (1, 2 oder 0): ")

                        if year_choice == '1':
                            year = get_valid_year(min_year, max_year)
                            films, columns = search_film_by_genre_and_year(genre_num, year)
                            print_rows_paginated(films, columns)
                            log_type = "genre_year" 
                            params = {"genre": genre_name, "year": year}
                            results_count = len(films)
                            log_search_query(log_type, params, results_count)     
                            
                        
                        elif year_choice == '2':
                            start_year, end_year = get_valid_year_range(min_year, max_year)
                            films, columns = search_film_by_genre_and_year_range(genre_num, start_year, end_year)
                            print_rows_paginated(films, columns)
                            log_type = "genre_year_range" 
                            params = {"genre": genre_name, "year_from": start_year, "year_to": end_year}
                            results_count = len(films)
                            log_search_query(log_type, params, results_count) 
                            
                        
                        elif year_choice == '0':
                            break
                        
                        else:
                            print("Ungültige Auswahl. Bitte wählen Sie 1, 2 oder 0.")
                        
                
                elif sub_choice == '0':
                    break
                else:
                    print("Ungültige Auswahl. Bitte wählen Sie 1, 2 oder 0.")


        elif choice == '3':
            # Suche nach Schauspieler/in (oder Teile des Namens)
            actor = get_search_actor()
            films, columns = search_film_by_actor(actor)
            print_rows_paginated(films, columns)
            log_type = "actor" 
            params = {"actor": actor}
            results_count = len(films)
            log_search_query(log_type, params, results_count) 
            

        elif choice == '4':
            # Beliebteste Suchanfragen anzeigen
            while True:
                print("\n" + "=" * 60)
                print(" " * 16 + "STATISTIK DER SUCHANFRAGEN")
                print("=" * 60)
                print("1. Top-5 der beliebtesten Suchanfragen anzeigen")
                print("2. Die 5 letzten eindeutigen Suchanfragen anzeigen")
                print("0. Beenden")

                stat_choice = input("\nWählen Sie einen Menüpunkt (1, 2 oder 0): ")

                if stat_choice == '1':
                    show_popular_queries(limit=5)
                elif stat_choice == '2':
                    show_last_unique_queries(limit=5)
                elif stat_choice == '0':
                    break    
                else:
                    print("Ungültige Auswahl.")
               

        elif choice == '0':
            print("\nProgramm beendet. Vielen Dank, dass Sie unseren Service genutzt haben!")
            break
        else:
            print("Ungültige Auswahl. Bitte wählen Sie 1, 2, 3, 4 oder 0.")
