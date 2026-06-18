Szymon Świderski 343159
Krzysztof Sitarz 343147

Projekt na Fizyke: Gra w Życie (Conway's Game of Life)
W ramach projektu napisaliśmy symulator słynnej "Gry w Życie" w Pythonie (biblioteka Pygame). To klasyczny automat komórkowy, który na pierwszy rzut oka wygląda jak prosta gra, ale w praktyce to świetny matematyczny model ilustrujący zachowanie układów złożonych i teorię chaosu w fizyce.

Zasady gry (każda komórka ma 8 sąsiadów):
- Narodziny: Martwa komórka z dokładnie 3 sąsiadami ożywa.
- Przetrwanie: Żywa komórka z 2 lub 3 sąsiadami żyje dalej.
- Śmierć: W każdym innym przypadku komórka umiera (z "samotności" poniżej 2 lub "przeludnienia" powyżej 3 sąsiadów).

Związki z fizyką

Teoria Chaosu i Efekt Motyla: Układ jest w 100% deterministyczny, ale zmiana stanu zaledwie jednej komórki startowej potrafi całkowicie zmienić całą przyszłą ewolucję planszy.

Emergencja: Tak jak zderzenia prostych atomów generują złożone ciśnienie gazu, tak z zaledwie kilku banalnych reguł wyłaniają się skomplikowane, "ruchome" struktury makroskopowe.

Entropia i Równowaga: Symulacja obrazuje termodynamiczną strzałkę czasu. Losowe układy z czasem "wypalają się", przechodząc w stan równowagi (martwa plansza lub proste oscylacje).

Obsługa programu:
Myszka – ręczne rysowanie układów na planszy.
Strzałki (Góra/Dół) – regulacja prędkości symulacji.
Przyciski menu – wczytywanie gotowych struktur i tryb losowy.
