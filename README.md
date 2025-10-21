<div align="center">
   <a href="https://github.com/Sang-Buster/Argus">
      <img src="https://raw.githubusercontent.com/Sang-Buster/Argus/refs/heads/main/assets/favicon.svg" width=20% alt="logo">
   </a>   
   <h1>Argus</h1>
   <h5>A UAV Remote ID Spoofing Defense System.</h5>
</div>

**Graph-Theoretic Modeling and Cryptographic Defenses Against Remote ID Spoofing Attacks**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Argus is a research framework for investigating UAV swarm vulnerabilities to Remote ID spoofing attacks. It combines graph-theoretic analysis with cryptographic defenses to detect and prevent:

- 🎭 **Phantom UAV Injection**: Non-existent UAVs broadcasting fake Remote ID messages
- 📍 **Position Falsification**: Legitimate UAVs reporting spoofed GPS coordinates
- 🔀 **Coordinated Attacks**: Multiple synchronized spoofers disrupting swarm consensus

### Key Features

- **Swarm Simulation**: Dynamic graph-based UAV network modeling with configurable parameters
- **Attack Injection**: Multiple spoofing scenarios with ground truth tracking
- **Detection Methods**:
  - Spectral analysis via Laplacian eigenvalues
  - Centrality-based anomaly detection
  - Machine learning with Node2Vec embeddings + isolation forests
  - Cryptographic verification with Ed25519 signatures (100% TPR, 0% FPR!)
- **Consensus Analysis**: Quantify attack impact on swarm coordination
- **Visualization**:
  - Publication-quality plots (ROC curves, heatmaps, comparisons) - 300 DPI PDF+PNG
  - **Live real-time animation** with PyQt5 - Watch UAVs move and attacks unfold!
  - Enhanced interactive visualization with detection overlay

## Installation

### Prerequisites

- Python 3.10 or higher
- pip or uv package manager

### Quick Install

```bash
# Clone the repository
git clone <repository-url>
cd Argus

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Argus in development mode
pip install -e .

# Verify installation
pytest tests/ -v
```

## Quick Start

### 1. Simulate a Clean UAV Swarm

```python
from argus.core.swarm import Swarm
import numpy as np

# Create reproducible simulation
rng = np.random.default_rng(seed=42)
swarm = Swarm(
    num_uavs=20,
    comm_range=100.0,
    bounds=(1000, 1000, 200),
    rng=rng
)

# Run for 10 seconds
for t in range(10):
    swarm.step(dt=1.0)
    print(f"Time {t}s: {swarm.get_graph().number_of_edges()} links")
```

### 2. Inject and Detect Phantom UAVs

```python
from argus.attacks.phantom_uav import PhantomInjector
from argus.attacks import AttackScenario, AttackType
from argus.detection.spectral import SpectralDetector

# Configure phantom attack
attack = AttackScenario(
    attack_type=AttackType.PHANTOM,
    start_time=5.0,
    duration=10.0,
    phantom_count=3
)

# Setup detection
detector = SpectralDetector()
detector.train([swarm.get_graph().copy() for _ in range(20)])

# Run with attack
injector = PhantomInjector()
for t in range(20):
    if attack.is_active(float(t)):
        injector.inject(swarm, attack, float(t))

    swarm.step(dt=1.0)
    result = detector.detect(swarm.get_graph())

    metrics = result.compute_metrics()
    print(f"TPR: {metrics['tpr']:.2%}, FPR: {metrics['fpr']:.2%}")
```

### 3. Run Complete Experiment from Config

```bash
# Run predefined experiment
python scripts/run_experiment.py --config configs/phantom_attack.yaml

# Run parameter sweep
python scripts/sweep_parameters.py \
    --config configs/baseline.yaml \
    --param phantom_count \
    --values 1,3,5,10,15
```

## Project Structure

```
argus/
├── core/              # Simulation engine (UAV, swarm, Remote ID)
├── attacks/           # Attack injection (phantom, position spoof, coordinated)
├── detection/         # Detection algorithms (spectral, centrality, ML)
├── crypto/            # Ed25519 signing and verification
├── consensus/         # Swarm consensus algorithms
├── evaluation/        # Metrics, visualizations, ROC curves
├── experiments/       # Experiment runner and configuration
└── utils/             # Random seeds, logging

tests/
├── unit/              # Unit tests for individual components
├── integration/       # End-to-end scenario tests
├── contract/          # Interface compliance tests
└── performance/       # Benchmark and profiling tests

configs/               # YAML experiment configurations
scripts/               # CLI tools for running experiments
docs/                  # Documentation and examples
results/               # Experiment outputs (gitignored)
```

## Configuration

### Example Experiment Config

`configs/my_experiment.yaml`:

```yaml
experiment_name: "phantom_detection_experiment"
random_seed: 42
swarm_size: 50
comm_range: 100.0
simulation_duration: 180.0
update_frequency: 1.0

attack_scenario:
  attack_type: "phantom"
  start_time: 60.0
  duration: 60.0
  phantom_count: 5

enable_crypto: false

detection_methods:
  - "spectral"
  - "centrality"
  - "node2vec"

output_dir: "results/my_experiment"
```

## Documentation

**📚 [Complete Documentation Index](docs/README.md)**

**Quick Links**:

- **[Quickstart Guide](docs/QUICKSTART.md)** - Get started in 10 minutes
- **[Project Status](docs/STATUS.md)** - Complete status & features
- **[Algorithm Details](docs/algorithm_details.md)** - Theory and implementation
- **[Data Formats](docs/data_formats.md)** - Specifications and schemas
- **[References](docs/references.md)** - 19 research paper citations

**Design Artifacts** (Spec Kit):

- [Specification](specs/001-uav-remote-id-defense/spec.md) - Requirements and user stories
- [Implementation Plan](specs/001-uav-remote-id-defense/plan.md) - Architecture decisions
- [Data Model](specs/001-uav-remote-id-defense/data-model.md) - Entity relationships

## Research Background

This project investigates defenses against Remote ID spoofing, a critical security challenge for UAV swarms. Remote ID is mandated by aviation authorities (FAA 14 CFR Part 89) but lacks authentication, making it vulnerable to falsified messages.

### Key Research Questions

1. Can graph-theoretic metrics detect topological anomalies from phantom UAVs?
2. How effective is machine learning (Node2Vec + isolation forests) vs pure graph analysis?
3. What is the performance overhead of Ed25519 cryptographic signing for real-time swarms?
4. How do spoofing attacks impact swarm consensus algorithms?

### Methodology

- **Simulation**: Software-only UAV swarm modeling (no hardware required)
- **Attack Scenarios**: Phantom injection, position falsification, coordinated spoofers
- **Detection**: Spectral analysis, centrality metrics, ML embeddings
- **Defense**: Ed25519 digital signatures for message authentication
- **Evaluation**: TPR, FPR, detection latency, consensus error

## Performance Benchmarks

Expected performance on modern laptop (8 cores, 16GB RAM):

| Operation                      | Time       |
| ------------------------------ | ---------- |
| Simulate 50 UAVs for 100 steps | ~5 seconds |
| Spectral detection (100 nodes) | ~40ms      |
| Node2Vec detection (100 nodes) | ~80ms      |
| Ed25519 signing                | ~0.05ms    |
| Ed25519 verification           | ~0.1ms     |

## Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=argus --cov-report=html

# Run specific test suites
pytest tests/unit/           # Unit tests only
pytest tests/integration/    # Integration tests only
pytest tests/performance/    # Performance benchmarks
```

## Contributing

This is a research project. Contributions are welcome! Areas of interest:

- Additional detection algorithms (GNNs, threshold signatures)
- Real-world Remote ID traffic datasets
- Hardware integration (RTL-SDR, physical UAVs)
- Scalability optimizations for larger swarms

## References

1. Peel, L., et al. (2015). "Detecting Change Points in Evolving Networks"
2. Olfati-Saber, R., & Murray, R. M. (2004). "Consensus Problems in Networks"
3. Grover, A., & Leskovec, J. (2016). "node2vec: Scalable Feature Learning"
4. Liu, F. T., et al. (2008). "Isolation Forest"
5. Bernstein, D. J., et al. (2012). "High-speed high-security signatures" (Ed25519)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

**Sang Xing** (solo research project)

For questions or collaboration: [xings@my.erau.edu](mailto:xings@my.erau.edu)

---

🚁 **Argus**: Vigilant guardian against UAV Remote ID spoofing
