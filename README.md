# Miasta i Drogi (Problem Trójek w Grafach)

Repozytorium zawiera rozwiązanie problemu zliczania konfiguracji dróg między $m$ miastami, w których zachowany jest warunek braku "pustych trójek".

## 📝 Opis zadania
Dla zadanej liczby miast $m > 2$, program wyznacza liczbę grafów prostych, w których **każdy podzbiór 3 wierzchołków posiada co najmniej jedną krawędź**. 

Z perspektywy teorii grafów oznacza to zliczanie grafów, których **liczba niezależności $\alpha(G)$ jest mniejsza niż 3** ($\alpha(G) < 3$). Jest to równoważne stwierdzeniu, że dopełnienie grafu ($\bar{G}$) nie zawiera trójkąta ($K_3$).

## 🧮 Powiązanie z OEIS
Liczba poprawnych konfiguracji dla kolejnych $m$ odpowiada ciągowi **[OEIS A213434](https://oeis.org/A213434)**.

### Wyniki weryfikacyjne:
| Miasta ($m$) | Wszystkie grafy ($2^E$) | Poprawne grafy ($k$) |
| :---: | :---: | :---: |
| 3 | 8 | 7 |
| 4 | 64 | 41 |
| 5 | 1 024 | 388 |
| 6 | 32 768 | 5 789 |
| 7 | 2 097 152 | 133 501 |
| 8 | 268 435 456 | 4 682 300 |

## 🚀 Metodologia i Wydajność

### Implementacja (script.py)
Program wykorzystuje algorytm typu **Brute-Force**, który:
1. Generuje pełną przestrzeń stanów dla krawędzi grafu.
2. Weryfikuje każdą kombinację pod kątem obecności zbiorów niezależnych rozmiaru 3.

### Ograniczenia
Z uwagi na wykładniczy wzrost liczby grafów ($2^{m(m-1)/2}$), podejście Brute-Force jest skuteczne jedynie dla niskich wartości $m$. Dla $m \ge 9$ zaleca się stosowanie metod opartych na wielomianach wieżowych lub generowaniu grafów triangle-free dla dopełnień.

## 🛠️ Uruchomienie
```bash
run_project.bat
