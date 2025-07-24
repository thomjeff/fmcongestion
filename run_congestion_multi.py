#!/usr/bin/env python3
import argparse
import pandas as pd
import itertools
from start_time_detection import will_catch

def main():
    parser = argparse.ArgumentParser(
        description="Detect potential overlaps among multiple race events."
    )
    parser.add_argument(
        "csv_file", help="Path to the participants CSV file (must include 'event','pace','distance')"
    )
    parser.add_argument(
        "--event", action="append", required=True,
        help="Event name (e.g. 'Full', '10K'). Repeat for each event."
    )
    parser.add_argument(
        "--start", action="append", type=float, required=True,
        help="Start time of corresponding event in minutes since midnight (e.g. 420 for 07:00). Repeat."
    )
    parser.add_argument(
        "--x", type=float, default=0.1,
        help="Fraction of fastest runners in the following event (default 0.1)."
    )
    parser.add_argument(
        "--y", type=float, default=0.1,
        help="Fraction of slowest runners in the preceding event (default 0.1)."
    )
    args = parser.parse_args()

    if len(args.event) != len(args.start):
        parser.error("--event and --start must have the same count")

    # Pair events with their start times
    starts = dict(zip(args.event, args.start))
    df = pd.read_csv(args.csv_file)

    # Sort events by their start times
    sorted_events = sorted(starts.keys(), key=lambda e: starts[e])

    print("Checking overlaps among events:")
    for prev, curr in itertools.combinations(sorted_events, 2):
        start_prev = starts[prev]
        start_curr = starts[curr]
        will, dist, time = will_catch(
            df, prev, curr, start_prev, start_curr, x=args.x, y=args.y
        )

        if will:
            hh = int(time // 60)
            mm = int(time % 60)
            time_str = f"{hh:02d}:{mm:02d}"
            status = "⚠️"
        else:
            time_str = "N/A"
            status = "✅"

        print(
            f"{status} '{curr}' catching '{prev}'? {will} | "
            f"Catch at {dist:.2f} km | Around {time_str}"
        )

if __name__ == "__main__":
    main()
