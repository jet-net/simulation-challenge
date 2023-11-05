from __future__ import annotations

import argparse
import os

import simulation_challenge as sc
from simulation_challenge.data import Samples
from simulation_challenge.submission import Submission

# TODO: implement CI to run this script on all submissions


def evaluate_submission(sub: Submission, real_datasets_dir: str):
    """Evaluates the given submission for all samples provided.

    Args:
        sub (Submission): submission.
        real_datasets_dir (str): Path to directory containing real datasets.
    """

    print(f"Evaluating submission {sub.name}...")

    results = {}

    for dataset, data_classes in sub.samples.items():
        results[dataset] = {}
        for data_class, gen_samples in data_classes.items():
            real_samples: Samples = sc.data.get_real_samples(
                dataset, data_class, real_datasets_dir
            )
            gen_samples.download()

            print(f"Evaluating {dataset} {data_class}...")
            results[dataset][data_class] = sc.evaluate.evaluate(
                real_samples, gen_samples
            )

    print(results)

    # TODO: save results to file


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--real-datasets-dir",
        default="./datasets/",
        help="path to directory containing real datasets",
        type=str,
    )

    parser.add_argument(
        "--gen-datasets-dir",
        default="./datasets/",
        help="path to directory containing generated samples",
        type=str,
    )

    parser.add_argument(
        "--submission-dir",
        default="./submissions/",
        help="path to directory containing submissions",
        type=str,
    )

    parser.add_argument(
        "--submission",
        help="submission name",
        type=str,
    )

    parser.add_argument(
        "--evaluate", action=argparse.BooleanOptionalAction, default=False
    )

    args = parser.parse_args()

    subs = []
    if args.submission == "all":
        for submission in os.listdir(args.submission_dir):
            subs.append(
                sc.submission.load_submission(
                    args.submission_dir, submission, args.gen_datasets_dir
                )
            )
    else:
        subs.append(
            sc.submission.load_submission(
                args.submission_dir, args.submission, args.gen_datasets_dir
            )
        )

    if args.evaluate:
        for sub in subs:
            evaluate_submission(sub, args.real_datasets_dir)
