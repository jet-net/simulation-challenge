from __future__ import annotations

from jetnet import evaluation

from .data import Samples


def evaluate(
    real_samples: Samples,
    gen_samples: Samples,
    num_w1_eval_samples: int = 50_000,
    num_w1_batches: int = 5,
) -> dict:
    """Evaluates the given generated samples against the real samples using the JetNet library.

    Args:
        real_samples (np.ndarray): Array of shape ``(num_samples, num_particles, num_features)`` containing the real data.
        gen_samples (np.ndarray): Array of shape ``(num_samples, num_particles, num_features)`` containing the generated data.

    Returns:
        dict: Dictionary of metrics.
    """

    scores = {}

    # W1 distance between mass distributions
    scores["w1m"] = evaluation.w1m(
        real_samples.samples,
        gen_samples.samples,
        num_eval_samples=num_w1_eval_samples,
        num_batches=num_w1_batches,
        return_std=True,
    )

    # W1 distance between particle feature distributions
    scores["w1p"] = evaluation.w1p(
        real_samples.samples,
        gen_samples.samples,
        exclude_zeros=True,
        num_eval_samples=num_w1_eval_samples,
        num_batches=num_w1_batches,
        return_std=True,
    )

    # FPD and KPD using EFPs
    scores["fpd"] = evaluation.fpd(real_samples.get_efps(), gen_samples.get_efps())
    scores["kpd"] = evaluation.kpd(real_samples.get_efps(), gen_samples.get_efps())

    return scores
