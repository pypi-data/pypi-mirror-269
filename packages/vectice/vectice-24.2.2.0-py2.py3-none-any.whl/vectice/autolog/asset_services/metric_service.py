from __future__ import annotations

import ast
from functools import reduce
from typing import TYPE_CHECKING, Any

from vectice.utils.code_parser import VariableVisitor, preprocess_code

if TYPE_CHECKING:
    from keras.models import Model as KerasModel


class MetricService:
    def __init__(self, cell_data: dict):
        self._cell_data = cell_data
        self._model_cell = None

    def _get_model_metrics(self, data: dict) -> dict[str, Any]:
        # TODO mix of models ?
        cell_content = data["cell"]
        variables = data["variables"]

        if not cell_content:
            return {}
        # Get model cell content for metrics
        self._model_cell = preprocess_code(cell_content)

        tree = ast.parse(self._model_cell)
        visitor = VariableVisitor(True)
        visitor.visit(tree)

        metrics = list(visitor.metric_variables)

        return reduce(
            lambda identified_metrics, key: (
                {**identified_metrics, key: variables[key]}
                if key in metrics and isinstance(variables[key], (int, float))
                else identified_metrics
            ),
            variables.keys(),
            {},
        )

    def _get_keras_training_metrics(self, model: KerasModel) -> dict[str, float]:
        try:
            return {
                str(key)
                + "_train": float(model.get_metrics_result()[key].numpy())  # pyright: ignore[reportGeneralTypeIssues]
                for key in model.get_metrics_result().keys()  # pyright: ignore[reportGeneralTypeIssues]
            }
        except Exception:
            return {}
