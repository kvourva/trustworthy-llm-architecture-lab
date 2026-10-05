"""Command line interface for producing a labelled synthetic dataset."""

import argparse
import csv
from pathlib import Path

from trustworthy_llm.data import generate_incidents


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, default=200)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path("data/synthetic/incidents.csv"))
    args = parser.parse_args()
    incidents = generate_incidents(args.count, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=["incident_id", "category", "description", "risk_level", "synthetic"],
        )
        writer.writeheader()
        writer.writerows(
            {
                "incident_id": item.incident_id,
                "category": item.category,
                "description": item.description,
                "risk_level": item.risk_level.value,
                "synthetic": item.synthetic,
            }
            for item in incidents
        )
    print(f"Wrote {len(incidents)} explicitly synthetic incidents to {args.output}")


if __name__ == "__main__":
    main()
