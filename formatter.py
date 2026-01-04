# formatter.py — Funktionen zur Formatierung der Ausgabe (z. B. Tabellen)

from tabulate import tabulate

def print_header():
    """
    Gibt die Kopfzeile des Programms aus.
    """
    print("=" * 60)
    print(" " * 16 + "🎥 FILMSUCHSERVICE")
    print("=" * 60)


def show_table(lst_2D, columns):
    """
    Gibt eine zweidimensionale Liste (Datenzeilen) in Tabellenform aus.
    
    Args:
        lst_2D (list[tuple]): Liste der Zeilen, jede Zeile ist ein Tupel von Werten.
        columns (list[str]): Spaltenüberschriften.
    """
    print(tabulate(lst_2D, headers=columns, tablefmt="grid"))


def print_rows_paginated(lst_2D, columns):
    """
    Gibt die Tabelle seitenweise aus (standardmäßig 10 Einträge pro Seite).
    
    Args:
        lst_2D (List[Row]): Jede Zeile wird als Tupel dargestellt.
        columns (list of str): Spaltenüberschriften.
    """
    for i in range(0, len(lst_2D), 10):
        batch = lst_2D[i:i + 10]
        print(f'\nFilme {i + 1} bis {i + len(batch)} von {len(lst_2D)}:')
        show_table(batch, columns)

        if i + 10 < len(lst_2D):
            cmd = input("\nEnter — weiter, q — beenden: ").lower()
            if cmd == 'q':
                print("Ausgabe gestoppt.")
                break
    print('\n______________________________________________________________________________________')
