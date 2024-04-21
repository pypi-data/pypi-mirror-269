from __future__ import annotations

import warnings
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable, Optional, Sequence

    import matplotlib.axes as mpla

    from .figure import Figure


class Plot(ABC):
    @abstractmethod
    def draw_on(self, ax: mpla.Axes) -> None:
        """Draw plot onto provided axes."""

    def __add__(self, plot: Plot) -> Plot:
        return AddPlot(left=self, right=plot)


@dataclass(frozen=True)
class AddPlot(Plot):
    left: Plot
    right: Plot

    def draw_on(self, ax: mpla.Axes) -> None:
        self.left.draw_on(ax)
        self.right.draw_on(ax)


@dataclass(frozen=True)
class NullPlot(Plot):
    """A Plot that doesn't draw anything on the given Axes."""

    def draw_on(self, ax: mpla.Axes) -> None:
        pass


@dataclass(frozen=True)
class FigureTeePlot(Plot):
    plot: Plot
    make_figure: Callable[[Plot], Figure]
    file_name: str
    dpi: int = 200

    def draw_on(self, ax: mpla.Axes) -> None:
        # Do our job and draw the child plot
        self.plot.draw_on(ax)
        # Also save a side copy of the plot
        tee_fig = self.make_figure(self.plot).figure()
        tee_fig.savefig(self.file_name, dpi=self.dpi)


@dataclass(frozen=True, eq=False)
class PlotOnSameAxes(Plot):
    plots: Sequence[Plot]

    def draw_on(self, ax: mpla.Axes) -> None:
        for plot in reversed(self.plots):
            plot.draw_on(ax)


@dataclass(frozen=True)
class PlotIf(Plot):
    condition: bool
    plot: Plot

    def draw_on(self, ax: mpla.Axes) -> None:
        if self.condition:
            self.plot.draw_on(ax)


@dataclass(frozen=True)
class PlotIfElse(Plot):
    condition: bool
    plot_if: Plot
    plot_else: Plot

    def draw_on(self, ax: mpla.Axes) -> None:
        if self.condition:
            self.plot_if.draw_on(ax)
        else:
            self.plot_else.draw_on(ax)


@dataclass(frozen=True)
class Decorations(Plot):
    xlabel: Optional[str] = None
    ylabel: Optional[str] = None
    title: Optional[str] = None

    def draw_on(self, ax: mpla.Axes) -> None:
        if self.xlabel is not None:
            ax.set_xlabel(self.xlabel)
        if self.ylabel is not None:
            ax.set_ylabel(self.ylabel)
        if self.title is not None:
            ax.set_title(self.title)


@dataclass(frozen=True, eq=False)
class WithAxisLabels(Plot):
    plot: Plot
    xlabel: str
    ylabel: str

    def __post_init__(self) -> None:
        warnings.warn(
            "WithAxisLabels is deprecated, use Decorations instead",
            FutureWarning,
            stacklevel=2,
        )

    def draw_on(self, ax: mpla.Axes) -> None:
        (self.plot + Decorations(xlabel=self.xlabel, ylabel=self.ylabel)).draw_on(ax)


@dataclass(frozen=True, eq=False)
class WithPlotTitle(Plot):
    plot: Plot
    title: str

    def __post_init__(self) -> None:
        warnings.warn(
            "WithPlotTitle is deprecated, use Decorations instead",
            FutureWarning,
            stacklevel=2,
        )

    def draw_on(self, ax: mpla.Axes) -> None:
        (self.plot + Decorations(title=self.title)).draw_on(ax)
