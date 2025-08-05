
import argparse
import pandas as pd
from start_time_detection import find_overlap

def load_data(pace_file):
    df = pd.read_csv(pace_file)
    df.columns = df.columns.str.strip().str.capitalize()
    return df

def parse_overlaps(overlaps_file, prev_event, curr_event):
    df = pd.read_csv(overlaps_file)
    df.columns = df.columns.str.strip().str.capitalize()
    filtered = df[
        (df['Event'].str.strip().str.lower() == prev_event.lower()) &
        (df['Overlapswith'].str.contains(curr_event, case=False))
    ]
    return filtered

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pace_file")
    parser.add_argument("--prev_event", required=True)
    parser.add_argument("--curr_event", required=True)
    parser.add_argument("--start_prev", type=int, required=True)
    parser.add_argument("--start_curr", type=int, required=True)
    parser.add_argument("--overlaps_file", required=True)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    df = load_data(args.pace_file)
    overlaps = parse_overlaps(args.overlaps_file, args.prev_event, args.curr_event)

    for _, row in overlaps.iterrows():
        seg_start = float(row["Start"])
        seg_end = float(row["End"])

        if args.verbose:
            print(f"🔍 Checking {args.prev_event} vs {args.curr_event} from {seg_start}km to {seg_end}km...")

        summary = find_overlap(
            df,
            prev_event=args.prev_event,
            curr_event=args.curr_event,
            start_prev=args.start_prev,
            start_curr=args.start_curr,
            seg_start=seg_start,
            seg_end=seg_end
        )

        if summary["cumulative_overlap"] == 0:
            print("✅ No overlap detected between events in this segment.")
        else:
            print(f"🟦 Overlap segment: {seg_start} km → {seg_end} km")
            print(f"👥 Total in '{args.curr_event}': {summary['curr_total']} runners")
            print(f"👥 Total in '{args.prev_event}': {summary['prev_total']} runners")
            print(f"⚠️ First overlap at {summary['first_overlap_time']} at {summary['first_overlap_km']}km")
            print(f"📈 Cumulative overlap: {summary['cumulative_overlap']} runners")

if __name__ == "__main__":
    main()
