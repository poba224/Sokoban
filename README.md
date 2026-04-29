# Sokoban

## Mi ez a projekt

Ez a projekt egy Sokoban-játék és a hozzá tartozó solver(ek).
A cél egy játszható játék és különböző solver-megoldások összehasonlítása.
Az összehasonlítás matplotlib grafikonokkal történik több szempont szerint:

- megoldás hossza (lépések száma)
- megoldási idő

## A játék célja

A Sokoban egy logikai tologatós játék, ahol a játékos ládákat mozgat egy
rácspályán. A feladat az, hogy minden ládát célmezőre tolj.

Fontos szabályok:

- A játékos csak tolni tudja a ládát, húzni nem.
- Egyszerre csak egy láda mozgatható.
- Falon vagy másik ládán keresztül nem lehet mozgatni.

Részletesebb leírás:

- [Sokoban - Wikipedia](https://en.wikipedia.org/wiki/Sokoban)

## Indítás

- Környezet: **Python 3.11.5**
- A játékhoz pygame kell.
- Az összehasonlító grafikonhoz matplotlib kell.
- A játék pygame ablakban fut.
- Irányítás: nyilakkal (fel, le, balra, jobbra).
- Kilépés az ablak bezárásával.

## Fájlok

- **sokoban.py** - pygame-es játék. A **level_path** változóban beírt pályát tölti be.
- **generator.py** - random pályákat készít a **levels/** mappába. Azért van,
  hogy legyenek saját pályák a mérésekhez, és ne internetről kelljen pályákat
  letölteni.
- **compare_solvers.py** - lefuttatja a kiválasztott solvereket a pályákon, majd
  matplotlib grafikont rajzol időre és lépésszámra.
- **bfs.py** - BFS solver. Optimális megoldást keres, de lassú lehet.
- **dfs.py** - DFS solver. Néha gyorsan talál megoldást, de nem
  optimális.
- **astar.py** - gyors A* solver greedy, 2x súlyozott heurisztikával.
  Gyorsan talál megoldást, de az út lehet hosszabb.

## Használat

A játékot a **sokoban.py** indítja. Mindig azt a pályát tölti be, amelyik a
fájlban a **level_path** változóban szerepel.

A pályagenerálás a **generator.py** fájllal történik. Ez új pályákat ír a
**levels/** mappába, ezért felülírhatja a meglévő pályákat. A generátor célja,
hogy legyenek mérhető saját pályák, és ne kelljen az internetről pályákat
letölteni. A generálás a pályáktól függően akár 45 percig is eltarthat, és
nincs erős időkorlát a teljes generálás maximális idejére.

(Ha pályát akarsz generálni a **level_settings** listában lehet állítani a
méretet, darabszámot, falak számát, és ládák számát. A generátor A*-gal
ellenőrzi, és csak megoldható pályát ment.)

A solverek összehasonlítását a **compare_solvers.py** végzi. Lefuttatja a
kiválasztott solvereket a pályákon, majd két grafikont rajzol egyet az időre,
egyet a megoldás hosszára.


## Pályajelölések

- **#** fal
- **szóköz**: üres mező
- **.** célmező
- **$** láda
- **\*** láda a célmezőn
- **@** játékos
- **+** játékos a célmezőn
