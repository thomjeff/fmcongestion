#!/usr/bin/env python3
import argparse
import pandas as pd
from start_time_detection import will_catch

def main():
    parser = argparse.ArgumentParser(description="Detect course congestion between two events.")
    parser.add_argument("csv_file", help="Path to participants CSV file")
    parser.add_argument("--prev_event", required=True, help="Name of preceding event (e.g. '10K')")
    parser.add_argument("--curr_event", required=True, help="Name of upcoming event (e.g. 'Half')")
    parser.add_argument("--start_prev", type=float, required=True,
                        help="Start time of preceding event in minutes since midnight (e.g. 420 for 07:00)")
    parser.add_argument("--start_curr", type=float, required=True,
                        help="Start time of upcoming event in minutes since midnight (e.g. 450 for 07:30)")
    parser.add_argument("--x", type=float, default=0.1,
                        help="Fraction of fastest runners in upcoming event (0-1)")
    parser.add_argument("--y", type=float, default=0.1,
                        help="Fraction of slowest runners in preceding event (0-1)")
    args = parser.parse_args()

    df = pd.read_csv(args.csv_file)
    will, dist, time = will_catch(df, args.prev_event, args.curr_event,
                                  args.start_prev, args.start_curr, x=args.x, y=args.y)

    if will:
        hours = int(time // 60)
        minutes = int(time % 60)
        print(f"⚠️ Catch occurs at {dist:.2f} km, around {hours:02d}:{minutes:02d}.")
    else:
        print("✅ No catch before the preceding event course finishes.")

if __name__ == "__main__":
    main()
