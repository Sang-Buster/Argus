<div align="center">
   <a href="https://github.com/Sang-Buster/Argus">
      <img src="https://raw.githubusercontent.com/Sang-Buster/Argus/refs/heads/main/assets/favicon.svg" width=20% alt="logo">
   </a>   
   <h1>Argus</h1>
   <a href="https://deepwiki.com/Sang-Buster/Argus"><img src="https://deepwiki.com/badge.svg" alt="Ask DeepWiki"></a>
   <a href="https://pypi.org/project/argus_uav/"><img src="https://img.shields.io/pypi/v/argus_uav" alt="PyPI"></a>
   <a href="https://github.com/Sang-Buster/Argus/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Sang-Buster/Argus" alt="License"></a>
   <a href="https://github.com/astral-sh/uv"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv"></a>
   <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
   <a href="https://github.com/Sang-Buster/Force-Fusion/commits/main"><img src="https://img.shields.io/github/last-commit/Sang-Buster/Argus" alt="Last Commit"></a>
   <h6 align="center"><small>A UAV Remote ID Spoofing Defense System.</small></h6>
   <p><b>#UAV Swarm Security &emsp; #Remote ID Spoofing &emsp; #Graph-Theoretic Modeling &emsp; #Cryptographic Defenses</b></p>
</div>

---

<h2 align="center" id="-table-of-contents">📑 Table of Contents</h2>

<p align="left">
<li><a href="#-overview">🔭 Overview</a></li>
<li><a href="#-key-features">✨ Key Features</a></li>
<li><a href="#-installation">📦 Installation</a></li>
<li><a href="#-quick-start">🚀 Quick Start</a></li>
<li><a href="#-testing">🧪 Testing</a></li>
<li><a href="#-project-structure">📁 Project Structure</a></li>
<li><a href="#-documentation">📚 Documentation</a></li>
<li><a href="#-research-background">🔬 Research Background</a></li>
<li><a href="#-contributing">🤝 Contributing</a></li>
<li><a href="#-references">📖 References</a></li>
</p>

---

<h2 align="center" id="-overview">🔭 Overview</h2>

**Argus** is a research framework for investigating UAV swarm vulnerabilities to Remote ID spoofing attacks. It combines graph-theoretic analysis with cryptographic defenses to detect and prevent:

<table>
  <tr>
    <th>📄 Paper</th>
    <th>👨🏻‍🏫 Presentation</th>
  </tr>
  <tr>
    <td align="center">
          <a href="https://github.com/Sang-Buster/Argus/blob/main/assets/paper.pdf"><img src="https://raw.githubusercontent.com/Sang-Buster/Argus/refs/heads/main/assets/paper.png" /></a>
          <a href="https://github.com/Sang-Buster/Argus/blob/main/assets/paper.pdf"><img src="https://img.shields.io/badge/View%20More-282c34?style=for-the-badge&logoColor=white" width="100" /></a>
    </td>
    <td align="center">
          <a href="https://github.com/Sang-Buster/Argus/blob/main/assets/presentation.pdf"><img src="https://raw.githubusercontent.com/Sang-Buster/Argus/refs/heads/main/assets/presentation.png" /></a>
          <a href="https://github.com/Sang-Buster/Argus/blob/main/assets/presentation.pdf"><img src="https://img.shields.io/badge/View%20More-282c34?style=for-the-badge&logoColor=white" width="100" /></a>
    </td>
  </tr>
</table>

---

<h2 align="center" id="-key-features">✨ Key Features</h2>

### 🎮 Simulation & Attacks

- **Swarm Simulation** — Dynamic graph-based UAV network modeling with configurable parameters
- **Attack Injection** — Multiple spoofing scenarios with ground truth tracking

### ⚔️ Attack Types

| Attack Type                   | Description                                               |
| ----------------------------- | --------------------------------------------------------- |
| 🎭 **Phantom UAV Injection**  | Non-existent UAVs broadcasting fake Remote ID messages    |
| 📍 **Position Falsification** | Legitimate UAVs reporting spoofed GPS coordinates         |
| 🔀 **Coordinated Attacks**    | Multiple synchronized spoofers disrupting swarm consensus |

### 🔍 Detection Methods

| Method                   | Description                             | Performance                 |
| ------------------------ | --------------------------------------- | --------------------------- |
| 📊 **Spectral Analysis** | Laplacian eigenvalue anomaly detection  | Fast & lightweight          |
| 🎯 **Centrality-Based**  | Graph centrality metric analysis        | Good for structural changes |
| 🤖 **Machine Learning**  | Node2Vec embeddings + Isolation Forests | Adaptive detection          |
| 🔐 **Cryptographic**     | Ed25519 signature verification          | **100% TPR, 0% FPR!**       |

### 📈 Analysis & Visualization

- **Consensus Analysis** — Quantify attack impact on swarm coordination
- **Publication-Quality Plots** — ROC curves, heatmaps, comparisons (300 DPI PDF+PNG)
- **Live Real-Time Animation** — Watch UAVs move and attacks unfold with PySide6 (Qt6)
- **Interactive Detection Overlay** — Enhanced visualization with detection status

---

<h2 align="center" id="-installation">📦 Installation</h2>

### Prerequisites

> 🐍 Python 3.10 or higher with pip or uv package manager

### From PyPI (Recommended)

```bash
# Install from PyPI
pip install argus_uav

# Verify installation
argus --help
```

### From Source (For Development)

```bash
# Clone the repository
git clone https://github.com/Sang-Buster/Argus.git
cd Argus

# Create virtual environment
uv sync
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Verify installation
argus --help
pytest tests/ -v
```

---

<h2 align="center" id="-quick-start">🚀 Quick Start</h2>

### 🎛️ Interactive CLI (Recommended)

The easiest way to get started:

```bash
# Launch interactive mode
argus

# Quick command-line usage
argus --attack phantom --detectors all --mode comparison

# See all options
argus --help
```

> 📖 **See [CLI User Guide](docs/CLI.md) for complete documentation.**

The CLI provides:

- ✨ **Interactive mode** — Guided experience for beginners
- 🎬 **Live visualization** — Watch attacks and detection in real-time
- 📊 **Performance comparison** — Automated benchmarking and plots
- 🎯 **Full coverage** — Test any combination of 3 attacks × 4 detection methods

### 1️⃣ Simulate a Clean UAV Swarm

```python
from argus_uav.core.swarm import Swarm
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

### 2️⃣ Inject and Detect Phantom UAVs

```python
from argus_uav.attacks.phantom_uav import PhantomInjector
from argus_uav.attacks import AttackScenario, AttackType
from argus_uav.detection.spectral import SpectralDetector

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

> For advanced experiments with custom configurations, use the Python API directly. See the `examples/` directory for comprehensive demonstrations.

### 3️⃣ Compare All Detection Methods

```bash
# Run performance comparison with all detectors
argus --attack phantom --detectors all --mode comparison

# Live visualization with specific detectors
argus --attack coordinated --detectors spectral crypto --mode live

# Both live and comparison modes
argus --attack position --detectors centrality --mode both

# Custom swarm configuration
argus --attack phantom --detectors all --mode comparison \
    --num-uavs 50 --comm-range 150
```

---

<h2 align="center" id="-testing">🧪 Testing</h2>

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

---

<h2 align="center" id="-project-structure">📁 Project Structure</h2>

```
src/argus_uav/
├── 🎮 core/           # Simulation engine (UAV, swarm, Remote ID)
├── ⚔️ attacks/        # Attack injection (phantom, position spoof, coordinated)
├── 🔍 detection/      # Detection algorithms (spectral, centrality, ML)
├── 🔐 crypto/         # Ed25519 signing and verification
├── 🤝 consensus/      # Swarm consensus algorithms
├── 📊 evaluation/     # Metrics, visualizations, ROC curves
├── 🧪 experiments/    # Experiment runner and configuration
└── 🛠️ utils/          # Random seeds, logging

tests/
├── unit/              # Unit tests for individual components
├── integration/       # End-to-end scenario tests
├── contract/          # Interface compliance tests
└── performance/       # Benchmark and profiling tests

assets/                # Images, paper, presentation
docs/                  # Documentation and examples
examples/              # Example demonstrations and scripts
results/               # Experiment outputs (gitignored)
```

---

<h2 align="center" id="-documentation">📚 Documentation</h2>

**📖 [Complete Documentation Index](docs/README.md)**

### Quick Links

| Guide                                             | Description                 |
| ------------------------------------------------- | --------------------------- |
| 🚀 [Quickstart Guide](docs/QUICKSTART.md)         | Get started in 10 minutes   |
| 📊 [Project Status](docs/STATUS.md)               | Complete status & features  |
| 🧮 [Algorithm Details](docs/algorithm_details.md) | Theory and implementation   |
| 📋 [Data Formats](docs/data_formats.md)           | Specifications and schemas  |
| 📖 [References](docs/references.md)               | 19 research paper citations |

---

<h2 align="center" id="-research-background">🔬 Research Background</h2>

This project investigates defenses against Remote ID spoofing, a critical security challenge for UAV swarms. Remote ID is mandated by aviation authorities (FAA 14 CFR Part 89) but lacks authentication, making it vulnerable to falsified messages.

### 🎯 Key Research Questions

1. Can graph-theoretic metrics detect topological anomalies from phantom UAVs?
2. How effective is machine learning (Node2Vec + Isolation Forests) vs pure graph analysis?
3. What is the performance overhead of Ed25519 cryptographic signing for real-time swarms?
4. How do spoofing attacks impact swarm consensus algorithms?

### 🔧 Methodology

| Aspect               | Approach                                                        |
| -------------------- | --------------------------------------------------------------- |
| **Simulation**       | Software-only UAV swarm modeling (no hardware required)         |
| **Attack Scenarios** | Phantom injection, position falsification, coordinated spoofers |
| **Detection**        | Spectral analysis, centrality metrics, ML embeddings            |
| **Defense**          | Ed25519 digital signatures for message authentication           |
| **Evaluation**       | TPR, FPR, detection latency, consensus error                    |

---

<h2 align="center" id="-contributing">🤝 Contributing</h2>

This is a research project. Contributions are welcome!

### 🌟 Areas of Interest

- 🧠 Additional detection algorithms (GNNs, threshold signatures)
- 📡 Real-world Remote ID traffic datasets
- 🔧 Hardware integration (RTL-SDR, physical UAVs)
- 📈 Scalability optimizations for larger swarms

---

<h2 align="center" id="-references">📖 References</h2>

1. Peel, L., et al. (2015). _"Detecting Change Points in Evolving Networks"_
2. Olfati-Saber, R., & Murray, R. M. (2004). _"Consensus Problems in Networks"_
3. Grover, A., & Leskovec, J. (2016). _"node2vec: Scalable Feature Learning"_
4. Liu, F. T., et al. (2008). _"Isolation Forest"_
5. Bernstein, D. J., et al. (2012). _"High-speed high-security signatures"_ (Ed25519)
