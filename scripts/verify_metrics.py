#!/usr/bin/env python3
"""Recalcula las métricas publicadas desde la matriz de confusión."""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "metrics.json"


def divide(numerator: int, denominator: int) -> float:
    if denominator == 0:
        raise ZeroDivisionError("El denominador de una métrica es cero")
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

    print(f"Recall:                    {100 * metrics['recall']:.2f} %")
    print(f"Precisión:                 {100 * metrics['precision']:.2f} %")
    print(f"F1-score:                  {100 * metrics['f1_score']:.2f} %")
    print(f"Tasa de falsos positivos:  {100 * metrics['false_positive_rate']:.2f} %")
    print("Todas las métricas publicadas fueron verificadas.")


if __name__ == "__main__":
    main()
