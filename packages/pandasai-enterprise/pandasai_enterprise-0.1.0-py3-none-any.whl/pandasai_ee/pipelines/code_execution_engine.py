# Copyright (c) 2024 Sinaptik GmbH
import ast
from pandasai.helpers.optional import get_environment
from pandasai.exceptions import NoResultFoundError
import base64
import datetime
import io
import pandas as pd
from typing import Any, List

import matplotlib.pyplot
from matplotlib import pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
from matplotlib.container import BarContainer
import math


class CodeExecutionEngine:
    """
    Handle the logic on how to handle different lines of code
    """

    _code: str
    _environment: dict
    _plots: dict

    def __init__(
        self, code: str = None, additional_dependencies: List[dict] = []
    ) -> None:
        self._code = code
        self._environment = get_environment(additional_dependencies)
        self._plots = []

    def add_to_env(self, key: str, value: Any) -> None:
        """
        Expose extra variables in the code to be used
        Args:
            key (str): Name of variable or lib alias
            value (Any): It can any value int, float, function, class etc.
        """
        self._environment[key] = value

    def execute(self, code: str) -> Any:
        """
        Executes the return updated environment
        """
        self._patch_libs()
        exec(code, self._environment)

        # Get the result
        if "result" not in self._environment:
            var_name, subscript = self._get_variable_last_line_of_code(code)
            if var_name and var_name in self._environment:
                if subscript is not None:

                    result = self._environment[var_name][subscript]
                else:
                    result = self._environment[var_name]

            raise NoResultFoundError("No result returned")
        else:
            result = self._environment["result"]

        if isinstance(result, dict) and result["type"] == "plot":

            for plot in self._plots:
                if plot["type"] == "plot":
                    result["value"] = plot["value"]

        return self._environment["result"]

    def _get_variable_last_line_of_code(self, code: str) -> str:
        """
        Returns variable name from the last line if it is a variable name or assigned.
        Args:
            code (str): Code in string.

        Returns:
            str: Variable name.
        """
        try:
            tree = ast.parse(code)
            last_statement = tree.body[-1]

            if isinstance(last_statement, ast.Assign):
                return self._get_assign_variable(last_statement)
            elif isinstance(last_statement, ast.Expr):
                return self._get_expr_variable(last_statement)

            return ast.unparse(last_statement).strip()

        except SyntaxError:
            return None

    def _get_assign_variable(self, assign_node):
        """
        Extracts the variable name from an assignment node.

        Args:
            assign_node (ast.Assign): Assignment node.

        Returns:
            str: Variable name.
        """
        if isinstance(assign_node.targets[0], ast.Subscript):
            return self._get_subscript_variable(assign_node.targets[0])
        elif isinstance(assign_node.targets[0], ast.Name):
            return assign_node.targets[0].id, None

    def _get_expr_variable(self, expr_node):
        """
        Extracts the variable name from an expression node.

        Args:
            expr_node (ast.Expr): Expression node.

        Returns:
            str: Variable name.
        """
        if isinstance(expr_node.value, ast.Subscript):
            return self._get_subscript_variable(expr_node.value)
        elif isinstance(expr_node.value, ast.Name):
            return expr_node.value.id, None

    def _get_subscript_variable(self, subscript_node):
        """
        Extracts the variable name from a subscript node.

        Args:
            subscript_node (ast.Subscript): Subscript node.

        Returns:
            str: Variable name.
        """
        if isinstance(subscript_node.value, ast.Name):
            variable_name = subscript_node.value.id
            return variable_name, subscript_node.slice.value

    def _patch_libs(self) -> None:
        """
        Patch global libs and function that needs to be overridden
        """
        matplotlib.pyplot.savefig = self._savefig

    def _savefig(self, *args, **kwargs):
        """
        Handle how to save image
        """
        fig = plt.gcf()
        gca = plt.gca()

        duplicate_index = None
        for i, output in enumerate(self._plots):
            if output["type"] == "plot":
                duplicate_index = i

        try:
            plot_data = self._plt_to_chartjs_json(fig, gca)
        except Exception:
            plot_data = None

        if plot_data is None:
            plot_data = self._fig_to_base64_image(fig)

        plot_entry = {
            "type": "plot",
            "message": "Plot generated: <plot>",
            "value": plot_data,
        }

        if duplicate_index is not None:
            self._plots[duplicate_index] = plot_entry
        else:
            self._plots.append(plot_entry)

    def _fig_to_base64_image(self, fig) -> str:
        """
        Return base64 image of matplotlib representation
        Args:
            fig (Figure): Matplotlib Figure

        Returns:
            str: base64 string representation
        """
        buffer = io.BytesIO()

        fig.savefig(buffer, format="png")
        buffer.seek(0)

        base64_string = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"

        buffer.close()

        return base64_string

    def _has_subplots(self, gcf):
        return len(gcf.get_axes()) > 1

    def _get_plot_orientation(self, gca) -> str:
        """
        Re
        Args:
            gca (Axes): matplotlib axes

        Returns:
            str: "veritical" or "horizontal"
        """
        if len(gca.containers) > 0:
            return gca.containers[0].orientation
        else:
            return "vertical"

    def _are_all_plots_of_same_type(self, gca):

        line_count = sum(isinstance(item, plt.Line2D) for item in gca.get_children())
        bar_count = sum(
            isinstance(item, plt.Rectangle) and (item.get_x() != 0 or item.get_y() != 0)
            for item in gca.get_children()
        )
        pie_count = sum(isinstance(item, patches.Wedge) for item in gca.get_children())

        plot_types_count = [line_count, bar_count, pie_count]

        non_zero_plot_counts = [count for count in plot_types_count if count != 0]

        return len(non_zero_plot_counts) == 1

    def _get_line_plot_data(self, gca):
        """
        Get json data for line plot

        Parameters:
        - gca (Axes): The current axes object.

        Returns:
        - dict: {"label", "data", "backgroundColor", "borderColor"}
        """
        x_axes_type = "category"

        lines = gca.get_lines()

        if len(lines) == 0:
            return None, None, None

        data = []
        labels = []

        for line in lines:
            x_data = line.get_xdata().tolist()
            y_data = line.get_ydata().tolist()
            color = line.get_color()

            if isinstance(x_data, list) and all(isinstance(x, float) for x in x_data):
                labels.extend([round(x_, 2) for x_ in x_data])
            else:
                labels.extend(x_data)

            if isinstance(x_data, list) and all(
                isinstance(x, (pd.Timestamp, datetime.datetime, datetime.date))
                for x in x_data
            ):
                x_axes_type = "time"

            dataset = {
                "type": "line",
                "label": line.get_label(),
                "data": [
                    {
                        "x": (
                            round(x_data, 2)
                            if isinstance(x_data, (float))
                            else x_data[i]
                        ),
                        "y": y,
                    }
                    for i, y in enumerate(y_data)
                ],
                "backgroundColor": mcolors.to_hex(color),
                "borderColor": mcolors.to_hex(color),
                "fill": False,
            }

            data.append(dataset)

        labels = sorted(list(set(labels)))

        if x_axes_type == "time":
            labels = sorted(labels)

        return data, labels, x_axes_type

    def _get_bar_plot_data(self, gca):
        """
        Get json data for bar plot

        Parameters:
        - gca (Axes): The current axes object.

        Returns:
        - dict: {"label", "data", "backgroundColor", "borderColor"}
        """
        bars = gca.patches
        if len(bars) == 0:
            return None, None

        orientation = self._get_plot_orientation(gca)

        data = []

        if orientation == "horizontal":
            x_tick_labels = gca.get_yticklabels()
        else:
            x_tick_labels = gca.get_xticklabels()

        handles, legend_labels = gca.get_legend_handles_labels()

        if len(handles) > 0:
            for i, handle in enumerate(handles):
                if isinstance(handle, BarContainer):
                    bar_group = []
                    bar_colors = []
                    for bar in handle:
                        height = bar.get_height()
                        width = bar.get_width()
                        x_coord = bar.get_x()
                        bar_group.append({"x": x_coord + width / 2, "y": height})
                        bar_colors.append(mcolors.to_hex(bar.get_facecolor()))

                    label = legend_labels[i]

                    dataset = {
                        "type": "bar",
                        "label": label,
                        "data": bar_group,
                        "backgroundColor": bar_colors,
                        "borderColor": bar_colors,
                    }

                    data.append(dataset)

            total_bars = len(bars)
            total_handles = len(handles)

            # Handles case for histogram where BarContainer doesn't exists
            if len(data) == 0 and total_bars >= total_handles:
                break_point = int(total_bars / total_handles)
                bar_datasets = [
                    bars[i : i + break_point] for i in range(0, total_bars, break_point)
                ]

                for i, bar_dataset in enumerate(bar_datasets):
                    bar_group = []
                    bar_colors = []
                    for bar in bar_dataset:
                        height = bar.get_height()
                        width = bar.get_width()
                        x_coord = bar.get_x()
                        bar_group.append({"x": x_coord + width / 2, "y": height})
                        bar_colors.append(mcolors.to_hex(bar.get_facecolor()))

                    dataset = {
                        "type": "bar",
                        "data": bar_group,
                        "backgroundColor": bar_colors,
                        "borderColor": bar_colors,
                    }
                    if len(legend_labels) > i:
                        dataset["label"] = legend_labels[i]

                    data.append(dataset)

        else:
            groups = len(x_tick_labels)

            bar_datasets = [bars[i : i + groups] for i in range(0, len(bars), groups)]

            for i, bar_dataset in enumerate(bar_datasets):
                bar_group = []
                bar_colors = []
                for bar in bar_dataset:
                    height = bar.get_height()
                    width = bar.get_width()
                    x_coord = bar.get_x()
                    bar_group.append({"x": x_coord + width / 2, "y": height})
                    bar_colors.append(mcolors.to_hex(bar.get_facecolor()))

                dataset = {
                    "type": "bar",
                    "data": bar_group,
                    "backgroundColor": bar_colors,
                    "borderColor": bar_colors,
                }
                if len(legend_labels) > i:
                    dataset["label"] = legend_labels[i]

                data.append(dataset)

        return data, [x_tick.get_text() for x_tick in x_tick_labels]

    def _calculate_pie_wedge_percentage(self, wedge) -> float:
        """
        extra
        Args:
            wedge (Wedge): pie chart wedge

        Returns:
            float: percentage of float
        """
        r = wedge.r
        theta1 = wedge.theta1
        theta2 = wedge.theta2

        theta = theta2 - theta1

        area_sector = (theta / 360) * math.pi * r**2

        total_area_circle = math.pi * r**2

        percentage_covered = (area_sector / total_area_circle) * 100

        return round(percentage_covered, 2)

    def _get_pie_plot_data(self, gca):
        """
        Get json data for bar plot

        Parameters:
        - gca (Axes): The current axes object.

        Returns:
        - dict: {"label", "data", "backgroundColor", "borderColor"}
        """
        handles, labels = gca.get_legend_handles_labels()

        if handles is None or len(handles) == 0:
            return None, None

        colors = []
        wedges = []

        for i, wedge in enumerate(handles):
            color = wedge.get_facecolor()
            colors.append(mcolors.to_hex(color))
            wedges.append(self._calculate_pie_wedge_percentage(wedge))

        return [
            {
                "type": "pie",
                "label": labels,
                "data": wedges,
                "backgroundColor": colors,
                "borderColor": colors,
            }
        ], labels

    def _get_plot_type(self, gca):
        """
        Determine the type of plot based on the elements in the current axes.

        Parameters:
        - gca (Axes): The current axes object.

        Returns:
        - str: The type of plot ('line', 'bar', 'hist', 'pie', or 'unknown').
        """
        plot_types = {
            plt.Line2D: "line",
            patches.Rectangle: "bar",
            patches.Wedge: "pie",
        }

        for item in gca.get_children():
            for plot_type, plot_name in plot_types.items():
                if isinstance(item, plot_type):
                    return plot_name

        return "unknown"

    def _is_multi_plot_type(self, gca):
        """
        Determine the type of plot based on the elements in the current axes.

        Parameters:
        - gca (Axes): The current axes object.

        Returns:
        - str: The type of plot ('line', 'bar', 'hist', 'pie', or 'unknown').
        """
        plot_types = {
            plt.Line2D: "line",
            patches.Rectangle: "bar",
            patches.Wedge: "pie",
        }
        plot_type_count = 0
        type_names = []
        has_pie = False
        for item in gca.get_children():
            for plot_type, _ in plot_types.items():
                if isinstance(item, plot_type) and plot_type not in type_names:
                    if isinstance(item, patches.Wedge):
                        has_pie = True
                    type_names.append(plot_type)
                    plot_type_count += 1

        if has_pie:
            return False

        return plot_type_count > 1

    def _get_datasets_and_labels(self, plot_type, gca, gcf):
        """
        Get Datasets and Labels
        Args:
            plot_type (str): type of plot
            gca (MatplotlibAxes): Axes of matplotlib
            gcf (MatplotLib Figure): Figure of matplotlib

        Returns:
            dataset, labels, axes_type
        """
        axes_type = "category"
        orientation = "vertical"

        if self._is_multi_plot_type(gca):
            datasets = []

            # Check and get line plot data
            line_data, labels, axes_type = self._get_line_plot_data(gca)
            if line_data is not None:
                datasets.extend(line_data)

            # Check and get bar plot data
            bar_data, labels = self._get_bar_plot_data(gca)
            if bar_data is not None:
                orientation = self._get_plot_orientation(gca)
                datasets.extend(bar_data)

            # Skip pie cannot be multiplot
            return datasets, labels, axes_type, orientation

        else:
            if plot_type == "line":
                line_data, line_labels, axes_type = self._get_line_plot_data(gca)
                return line_data, line_labels, axes_type, orientation
            elif plot_type == "bar":
                bar_data, bar_labels = self._get_bar_plot_data(gca)
                orientation = self._get_plot_orientation(gca)
                return bar_data, bar_labels, axes_type, orientation
            elif plot_type == "pie":
                pie_data, pie_labels = self._get_pie_plot_data(gca)
                return pie_data, pie_labels, axes_type, orientation

    def _plt_to_chartjs_json(self, gcf, gca):

        if self._has_subplots(gcf):
            return None

        plot_type = self._get_plot_type(gca)

        if plot_type == "unknown":
            return None

        datasets, labels, axes_type, orientation = self._get_datasets_and_labels(
            plot_type, gca, gcf
        )

        x_label = gca.get_xlabel()
        y_label = gca.get_ylabel()
        title = gca.get_title()

        _, labels_in_legends = gca.get_legend_handles_labels()

        plot_data = {
            "type": plot_type,
            "data": {"labels": labels, "datasets": datasets},
            "options": {
                "indexAxis": "x" if orientation == "vertical" else "y",
                "plugins": {
                    "legend": {
                        "display": len(labels_in_legends) > 0,
                    },
                    "title": {"text": title, "display": len(title) > 0},
                },
                "scales": {
                    "x": {
                        "title": {
                            "text": x_label,
                            "display": len(x_label) > 0,
                            "font": {
                                "size": 14,
                            },
                        }
                    },
                    "y": {
                        "title": {
                            "text": y_label,
                            "display": len(y_label) > 0,
                            "font": {
                                "size": 14,
                            },
                        }
                    },
                },
            },
        }

        if orientation == "vertical":
            plot_data["options"]["scales"]["x"]["type"] = axes_type
        else:
            plot_data["options"]["scales"]["y"]["type"] = axes_type

        return plot_data
