#!/usr/bin/env python3
from decimal import Decimal, ROUND_HALF_UP
import csv
from pathlib import Path

ROOT=Path(__file__).resolve().parent
WEIGHTS={"C1":30,"C2":15,"C3":10,"C4":10,"C5":10,"C6":15,"C7":10}
TIE=("C1","C2")

with (ROOT/"SCORE_MATRIX.csv").open(encoding="utf-8-sig",newline="") as f:
    rows=list(csv.DictReader(f))

out=[]
for r in rows:
    raw=sum(Decimal(r[c])*Decimal(str(w))/Decimal("10") for c,w in WEIGHTS.items())
    rounded=int(raw.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    if rounded != int(r["rounded_total"]):
        raise ValueError(f"{r['sport']}: {rounded} != {r['rounded_total']}")
    out.append((r["sport"],rounded,int(r["C1"]),int(r["C2"])))

out.sort(key=lambda x:(-x[1],-x[2],-x[3],x[0].casefold()))
print("rank,sport,total")
for i,(name,total,*_) in enumerate(out,1):
    print(f"{i},{name},{total}")
