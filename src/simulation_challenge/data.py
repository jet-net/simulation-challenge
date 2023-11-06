"""
Methods for accessing real and generated data.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import h5py
import jetnet
import numpy as np

_valid_datasets = {"jetnet": ["g30"]}  # TODO: more datasets


@dataclass
class Samples:
    """
    Class for jet samples. Downloads, loads, and stores the samples. Also calculates and stores EFPs.

    Args:
        dataset (str): dataset of the samples, e.g. "jetnet".
        data_class (str): jet type of the sample, e.g. "g30".
        download_url (str): URL to download samples.
        download_path (str): Path to downloaded samples.
        downloaded (bool): Whether the samples have been downloaded.
        md5 (optional, str): MD5 hash of the downloaded samples, to verify integrity of download.
        samples (np.ndarray): Array of shape ``(num_samples, num_particles, num_features)`` containing the samples.
        efps_path (str): Path to EFPs numpy file.
        efps (np.ndarray): Array of shape ``(num_samples, num_efps)`` containing the calculated EFPs.
    """

    dataset: str = None
    data_class: str = None

    download_url: str = None
    download_path: str = None
    downloaded: bool = False
    md5: str = None
    samples: np.ndarray = None

    efps_path: str = None
    efps: np.ndarray = None

    def __post_init__(self):
        """Loads EFPs if they exist."""
        if Path(self.download_path).exists():
            self.downloaded = True

        self.efps_path = Path(self.download_path).parent / f"{self.data_class}_efps.npy"

        if Path(self.efps_path).exists():
            self.efps = np.load(self.efps_path)

    def load_samples(self, num_samples: int = 50_000):
        """
        Verifies integrity of downloaded file (if md5 hash provided)
        and loads the samples from the HDF5 file.
        """
        if self.downloaded is False:
            raise RuntimeError("Samples need to be downloaded before loading.")

        if self.md5 is not None:
            match_md5, fmd5 = jetnet.datasets.utils._check_md5(self.download_path, self.md5)
            if not match_md5:
                raise RuntimeError("Downloaded file MD5 does not match expected MD5.")

        with h5py.File(self.download_path, "r") as f:
            self.samples = np.array(f["particle_features"])[:num_samples]

    def download(self, overwrite: bool = False):
        """Downloads the samples if they do not exist and loads them."""
        if self.downloaded:
            print(f"File exists: {self.download_path}.")
            if not overwrite:
                print("Skipping download.")
                self.load_samples()
                return

        print(f"Downloading to {self.download_path}.")

        Path.mkdir(Path(self.download_path).parent, exist_ok=True, parents=True)
        jetnet.datasets.utils.download_progress_bar(self.download_url, self.download_path)
        self.downloaded = True

        self.load_samples()

    def get_efps(self):
        """Calculates the EFPs if not already cached and returns them."""
        if self.samples is None:
            raise RuntimeError("Samples need to be loaded before calculating EFPs.")

        if self.efps is None:
            print("Calculating EFPs...")
            self.efps = jetnet.utils.efps(self.samples)
            np.save(self.efps_path, self.efps)

        return self.efps


def get_real_samples(
    dataset: str, data_class: str, data_dir: str, num_samples: int = 50_000
) -> np.ndarray:
    """Downloads, if necessaryk and loads the real data for the given dataset and data class.

    Args:
        dataset (str): Choices are ["jetnet"].
        data_class (str): Choices are ["g30"] for jetnet.
        data_dir (str): Directory in which data is located, or in which to download the dataset.
        num_samples (int, optional): Number of samples to return. Defaults to 50,000.

    Returns:
        np.ndarray: Array of shape ``(num_samples, num_particles, num_features)`` containing the real data.
    """
    if dataset not in _valid_datasets:
        raise ValueError(f"Invalid dataset: {dataset}")

    if data_class not in _valid_datasets[dataset]:
        raise ValueError(f"Invalid data class {data_class} for dataset {dataset}")

    data_args = {
        "data_dir": f"{data_dir}/{dataset}",
        "jet_features": None,
        "download": True,
    }

    if dataset == "jetnet":
        # dataset-specific args
        data_args |= {"particle_features": ["etarel", "phirel", "ptrel"]}

        if data_class.endswith("30"):
            data_args |= {"num_particles": 30, "jet_type": data_class[:-2]}
        elif data_class.endswith("150"):
            data_args |= {"num_particles": 150, "jet_type": data_class[:-3]}

        pf, _ = jetnet.datasets.JetNet.getData(**data_args)
        pf = pf[-num_samples:]
        real_samples = Samples(
            dataset=dataset,
            # remove "30" to match jetnet file naming convention
            data_class=data_class if data_class.endswith("150") else data_class[:-2],
            samples=pf,
            download_path=f"{data_dir}/{dataset}/{data_class}.hdf5",
        )

    return real_samples
