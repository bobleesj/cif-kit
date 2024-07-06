import time
import os
import pandas as pd
import matplotlib.pyplot as plt
from core.utils import prompt
import click
from cifkit import CifEnsemble
from os.path import join
from core.utils.histogram import plot_distance_histogram


def move_files_based_on_min_dist(cif_dir):
    filter_files_by_min_dist(cif_dir)


def filter_files_by_min_dist(cif_dir, isInteractiveMode=True):
    """
    Filter files for files below the minimum distance threshold.
    """

    # Initialize the ensemble
    ensemble = CifEnsemble(cif_dir)
    min_dists = []

    # Get all the distances
    for idx, cif in enumerate(ensemble.cifs, start=1):
        start_time = time.perf_counter()
        prompt.print_progress_current(
            idx, cif.file_name, cif.supercell_atom_count, ensemble.file_count
        )

        # Lazy loading
        min_dist = cif.shortest_distance
        min_dists.append(min_dist)
        elasped_time = time.perf_counter() - start_time
        prompt.print_finished_progress(
            cif.file_name, cif.supercell_atom_count, elasped_time
        )

    # Folder to save the histogram
    histogram_save_path = os.path.join(cif_dir, "plot", "histogram-min-dist.png")
    plot_directory = os.path.join(cif_dir, "plot")
    if not os.path.exists(plot_directory):
        os.makedirs(plot_directory)

    # Plot histogram
    plot_distance_histogram(min_dists, histogram_save_path, ensemble.file_count)
    print("Histogram saved. Please check the 'plot' folder of the cif folder.")

    if isInteractiveMode:
        click.echo(
            "Note: .cif files with minimum distance below threashold are relocated."
        )
        prompt_dist_threshold = "\nEnter the threashold distance (unit in Å)"
        dist_threshold = click.prompt(prompt_dist_threshold, type=float)

    # Filter files based on the minimum distance
    filtered_file_paths = ensemble.filter_by_min_distance(0.0, dist_threshold)
    filtered_dir_path = join(ensemble.dir_path, f"min_dist_below_{dist_threshold}")
    # Move filtered files to a new directory
    if filtered_file_paths:
        ensemble.move_cif_files(filtered_file_paths, filtered_dir_path)

    print(f"Moved {len(filtered_file_paths)} files to {filtered_dir_path}")
    prompt.print_done_with_option()