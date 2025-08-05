fmcongestion/
├── README.md                      # Updated authoritative guide (you’ve got this)
├── CHANGELOG.md                  # Human-readable version history
├── LICENSE                      # Apache-2.0 already present
├── scripts/                     # Core Python scripts
│   ├── detect_overlap.py        # Current upgraded v1 engine
│   └── ... (legacy: run_congestion.py etc. -- consider archiving in legacy/)
├── data/
│   ├── overlaps.csv
│   ├── your_pace_data.csv       # Sample input (maybe rename to sample_pace_data.csv)
│   └── summary_template.xlsx
│   └── summary_dashboard.xlsx
├── examples/                   # Example invocations, input/output snapshots
├── .github/
│   ├── workflows/              # Optional: CI (lint/test), release automation
├── docs/                      # Optional deeper documentation or migration notes
