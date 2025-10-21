<!--
Sync Impact Report:
- Version change: Initial → 1.0.0
- Initial constitution creation for UAV Remote ID Spoofing research project
- Principles established: Code Quality, Test Coverage, Performance Standards, Research Rigor, Reproducibility, Documentation Excellence
- Templates: ✅ All templates aligned with constitution principles
- Follow-up: None - all principles concrete
-->

# Argus Constitution

## Core Principles

### I. Code Quality and Modularity

The codebase MUST maintain clear separation of concerns with independent, testable modules. Every component (simulator, attack models, detection methods, cryptographic defenses) MUST be implemented as standalone modules with well-defined interfaces. Code MUST follow PEP 8 style guidelines with type hints for all function signatures. Complex algorithms MUST include inline comments explaining mathematical or cryptographic operations.

**Rationale**: Modular architecture enables independent testing of attack scenarios vs defense mechanisms, facilitates reproducible experiments, and allows other researchers to extend or modify specific components without touching unrelated code.

### II. Test Coverage (NON-NEGOTIABLE)

Unit tests MUST be written for all core functions before implementation (TDD approach). Integration tests MUST validate attack injection, detection pipelines, and end-to-end scenarios. Test coverage MUST exceed 80% for core simulation and detection modules. Each attack scenario and detection method MUST have corresponding test cases with known ground truth.

**Rationale**: Research-grade software requires verifiable correctness. Tests serve as executable specifications and ensure that experimental results are reproducible and trustworthy.

### III. Performance Standards

Graph algorithms MUST efficiently handle swarms of 50-100 UAV nodes. Cryptographic operations (Ed25519 signing/verification) MUST complete in under 10ms per message. Spectral analysis and machine learning inference MUST run in near real-time (< 100ms per detection cycle). Memory usage MUST remain reasonable for commodity hardware (< 4GB RAM).

**Rationale**: Simulation performance directly impacts experimental iteration speed. These standards ensure the simulator remains practical for parameter sweeps and large-scale experiments.

### IV. Research Rigor and Metrics

All experimental results MUST include quantitative evaluation metrics: True Positive Rate (TPR), False Positive Rate (FPR), detection latency, computational overhead, and consensus error rates. Experiments MUST use fixed random seeds for reproducibility. Comparative analysis MUST be provided for all defense strategies (graph-only, crypto-only, hybrid). Every claim MUST be backed by data with appropriate statistical measures (mean, std dev, confidence intervals where applicable).

**Rationale**: Research validity depends on rigorous quantitative evaluation and reproducibility. These standards ensure results can be validated by peer reviewers and other researchers.

### V. Reproducibility

All experiments MUST be configurable via YAML or JSON parameter files with version-controlled defaults. Dependencies MUST be pinned to specific versions in requirements.txt. Random seeds MUST be configurable and logged. Experiment configurations and results MUST be saved with timestamps for traceability. Scripts MUST support batch execution for parameter sweeps.

**Rationale**: Reproducibility is the cornerstone of scientific research. Version-controlled configurations enable others to replicate experiments exactly and validate findings.

### VI. Documentation Excellence

Every module MUST have docstrings explaining purpose, parameters, return values, and raised exceptions. The README MUST include setup instructions, dependency installation, quick start examples, and references to key papers. Complex algorithms (spectral analysis, Node2Vec, consensus) MUST include citations to source papers. Visualization outputs MUST have clear axis labels, legends, and captions.

**Rationale**: Clear documentation accelerates onboarding, enables peer review, and ensures the research artifact remains useful beyond the initial development phase.

## Software-Only Development

All development MUST focus on pure software simulation with zero hardware dependencies during the initial research phase. No RTL-SDR, Raspberry Pi, or physical UAV hardware should be required to run experiments. Simulated Remote ID traffic MUST be generated programmatically. Hardware integration MAY be considered as a future extension only after core simulation and defense mechanisms are validated.

**Rationale**: Software simulation allows rapid iteration without hardware procurement delays or physical testing constraints. Hardware can be added later for real-world validation.

## Development Workflow

### Code Review and Quality Gates

All feature branches MUST pass linting (flake8/pylint) before merge. All tests MUST pass before code review. Pull requests MUST include test coverage reports. Experimental code MAY have relaxed standards, but production simulation and detection code MUST meet all principles.

### Experiment Tracking

Experiment results MUST be stored in a structured format (e.g., `results/YYYY-MM-DD_experiment_name/`). Parameter files, output data, and generated plots MUST be co-located. A manifest file MUST track experiment metadata (date, commit hash, parameters, metrics summary).

## Governance

This constitution supersedes all ad-hoc development practices. All code reviews MUST verify compliance with these principles. Deviations MUST be explicitly justified in PR descriptions with rationale and approval. Amendments to this constitution require updating the version number and documenting the change rationale.

Complexity introduced for "quick experiments" MUST be refactored before merge to main branch. When in doubt, prioritize simplicity and clarity over premature optimization.

**Version**: 1.0.0 | **Ratified**: 2025-10-21 | **Last Amended**: 2025-10-21
