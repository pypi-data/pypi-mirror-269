"""
Command line interface for the neuroflow package.
"""

from pathlib import Path

import click

from neuroflow.atlases.atlases import Atlases
from neuroflow.connectome.connectome_reconstructor import ConnectomeReconstructor
from neuroflow.covariates.covariates_collector import CovariatesCollector
from neuroflow.files_mapper.files_mapper import FilesMapper
from neuroflow.parcellation.parcellation import Parcellation
from neuroflow.recon_tensors.dipy.dipy_tensors import DipyTensors
from neuroflow.recon_tensors.mrtrix3.mrtrix3_tensors import MRTrix3Tensors


# Example CLI script with a basic command structure
@click.group()  # This decorator defines a group of commands, allowing subcommands
def cli():
    """This is the main entry point for the CLI."""
    pass  # This is just a placeholder for the main CLI group


# Define a subcommand
@cli.command()  # This decorator creates a new command within the CLI group
@click.argument(
    "input_dir", type=click.Path(exists=True)
)  # Require an directory with preprocessing results
@click.argument(
    "output_dir",
    type=click.Path(),
    # help="Output directory for NeuroFlow's results",
)
@click.argument(
    "google_credentials",
    type=click.Path(exists=True),
    # help="Path to the Google credentials file",
)
@click.option(
    "--patterns_file",
    type=click.Path(exists=True),
    help="Path to the patterns file",
)
@click.option(
    "--atlases",
    type=str,
    help="The atlases to use for the analysis",
)
@click.option(
    "--max_bval",
    type=int,
    default=1000,
    help="Maximum b-value for diffusion data",
)
def process(
    input_dir: str,
    output_dir: str,
    patterns_file: str,
    google_credentials: str,
    atlases: str,
    max_bval: int,
):
    """
    Process the preprocessed data for the participant.

    Parameters
    ----------
    input_dir : str
        The path to the preprocessed data
    output_directory : str
        The path to the output directory
    patterns_file : str
        The path to the patterns file
    google_credentials : str
        The path to the Google credentials
    atlases : list
        The atlases to use for the analysis
    max_bval : int
        The maximum b-value for diffusion data
    """
    print(atlases)
    atlases = atlases.split(",") if atlases else None
    preprocessed_directory = Path(input_dir)
    output_directory = Path(output_dir)
    google_credentials = Path(google_credentials)
    patterns_file = Path(patterns_file) if patterns_file else None
    print("Processing the data...")
    print(f"Preprocessed directory: {preprocessed_directory}")
    print(f"Output directory: {output_directory}")
    print(f"Patterns file: {patterns_file}")
    print(f"Google credentials: {google_credentials}")
    print(f"Atlases: {atlases}")
    print(f"Max b-value: {max_bval}")

    mapper = (
        FilesMapper(path=preprocessed_directory)
        if patterns_file is None
        else FilesMapper(path=preprocessed_directory, patterns=patterns_file)
    )
    dipy_tensors = DipyTensors(
        mapper=mapper, output_directory=output_directory, max_bvalue=max_bval
    )
    mrtrix3_tensors = MRTrix3Tensors(
        mapper=mapper, output_directory=output_directory, max_bvalue=max_bval
    )
    atlases = Atlases(mapper=mapper, output_directory=output_directory, atlases=atlases)
    parcellation_dipy = Parcellation(
        tensors_manager=dipy_tensors,
        atlases_manager=atlases,
        output_directory=output_directory,
    )
    parcellation_mrtrix3 = Parcellation(
        tensors_manager=mrtrix3_tensors,
        atlases_manager=atlases,
        output_directory=output_directory,
    )
    covariates = CovariatesCollector(
        mapper=mapper,
        google_credentials_path=google_credentials,
        output_directory=output_directory,
    )
    connectome_recon = ConnectomeReconstructor(
        mapper=mapper, atlases_manager=atlases, output_directory=output_directory
    )
    print("Running atlas registrations and parcellations of Dipy-derived metrics...")
    _ = parcellation_dipy.run()
    print("Running atlas registrations and parcellations of MRtrix3-derived metrics...")
    _ = parcellation_mrtrix3.run()
    print("Saving participant and session's covariates...")
    _ = covariates.save_to_file()
    print("Reconstructing the connectome...")
    _ = connectome_recon.run()


if __name__ == "__main__":
    cli()
