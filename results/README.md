# Experiment Results Directory

This directory stores experiment outputs from Argus UAV simulations.

## Directory Structure

Each experiment creates a timestamped subdirectory:

```
results/
├── YYYY-MM-DD_experiment_name/
│   ├── config.yaml              # Experiment configuration
│   ├── metrics.json             # Detection metrics and performance
│   ├── graph_snapshots.pkl      # Saved graph states (optional)
│   ├── manifest.json            # Metadata (commit hash, timestamps)
│   └── figures/                 # Visualization outputs
│       ├── roc_curve.png
│       ├── consensus_error.png
│       └── detection_comparison.png
└── README.md                    # This file
```

## File Formats

### config.yaml

YAML copy of the experiment configuration used to run the simulation.
Ensures reproducibility by capturing all parameters.

### metrics.json

JSON file containing detection metrics:

```json
{
  "spectral": {
    "tpr": 0.85,
    "fpr": 0.08,
    "f1": 0.88,
    "detection_time": 0.045
  },
  "node2vec": {
    "tpr": 0.92,
    "fpr": 0.05,
    "f1": 0.93,
    "detection_time": 0.087
  }
}
```

### graph_snapshots.pkl

Pickled NetworkX graphs captured at key simulation moments:

- t=0: Initial configuration
- Attack start/end times
- Regular intervals for time series analysis

### manifest.json

Experiment metadata for tracking:

```json
{
  "experiment_name": "phantom_attack_experiment",
  "start_time": "2025-10-21T14:30:00Z",
  "end_time": "2025-10-21T14:32:15Z",
  "git_commit": "abc123...",
  "config_hash": "def456...",
  "python_version": "3.10.12",
  "random_seed": 42
}
```

## Usage

Results are automatically saved by `ExperimentRunner`. To load results:

```python
import json
from pathlib import Path

results_dir = Path("results/2025-10-21_phantom_attack")

# Load metrics
with open(results_dir / "metrics.json") as f:
    metrics = json.load(f)

# Load graphs
import pickle
with open(results_dir / "graph_snapshots.pkl", "rb") as f:
    snapshots = pickle.load(f)
```

## Gitignore

Individual result directories are gitignored to avoid bloating the repository.
Only this README and example configurations are tracked.

## Cleanup

To remove old results:

```bash
# Remove results older than 30 days
find results/ -mindepth 1 -maxdepth 1 -type d -mtime +30 -exec rm -rf {} \;

# Keep only most recent 10 experiments
ls -t results/ | tail -n +11 | xargs -I {} rm -rf results/{}
```
