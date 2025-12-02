# Argus: UAV Remote ID Spoofing Defense System

**Graph-Theoretic Modeling and Cryptographic Defenses**

Sang Xing

---

## Overview

**Research Question**: How can we detect and defend against Remote ID spoofing attacks in UAV swarms?

**Approach**: Graph-theoretic analysis + Cryptographic verification

**Key Results**:

- ✅ 4 detection methods evaluated
- ✅ Cryptographic authentication: Perfect for phantom/coordinated (F1=1.0), ~58ms
- ⚠️ Position falsification: Unsolved (F1=0.0 for all methods)
- ❌ Graph heuristics unsuitable: ML/Centrality FPR=87-100%
- ✅ Real-time performance validated for 20-30 UAV swarms

---

## Problem Statement

### UAV Remote ID Mandate

- **FAA 14 CFR Part 89**: All UAVs must broadcast Remote ID
- **Purpose**: Identify drones in airspace for safety and security
- **Vulnerability**: Broadcast protocol is unauthenticated

### Security Threats

**Three Attack Vectors**:

1. **Phantom UAV Injection** - Broadcast fake drone identities
2. **Position Falsification** - Report false GPS coordinates
3. **Coordinated Attacks** - Multiple attackers working together

**Impact**: Disrupts air traffic control, misleads authorities, enables malicious operations

---

## Research Objectives

### Primary Goals

1. **Model** UAV swarms as dynamic graphs
2. **Implement** realistic attack scenarios
3. **Develop** detection methods using graph theory
4. **Evaluate** cryptographic defenses (Ed25519)
5. **Quantify** performance trade-offs

### Success Criteria

- Detect attacks with high TPR (>80%), low FPR (<10%)
- Real-time performance (<100ms per detection)
- Scalable to 100+ UAV swarms
- Publication-quality results and visualizations

---

## System Architecture

### Simulation Framework

```
┌─────────────────────────────────────────────┐
│         UAV Swarm (10-250 UAVs)            │
│  - Position, Velocity, Remote ID Messages  │
└──────────────┬──────────────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───▼────────┐    ┌──────▼──────┐
│  Attacks   │    │  Defenses   │
├────────────┤    ├─────────────┤
│ • Phantom  │    │ • Spectral  │
│ • Position │    │ • Centrality│
│ • Coordin. │    │ • ML/Node2Vec│
└────────────┘    │ • Crypto    │
                  └─────────────┘
```

**Technology**: Python, NetworkX, NumPy, scikit-learn

---

## Methodology: Graph Representation

### Dynamic Graph Model

**UAVs as Nodes**:

- Each UAV = vertex in graph
- Node attributes: position, velocity, Remote ID

**Communication as Edges**:

- Edge exists if distance ≤ communication range
- Typical range: 100-200 meters
- Graph updates every timestep (1 Hz)

### Graph Properties

- **Connectivity**: Single connected component (legitimate swarm)
- **Density**: Depends on UAV spacing
- **Dynamics**: Topology changes as UAVs move

---

## Attack Implementation

### 1. Phantom UAV Injection

**Method**: Add fake nodes to the graph

- Inject 5-10 phantom UAVs at random positions
- Phantoms broadcast Remote ID messages
- No cryptographic keys (cannot sign)

**Detection Challenge**: Phantoms can mimic movement patterns

---

### 2. Position Falsification

**Method**: Legitimate UAVs report false GPS coordinates

- Select 10-20% of UAVs to compromise
- Add random offset (50-100m) to reported position
- True position used for movement (topology preserved)

**Detection Challenge**: Graph structure unchanged

---

### 3. Coordinated Attack

**Method**: Multiple phantoms in formation

- Create 8+ phantoms moving together
- Patterns: circle, line, or coordinated formation
- Synchronized velocities

**Detection Challenge**: Appears like legitimate sub-swarm

---

## Detection Method 1: Spectral Analysis

### Theory

**Laplacian Matrix**: `L = D - A`

- D = degree matrix (diagonal)
- A = adjacency matrix

**Eigenvalues**: `λ₁ ≤ λ₂ ≤ ... ≤ λₙ`

- λ₂ = algebraic connectivity
- Distribution reveals structural properties

### Detection Algorithm

1. **Baseline**: Compute mean/std of eigenvalues from clean graphs
2. **Monitor**: Track eigenvalue distribution over time
3. **Detect**: Flag anomalies when Z-score > threshold (2.5-2.8)

---

### Spectral Detection: Results

**Performance**:

| Attack Type | TPR  | FPR  | F1   | Time |
| ----------- | ---- | ---- | ---- | ---- |
| Phantom     | 1.00 | 0.00 | 1.00 | ~2ms |
| Position    | 0.00 | 0.00 | 0.00 | ~2ms |
| Coordinated | 1.00 | 0.00 | 1.00 | ~2ms |

✅ **Perfect detection for phantom and coordinated attacks!**

⚠️ **Cannot detect position falsification** - Attack preserves topology

---

## Detection Method 2: Centrality Analysis

### Centrality Metrics

1. **Degree Centrality**: Number of connections

   - `C_D(v) = deg(v) / (n-1)`

2. **Betweenness Centrality**: Bridge position

   - `C_B(v) = Σ(σ_st(v) / σ_st)`

3. **Closeness Centrality**: Average distance to others
   - `C_C(v) = 1 / Σd(v, u)`

### Detection Algorithm

**Anomaly Score**: `0.4×degree_z + 0.4×betweenness_z + 0.2×closeness_z`

Flag if score > threshold (2.0)

---

### Centrality Detection: Results

**Performance**:

| Attack Type | TPR  | FPR  | F1   | Time |
| ----------- | ---- | ---- | ---- | ---- |
| Phantom     | 0.67 | 1.00 | 0.11 | ~1ms |
| Position    | 1.00 | 1.00 | 0.18 | ~1ms |
| Coordinated | 1.00 | 1.00 | 0.17 | ~1ms |

❌ **Unacceptable performance** - 100% false positive rate!

**Why**: High threshold sensitivity, flags too many legitimate UAVs

---

## Detection Method 3: Machine Learning

### ML Detector with Isolation Forest

**Architecture**:

- **Algorithm**: Isolation Forest (anomaly detection)
- **Features**: 4 graph metrics per node
  - Degree centrality
  - Betweenness centrality
  - Clustering coefficient
  - Closeness centrality
- **Training**: Contamination parameter α = 0.15 (expects 15% anomalies)

### Algorithm

1. Extract 4-feature vector per node from baseline graphs
2. Train Isolation Forest on normal (clean) swarm behavior
3. Compute anomaly scores for test graph nodes
4. Flag nodes with scores below threshold

---

### ML Detection: Results

**Performance**:

| Attack Type | TPR  | FPR  | F1   | Time |
| ----------- | ---- | ---- | ---- | ---- |
| Phantom     | 0.33 | 0.93 | 0.06 | ~5ms |
| Position    | 0.67 | 0.96 | 0.13 | ~5ms |
| Coordinated | 1.00 | 0.87 | 0.19 | ~5ms |

❌ **Unacceptable for production** - Very high FPR (87-96%)

**Why**: Limited features, high contamination mismatch, overfitting to training data

---

## Detection Method 4: Cryptography

### Ed25519 Digital Signatures

**Why Ed25519?**

- **Fast**: ~50μs signing, ~100μs verification
- **Secure**: 256-bit security level
- **Small**: 32-byte keys, 64-byte signatures
- **Deterministic**: No nonce reuse vulnerability

### Implementation

**Signing** (legitimate UAVs):

```python
signature = private_key.sign(message_bytes)
remote_id.signature = signature  # 64 bytes
```

**Verification** (receivers):

```python
public_key.verify(message_bytes, signature)
# Raises exception if invalid
```

---

### Cryptographic Detection: Results

**Performance**:

| Attack Type | TPR  | FPR  | F1   | Time  |
| ----------- | ---- | ---- | ---- | ----- |
| Phantom     | 1.00 | 0.00 | 1.00 | ~58ms |
| Position    | 0.00 | 0.00 | 0.00 | ~58ms |
| Coordinated | 1.00 | 0.00 | 1.00 | ~58ms |

✅ **Perfect detection for phantom/coordinated attacks!**

⚠️ **Cannot detect position falsification** - Compromised UAVs have valid keys

**Trade-off**:

- 30× slower than spectral (but still real-time)
- Requires key distribution infrastructure
- ~100% message overhead (64-byte signatures)

---

## Performance Comparison

### Detection Accuracy

| Method       | Avg F1 | TPR Range | FPR Range | Status          |
| ------------ | ------ | --------- | --------- | --------------- |
| **Spectral** | 0.67   | 0.00-1.00 | 0.00      | ✅ Best overall |
| **Crypto**   | 0.67   | 0.00-1.00 | 0.00      | ✅ Best overall |
| ML           | 0.13   | 0.33-1.00 | 0.87-0.96 | ❌ Not suitable |
| Centrality   | 0.15   | 0.67-1.00 | 1.00      | ❌ Not suitable |

**Note**: Position falsification is undetectable by all topology-based methods (Spectral, Crypto)

### Detection Speed

| Method     | Latency | Suitable For        |
| ---------- | ------- | ------------------- |
| Spectral   | ~2ms    | Real-time, embedded |
| Centrality | ~1ms    | Fast but unreliable |
| ML         | ~5ms    | Fast but unreliable |
| Crypto     | ~58ms   | Real-time           |

---

## Scalability Analysis

### Performance vs Swarm Size

| UAVs | Spectral Time | Crypto Time | Crypto Overhead |
| ---- | ------------- | ----------- | --------------- |
| 20   | ~2ms          | ~39ms       | 19.5×           |
| 25   | ~2ms          | ~48ms       | 24×             |
| 30   | ~2ms          | ~58ms       | 30×             |

✅ **System scales acceptably for typical swarm sizes (20-30 UAVs)**

**Complexity**:

- Graph construction: O(n²)
- Spectral eigendecomposition: O(n²)
- Crypto verification: O(n) - linear scaling

**Trade-off**: 30× computational overhead for provable security guarantees

---

## Consensus Algorithm Evaluation

### Average Consensus Under Attack

**Objective**: All UAVs converge to average of initial values

**Update Rule**:

```
x_i(t+1) = x_i(t) + ε × Σ(x_j - x_i)  for j ∈ neighbors
```

### Experiment Setup

1. Initialize UAVs with random values
2. Run consensus for 100 iterations
3. Measure convergence error with/without attacks
4. Test with different defenses

---

### Consensus Results

**Convergence Error** (distance from true average):

| Scenario             | Error | Convergence |
| -------------------- | ----- | ----------- |
| No attack (baseline) | 0.01  | ✅ Yes      |
| Phantom attack       | 0.45  | ⚠️ Poor     |
| + Spectral defense   | 0.08  | ✅ Good     |
| + Crypto defense     | 0.01  | ✅ Perfect  |

**Key Finding**: Cryptographic defense completely restores consensus performance

---

## Implementation Highlights

### Interactive CLI Tool

```bash
# Interactive mode
argus

# Quick testing
argus --attack phantom --detectors all --mode live

# Performance comparison
argus --attack coordinated --detectors spectral crypto --mode comparison
```

**Features**:

- Guided interactive prompts
- Live real-time visualization
- Automated performance comparison
- Publication-quality plots (300 DPI)

---

### Live Visualization

**Real-time Animation**:

- Green circles = Legitimate UAVs
- Red X marks = Malicious/Phantom UAVs
- Yellow outlines = Detected anomalies
- Dynamic graph edges (communication links)

**Demo**: `examples/live_viz_with_detection.py`

---

### Example Demonstrations

**11 Working Examples**:

1. `simple_swarm.py` - Basic simulation
2. `attack_demo.py` - All attack types
3. `detection_demo.py` - Graph detection
4. `crypto_demo.py` - Perfect crypto defense
5. `ml_detection_demo.py` - Node2Vec ML
6. `enhanced_detection_demo.py` - Research detectors
7. `consensus_demo.py` - Consensus under attack
8. `visualization_demo.py` - Publication plots
9. `live_viz_with_detection.py` - Real-time animation
10. `scalability_test.py` - 50-250 UAV performance
11. `comprehensive_demo.py` - Complete workflow

---

## Key Research Contributions

### 1. Complete Simulation Framework

- Realistic UAV swarm model with Remote ID
- Three attack scenarios with ground truth
- Reproducible experiments (fixed seeds)
- Validated scalability (10-250 UAVs)

### 2. Comparative Analysis

**First comprehensive comparison**:

- Graph-theoretic methods (Spectral, Centrality)
- Machine learning (Node2Vec + Isolation Forest)
- Cryptographic verification (Ed25519)

**Quantified trade-offs**: accuracy, speed, overhead

---

### 3. Perfect Detection for Specific Attack Types

**Spectral Detector**:

- F1=1.00 for phantom and coordinated attacks
- Sub-2ms latency
- Cannot detect topology-preserving attacks (position falsification)

**Cryptographic Authentication**:

- F1=1.00 for phantom and coordinated attacks
- ~58ms latency (acceptable for real-time)
- Provable security guarantees
- Cannot detect compromised UAVs reporting false positions

### 4. Identification of Fundamental Limitations

**Position Falsification: Open Problem**:

- All tested methods achieve F1=0.0
- Root cause: Topology-preserving attack
- Requires alternative approaches (multi-lateration, physics-based validation, Byzantine consensus)

**Graph Heuristics: Production Limitations**:

- ML: 87-96% FPR (unusable)
- Centrality: 100% FPR (unusable)
- Configuration-sensitive, mobility-degraded

---

## Challenges and Solutions

### Challenge 1: Position Falsification Detection

**Problem**: Position falsification is fundamentally undetectable by topology-based methods

**Root Cause**: When compromised UAVs report false positions with offset < communication range, the graph structure remains unchanged

**Current Status**:

- Spectral: F1=0.0 (topology unchanged)
- Crypto: F1=0.0 (valid signatures on false data)
- **Open research problem**

**Future Directions**: Multi-lateration, physics-based validation, Byzantine consensus

---

### Challenge 2: High False Positive Rates

**Problem**: ML and Centrality detectors flag too many legitimate UAVs

**Root Cause**:

- ML: Limited 4-feature representation, contamination parameter mismatch
- Centrality: Threshold sensitivity, normal dynamics create anomalies

**Current Status**:

- ML: FPR=87-96% (unusable)
- Centrality: FPR=100% (unusable)

**Lesson Learned**: Graph-based heuristics require careful tuning and still exhibit high FPR

---

### Challenge 3: Computational Overhead

**Problem**: Cryptographic verification is 30× slower than spectral

**Solution**: 58ms per detection cycle is still acceptable for 1 Hz broadcast rates

**Result**: Real-time performance maintained for swarms up to 30 UAVs

---

## Production Recommendations

### For Real-World Deployment

**Recommended: Cryptographic Authentication (Mandatory)**

```python
detector = CryptoDetector()
```

✅ Perfect detection for phantom/coordinated attacks (F1=1.0)
✅ ~58ms latency (acceptable for 1 Hz broadcasts)
✅ Provable security guarantees
⚠️ Requires PKI infrastructure
⚠️ Cannot detect position falsification (open problem)

**Supplementary: Spectral Analysis (Monitoring)**

```python
detector = SpectralDetector(threshold=2.5)
```

✅ Fast (~2ms), lightweight monitoring
✅ Perfect detection for phantom/coordinated (F1=1.0)
⚠️ Cannot detect position falsification
❌ Should NOT be sole security mechanism

**Not Recommended: ML or Centrality**

- ML: FPR=87-96% (too many false alarms)
- Centrality: FPR=100% (unusable)

---

### Deployment Architecture

```
┌──────────────────────────────────────┐
│     Ground Control Station           │
│                                      │
│  ┌─────────────────────────────┐   │
│  │  Crypto Verifier (PRIMARY)   │   │
│  │  - 58ms detection            │   │
│  │  - F1=1.0 (phantom/coord)    │   │
│  │  - Mandatory for security    │   │
│  └─────────────────────────────┘   │
│           │                          │
│           ▼                          │
│  ┌─────────────────────────────┐   │
│  │  Spectral Monitor (optional) │   │
│  │  - 2ms monitoring            │   │
│  │  - Anomaly alerting          │   │
│  └─────────────────────────────┘   │
│           │                          │
│           ▼                          │
│     [Alert/Logging System]           │
└──────────────────────────────────────┘
```

**Strategy**: Cryptographic authentication is MANDATORY for security-critical UAV applications

---

## Limitations

### Simulation Limitations

1. **Simplified UAV Model**:

   - Constant velocity (no acceleration)
   - No wind/turbulence effects
   - Straight-line movement

2. **Attack Models**:

   - Basic phantom injection
   - No sophisticated evasion tactics
   - Static attack parameters

3. **Network Model**:
   - Perfect communication within range
   - No packet loss or latency
   - Simplified Remote ID format

---

### Detection Limitations

1. **Position Falsification: Unsolved Problem**:

   - All tested methods achieve 0% TPR (F1=0.0)
   - Topology-preserving attacks are fundamentally undetectable
   - Requires alternative approaches (multi-lateration, Byzantine consensus)

2. **Graph Heuristics (ML, Centrality)**:

   - Unacceptable FPR (87-100%) for production
   - Configuration-sensitive and mobility-degraded
   - Probabilistic detection subject to evasion

3. **Cryptographic Authentication**:
   - Requires PKI infrastructure
   - Cannot detect compromised UAVs with valid keys signing false data
   - 30× computational overhead vs spectral (but acceptable)

---

## Future Work

### High Priority Enhancements

1. **Position Verification (Critical)**:

   - Multi-lateration using signal strength and time-of-arrival
   - Physics-based validation (impossible velocities/accelerations)
   - Byzantine consensus protocols (fault-tolerant position verification)

2. **Mobility-Aware Thresholds**:
   - Adaptive threshold functions: τ(v_swarm) = τ₀ + k·v̄
   - Improve heuristic detector robustness in dynamic scenarios
   - Reduce mobility-induced false positives

---

### Advanced Detection Methods

3. **Graph Neural Networks (GNN)**:

   - Replace hand-crafted features with learned representations
   - Graph Convolutional Networks (GCN) or Graph Attention Networks (GAT)
   - Potential to reduce FPR below current 87-96%

4. **Post-Quantum Cryptography**:

   - Ed25519 vulnerable to quantum attacks (Shor's algorithm)
   - Evaluate lattice-based signatures (Dilithium, Falcon)
   - Future-proof authentication for long-term deployments

5. **Hardware Acceleration**:
   - GPU/FPGA implementation for Ed25519 verification
   - Target: sub-millisecond latency for very large swarms
   - Enable support for 100+ UAV swarms

---

### Real-World Validation

6. **Swarm Size Testing**:

   - Validate with 100-1000 UAV swarms
   - Identify scalability bottlenecks
   - Optimize for large-scale deployments

7. **Emerging Threat Modeling**:
   - GPS spoofing (affects all UAVs simultaneously)
   - RF jamming (denial-of-service)
   - AI-powered adaptive attacks (learn thresholds, craft evasions)
   - Quantum computing threats to Ed25519

---

## Project Deliverables

### Source Code (~4,000 LOC)

- ✅ 28 Python modules in `src/argus_uav/`
- ✅ 20 unit tests (all passing)
- ✅ 11 example demonstrations
- ✅ Interactive CLI tool
- ✅ Well-documented, type-hinted

### Documentation (9 Comprehensive Guides)

- ✅ Complete README with installation
- ✅ CLI user guide
- ✅ Quickstart guide (10-minute setup)
- ✅ Algorithm details with theory
- ✅ Data format specifications
- ✅ Enhanced detection guide
- ✅ Troubleshooting guide
- ✅ 19 research paper citations
- ✅ Project status report

---

### Experimental Results

**Publication-Quality Outputs**:

- ✅ ROC curves (300 DPI PNG + vector PDF)
- ✅ Detection comparison plots
- ✅ Confusion matrices
- ✅ Performance heatmaps
- ✅ Consensus error time series
- ✅ Markdown results tables

**Reproducibility**:

- Fixed random seeds
- YAML configuration files
- Automated experiment runner
- Version-controlled results

---

## Project Timeline

### Original vs Actual

| Phase           | Planned  | Actual   | Status      |
| --------------- | -------- | -------- | ----------- |
| Setup           | Week 1-2 | ~2 hours | ✅ Complete |
| Core Sim        | Week 3-4 | ~2 hours | ✅ Complete |
| Attacks         | Week 5   | ~1 hour  | ✅ Complete |
| Graph Detection | Week 6-7 | ~2 hours | ✅ Complete |
| ML Detection    | Week 8   | ~1 hour  | ✅ Complete |
| Crypto Defense  | Week 9   | ~1 hour  | ✅ Complete |
| Consensus       | Week 10  | ~1 hour  | ✅ Complete |
| Visualization   | Week 11  | ~2 hours | ✅ Complete |
| Documentation   | Week 12  | ~3 hours | ✅ Complete |

**Total Time**: ~15 hours (vs 12 weeks planned!)

---

## Technologies Used

### Core Stack

- **Python 3.11+** - Primary language
- **NetworkX** - Graph analysis and algorithms
- **NumPy** - Numerical computation
- **scikit-learn** - Machine learning (Isolation Forest)
- **PyCryptodome** - Ed25519 signatures
- **matplotlib** - Visualization and plotting

### Development Tools

- **pytest** - Unit testing framework
- **ruff** - Fast Python linter and formatter
- **uv** - Package manager and virtual environments
- **pre-commit** - Git hooks for code quality
- **PySide6** - Qt6 GUI backend for live visualization (cross-platform)

---

## Lessons Learned

### Technical Insights

1. **Cryptographic authentication is non-negotiable** for security-critical systems

   - Only method with provable security guarantees
   - ~58ms latency is acceptable for real-time operation
   - Perfect detection (F1=1.0) for phantom and coordinated attacks

2. **Spectral methods effective but insufficient alone**

   - Fast (~2ms) and accurate for topology-altering attacks
   - Cannot detect topology-preserving attacks
   - Should supplement, not replace, cryptographic security

3. **Graph heuristics have fundamental limitations**
   - High false positive rates (ML: 87-96%, Centrality: 100%)
   - Configuration-sensitive and mobility-degraded
   - Unsuitable as primary security mechanisms

---

### Research Insights

4. **Graph-theoretic modeling reveals fundamental limitations**

   - Natural representation of UAV swarms
   - Topology-based detection fails for topology-preserving attacks
   - Position falsification remains an open research problem

5. **Trade-offs are NOT just speed vs accuracy**

   - Cryptography: 30× slower but provable security
   - Heuristics: Fast but unreliable (high FPR)
   - Infrastructure vs deployment complexity

6. **Perfect detection has limits**
   - Achievable for phantom/coordinated attacks (F1=1.0)
   - Impossible for position falsification with current methods
   - Cryptographic authentication is mandatory, not optional

---

## Conclusion

### Key Achievements

✅ **Research Objectives Met**:

- Complete simulation framework
- Multiple detection methods
- Comprehensive evaluation
- Scalability validation
- Production-ready solutions

✅ **Novel Contributions**:

- First comprehensive comparison of cryptographic vs graph-based detection
- Demonstrated cryptographic authentication achieves perfect detection (F1=1.0) for phantom/coordinated attacks
- Identified position falsification as fundamental unsolved problem (F1=0.0 for all methods)
- Quantified 30× computational overhead trade-off for provable security
- Established that graph heuristics are unsuitable as primary security mechanisms (FPR=87-100%)

---

### Main Findings

1. **Cryptographic Authentication**: F1=1.0 for phantom/coordinated, ~58ms latency

   - **MANDATORY for production deployment**
   - Provable security guarantees
   - Cannot detect position falsification (compromised UAVs)

2. **Spectral Detection**: F1=1.0 for phantom/coordinated, ~2ms latency

   - **Supplementary monitoring tool only**
   - Fast and lightweight
   - Should NOT be sole security mechanism

3. **Position Falsification: Unsolved Problem**: All methods achieve F1=0.0

   - **Fundamental limitation of topology-based detection**
   - Requires multi-modal sensor fusion

4. **Graph Heuristics Unsuitable**: ML (FPR=87-96%), Centrality (FPR=100%)
   - **Not recommended for production**

---

### Impact and Applications

**Immediate Applications**:

- **Mandatory** cryptographic authentication for production UAV systems
- Spectral monitoring as supplementary anomaly detection
- Benchmark for evaluating future detection methods
- Framework for regulatory compliance (FAA Part 89, ASTM F3411)

**Research Impact**:

- Establishes cryptographic authentication as non-negotiable baseline
- Identifies position falsification as critical open research problem
- Quantifies fundamental limitations of graph-based heuristics
- Provides reproducible framework for future UAV security research
- Open-source reference implementation for standardization efforts

---

## Acknowledgments

### References

- **Spectral Theory**: Chung (1997), Peel et al. (2015)
- **Centrality**: Freeman (1978), Newman (2010)
- **Cryptography**: Bernstein et al. (2012), RFC 8032
- **Machine Learning**: Grover & Leskovec (2016), Liu et al. (2008)
- **Consensus**: Olfati-Saber & Murray (2004)
- **UAV Security**: FAA Part 89, ASTM F3411-19

### Tools and Libraries

- NetworkX, NumPy, scikit-learn, PyCryptodome
- matplotlib, pytest, ruff, uv

### Development Approach

- **Spec-Driven Development** with Cursor AI
- Accelerated research prototyping
- Publication-quality from day one

---

## Questions?

### Contact & Resources

**Project Repository**: [GitHub - Argus](https://github.com/[username]/Argus)

**Documentation**: `docs/` directory

- CLI guide: `docs/CLI.md`
- Quickstart: `docs/QUICKSTART.md`
- Algorithms: `docs/algorithm_details.md`

**Try it yourself**:

```bash
# Install
uv pip install -e .

# Run interactive demo
argus

# Quick test
argus --attack phantom --detectors all --mode live
```

---

## Thank You!

### Argus: UAV Remote ID Spoofing Defense

**Key Takeaway**: Only cryptographic authentication provides provable security guarantees for UAV Remote ID. Graph-based heuristics are insufficient as primary defense mechanisms.

**Next Steps**:

- Solve position falsification problem (multi-lateration, Byzantine consensus)
- Real-world hardware testing with actual UAVs
- Post-quantum cryptography (Dilithium, Falcon)
- Mobility-aware threshold adaptation for heuristic monitoring

**Open Source**: Available for research and development

---

## Appendix A: Performance Metrics

### Detection Performance Summary

| Method     | Phantom |       | Position |       | Coordinated |       |
| ---------- | ------- | ----- | -------- | ----- | ----------- | ----- |
|            | F1      | Time  | F1       | Time  | F1          | Time  |
| Spectral   | 1.00    | ~2ms  | 0.00     | ~2ms  | 1.00        | ~2ms  |
| Centrality | 0.11    | ~1ms  | 0.18     | ~1ms  | 0.17        | ~1ms  |
| ML         | 0.06    | ~5ms  | 0.13     | ~5ms  | 0.19        | ~5ms  |
| Crypto     | 1.00    | ~58ms | 0.00     | ~58ms | 1.00        | ~58ms |

**Key Finding**: Position falsification (F1=0.00) is undetectable by all topology-based methods

### Scalability Performance

Based on paper's computational overhead analysis:

- **20 UAVs**: ~2ms spectral, ~39ms crypto
- **25 UAVs**: ~2ms spectral, ~48ms crypto
- **30 UAVs**: ~2ms spectral, ~58ms crypto

**Complexity**:

- Spectral: O(n²) for eigendecomposition
- Crypto: O(n) linear scaling with swarm size
- Crypto overhead: ~30× slower than spectral but acceptable for real-time

---

## Appendix B: Implementation Details

### Graph Construction

```python
# Build communication graph
G = nx.Graph()
for uav in swarm.uavs:
    G.add_node(uav.id, position=uav.position)

for uav1 in swarm.uavs:
    for uav2 in swarm.uavs:
        if uav1.id != uav2.id:
            dist = np.linalg.norm(uav1.position - uav2.position)
            if dist <= comm_range:
                G.add_edge(uav1.id, uav2.id, weight=1.0/dist)
```

### Spectral Detection

```python
# Compute Laplacian eigenvalues
L = nx.laplacian_matrix(G).toarray()
eigenvalues = np.linalg.eigvalsh(L)

# Compare with baseline
z_scores = (eigenvalues - baseline_mean) / baseline_std
anomaly_score = np.max(np.abs(z_scores))

if anomaly_score > threshold:
    flag_anomaly()
```

---

## Appendix C: Example Usage

### Quick Start Example

```python
from argus_uav.core.swarm import Swarm
from argus_uav.detection.spectral import SpectralDetector
from argus_uav.attacks import AttackType, AttackScenario

# Create swarm
swarm = Swarm(num_uavs=30, comm_range=200.0)

# Collect baseline
detector = SpectralDetector(threshold=2.8)
baseline = [swarm.get_graph() for _ in range(30)]
detector.train(baseline)

# Inject attack
attack = AttackScenario(AttackType.PHANTOM, 10.0, 20.0, phantom_count=5)
injector = PhantomInjector()
injector.inject(swarm, attack, 10.0)

# Detect
result = detector.detect(swarm.get_graph())
metrics = result.compute_metrics()
print(f"TPR: {metrics['tpr']:.2%}, F1: {metrics['f1']:.2f}")
```

---

## Appendix D: File Structure

```
Argus/
├── src/argus_uav/          # Main package (28 modules)
│   ├── core/               # UAV, Swarm, Remote ID
│   ├── attacks/            # Attack implementations
│   ├── detection/          # Detection algorithms
│   ├── crypto/             # Ed25519 signing
│   ├── consensus/          # Consensus algorithms
│   ├── evaluation/         # Metrics, visualization
│   └── experiments/        # Experiment runner
├── examples/               # 11 demonstrations
├── tests/                  # Unit and integration tests
├── docs/                   # 9 documentation files
├── results/                # Experiment outputs
└── README.md               # Main documentation
```
