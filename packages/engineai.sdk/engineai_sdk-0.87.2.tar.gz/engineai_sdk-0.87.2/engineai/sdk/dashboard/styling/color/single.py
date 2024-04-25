"""Spec for SingleColor class."""

from typing import Any

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.utils import generate_input

from .palette import Palette


class Single(AbstractFactory):
    """Class for creating a single color instance.

    Create a class representing a single color within
    a palette for a Timeseries widget.
    """

    @type_check
    def __init__(self, color: Palette):
        """Constructor for Single.

        Args:
            color: a color from Palette.
        """
        super().__init__()
        self.__color = color.color

    def build(self) -> Any:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return generate_input(
            "ColorSingleInput",
            customColor=self.__color,
        )
