# Sokoban

## Mi ez a projekt
Ez a projekt egy Sokoban-játék és a hozzá tartozó solver(ek).
A cél egy játszható játék és különböző solver-megoldások összehasonlítása.
Az összehasonlítás matplotlib grafikonokkal történik több szempont szerint:
- megoldás hossza (lépések száma)
- megoldási idő

## A játék célja
A Sokoban egy logikai tologatós játék, ahol a játékos ládákat mozgat egy rácspályán.
A feladat az, hogy minden ládát célmezőre tolj.

Fontos szabályok:
- A játékos csak tolni tudja a ládát, húzni nem.
- Egyszerre csak egy láda mozgatható.
- Falon vagy másik ládán keresztül nem lehet mozgatni.

Részletesebb leírás:
- [Sokoban - Wikipedia](https://en.wikipedia.org/wiki/Sokoban)

## Indítás
- Környezet: Python 3.11.5
- Telepítsd a pygame-et: "pip install pygame"
- Indítás: "python sokoban.py"
- A játék pygame ablakban fut
- Irányítás: nyílakkal (fel, le, balra, jobbra)
- Kilépés az ablak bezárásával

## Konvencionális jelölések
- "#" fal
- " " üres mező
- "." célmező
- "$" láda
- "*" láda a célmezőn
- "@" játékos
- "+" játékos a célmezőn
