#!/usr/bin/env python3
"""
Live UAV swarm visualization.

Real-time animated plot showing UAV movement, connections, and attacks.

Note: This opens an interactive matplotlib window. Close the window to exit.
"""

# Set matplotlib backend to Qt5 before importing pyplot
import matplotlib

matplotlib.use("Qt5Agg")

import numpy as np

from argus.attacks import AttackScenario, AttackType
from argus.attacks.phantom_uav import PhantomInjector
from argus.core.swarm import Swarm
from argus.evaluation.live_visualization import LiveSwarmVisualizer


def main():
    """Run live visualization demonstration."""
    print("\n" + "=" * 70)
    print("📺 LIVE UAV SWARM VISUALIZATION")
    print("=" * 70)

    print("\nInitializing visualization...")
    print("  • Green circles: Legitimate UAVs")
    print("  • Red X marks: Phantom UAVs")
    print("  • Gray lines: Communication links")

    # Create swarm
    rng = np.random.default_rng(seed=42)
    swarm = Swarm(num_uavs=30, comm_range=200.0, bounds=(500, 500, 100), rng=rng)

    # Setup attack to inject mid-simulation
    attack = AttackScenario(
        attack_type=AttackType.PHANTOM, start_time=15.0, duration=20.0, phantom_count=5
    )

    injector = PhantomInjector()
    attack_injected = False

    # Create visualizer
    visualizer = LiveSwarmVisualizer(swarm, figsize=(14, 10), update_interval=200)

    # Define attack injection callback
    def inject_attack_callback(frame):
        nonlocal attack_injected
        current_time = swarm.simulation_time

        if attack.is_active(current_time) and not attack_injected:
            injector.inject(swarm, attack, current_time)
            attack_injected = True
            print(f"\n⚠️  Phantom attack injected at t={current_time:.1f}s!")

        if current_time >= attack.start_time + attack.duration and attack_injected:
            injector.remove_phantoms(swarm)
            attack_injected = False
            print(f"\n✓ Phantoms removed at t={current_time:.1f}s")

    print("\n🎬 Starting animation...")
    print("   (Close the window to stop)")
    print("\n⏱️  Timeline:")
    print("   • t=0-15s:  Normal operation (30 UAVs)")
    print("   • t=15-35s: PHANTOM ATTACK (5 phantoms injected)")
    print("   • t=35s+:   Attack removed, back to normal")
    print()

    try:
        # Run animation (60 frames = 60 seconds of simulation)
        visualizer.animate(frames=60, attack_callback=inject_attack_callback)
    except KeyboardInterrupt:
        print("\n\n⏹️  Animation stopped by user")

    print("\n✅ Visualization complete!")


if __name__ == "__main__":
    main()
