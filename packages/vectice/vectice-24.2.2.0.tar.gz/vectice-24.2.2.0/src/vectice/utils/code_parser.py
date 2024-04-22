from __future__ import annotations

import ast
import re
from collections import OrderedDict
from typing import Any


class VariableVisitor(ast.NodeVisitor):
    def __init__(self, model_metrics: bool = False):
        self.variables: OrderedDict[str, None] = OrderedDict()
        self.processed_variables: set[str] = set()
        self.function_call_args: set[str] = set()
        self.function_call_kwargs: set[str] = set()
        self.variable_calls: set[str] = set()
        self.vectice_call_vars: set[str] = set()
        self.metric_variables: set[str] = set()
        self.model_metrics = model_metrics

    ##### Implement NodeVisitor methods

    def visit_Assign(self, node: ast.Assign) -> None:  # noqa: N802
        for target in node.targets:
            self._extract_variables_from_target(target)
        self.generic_visit(node)
        if self.model_metrics:
            self._extract_metric_vars(node)

    def visit_Name(self, node: ast.Name) -> None:  # noqa: N802
        var_name = node.id
        # get functions args and kwargs
        args_kwargs = self.function_call_args.union(self.function_call_kwargs)
        all_processed_vars = self.processed_variables.union(self.variable_calls)
        if var_name not in all_processed_vars and var_name not in args_kwargs:
            self.variables[var_name] = None
            self.processed_variables.add(var_name)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:  # noqa: N802
        if isinstance(node.func, ast.Name) or isinstance(node.func, ast.Attribute):
            # Get variables that call functions
            if isinstance(node.func, ast.Attribute):
                try:
                    # Calls will fail
                    self.variable_calls.add(node.func.value.id)  # pyright: ignore[reportAttributeAccessIssue]
                except AttributeError:
                    pass
            # Record function args, kwargs.
            args = node.args + node.keywords
            for arg in args:
                arg_value = self._get_arg_or_kwarg_val(arg)
                if arg_value:
                    if hasattr(arg_value, "__iter__") and not isinstance(arg_value, str):
                        self.function_call_args = self.function_call_args.union(arg_value)
                    else:
                        self.function_call_args.add(arg_value)  # pyright: ignore[reportAttributeAccessIssue]
                if (
                    hasattr(node.func, "id")
                    and self._is_vectice_call_vars(node.func.id)  # pyright: ignore[reportAttributeAccessIssue]
                    and arg_value
                ):
                    if hasattr(arg_value, "__iter__") and not isinstance(arg_value, str):
                        self.vectice_call_vars = self.vectice_call_vars.union(arg_value)
                    else:
                        self.vectice_call_vars.add(arg_value)
        self.generic_visit(node)

    ##### VariableVisitor methods

    def _extract_variables_from_target(self, target: ast.expr) -> None:
        if isinstance(target, ast.Constant):
            return
        if isinstance(target, ast.Name):
            self.visit_Name(target)
        elif isinstance(target, ast.Tuple):
            for element in target.elts:
                if isinstance(element, ast.Name):
                    self.visit_Name(element)

    def _add_metric_variables(self, metric_variable: str, node: ast.Assign) -> None:
        try:
            function_call_name = node.value.func.id  # pyright: ignore[reportAttributeAccessIssue]
        except Exception:
            function_call_name = None

        is_metric_call = self._is_metric_call_vars(function_call_name) if function_call_name else False

        if is_metric_call:
            self.metric_variables.add(metric_variable)

    def _extract_metric_vars(self, node: ast.Assign) -> None:
        # Get the variable
        for target in node.targets:
            metric_variable = None
            if isinstance(target, ast.Name):
                metric_variable = target.id
            if metric_variable:
                self._add_metric_variables(metric_variable, node)

    def _get_arg_or_kwarg_val(self, arg: Any) -> Any | None:
        try:
            # arg value
            return arg.id
        except AttributeError:
            pass
        try:
            # kwarg value if not a variable
            return arg.value.value
        except AttributeError:
            pass
        try:
            # kwarg value if it is a variable
            return arg.value.id
        except AttributeError:
            pass
        try:
            # kwarg value if it is a list
            return {arg_value.id for arg_value in arg.value.elts}
        except AttributeError:
            pass
        return None

    def _is_vectice_call_vars(self, func_name: str) -> bool:
        vectice_functions = [
            "NoResource",
            "Resource",
            "Table",
            "SnowflakeResource",
            "FileResource",
            "GCSResource",
            "S3Resource",
            "BigQueryResource",
            "DatabricksTableResource",
        ]
        if func_name in vectice_functions:
            return True
        return False

    def _is_metric_call_vars(self, func_name: str) -> bool:
        from sklearn.metrics import (
            _classification,  # pyright: ignore[reportPrivateUsage]
            _ranking,  # pyright: ignore[reportPrivateUsage]
            _regression,  # pyright: ignore[reportPrivateUsage]
            _scorer,  # pyright: ignore[reportPrivateUsage]
            cluster,  # pyright: ignore[reportPrivateUsage]
        )

        all_metrics = dir(_ranking) + dir(_scorer) + dir(cluster) + dir(_regression) + dir(_classification)

        if func_name in all_metrics:
            return True
        return False


def parse_comments(code: str) -> list[dict]:
    # Get all comments and variables
    comments_and_variables = r"##\s*(.*?)(?:$|\n)|(.+?)\s*=\s*.*?(?:$|\n)"
    all_comments_and_variables = []
    for idx, match in enumerate(re.findall(comments_and_variables, code)):
        comment, variable = match
        # Create placeholder for no variable found
        variable = variable if variable else f"variable_{idx}"
        # Remove empty string matches
        comment = comment if comment else None
        all_comments_and_variables.append({"variable": variable, "comment": comment})
    return all_comments_and_variables


def preprocess_code(code: str) -> str:
    # Remove or comment out lines with % or ! commands
    code = re.sub(r"^\s*%[^\n]*$", "#", code, flags=re.MULTILINE)
    code = re.sub(r"^\s*![^\n]*$", "#", code, flags=re.MULTILINE)
    # remove a notebooks helper function calls ?
    code = re.sub(r".*?\?$", "", code, flags=re.MULTILINE)

    return code
