"""Computing CER/WER."""

import math

import pytest
from ie_eval.metrics.assignment_based import (
    compute_oiecerewer,
    compute_oinerval,
)
from ie_eval.scorer import (
    OiEcerEwer,
    OiNerval,
    calc_dist_sus_entity,
)

from tests import FIXTURES


@pytest.mark.parametrize(
    (
        "label",
        "prediction",
        "char_level",
        "expected_substitution_cost",
    ),
    [
        (
            ("Person", "George Washington"),
            ("Place", "George Washington"),
            True,
            1.0,
        ),
        (
            ("Person", "George Washington"),
            ("Place", "George Washington"),
            False,
            1.0,
        ),
        (
            ("Person", "George Washington"),
            ("Person", "George Washington"),
            True,
            0.0,
        ),
        (
            ("Person", "George Washington"),
            ("Person", "George Washington"),
            False,
            0.0,
        ),
        (
            ("Person", "George Washington"),
            ("Person", "George Washingtn"),
            True,
            0.058823529411764705,
        ),
        (
            ("Person", "George Washington"),
            ("Person", "George Washingtn"),
            False,
            0.5,
        ),
    ],
)
def test_calc_dist_sus_entity(
    label,
    prediction,
    char_level,
    expected_substitution_cost,
):
    sust_cost = calc_dist_sus_entity(prediction, label, char_level)
    assert math.isclose(expected_substitution_cost, sust_cost)


@pytest.mark.parametrize(
    (
        "labels",
        "predictions",
        "char_level",
        "expected_num_ne_gt",
        "expected_num_ne_hyp",
        "expected_cost_matrix",
        "expected_errors",
    ),
    [
        (
            [("Person", "George Washington"), ("Place", "Valencia")],
            [("Person", "George Washingtn")],
            True,
            2,
            1,
            [[0.058823529411764705, 1.0], [1.0, 1.0]],
            1.058823529411764705,
        ),
        (
            [("Person", "George Washington"), ("Place", "Valencia")],
            [("Person", "George Washingtn")],
            False,
            2,
            1,
            [[0.5, 1.0], [1.0, 1.0]],
            1.5,
        ),
        (
            [("Person", "George Washington"), ("Place", "Valencia")],
            [("Place", "Valencia")],
            True,
            2,
            1,
            [[1.0, 1.0], [0.0, 1.0]],
            1.0,
        ),
        (
            [("Person", "George Washington"), ("Place", "Valencia")],
            [("Place", "Valencia")],
            False,
            2,
            1,
            [[1.0, 1.0], [0.0, 1.0]],
            1.0,
        ),
        (
            [("Person", "George Washington"), ("Place", "Valencia")],
            [],
            False,
            2,
            0,
            [[1.0, 1.0], [1.0, 1.0]],
            2.0,
        ),
        (
            [],
            [("Person", "George Washington"), ("Place", "Valencia")],
            False,
            0,
            2,
            [[1.0, 1.0], [1.0, 1.0]],
            2.0,
        ),
    ],
)
def test_oi_ecer_ewer_eval(
    labels,
    predictions,
    char_level,
    expected_num_ne_gt,
    expected_num_ne_hyp,
    expected_cost_matrix,
    expected_errors,
):
    score = OiEcerEwer(labels, predictions, char_level)
    assert score.num_ne_gt == expected_num_ne_gt
    assert score.num_ne_hyp == expected_num_ne_hyp
    assert score.costs == expected_cost_matrix
    assert score.errors == expected_errors


@pytest.mark.parametrize(
    (
        "labels",
        "predictions",
        "nerval_threshold",
        "expected_num_ne_gt",
        "expected_num_ne_hyp",
        "expected_cost_matrix",
        "expected_true_positives",
        "expected_false_positives",
        "expected_false_negatives",
    ),
    [
        (
            [("Person", "George Washington"), ("Place", "Valencia")],
            [("Person", "George Washingtn")],
            0.0,
            2,
            1,
            [[2.0, 1.0], [2.0, 1.0]],
            0,
            1,
            2,
        ),
        (
            [("Person", "George Washington"), ("Place", "Valencia")],
            [("Person", "George Washingtn")],
            30.0,
            2,
            1,
            [[0.0, 1.0], [2.0, 1.0]],
            1,
            0,
            1,
        ),
        (
            [("Person", "George Washington"), ("Place", "Valencia")],
            [("Person", "George Washingtn")],
            100.0,
            2,
            1,
            [[0.0, 1.0], [2.0, 1.0]],
            1,
            0,
            1,
        ),
        (
            [("Person", "George Washington"), ("Place", "Valencia")],
            [("Place", "Valencia")],
            0.0,
            2,
            1,
            [[2.0, 1.0], [0.0, 1.0]],
            1,
            0,
            1,
        ),
        (
            [("Person", "George Washington"), ("Place", "Valencia")],
            [("Place", "Valencia")],
            30.0,
            2,
            1,
            [[2.0, 1.0], [0.0, 1.0]],
            1,
            0,
            1,
        ),
        (
            [("Person", "George Washington"), ("Place", "Valencia")],
            [("Place", "Valencia")],
            100.0,
            2,
            1,
            [[2.0, 1.0], [0.0, 1.0]],
            1,
            0,
            1,
        ),
        (
            [("Person", "George Washington"), ("Place", "Valencia")],
            [],
            0.0,
            2,
            0,
            [[1.0, 1.0], [1.0, 1.0]],
            0,
            0,
            2,
        ),
        (
            [],
            [("Person", "George Washington"), ("Place", "Valencia")],
            0.0,
            0,
            2,
            [[1.0, 1.0], [1.0, 1.0]],
            0,
            2,
            0,
        ),
    ],
)
def test_oi_nerval_eval(
    labels,
    predictions,
    nerval_threshold,
    expected_num_ne_gt,
    expected_num_ne_hyp,
    expected_cost_matrix,
    expected_true_positives,
    expected_false_positives,
    expected_false_negatives,
):
    score = OiNerval(labels, predictions, nerval_threshold)
    assert expected_num_ne_gt == score.num_ne_gt
    assert expected_num_ne_hyp == score.num_ne_hyp
    assert expected_cost_matrix == score.costs
    assert expected_true_positives == score.true_positives
    assert expected_false_positives == score.false_positives
    assert expected_false_negatives == score.false_negatives


@pytest.mark.parametrize(
    (
        "label_dir",
        "prediction_dir",
        "shuffled_prediction_dir",
        "expected_table",
    ),
    [
        (
            FIXTURES / "labels",
            FIXTURES / "predictions",
            FIXTURES / "shuffled_predictions",
            """| Category | ECER (%) | EWER (%) | N entities | N documents |
|:---------|:--------:|:--------:|-----------:|------------:|
| total    |  21.33   |  28.27   |         28 |           5 |""",
        ),
    ],
)
def test_compute_oi_ecer_ewer(
    label_dir,
    prediction_dir,
    shuffled_prediction_dir,
    expected_table,
):
    table = compute_oiecerewer(label_dir, prediction_dir)
    table_shuffled = compute_oiecerewer(
        label_dir,
        shuffled_prediction_dir,
    )
    assert table.get_string(sortby="Category") == expected_table
    assert table_shuffled.get_string(sortby="Category") == expected_table


@pytest.mark.parametrize(
    (
        "label_dir",
        "prediction_dir",
        "shuffled_prediction_dir",
        "expected_table",
    ),
    [
        (
            FIXTURES / "labels",
            FIXTURES / "predictions",
            FIXTURES / "shuffled_predictions",
            """| Category | Precision (%) | Recall (%) | F1 (%) | N entities | N documents |
|:---------|:-------------:|:----------:|:------:|-----------:|------------:|
| total    |     82.14     |   82.14    | 82.14  |         28 |           5 |""",
        ),
    ],
)
def test_compute_nerval(
    label_dir,
    prediction_dir,
    shuffled_prediction_dir,
    expected_table,
):
    table = compute_oinerval(label_dir, prediction_dir)
    table_shuffled = compute_oinerval(
        label_dir,
        shuffled_prediction_dir,
    )
    assert table.get_string(sortby="Category") == expected_table
    assert table_shuffled.get_string(sortby="Category") == expected_table
