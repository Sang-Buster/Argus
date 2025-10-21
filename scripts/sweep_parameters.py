#!/usr/bin/env python3
"""
CLI script for parameter sweep experiments.

Usage:
    python scripts/sweep_parameters.py --config configs/phantom_attack.yaml --param phantom_count --values 1,3,5,10
"""

import argparse
from pathlib import Path

import yaml

from argus.attacks import AttackScenario, AttackType
from argus.experiments.config_schema import ExperimentConfig
from argus.experiments.runner import ExperimentRunner


def load_config(config_path: Path) -> ExperimentConfig:
    """Load experiment configuration from YAML file."""
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
        description="Run parameter sweep for Argus experiments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Sweep phantom count
  python scripts/sweep_parameters.py \\
      --config configs/phantom_attack.yaml \\
      --param phantom_count \\
      --values 1,3,5,10,15
  
  # Sweep communication range
  python scripts/sweep_parameters.py \\
      --config configs/baseline_swarm.yaml \\
      --param comm_range \\
      --values 50,100,150,200,250
        """,
    )

    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to base YAML configuration file",
    )

    parser.add_argument(
        "--param",
        type=str,
        required=True,
        help="Parameter name to sweep (e.g., phantom_count, comm_range)",
    )

    parser.add_argument(
        "--values",
        type=str,
        required=True,
        help="Comma-separated parameter values (e.g., 1,3,5,10)",
    )

    parser.add_argument("--output", type=Path, help="Override base output directory")

    args = parser.parse_args()

    # Parse values
    try:
        # Try parsing as integers first
        values = [int(v.strip()) for v in args.values.split(",")]
    except ValueError:
        try:
            # Try parsing as floats
            values = [float(v.strip()) for v in args.values.split(",")]
        except ValueError:
            # Keep as strings
            values = [v.strip() for v in args.values.split(",")]

    # Load configuration
    print(f"📂 Loading base configuration from {args.config}")
    config = load_config(args.config)

    if args.output is not None:
        config.output_dir = args.output

    # Display sweep info
    print("\n🔄 Parameter Sweep Configuration:")
    print(f"   • Base experiment: {config.experiment_name}")
    print(f"   • Parameter: {args.param}")
    print(f"   • Values: {values}")
    print(f"   • Number of runs: {len(values)}")
    print(f"   • Output directory: {config.output_dir}")

    # Run sweep
    print("\n🚀 Starting parameter sweep...\n")

    runner = ExperimentRunner(config)
    sweep_results = runner.run_parameter_sweep(args.param, values)

    # Display summary
    print("\n" + "=" * 70)
    print("📊 PARAMETER SWEEP RESULTS")
    print("=" * 70)

    print(
        f"\n{args.param:<15} | {'TPR':>8} | {'FPR':>8} | {'F1':>8} | {'Time(ms)':>10}"
    )
    print("-" * 70)

    for value, results in sweep_results.items():
        # Average metrics across all detectors
        all_metrics = list(results.detection_metrics.values())
        if all_metrics:
            avg_tpr = sum(m["tpr"] for m in all_metrics) / len(all_metrics)
            avg_fpr = sum(m["fpr"] for m in all_metrics) / len(all_metrics)
            avg_f1 = sum(m["f1"] for m in all_metrics) / len(all_metrics)
            avg_time = sum(m["detection_time"] for m in all_metrics) / len(all_metrics)

            print(
                f"{str(value):<15} | {avg_tpr:>7.2%} | {avg_fpr:>7.2%} | "
                f"{avg_f1:>8.3f} | {avg_time * 1000:>9.2f}"
            )

    print("\n✅ Parameter sweep complete!")
    print(f"   Results saved to: {config.output_dir}/")
    print()

    return 0


if __name__ == "__main__":
    exit(main())
