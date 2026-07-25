"""Run the deterministic Ant Colony world demonstration."""

from ant_colony.observation import render_world
from ant_colony.scenarios import create_demonstration_state
from ant_colony.simulation import run_steps


def main() -> None:
    """Display the demonstration world before and after five steps."""

    initial_state = create_demonstration_state()
    final_state = run_steps(initial_state, steps=5)

    print(render_world(initial_state))
    print()
    print(render_world(final_state))


if __name__ == "__main__":
    main()