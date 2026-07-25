from ant_colony.__main__ import main


def test_main_displays_initial_and_final_world_states(
    capsys: object,
) -> None:
    main()

    captured = capsys.readouterr()  # type: ignore[attr-defined]

    assert captured.out == (
        "step=0\n"
        "terrain:\n"
        "SRRWW\n"
        "SMMWW\n"
        "SSMRR\n"
        "moisture:\n"
        "030 015 010 100 100\n"
        "040 075 080 100 100\n"
        "035 045 070 020 015\n"
        "\n"
        "step=5\n"
        "terrain:\n"
        "SRRWW\n"
        "SMMWW\n"
        "SSMRR\n"
        "moisture:\n"
        "030 015 010 100 100\n"
        "040 075 080 100 100\n"
        "035 045 070 020 015\n"
    )