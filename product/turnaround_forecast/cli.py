"""python -m turnaround_forecast records.csv --origin 2026-01-01 [--claim DAYS SHARE] [--tau2 X]
records.csv needs columns received, accepted (YYYY-MM-DD) and optionally first_online."""
import argparse, json, sys
import pandas as pd
from .core import forecast, claim_check
def main(argv=None):
    ap = argparse.ArgumentParser(prog="turnaround_forecast", description=__doc__); ap.add_argument("csv"); ap.add_argument("--origin", required=True); ap.add_argument("--tau2", type=float)
    ap.add_argument("--claim", nargs=2, type=float, metavar=("DAYS", "SHARE")); a = ap.parse_args(argv); rec = pd.read_csv(a.csv)
    out = forecast(rec, a.origin, a.tau2)
    if a.claim: out["claim_check"] = claim_check(rec, a.origin, int(a.claim[0]), a.claim[1], a.tau2)
    print(json.dumps(out, indent=1)); return 0
if __name__ == "__main__": sys.exit(main())
