"""Launch the graphical Terroir Simulator demonstration."""

from terroir_simulator.observation.pygame_renderer import show_world
from terroir_simulator.scenarios import create_demonstration_state


def main() -> None:
    """Display the existing demonstration as a graphical scene."""

    show_world(create_demonstration_state())


if __name__ == "__main__":
    main()