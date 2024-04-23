"""Scorer."""
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import NamedTuple

import numpy as np
from munkres import Munkres

# Global Munkres algorithm
M = Munkres()


# Global function for ECER, EWER and NERVAL
def calc_dist_sus_entity(
    hyp_ne: tuple[str, str],
    gt_ne: tuple[str, str],
    char_level: bool,
) -> float:
    """Calculate substitution distance between 2 entities (hyp_ne, gt_ne).

    Args:
        hyp_ne (tuple): hypothesized Named Entity, format: (category, transcription)
        gt_ne (tuple): label Named Entity, format: (category, transcription)
        char_level (bool): if True, evaluate at character level.

    Returns:
        float: edit distance in range [0.0, 1.0]
    """
    # Check coincidence of NE category
    if hyp_ne[0] != gt_ne[0]:
        return 1.0

    hyp_word_transcription = hyp_ne[1]
    gt_word_transcription = gt_ne[1]

    if char_level is False:
        # Split by word
        hyp_word_transcription = hyp_word_transcription.split()
        gt_word_transcription = gt_word_transcription.split()

    # Tuples of (distance, correct tokens )
    vec_dist_pre = [(i, 0) for i in range(len(gt_word_transcription) + 1)]
    vec_dist_act = [(0, 0)] * (len(gt_word_transcription) + 1)

    # if char_level == true, then the string is explored character by character (including space)
    for j in range(len(hyp_word_transcription)):
        vec_dist_act[0] = (j + 1, 0)
        for i in range(len(gt_word_transcription)):
            dist_ins = (vec_dist_act[i][0] + 1, vec_dist_act[i][1])
            dist_bor = (vec_dist_pre[i + 1][0] + 1, vec_dist_pre[i + 1][1])

            cost_sus = int(hyp_word_transcription[j] != gt_word_transcription[i])
            dist_sus = (
                vec_dist_pre[i][0] + cost_sus,
                vec_dist_pre[i][1] + (1 - cost_sus),
            )

            vec_dist_act[i + 1] = min(dist_ins, dist_bor, dist_sus)

        vec_dist_pre, vec_dist_act = vec_dist_act, vec_dist_pre

    # Saturation of CER/WER (min(CER, 1.0))
    return min(float(vec_dist_pre[-1][0]) / float(len(gt_word_transcription)), 1.0)


@dataclass
class OiEcerEwer:
    """Base class for order independent ECER / EWER computation."""

    labels: list[tuple[str, str]]
    predictions: list[tuple[str, str]]
    compute_ecer: bool

    costs: list[list[float]] = field(default_factory=list)
    errors: float = 0.0

    def __post_init__(self):
        """After object creation, generate cost matrix and compute errors."""
        # Generate cost matrix
        self._generate_cost_matrix()

        # Generate error
        self._compute_errors()

    @property
    def num_ne_gt(self) -> int:
        """Compute number of NEs in the label."""
        return len(self.labels)

    @property
    def num_ne_hyp(self) -> int:
        """Compute number of NEs in the prediction."""
        return len(self.predictions)

    def _generate_cost_matrix(self) -> None:
        """Generation of square cost matrix."""
        max_num_ne = max(self.num_ne_gt, self.num_ne_hyp)
        for i in range(max_num_ne):
            self.costs.append([1.0] * max_num_ne)

        # Population of cost matrix
        for i in range(max_num_ne):
            gt_ne_i = False if i >= self.num_ne_gt else self.labels[i]
            for j in range(max_num_ne):
                hyp_ne_j = False if j >= self.num_ne_hyp else self.predictions[j]
                if not gt_ne_i or not hyp_ne_j:
                    # One of them does not exist => Padding with dummy symbols
                    # Cost equal to insertion or deletion of GT or HYP NE, respectively
                    self.costs[i][j] = 1.0
                else:
                    # Both of them exist: cost equal to substitution
                    self.costs[i][j] = calc_dist_sus_entity(
                        hyp_ne_j,
                        gt_ne_i,
                        char_level=self.compute_ecer,
                    )

    def _compute_errors(self) -> None:
        """Compute the best entity assignment between labels and predictions at character level."""
        self.errors = 0.0

        if self.num_ne_hyp == 0 and self.num_ne_gt == 0:
            # No errors
            self.errors = 0.0
            # TODO: https://gitlab.teklia.com/ner/metrics/ie-eval/-/issues/7

        elif (self.num_ne_hyp != 0 and self.num_ne_gt == 0) or (
            self.num_ne_hyp == 0 and self.num_ne_gt != 0
        ):
            # Only one exists (XOR) -> All detected NEs are errors
            self.errors = self.num_ne_hyp + self.num_ne_gt
            # TODO: https://gitlab.teklia.com/ner/metrics/ie-eval/-/issues/7

        else:
            # General case computation
            # Execute Munkres/Hungarian algorithm
            indexes = M.compute(self.costs)
            for i, j in indexes:
                self.errors += self.costs[i][j]


@dataclass
class OiNerval:
    """Base class for order independent Nerval computation of Precision, Recall and F1 scores."""

    labels: list[tuple[str, str]]
    predictions: list[tuple[str, str]]
    nerval_threshold: float = 30.0

    costs: list[list[float]] = field(default_factory=list)

    true_positives: int = 0
    false_positives: int = 0
    false_negatives: int = 0

    def __post_init__(self):
        """After object creation, generate cost matrix and compute errors."""
        # Generate cost matrix
        self._generate_cost_matrix()

        # Generate error
        self._compute_metric()

    @property
    def num_ne_gt(self) -> int:
        """Returns the number of NEs in the label."""
        return len(self.labels)

    @property
    def num_ne_hyp(self) -> int:
        """Returns the number of NEs in the prediction."""
        return len(self.predictions)

    def _generate_cost_matrix(self) -> None:
        """Generation of square cost matrix."""
        fixed_nerval_threshold = self.nerval_threshold / 100.0
        max_num_ne = max(self.num_ne_gt, self.num_ne_hyp)

        for i in range(max_num_ne):
            self.costs.append([1.0] * max_num_ne)

        # Population of cost matrix
        for i in range(max_num_ne):
            gt_ne_i = False if i >= self.num_ne_gt else self.labels[i]
            for j in range(max_num_ne):
                hyp_ne_j = False if j >= self.num_ne_hyp else self.predictions[j]
                if not gt_ne_i or not hyp_ne_j:
                    # One of them does not exist => Padding with dummy symbols
                    # Cost equal to insertion or deletion of GT or HYP NE, respectively
                    self.costs[i][j] = 1.0
                else:
                    # Both of them exist: cost equal to substitution
                    self.costs[i][j] = 2 * calc_dist_sus_entity(
                        hyp_ne_j,
                        gt_ne_i,
                        char_level=True,
                    )
                    if self.costs[i][j] > 0 and gt_ne_i[0] == hyp_ne_j[0]:
                        # If there are character errors but tags match
                        # Set to extremes
                        self.costs[i][j] = (
                            0 if self.costs[i][j] <= (2 * fixed_nerval_threshold) else 2
                        )

    def _compute_metric(self) -> None:
        """Compute best entity assignment and return True Positives, False Positives, False Negatives."""
        if self.num_ne_gt == 0 and self.num_ne_hyp == 0:
            # No errors, TP = FP = FN = 0
            self.true_positives = 0
            self.false_positives = 0
            self.false_negatives = 0
            return

        if self.num_ne_hyp != 0 and self.num_ne_gt == 0:
            # Only hypothesis exists, all NEs are FP
            self.true_positives = 0
            self.false_positives = self.num_ne_hyp
            self.false_negatives = 0
            return

        if self.num_ne_gt != 0 and self.num_ne_hyp == 0:
            # Only GT exists, all NEs are FN
            self.true_positives = 0
            self.false_positives = 0
            self.false_negatives = self.num_ne_gt
            return

        # General case computation
        indexes = M.compute(self.costs)

        tp = 0
        fp = 0
        fn = 0

        for i, j in indexes:
            # Depending on match cost, decide
            if self.costs[i][j] == 0:  # Substitution without cost, TP
                tp = tp + 1
            elif self.costs[i][j] == 2:  # Substitution with cost = 2, FP and FN
                fn = fn + 1
                fp = fp + 1
            elif (
                self.costs[i][j] == 1
            ):  # Insertion or deletion with cost = 1, may be FP or FN
                if (
                    i >= self.num_ne_gt
                ):  # GT NE does not exist, therefore hypothesized NE is FP
                    fp = fp + 1
                elif (
                    j >= self.num_ne_hyp
                ):  # Hyp NE does not exist, therefore GT NE is FN
                    fn = fn + 1
                else:
                    raise Exception(
                        f"Error in substitution between NEs GT: {i} - Hyp: {j}. Cost is 1 but both exist",
                    )
            else:
                raise Exception(
                    "Cost matrix was not properly initialized in Nerval computation",
                )

        self.true_positives = tp
        self.false_positives = fp
        self.false_negatives = fn


class BagOfWords(NamedTuple):
    """Base class for bag-of-word metrics. Extension of bWER defined in End-to-End Page-Level Assessment of Handwritten Text Recognition (https://arxiv.org/pdf/2301.05935.pdf)."""

    labels: list[str | tuple[str, str]]
    predictions: list[str | tuple[str, str]]

    @property
    def label_counter(self) -> Counter[str]:
        """Split the label into a list of words."""
        return Counter(self.labels)

    @property
    def prediction_counter(self) -> Counter[str]:
        """Split the prediction into a list of words."""
        return Counter(self.predictions)

    @property
    def true_positives(self) -> int:
        """Count true positive words."""
        return sum((self.label_counter & self.prediction_counter).values())

    @property
    def false_positives(self) -> int:
        """Count false positive words."""
        return sum((self.prediction_counter - self.label_counter).values())

    @property
    def false_negatives(self) -> int:
        """Count false negatives words."""
        return sum((self.label_counter - self.prediction_counter).values())

    @property
    def all_words(self) -> list[str | tuple[str, str]]:
        """All tagged words."""
        return sorted(set(self.labels + self.predictions))

    @property
    def label_word_vector(self) -> np.array:
        """Iterate over the set of tagged words and count occurrences in the label."""
        return np.array(
            [self.labels.count(w) for w in self.all_words],
        )

    @property
    def prediction_word_vector(self) -> np.array:
        """Iterate over the set of words and count occurrences in the prediction."""
        return np.array(
            [self.predictions.count(word) for word in self.all_words],
        )

    @property
    def insertions_deletions(self) -> int:
        """Count unavoidable insertions and deletions. See Equation 8 from https://arxiv.org/pdf/2301.05935.pdf."""
        return abs(len(self.labels) - len(self.predictions))

    @property
    def substitutions(self) -> int:
        """Count substitutions. See Equation 8 from https://arxiv.org/pdf/2301.05935.pdf."""
        return (
            np.absolute(self.prediction_word_vector - self.label_word_vector).sum()
            - self.insertions_deletions
        ) / 2

    @property
    def errors(self) -> int:
        """Count total number of errors."""
        return self.substitutions + self.insertions_deletions


class MicroAverageErrorRate:
    """Compute total error rates."""

    def __init__(self) -> None:
        """Initialize errors and counts.

        Examples:
            >>> score = MicroAverageErrorRate()
        """
        self.label_word_count = defaultdict(int)
        self.error_count = defaultdict(int)
        self.count = defaultdict(int)

    def update(self, key: str, score: BagOfWords | OiEcerEwer) -> None:
        """Update the score with the current evaluation for a given key.

        Args:
            key (str): Category to update.
            score (TextEval): Current score.

        Examples:
            >>> score.update("total", [("person", "Georges"), ("person", "Washington")])
        """
        self.label_word_count[key] += len(score.labels)
        self.count[key] += 1
        self.error_count[key] += score.errors

    @property
    def error_rate(self) -> dict[str, float]:
        """Error rate for each key."""
        return {
            key: min(100 * self.error_count[key] / self.label_word_count[key], 100)
            for key in self.label_word_count
        }

    @property
    def categories(self) -> list[str]:
        """Get all categories in the label."""
        return list(self.label_word_count.keys())


class MicroAverageFScore:
    """Compute total precision, recall, and f1 scores."""

    def __init__(self) -> None:
        """Initialize error counts.

        Examples:
            >>> score = MicroAverageFScore()
        """
        self.label_word_count = defaultdict(int)
        self.count = defaultdict(int)
        self.true_positives = defaultdict(int)
        self.false_positives = defaultdict(int)
        self.false_negatives = defaultdict(int)

    def update(self, key: str, score: BagOfWords) -> None:
        """Update the score with the current evaluation for a given key.

        Args:
            key (str): Category to update.
            score (BagOfWords): Current score.

        Examples:
            >>> score.update("total", BagOfWords(label.entities, pred.entities))
        """
        self.label_word_count[key] += len(score.labels)
        self.count[key] += 1
        self.true_positives[key] += score.true_positives
        self.false_positives[key] += score.false_positives
        self.false_negatives[key] += score.false_negatives

    @staticmethod
    def _recall_score(true_positives: int, false_negatives: int) -> float:
        """Compute the recall."""
        return (
            100 * true_positives / (true_positives + false_negatives)
            if true_positives + false_negatives > 0
            else 100
        )

    @staticmethod
    def _precision_score(true_positives: int, true_negatives: int) -> float:
        """Compute the precision."""
        return (
            100 * true_positives / (true_positives + true_negatives)
            if true_positives + true_negatives > 0
            else 100
        )

    @staticmethod
    def _f1_score(precision: float, recall: float) -> float:
        """Compute the F1 score."""
        return (
            2 * precision * recall / (precision + recall)
            if precision + recall > 0
            else 0
        )

    @property
    def recall(self) -> dict[str, float]:
        """Recall score for each key."""
        return {
            key: self._recall_score(self.true_positives[key], self.false_negatives[key])
            for key in self.count
        }

    @property
    def precision(self) -> dict[str, float]:
        """Precision score for each key."""
        return {
            key: self._precision_score(
                self.true_positives[key],
                self.false_positives[key],
            )
            for key in self.count
        }

    @property
    def f1_score(self) -> dict[str, float]:
        """F1 score for each key."""
        return {
            key: self._f1_score(self.precision[key], self.recall[key])
            for key in self.count
        }

    @property
    def categories(self) -> list[str]:
        """Get all categories in the label."""
        return list(self.label_word_count.keys())
