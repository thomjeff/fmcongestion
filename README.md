# Race Congestion Detection Suite

A modular Python toolkit to analyze and mitigate on-course congestion among running events. This repository offers two primary approaches:

- **Basic Congestion Check** (without route overlap constraints)  
  - `start_time_calculator_v2.py`  
  - `run_congestion.py`  
  - `run_congestion_multi.py`

- **Enhanced Overlap-Aware Check**  
  - `start_time_detection.py` (updated)  
  - Updated `run_congestion.py`  
  - Updated `run_congestion_multi.py`

---

## Table of Contents

1. [Prerequisites](#prerequisites)  
2. [Installation](#installation)  
3. [Usage](#usage)  
   - [Basic Check](#basic-check)  
   - [Overlap-Aware Check](#overlap-aware-check)  
4. [Configuration](#configuration)  
5. [File Descriptions](#file-descriptions)  
6. [License](#license)

---

## Prerequisites

- Python 3.7 or higher  
- [pandas](https://pandas.pydata.org/)  

```bash
pip install pandas
```

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-org/race-congestion.git
   cd race-congestion
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install pandas
   ```

---

## Usage

### Basic Check

#### Two-Event Check

```bash
python run_congestion.py your_pace_data.csv   --prev_event 10K --curr_event Half   --start_prev 420 --start_curr 460   --x 0.1 --y 0.1
```

- `--x` and `--y` define top/bottom fractions (e.g., 0.1 for 10%).  
- Outputs whether the fastest group of the upcoming event will catch the slowest group of the preceding event.

#### Multi-Event Check

```bash
python run_congestion_multi.py your_pace_data.csv   --event Full --start 420   --event 10K  --start 440   --event Half --start 460   --x 0.1 --y 0.1
```

- Evaluates all pairwise overlaps among provided events.

---

## Overlap-Aware Check

When routes share only partial segments, supply an overlaps CSV (`overlaps.csv`) with columns:

| Event | Start | End | Overlaps          |
|-------|-------|-----|-------------------|
| 10K   | 0     | 3   | Half, Full        |
| Half  | 3     | 6   | Full              |
| ...   | ...   | ... | ...               |

### Two-Event with Overlaps

```bash
python run_congestion.py your_pace_data.csv   --prev_event 10K --curr_event Half   --start_prev 420 --start_curr 460   --x 0.1 --y 0.1   --overlaps_file overlaps.csv
```

- Catches are only valid if they occur within shared segments defined in `overlaps.csv`.

### Multi-Event with Overlaps

```bash
python run_congestion_multi.py your_pace_data.csv   --event Full --start 420   --event 10K  --start 440   --event Half --start 460   --x 0.1 --y 0.1   --overlaps_file overlaps.csv
```

---

## Configuration

- **Pace Units**: Minutes/km (or seconds with consistent units).  
- **Start Times**: Minutes since midnight (e.g., 07:00 → 420).  
- **Fractions vs Counts**: Use the `_v2` calculator if you prefer absolute counts.

---

## File Descriptions

- **start_time_calculator_v2.py**:  
  Calculates ideal start offsets for sequential events based on top/bottom quantiles or absolute counts.

- **start_time_detection.py**:  
  Determines if and where a catch occurs, enforcing overlap constraints when provided.

- **run_congestion.py**:  
  CLI wrapper for two-event checks (basic or overlap-aware).

- **run_congestion_multi.py**:  
  CLI wrapper for multi-event pairwise checks (basic or overlap-aware).

- **overlaps.csv**:  
  Defines overlapping route segments to filter valid catch zones.

---

## License

Apache 2.0
