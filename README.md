# Sokoban

## Mi ez a projekt

Ez a projekt egy Sokoban-játék és a hozzá tartozó solver(ek).
A cél egy játszható játék és különböző solver-megoldások összehasonlítása.
Az összehasonlítás matplotlib grafikonokkal történik több szempont szerint:

- megoldás hossza (lépések száma)
- megoldási idő

A játék pygame ablakban fut PNG textúrákkal, van benne undo, reset,
pályaváltás, és játék közben futtatható solver. A projektben külön
pályaszerkesztő is van, és a solverek deadlock-szűrést használnak.

## A játék célja

A Sokoban egy logikai tologatós játék, ahol a játékos ládákat mozgat egy
rácspályán. A feladat az, hogy minden ládát célmezőre tolj.

Fontos szabályok:

- A játékos csak tolni tudja a ládát, húzni nem.
- Egyszerre csak egy láda mozgatható.
- Falon vagy másik ládán keresztül nem lehet mozgatni.

Részletesebb leírás:

- [Sokoban - Wikipedia](https://en.wikipedia.org/wiki/Sokoban)

## Telepítés

A projekt Python 3.11.5 alatt készült. Két külső csomag kell hozzá:
a *pygame* a játékhoz és a pályaszerkesztőhöz, a *matplotlib* a
solver-összehasonlító grafikonhoz. Mindkettő pontos verziója a
**requirements.txt** fájlban van: *pygame==2.5.2* és *matplotlib==3.8.1*.

Telepítés: *pip install -r requirements.txt*.

## Indítás

A játékot a *python sokoban.py* paranccsal lehet elindítani, ez egy
pygame ablakot nyit. Mindig az a pálya töltődik be, amelyik a
**sokoban.py** fájlban a **level_path** változóban szerepel, másik
pályához ezt a sort kell kézzel átírni.

### Vezérlés a játékablakban

- nyilak - mozgás
- **Z** - egy lépés visszavonása
- **R** - a pálya visszaállítása a kezdő állapotra
- **A** - A* solver futtatása és megoldás lejátszása
- **B** - BFS solver futtatása és megoldás lejátszása
- **Space** - következő pálya, csak ha az aktuális már megoldott

## Fájlok

- **sokoban.py** - pygame-es játék. A **level_path** változóban beírt
  pályát tölti be. Tudja az undót, resetet, pályaváltást, és játék
  közben futtatható benne a BFS és A* solver.
- **generator.py** - random pályákat készít a **levels/** mappába. Azért
  van, hogy legyenek saját pályák a mérésekhez, és ne internetről
  kelljen pályákat letölteni.
- **level_editor.py** - pygame-es pályaszerkesztő, kézzel készített
  pályákhoz.
- **compare_solvers.py** - lefuttatja a kiválasztott solvereket a
  pályákon, majd matplotlib grafikont rajzol időre és lépésszámra.
- **bfs.py** - BFS solver. Optimális megoldást keres, de lassú lehet.
- **dfs.py** - DFS solver. Néha gyorsan talál megoldást, de nem
  optimális.
- **astar.py** - gyors A* solver greedy, 5x súlyozott heurisztikával.
  Gyorsan talál megoldást, de az út lehet hosszabb.
- **deadlock.py** - dead-square és sarok deadlock szűrés. A három
  solver mind ezt használja.
- **png/** - a játék és a pályaszerkesztő ezekből a textúrákból
  rajzol.
- **levels/** - pályafájlok. A **palya.txt** egy kézzel készített pálya.


## Használat

### Pályagenerálás

Új pályákat a *python generator.py* paranccsal lehet készíteni. Ez
felülírhatja a **levels/** mappában a meglévő számozott pályákat és a
**solved.txt**-t is, ezért a generátor inkább mérésekhez való. A
generálás a beállításoktól függően akár 45 percig is eltarthat, és
nincs erős időkorlát a teljes generálás maximális idejére.

### Saját pálya készítése

Kézzel készített pályához a *python level_editor.py* paranccsal
lehet elindítani a pályaszerkesztőt. A szerkesztő mindig új fájlba
ment: az első szabad **sajat_XX.txt** nevet keresi, így a régebbi
saját pályákat nem írja felül.

Vezérlés:

- **1** fal
- **2** padló
- **3** cél
- **4** láda
- **5** játékos
- **6** láda célon
- **7** játékos célon
- bal kattintás - kiválasztott elem lerakása
- jobb kattintás - padló lerakása
- **V** - pálya formai ellenőrzése
- **A** - A*-megoldhatóság ellenőrzése időkorlát nélkül
- **S** - mentés új fájlba, de csak valid és A*-gal megoldható pályánál
- **N** - új üres pálya

Formai ellenőrzés:

- csak engedélyezett karakterek vannak a pályán
- pontosan egy játékos van
- a dobozok és célok száma megegyezik
- van legalább egy doboz

### Solverek összehasonlítása

A *python compare_solvers.py* parancs lefuttatja a kiválasztott
solvereket az összes számozott pályán, és két matplotlib grafikont
rajzol: egyet az időre, egyet a megoldás hosszára. Csak a számozott
pályákon fut, a **sajat_\*.txt** fájlokat és a **solved.txt**-t
automatikusan kihagyja.

## Pályajelölések

- **#** fal
- **szóköz**: üres mező
- **.** célmező
- **$** láda
- **\*** láda a célmezőn
- **@** játékos
- **+** játékos a célmezőn

## AI használat

A **png/** mappában lévő textúrák (**wall**, **floor**, **target**,
**box**, **box_on_target**, **player**) AI képgenerátorral készültek.

- **png/wall.png** fal
- **png/floor.png** padló
- **png/target.png** célmező
- **png/box.png** láda
- **png/box_on_target.png** láda a célmezőn
- **png/player.png** játékos