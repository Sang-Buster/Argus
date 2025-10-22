#!/usr/bin/env python3
"""
CLI script for running experiments from configuration files.

Usage:
    python scripts/run_experiment.py --config configs/phantom_attack.yaml
    python scripts/run_experiment.py --config configs/crypto_defense.yaml --output results/my_test
"""

import argparse
from pathlib import Path

import yaml

from argus_uav.attacks import AttackScenario, AttackType
from argus_uav.experiments.config_schema import ExperimentConfig
from argus_uav.experiments.runner import ExperimentRunner


def load_config(config_path: Path) -> ExperimentConfig:
    """
    Load experiment configuration from YAML file.

    Args:
        config_path: Path to YAML config file

    Returns:
        ExperimentConfig instance
    """
    with open(config_path) as f:
        config_dict = yaml.safe_load(f)

    # Convert attack_scenario dict to AttackScenario object
    if config_dict.get("attack_scenario") is not None:
        attack_dict = config_dict["attack_scenario"]
        attack_dict["attack_type"] = AttackType(attack_dict["attack_type"])
        config_dict["attack_scenario"] = AttackScenario(**attack_dict)

    # Convert output_dir to Path
    if "output_dir" in config_dict:
        config_dict["output_dir"] = Path(config_dict["output_dir"])

    return ExperimentConfig(**config_dict)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Run Argus UAV Remote ID spoofing experiment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run phantom attack experiment
  python scripts/run_experiment.py --config configs/phantom_attack.yaml
  
  # Run with custom output directory
  python scripts/run_experiment.py --config configs/crypto_defense.yaml --output results/test_run
  
  # Run all configured experiments
  for config in configs/*.yaml; do
      python scripts/run_experiment.py --config "$config"
  done
        """,
    )

    parser.add_argument(
        "--config", type=Path, required=True, help="Path to YAML configuration file"
    )

    parser.add_argument(
        "--output", type=Path, help="Override output directory from config"
    )

    parser.add_argument("--seed", type=int, help="Override random seed from config")

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress INFO logging (show only warnings/errors)",
    )

    args = parser.parse_args()

    # Validate config file exists
    if not args.config.exists():
        print(f"❌ Error: Config file not found: {args.config}")
        return 1

    # Set logging level
    if args.quiet:
        import logging

        logging.getLogger("argus").setLevel(logging.WARNING)

    # Load configuration
    print(f"📂 Loading configuration from {args.config}")
    config = load_config(args.config)

    # Apply overrides
    if args.output is not None:
        config.output_dir = args.output

    if args.seed is not None:
        config.random_seed = args.seed

    # Display experiment info
    print(f"\n🧪 Experiment: {config.experiment_name}")
    print(f"   • Swarm size: {config.swarm_size} UAVs")
    print(f"   • Communication range: {config.comm_range}m")
    print(f"   • Duration: {config.simulation_duration}s")
    print(f"   • Random seed: {config.random_seed}")
    print(f"   • Cryptography: {'Enabled' if config.enable_crypto else 'Disabled'}")

    if config.attack_scenario is not None:
        print(f"   • Attack: {config.attack_scenario.attack_type.value}")
        print(f"     - Start: {config.attack_scenario.start_time}s")
        print(f"     - Duration: {config.attack_scenario.duration}s")

    print(f"   • Detection methods: {', '.join(config.detection_methods)}")
    print(f"   • Output: {config.output_dir}")

    # Run experiment
    print("\n🚀 Starting experiment...\n")

    runner = ExperimentRunner(config)
    results = runner.run()

    # Display results
    print("\n✅ Experiment complete!")
    print(f"   • Execution time: {results.execution_time:.1f}s")
    print(f"   • Results saved to: {results.output_dir}")

    print("\n📊 Detection Performance:")
    for detector, metrics in results.detection_metrics.items():
        print(f"\n   {detector}:")
        print(f"      TPR: {metrics['tpr']:.2%}")
        print(f"      FPR: {metrics['fpr']:.2%}")
        print(f"      F1:  {metrics['f1']:.3f}")
        print(f"      Time: {metrics['detection_time'] * 1000:.2f}ms")

    print("\n📁 Generated files:")
    print("   • config.yaml - Experiment configuration")
    print("   • metrics.json - Quantitative metrics")
    print("   • results_table.md - Markdown summary")
    print("   • figures/*.png - Visualization plots")
    print("   • figures/*.pdf - Publication-quality PDFs")
    print()

    return 0


if __name__ == "__main__":
    exit(main())
