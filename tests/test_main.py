from ant_colony.__main__ import main


def test_main_displays_initial_and_final_world_states(
    capsys: object,
) -> None:
    main()

    captured = capsys.readouterr()  # type: ignore[attr-defined]

    assert captured.out == (
        "step=0\n"
        "SRRWW\n"
        "SMMWW\n"
        "SSMRR\n"
        "\n"
        "step=5\n"
        "SRRWW\n"
        "SMMWW\n"
        "SSMRR\n"
    )