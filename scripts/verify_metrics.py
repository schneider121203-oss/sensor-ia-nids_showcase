#!/usr/bin/env python3
"""Recalculate the published metrics from the disclosed confusion matrix."""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "metrics.json"


def divide(numerator: int, denominator: int) -> float:
    if denominator == 0:
        raise ZeroDivisionError("A metric denominator is zero")
    return numerator / denominator


def main() -> None:
    document = json.loads(DATA.read_text(encoding="utf-8"))
    matrix = document["confusion_matrix"]
    tp = int(matrix["true_positive"])
    fp = int(matrix["false_positive"])
    tn = int(matrix["true_negative"])
    fn = int(matrix["false_negative"])

    metrics = {
        "recall": divide(tp, tp + fn),
        "precision": divide(tp, tp + fp),
        "f1_score": divide(2 * tp, 2 * tp + fp + fn),
        "false_positive_rate": divide(fp, fp + tn),
    }

    expected_counts = document["sample_counts"]
    assert tp + fn == expected_counts["attack_associated"]
    assert fp + tn == expected_counts["benign"]
    assert tp + fp + tn + fn == expected_counts["total"]

    for name, calculated in metrics.items():
        reported = float(document["reported_metrics"][name])
        if not math.isclose(calculated, reported, rel_tol=0.0, abs_tol=1e-15):
            raise AssertionError(f"{name}: calculated={calculated}, reported={reported}")

    print(f"Recall:             {metrics['recall']:.2%}")
    print(f"Precision:          {metrics['precision']:.2%}")
    print(f"F1-score:           {metrics['f1_score']:.2%}")
    print(f"False-positive rate: {metrics['false_positive_rate']:.2%}")
    print("All published metrics verified.")


if __name__ == "__main__":
    main()
