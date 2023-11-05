"""
Methods to handle submissions and their metadata.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from .data import Samples


@dataclass
class Submission:
    name: str = None
    authors: list[str] = None
    affiliations: list[str] = None
    gen_samples: dict = None
    gen_datasets_dir: str = None
    container_path: str = None
    inference_command: str = None
    model_repository: str = None

    def __post_init__(self):
        self.samples = {}
        for dataset in self.gen_samples:
            # TODO: add checks for valid datasets?
            self.samples[dataset] = {}
            for data_class in self.gen_samples[dataset]:
                self.samples[dataset][data_class] = Samples(
                    dataset=dataset,
                    data_class=data_class,
                    download_url=self.gen_samples[dataset][data_class]["url"],
                    md5=self.gen_samples[dataset][data_class].get("md5", None),
                    download_path=f"{self.gen_datasets_dir}/{self.name}/{dataset}/{data_class}.hdf5",
                )


def load_submission(
    submission_dir: str, submission_name: str, gen_datasets_dir: str
) -> dict:
    """Loads the metadata for the given submission.

    Args:
        submission_dir (str): Directory containing the submission.
        submission_name (str): Name of the submission.

    Returns:
        Tuple[np.ndarray, dict]: Tuple containing the generated samples and the metadata.
    """
    submission_path = Path(submission_dir) / submission_name
    metadata_path = submission_path / "metadata.yml"

    if not Path(metadata_path).exists():
        raise FileNotFoundError(f"Metadata file not found: {metadata_path}")

    with metadata_path.open() as f:
        metadata = yaml.safe_load(f)

    return Submission(**metadata, gen_datasets_dir=gen_datasets_dir)
