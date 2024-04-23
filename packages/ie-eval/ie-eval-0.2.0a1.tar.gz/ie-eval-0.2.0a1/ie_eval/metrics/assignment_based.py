"""Compute the reading-order-independent ECER/EWER/Nerval metrics from a label/prediction dataset."""

import logging
from pathlib import Path

from bio_parser import GLOBAL_STAT_NAME
from bio_parser.utils import load_dataset
from prettytable import PrettyTable

from ie_eval.scorer import (
    MicroAverageErrorRate,
    MicroAverageFScore,
    OiEcerEwer,
    OiNerval,
)
from ie_eval.table_formatter import (
    make_oi_ecer_ewer_prettytable,
    make_oi_nerval_prettytable,
)

logger = logging.getLogger(__name__)


def compute_oiecerewer(
    label_dir: Path,
    prediction_dir: Path,
    by_category: bool = False,
    print_table: bool = True,
) -> PrettyTable:
    """Compute reading-order-independent ECER and EWER metrics.

    Args:
        label_dir (Path): Path to the directory containing BIO label files.
        prediction_dir (Path): Path to the directory containing BIO prediction files.
        by_category (bool, optional): Whether to compute the metric globally or for each category. Defaults to False. (Not implemented yet)
        print_table (bool, optional): Whether to print the table. Defaults to True.

    Returns:
        PrettyTable: The evaluation table formatted in Markdown.
    """
    dataset = load_dataset(label_dir, prediction_dir)
    # Initialize scores
    ecer_total_score_err = MicroAverageErrorRate()
    ewer_total_score_err = MicroAverageErrorRate()

    # Iterate over the dataset
    for label, prediction in dataset:
        ecer_score = OiEcerEwer(
            labels=label.entities,
            predictions=prediction.entities,
            compute_ecer=True,
        )

        ewer_score = OiEcerEwer(
            labels=label.entities,
            predictions=prediction.entities,
            compute_ecer=False,
        )

        # Micro average
        ecer_total_score_err.update(GLOBAL_STAT_NAME, ecer_score)
        ewer_total_score_err.update(GLOBAL_STAT_NAME, ewer_score)

        # TODO: https://gitlab.teklia.com/ner/metrics/ie-eval/-/issues/12
        if by_category:
            continue

    # Format and display results
    table = make_oi_ecer_ewer_prettytable(
        ecer_total_score_err,
        ewer_total_score_err,
    )
    if print_table:
        print(table)  # noqa: T201
    return table


def compute_oinerval(
    label_dir: Path,
    prediction_dir: Path,
    nerval_threshold: float = 30.0,
    by_category: bool = False,
    print_table: bool = True,
) -> PrettyTable:
    """Compute reading-order-independent Nerval Precision, Recall and F1 scores.

    Args:
        label_dir (Path): Path to the directory containing BIO label files.
        prediction_dir (Path): Path to the directory containing BIO prediction files.
        nerval_threshold (float, default = 30.0): Threshold for the amount of character error that is tolerable during the computation (values in the range [0.0, 100.0]])
        by_category (bool, optional): Whether to compute the metric globally or for each category. Defaults to False. (Not implemented yet)
        print_table (bool, optional): Whether to print the table. Defaults to True.

    Returns:
        PrettyTable: The evaluation table formatted in Markdown.
    """
    dataset = load_dataset(label_dir, prediction_dir)
    # Initialize scores
    total_score_f1 = MicroAverageFScore()

    # Iterate over the dataset
    for label, prediction in dataset:
        score = OiNerval(
            labels=label.entities,
            predictions=prediction.entities,
            nerval_threshold=nerval_threshold,
        )

        # Micro average
        total_score_f1.update(GLOBAL_STAT_NAME, score)

        # TODO: https://gitlab.teklia.com/ner/metrics/ie-eval/-/issues/12
        if not by_category:
            continue

    # Format and display results
    table = make_oi_nerval_prettytable(
        total_score_f1,
    )
    if print_table:
        print(table)  # noqa: T201
    return table
