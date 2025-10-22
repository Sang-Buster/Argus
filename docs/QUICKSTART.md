# Argus Quickstart Guide

**Get started with UAV Remote ID spoofing research in 10 minutes.**

## Installation

```bash
# Install dependencies
uv pip install -r requirements.txt

# Install Argus in development mode
uv pip install -e .

# Verify installation
uv run python -c "import argus; print('✓ Argus installed')"
```

## Quick Examples

### 1. Simulate a UAV Swarm (30 seconds)

```python
from argus_uav.core.swarm import Swarm
import numpy as np

rng = np.random.default_rng(seed=42)
swarm = Swarm(num_uavs=30, comm_range=200.0, bounds=(500, 500, 100), rng=rng)

for t in range(10):
    swarm.step(dt=1.0)
    print(f"t={t}s: {swarm.get_statistics()}")
```

### 2. Inject Phantom Attack (1 minute)

```python
from argus_uav.attacks import AttackScenario, AttackType
from argus_uav.attacks.phantom_uav import PhantomInjector

attack = AttackScenario(AttackType.PHANTOM, 5.0, 10.0, phantom_count=5)
injector = PhantomInjector()
injector.inject(swarm, attack, 5.0)

print(f"Phantoms added! Total: {len(swarm.uavs)} UAVs")
```

### 3. Detect with Graph Methods (2 minutes)

```python
from argus_uav.detection.spectral import SpectralDetector

# Train on baseline
detector = SpectralDetector(threshold=1.0)
baseline = [swarm.get_graph().copy() for _ in range(20)]
detector.train(baseline)

# Detect
result = detector.detect(swarm.get_graph())
metrics = result.compute_metrics()

print(f"TPR: {metrics['tpr']:.2%}, FPR: {metrics['fpr']:.2%}, F1: {metrics['f1']:.2f}")
```

### 4. Perfect Detection with Crypto (3 minutes)

```python
from argus_uav.detection.crypto_detector import CryptoDetector

# Create crypto-enabled swarm
crypto_swarm = Swarm(30, 200.0, (500, 500, 100), rng, enable_crypto=True)

# Train detector
crypto_detector = CryptoDetector()
crypto_baseline = [crypto_swarm.get_graph() for _ in range(10)]
crypto_detector.train(crypto_baseline)

# Inject attack and detect
injector.inject(crypto_swarm, attack, 0.0)
result = crypto_detector.detect(crypto_swarm.get_graph())

print(f"Perfect detection: {result.compute_metrics()}")
# Expected: {'tpr': 1.0, 'fpr': 0.0, 'f1': 1.0}
```

### 5. Run Automated Experiment (5 minutes)

```bash
# Run from config file
uv run python scripts/run_experiment.py --config configs/phantom_attack.yaml

# Results saved to results/phantom_attack/ with:
# - metrics.json
# - results_table.md
# - figures/ (PNG + PDF plots)
```

### 6. Parameter Sweep (10 minutes)

```bash
# Sweep phantom count
uv run python scripts/sweep_parameters.py \
    --config configs/phantom_attack.yaml \
    --param phantom_count \
    --values 1,3,5,10,15

# Compare results across configurations
```

## Pre-Built Examples

Run the demonstration scripts:

```bash
# Simple swarm simulation
uv run python examples/simple_swarm.py

# Dense connected network
uv run python examples/dense_swarm.py

# All three attack types
uv run python examples/attack_demo.py

# Graph-based detection
uv run python examples/detection_demo.py

# Cryptographic defense
uv run python examples/crypto_demo.py

# Generate all visualizations
uv run python examples/visualization_demo.py
```

## Common Tasks

### Change Swarm Parameters

Edit `configs/baseline_swarm.yaml`:

```yaml
swarm_size: 75 # More UAVs
comm_range: 150.0 # Larger range
simulation_duration: 300.0 # Longer simulation
```

### Add New Attack Scenario

Create `configs/my_attack.yaml`:

```yaml
experiment_name: "my_custom_attack"
attack_scenario:
  attack_type: "phantom"
  phantom_count: 10
  start_time: 20.0
  duration: 40.0
detection_methods:
  - "spectral"
  - "crypto"
```

### Compare Detection Methods

```python
methods = {
    'Spectral': SpectralDetector(),
    'Centrality': CentralityDetector(),
    'Crypto': CryptoDetector()
}

for name, detector in methods.items():
    detector.train(baseline)
    result = detector.detect(test_graph)
    print(f"{name}: {result.compute_metrics()}")
```

## Troubleshooting

**ModuleNotFoundError: No module named 'argus'**

```bash
uv pip install -e .
```

**Plots don't appear**

```bash
# Use uv run to ensure proper environment
uv run python examples/visualization_demo.py
```

**Tests failing**

```bash
# Run tests with uv
uv run pytest tests/ -v
```

## Performance Tips

**For faster experiments:**

- Reduce `swarm_size` (30 instead of 50)
- Reduce `simulation_duration` (60s instead of 120s)
- Use fewer detection methods

**For better connectivity:**

- Increase `comm_range` (150-200m)
- Decrease bounds (smaller area)
- More UAVs in same space

**For better detection:**

- Lower thresholds (0.5-1.0 instead of 2.0)
- Collect more baseline graphs (30-50 instead of 20)
- Enable crypto for perfect accuracy

## Next Steps

1. Read [algorithm_details.md](algorithm_details.md) for theory
2. Check [data_formats.md](data_formats.md) for specifications
3. Review [references.md](references.md) for research papers
4. Run experiments and generate results!

## Getting Help

- Check [README.md](../README.md) for overview
- Read module docstrings for API details
- Examine test files for usage examples
- Review example scripts in `examples/`

Happy researching! 🚁
