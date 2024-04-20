from __future__ import annotations

import io
from typing import TYPE_CHECKING

from IPython.core.getipython import get_ipython
from seaborn._core.plot import theme_context

if TYPE_CHECKING:
    from collections.abc import Callable

    from IPython.lib.pretty import RepresentationPrinter
    from matplotlib.figure import Figure
    from seaborn.objects import Plot


def matplotlib_figure_to_pgf(fig: Figure, rp: RepresentationPrinter, cycle) -> None:  # noqa: ARG001
    with io.StringIO() as fp:
        fig.savefig(fp, format="pgf", bbox_inches="tight")
        text = fp.getvalue()

    rp.text(text)


def matplotlib_figure_to_pdf(fig: Figure) -> bytes:
    with io.BytesIO() as fp:
        fig.savefig(fp, format="pdf", bbox_inches="tight")
        return fp.getvalue()


def matplotlib_figure_to_svg(fig: Figure) -> str:
    with io.StringIO() as fp:
        fig.savefig(fp, format="svg", bbox_inches="tight")
        return fp.getvalue()


def seaborn_plot_to_pgf(plot: Plot, rp: RepresentationPrinter, cycle) -> None:
    plotter = plot.plot()
    with theme_context(plotter._theme):  # type: ignore  # noqa: SLF001
        return matplotlib_figure_to_pgf(plotter._figure, rp, cycle)  # type: ignore # noqa: SLF001


def seaborn_plot_to_pdf(plot: Plot) -> bytes:
    plotter = plot.plot()
    with theme_context(plotter._theme):  # type: ignore  # noqa: SLF001
        return matplotlib_figure_to_pdf(plotter._figure)  # type: ignore  # noqa: SLF001


def seaborn_plot_to_svg(plot: Plot) -> str:
    plotter = plot.plot()
    with theme_context(plotter._theme):  # type: ignore  # noqa: SLF001
        return matplotlib_figure_to_svg(plotter._figure)  # type: ignore  # noqa: SLF001


MIMES: dict[str, str] = {
    "pgf": "text/plain",
    "pdf": "application/pdf",
    "svg": "image/svg+xml",
}

MODULE_CLASSES: dict[str, list[tuple[str, str]]] = {
    "matplotlib": [("matplotlib.figure", "Figure")],
    "seaborn": [("seaborn._core.plot", "Plot")],
}

FUNCTIONS: dict[tuple[str, str], dict[str, Callable]] = {
    ("matplotlib.figure", "Figure"): {
        "pgf": matplotlib_figure_to_pgf,
        "pdf": matplotlib_figure_to_pdf,
        "svg": matplotlib_figure_to_svg,
    },
    ("seaborn._core.plot", "Plot"): {
        "pgf": seaborn_plot_to_pgf,
        "pdf": seaborn_plot_to_pdf,
        "svg": seaborn_plot_to_svg,
    },
}


def set_formatter(module: str, fmt: str, ip=None) -> None:
    if not ip and not (ip := get_ipython()):
        return

    if not (mime := MIMES.get(fmt)):
        raise NotImplementedError

    formatter = ip.display_formatter.formatters[mime]  # type:ignore

    if module_classes := MODULE_CLASSES.get(module):
        for module_class in module_classes:
            if function := FUNCTIONS.get(module_class, {}).get(fmt):
                formatter.for_type_by_name(*module_class, function)
