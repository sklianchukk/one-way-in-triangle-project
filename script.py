import itertools
import time
import os
import sys
from datetime import datetime

class ProjektObliczenia:
    def __init__(self, input_path, output_path, backup_dir):
        self.input_path = input_path
        self.output_path = output_path
        self.backup_dir = backup_dir
        self.m = 0
        self.start_time = 0.0

        # Upewniamy się, że wymagane foldery istnieją (tworzymy je, jeśli brakuje)
        os.makedirs(self.backup_dir, exist_ok=True)
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)


    def wczytaj_dane(self):
        """
        Wczytuje liczbę m z pliku.
        """
        try:
            with open(self.input_path, "r", encoding="utf-8") as f:
                self.m = int(f.read().strip())
            
            if self.m <= 2:
                raise ValueError("Liczba miast musi być większa niż 2.")
        except Exception:
            sys.exit(1)
        
        self.start_time = time.time()

    def _oblicz_granice(self, m):
        """
        Oblicza minimalną (Turan) i maksymalną liczbę dróg.
        """
        # Max: Graf pełny
        max_roads = (m * (m - 1)) // 2

        # Min: Twierdzenie Turana
        n1 = m // 2
        n2 = m - n1
        min_roads = (n1 * (n1 - 1)) // 2 + (n2 * (n2 - 1)) // 2

        return min_roads, max_roads

    def _czy_graf_poprawny(self, nodes, edges_set):
        """
        Sprawdza warunek zadania: 
        W każdej trójce miast musi istnieć co najmniej jedna droga.
        """
        for a, b, c in itertools.combinations(nodes, 3):
            if (a, b) not in edges_set and (a, c) not in edges_set and (b, c) not in edges_set:
                return False
        return True

    def _brute_force(self, m, min_roads):
        """
        Klasyczny algorytm Brute-Force.
        Generuje każdą możliwą kombinację dróg i sprawdza warunek.
        """
        nodes = list(range(m))
        # Lista wszystkich możliwych miejsc na drogę
        all_possible_edges = list(itertools.combinations(nodes, 2))
        N = len(all_possible_edges)
        
        valid_count = 0

        # Pętla po liczbie krawędzi (od min_roads do N)
        for r in range(min_roads, N + 1):
            # Generuje konkretne układy dróg o rozmiarze r
            for current_edges in itertools.combinations(all_possible_edges, r):
                # Konwersja na set dla szybszego wyszukiwania
                edges_set = set(current_edges)
                
                # Weryfikacja warunku
                if self._czy_graf_poprawny(nodes, edges_set):
                    valid_count += 1

        return valid_count

    def rozwiazanie(self):
        """Główna logika."""
        n = self.m

        # 1. Obliczenia matematyczne granic
        min_roads, max_roads = self._oblicz_granice(n)

        # 2. Obliczenia właściwe (liczenie sposobów)
        liczba_sposobow = self._brute_force(n, min_roads)
        
        czas_trwania = time.time() - self.start_time
        return liczba_sposobow, min_roads, max_roads, czas_trwania

    def generuj_raport(self, liczba, min_d, max_d, czas):
        """Generuje wyniki w tabeli HTML."""
        
        # 1. Zapis do pliku tekstowego
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(f"Liczba miast: {self.m}\n")
            f.write(f"Min drog: {min_d}\n")
            f.write(f"Max drog: {max_d}\n")
            f.write(f"Liczba sposobow: {liczba}\n")
            f.write(f"Przestrzen poszukiwan: 2^{max_d}\n")
            f.write(f"Czas: {czas:.4f} s\n")

        # 2. Generowanie HTML z Tabelą
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_file_str = datetime.now().strftime("%H-%M-%S_%d-%m")
        space_val = 2 ** max_d

        css_style = """
        <style>
        body { font-family: Arial, sans-serif; margin: 24px; }

        .wrap { max-width: 820px; margin: 0 auto; }
        h1 { font-size: 20px; margin: 0 0 12px 0; text-align: center}

        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 8px 10px; }
        th { background: #f3f3f3; text-align: left; }

        .footer { color: #666; font-size: 0.9em; margin-top: 10px; text-align: center}
        </style>
        """

        html_content = f"""<!doctype html>
        <html lang="pl">
        <head>
        <meta charset="utf-8">
        <title>Raport: {self.m} miast</title>
        {css_style}
        </head>
        <body>
        <div class="wrap">
            <h1>Raport z obliczeń</h1>

            <table>
            <tr><th>Parametr</th><th>Wartość</th></tr>
            <tr><td>Data wykonania</td><td>{now_str}</td></tr>
            <tr><td>Liczba miast (m)</td><td><b>{self.m}</b></td></tr>
            <tr><td>Minimalna liczba dróg (Twierdzenie Turana)</td><td>{min_d}</td></tr>
            <tr><td>Maksymalna liczba dróg</td><td>{max_d}</td></tr>
            <tr><td>Całkowita przestrzeń przeszukiwania</td><td>2<sup>{max_d}</sup> = {space_val}</td></tr>
            <tr><td><b>Liczba poprawnych sposobów</b></td><td><b>{liczba}</b></td></tr>
            <tr><td>Czas obliczeń</td><td>{czas:.4f} s</td></tr>
            </table>

            <div class="footer">
            Projekt z Języków Skryptowych | Wygenerowano automatycznie
            </div>
        </div>
        </body>
        </html>"""
                
        # Zapis unikalnego pliku
        current_report = os.path.join(self.backup_dir, f"raport_{time_file_str}.html")
        with open(current_report, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Rotacja backupu (3 minuty)
        backup_path = os.path.join(self.backup_dir, "raport_backup.html")
        update_needed = True
        if os.path.exists(backup_path):
            if (time.time() - os.path.getmtime(backup_path)) < 180:
                update_needed = False
        
        if update_needed:
            with open(backup_path, "w", encoding="utf-8") as f:
                f.write(html_content)

        # Otwarcie w przeglądarce
        if sys.platform == "win32":
            os.startfile(os.path.abspath(current_report))


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    app = ProjektObliczenia(
        input_path=os.path.join(BASE_DIR, "in", "input.txt"),
        output_path=os.path.join(BASE_DIR, "out", "output.txt"),
        backup_dir=os.path.join(BASE_DIR, "backup")
    )

    try:
        app.wczytaj_dane()
        res, mn, mx, t = app.rozwiazanie()
        app.generuj_raport(res, mn, mx, t)
        sys.exit(0)
    except Exception as e:
        print(f"Błąd wejścia: {e}")
        sys.exit(1)
