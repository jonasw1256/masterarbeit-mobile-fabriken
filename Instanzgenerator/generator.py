"""
Generator fuer die Instanzenleiter c3 bis c8
===========================================

Zweck: kleine Instanzen, die sich beweisbar bis zum Optimum loesen lassen und
trotzdem zur Benchmarkfamilie des Lehrstuhls (c5 bis c20) gehoeren. Die drei
vorhandenen Toy-Instanzen (hand_c2_f1, toy_c*) sind von Hand gebaut und haben
Gitterkoordinaten; ihre Zielwerte sind deshalb nicht mit den Benchmarkwerten
vergleichbar. Dieser Generator zieht aus denselben Verteilungen wie die
Benchmarkinstanzen, gemessen ueber alle 32 Dateien in `instances/`:

    Bearbeitungszeit t_p   ganzzahlig gleichverteilt   5 bis 30
    Teilegroesse a_p       ganzzahlig gleichverteilt  20 bis 350
    Faelligkeit d_i        ganzzahlig gleichverteilt  20 bis 150   je KUNDE
    Strafkosten alpha_i    ganzzahlig gleichverteilt   1 bis 10    je KUNDE
    Koordinaten            Kasten 1..100, Depot fest bei (50,50)

Faelligkeit und Strafkosten sind in der Benchmarkfamilie je Kunde einheitlich,
nicht je Teil. Das ist geprueft und wird hier nachgebildet.

Geometrie: `random` zieht die Kundenorte gleichverteilt im Kasten. `clustered`
zieht round(n/4), mindestens zwei Zentren gleichverteilt in 15..85 und streut
die Kunden mit Standardabweichung 8 darum. Das trifft die gemessene Struktur
der Benchmarkdateien: mittlerer Abstand zum naechsten Nachbarn rund 7 bis 9
bei clustered gegenueber rund 16 bei random.

Konstanten (Kapazitaet, Ruestzeiten, Kosten) sind in der gesamten
Benchmarkfamilie identisch und werden unveraendert uebernommen.

Aufruf
------
    python3 generator.py            # schreibt die Leiter nach ../instances_leiter
"""

import math
import random
from pathlib import Path

ZIEL = Path(__file__).resolve().parent.parent / "instances_leiter"

# In der gesamten Benchmarkfamilie identisch:
KAPAZITAET = 400
SETUP_B = 2
SETUP_MF = 12
REISEZEIT_JE_DISTANZ = 1
KOSTEN_RELOKATION = 200
KOSTEN_RUESTEN_MF = 5
KOSTEN_LIEFERUNG = 2
KOSTEN_ERSTE_MF = 2000

PROC = (5, 30)
SIZE = (20, 350)
DUE = (20, 150)
PEN = (1, 10)


def orte(rng, n, geometrie):
    """Kundenkoordinaten. Depot liegt fest bei (50,50) und ist nicht dabei."""
    if geometrie == "random":
        return [(rng.randint(1, 100), rng.randint(1, 100)) for _ in range(n)]

    zentren = [(rng.randint(15, 85), rng.randint(15, 85))
               for _ in range(max(2, round(n / 4)))]
    punkte = []
    for k in range(n):
        zx, zy = zentren[k % len(zentren)]      # gleichmaessig auf die Zentren
        x = min(100, max(1, round(rng.gauss(zx, 8))))
        y = min(100, max(1, round(rng.gauss(zy, 8))))
        punkte.append((x, y))
    return punkte


def bauen(n_kunden, n_mf, auftraege_je_kunde, geometrie, seed):
    rng = random.Random(seed)
    punkte = orte(rng, n_kunden, geometrie)

    jobs, jid = [], 0
    for i in range(1, n_kunden + 1):
        dd = rng.randint(*DUE)                  # je Kunde einheitlich
        pen = rng.randint(*PEN)
        for _ in range(auftraege_je_kunde):
            jobs.append((jid, i, rng.randint(*PROC), rng.randint(*SIZE), dd, pen))
            jid += 1

    z = []
    z.append(f"Number_Customers: {n_kunden}")
    z.append(f"Mobile Factories (MF): {n_mf}")
    z.append(f"MF Capacity: {KAPAZITAET}")
    z.append("Customer Orders per Customer: "
             + ", ".join([str(auftraege_je_kunde)] * n_kunden))
    z.append("")
    z.append("Jobs\tcustomer   proc\tsize\tDD\t\tPenalty")
    for j in jobs:
        z.append(f"{j[0]}\t\t{j[1]}\t\t{j[2]}\t\t{j[3]}\t\t{j[4]}\t\t{j[5]}")
    z.append("")
    z.append("//Locations  (depot: ID=0)")
    z.append("CustomerID\tX\tY")
    z.append("0\t50\t50")
    for i, (x, y) in enumerate(punkte, start=1):
        z.append(f"{i}\t{x}\t{y}")
    z.append("")
    z.append("//Setup Times")
    z.append(f"SetupBetweenBatches (Setup_B):      {SETUP_B}")
    z.append(f"SetupTimeMobileFactory (Setup_MF):  {SETUP_MF}")
    z.append(f"TravelTimePerDistance:              {REISEZEIT_JE_DISTANZ}")
    z.append("")
    z.append("//Costs")
    z.append("CostType\tValue")
    z.append(f"MobileFactoryRelocation:\t{KOSTEN_RELOKATION}")
    z.append(f"MobileFactorySetup:     \t{KOSTEN_RUESTEN_MF}")
    z.append(f"DeliveryCost:           \t{KOSTEN_LIEFERUNG}")
    z.append(f"InitialMFCost:              {KOSTEN_ERSTE_MF}")
    return "\n".join(z) + "\n"


def leiter():
    """c3 bis c8, beide Geometrien, zwei und fuenf Fabriken, zwei Auftraege.

    Der Aufwand haengt an der Teilezahl, nicht an der Kundenzahl. Mit zwei
    Auftraegen je Kunde sind das 6 bis 16 Teile. jobs3 waere sofort ausserhalb
    dessen, was sich beweisen laesst.

    Die Leiter beginnt bei c3, nicht bei c5. Grund: der erste Durchlauf am
    10.09.2026 hat clustered_c5_f2_jobs2 (10 Teile) nach 900 s und 811 240
    Knoten mit 50,4 % Gap offen gelassen. Zehn Teile sind also bereits
    ausserhalb des Beweisbaren. Die vier handgebauten Toys mit 8 Teilen waren
    beweisbar, also liegt die Grenze dort. c3 und c4 liefern die 6 und 8 Teile
    in der Statistik der Benchmarkfamilie, c5 und aufwaerts bleiben als offene
    Sprossen mit engen Schranken erhalten.
    """
    ZIEL.mkdir(exist_ok=True)
    gebaut = []
    for n in (3, 4, 5, 6, 7, 8):
        for geo in ("clustered", "random"):
            for f in (2, 5):
                # Fester, aus den Parametern abgeleiteter Seed: derselbe Aufruf
                # erzeugt immer dieselbe Datei.
                seed = 1000 * n + 10 * f + (0 if geo == "clustered" else 1)
                # Praefix `leiter`, damit die Namen sich nicht mit der
                # Benchmarkfamilie in `instances/` ueberschneiden.
                name = f"instance_leiter_{geo}_c{n}_f{f}_jobs2.txt"
                (ZIEL / name).write_text(bauen(n, f, 2, geo, seed), encoding="utf-8")
                gebaut.append(name)
    return gebaut


if __name__ == "__main__":
    for name in leiter():
        print("geschrieben:", name)
