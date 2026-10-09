# README

# Optimierung der Einsatzplanung mobiler Fabriken in dezentralen Produktionssystemen

Testinstanzen

Die Instanzen beschreiben die integrierte Produktions- und Distributionsplanung
mobiler Fabriken. Sie wurden verwendet, um ein gemischt-ganzzahliges lineares
Programm (MILP) und eine Fix-and-Optimize-Matheuristik zu prüfen und zu
vergleichen.

## Inhalt

| Ordner | Inhalt |
| --- | --- |
| `instances/` | 32 Benchmarkinstanzen, 5 bis 20 Kunden, 2 oder 5 Fabriken, 2 oder 3 Teile je Kunde, Kundenlage clustered oder random |
| `instances_leiter/` | 24 Leiterinstanzen mit 3 bis 8 Kunden, mit `Instanzgenerator/generator.py` erzeugt |
| `instances_kleinst/` | 5 Kleinstinstanzen für die Handrechnung und die Nachrechnung des Modells |
| `Instanzgenerator/` | Generator der Leiterinstanzen |

## Herkunft der Instanzen

Die 32 Benchmarkinstanzen wurden vom Lehrstuhl bereitgestellt. Die
Leiterinstanzen sind mit dem beiliegenden Generator aus den Wertebereichen der
Benchmarkinstanzen gleichverteilt gezogen. Die Kleinstinstanzen sind von Hand
gebaut.

## Dateiformat der Instanzen

Jede Instanz ist eine Textdatei. Sie nennt zuerst die Zahl der Kunden, die
Zahl der Fabriken, deren Bauraumfläche und die Zahl der Teile je Kunde. Es
folgen je Teil der Kunde, die Bearbeitungszeit, die Fläche, die Fälligkeit und
der Strafkostensatz, danach die Koordinaten von Depot (ID 0) und Kunden sowie
Rüstzeiten und Kostensätze.

## Generator

Der Generator benötigt nur Python 3 ohne weitere Pakete. Der Aufruf

```
cd Instanzgenerator
python3 generator.py
```

schreibt die Leiterinstanzen nach `instances_leiter/`. Jede Datei hat einen
festen Seed, der Aufruf erzeugt also genau die beiliegenden Dateien. Die Wertebereiche und
die Erzeugung der Geometrie stehen am Anfang von `generator.py`.

## Lizenz

Instanzen unter CC BY 4.0 (`LICENSE-DATA`), Generator unter der MIT-Lizenz
(`LICENSE`).
