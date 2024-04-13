import click
from click import echo, style


def get_user_input_on_supercell_method():
    echo(
        "\nWould you like to modify the default 2x2x2 supercell generation"
        " method for files over 100 atoms in the unit cell?"
    )
    is_supercell_generation_method_modified = click.confirm(
        "(Default: N)", default=False
    )

    if is_supercell_generation_method_modified:
        echo("\nChoose a supercell generation method:")
        echo("1. No shift (fastest)")
        echo("2. +1 +1 +1 shifts in x, y, z directions")
        echo("3. +-1, +-1, +-1 shifts (2x2x2 supercell generation, slowest)")

        method = click.prompt(
            "Choose your option by entering a number", type=int
        )

        if method == 1:
            echo("> You've selected: No shift (fastest)\n")
        elif method == 2:
            echo("> You've selected: +1 +1 +1 shifts in x, y, z directions\n")
        elif method == 3:
            echo("> You've selected: +-1, +-1, +-1 shifts (2x2x2 supercell)\n")
        else:
            echo("> Invalid option. Defaulting to 2x2x2 supercell.\n")
            method = 3
    else:
        method = None

    return method


def print_progress(filename_with_ext, num_of_atoms, elapsed_time, is_finished):
    if is_finished:
        echo(
            style(
                f"Processed {filename_with_ext} with {num_of_atoms} atoms in "
                f"{round(elapsed_time, 2)} s\n",
                fg="yellow",
            )
        )